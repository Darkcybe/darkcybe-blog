"""Offline structure and tracked-index safety checks (stdlib only; requires Git).

Checks inline Markdown links/images and HTML href/src links outside code/comments.
Reference-style links and GitBook-generated heading anchors need render review;
this is deliberately not a full Markdown renderer, YAML parser or URL checker.
"""

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


REQUIRED = (
    "README.md", "SUMMARY.md", "AGENTS.md", ".gitbook.yaml", "gitbook-docs.yaml",
    "start-here/README.md", "investigate/README.md", "detect/README.md",
    "build/README.md", "reference/README.md", "dispatches/README.md",
    "about/README.md", "docs/DESIGN-SYSTEM.md",
    "templates/technical-guide.md", "templates/tool-note.md",
    "templates/investigation-report.md", "templates/field-note.md",
)
LINK = re.compile(r'!?\[[^\]\n]*\]\((<[^>\n]*>|[^()\n]*(?:\([^()\n]*\)[^()\n]*)*)\)')

# No archive exceptions until a public asset workflow is explicitly reviewed.
UNSAFE_SUFFIXES = {
    '.key', '.pem', '.p12', '.pfx', '.jks', '.keystore',
    '.db', '.sqlite', '.sqlite3', '.db3', '.sql',
    '.db-wal', '.db-shm', '.sqlite-wal', '.sqlite-shm',
    '.pcap', '.pcapng', '.cap', '.evtx', '.log', '.dmp', '.dump', '.core',
    '.zip', '.7z', '.tar', '.tgz', '.gz', '.bz2', '.xz', '.rar',
}
UNSAFE_NAME = re.compile(
    r'(^|[._-])(env|credentials?|tokens?|secrets?)([._-]|$)'
)
SECRET_MARKERS = (
    re.compile(r'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----'),
    re.compile(r'\bgh[pousr]_[A-Za-z0-9]{36}\b'),
    re.compile(r'\bgithub_pat_[A-Za-z0-9_]{82}\b'),
    re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),
)


def publication_safety(root):
    """Scan the tracked index snapshot, never print matched secret values."""
    errors = []
    try:
        entries = subprocess.run(
            ['git', '-C', str(root), 'ls-files', '--stage', '-z'],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout
        for entry in entries.split(b'\0'):
            if not entry:
                continue
            metadata, raw_name = entry.split(b'\t', 1)
            mode, oid, stage = metadata.decode('ascii').split()
            name = raw_name.decode('utf-8', errors='replace')
            path = Path(name.lower())
            if stage != '0' or mode not in ('100644', '100755'):
                errors.append(f'{name!r}: unresolved or non-regular tracked file')
                continue
            if (set(path.suffixes) & UNSAFE_SUFFIXES
                    or any(part == '.env' or part.startswith('.env.') for part in path.parts)
                    or any(part in ('.ssh', '.aws') for part in path.parts)
                    or path.name in ('id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519', '.netrc', '.npmrc', '.pypirc')
                    or (UNSAFE_NAME.search(path.name) and path.suffix not in ('.md', '.py'))):
                errors.append(f'{name!r}: unsafe public file type or credential filename')
            blob = subprocess.run(
                ['git', '-C', str(root), 'cat-file', 'blob', oid],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            ).stdout
            # UTF-16 text is common in Windows evidence; inspect it too.
            encoding = 'utf-16' if blob.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8'
            text = blob.decode(encoding, errors='replace')
            if any(marker.search(text) for marker in SECRET_MARKERS):
                errors.append(f'{name!r}: high-confidence secret marker (value withheld)')
    except (OSError, subprocess.CalledProcessError):
        errors.append('publication safety: cannot inspect Git index; validation failed')
    return errors


def prose(text):
    """Remove examples, preserving line numbers for diagnostics."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"), text, flags=re.S)
    fence = None
    lines = []
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append("")
        elif fence:
            lines.append("")
        else:
            lines.append(re.sub(r"(`+).*?\1", "", line))
    return "\n".join(lines)


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src"):
                self.links.append((self.getpos()[0], value or ""))


def local_target(root, page, target):
    target = unescape(target)
    if not target or "\\" in target or re.search(r"\s|%(?![0-9a-fA-F]{2})", target):
        raise ValueError("empty or malformed link target")
    parts = urlsplit(target)
    if parts.scheme in ("https", "http", "mailto"):
        return None  # No external requests.
    if parts.scheme or parts.netloc or parts.path.startswith("/") or parts.query:
        raise ValueError("use a relative file path for internal links")
    if not parts.path and not parts.fragment:
        raise ValueError("empty internal link")
    resolved = (page.parent / unquote(parts.path)).resolve() if parts.path else page
    if not resolved.is_relative_to(root):
        raise ValueError("internal link escapes repository")
    if not resolved.is_file():
        raise ValueError("local target does not exist")
    return resolved


def validate(root):
    root = root.resolve()
    errors = publication_safety(root)
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"missing foundational file: {name}")
    seen = set()
    for page in sorted(root.rglob("*.md")):
        if ".git" in page.relative_to(root).parts or page.is_symlink():
            continue
        content = prose(page.read_text(encoding="utf-8"))
        links = []
        for number, line in enumerate(content.splitlines(), 1):
            matches = list(LINK.finditer(line))
            if re.search(r"\]\(", LINK.sub("", line)):
                errors.append(f"{page.relative_to(root)}:{number}: malformed Markdown link")
            if page.name == "SUMMARY.md" and re.match(r"\s*[*+-] ", line):
                if not re.fullmatch(r"\s*\* " + LINK.pattern, line):
                    errors.append(f"SUMMARY.md:{number}: expected one navigation link")
            for match in matches:
                raw = match[1].strip()
                # Optional Markdown title; angle brackets allow literal parentheses.
                raw = re.sub(r'\s+"[^"\n]*"$', '', raw)
                if raw.startswith("<") and raw.endswith(">"):
                    raw = raw[1:-1]
                links.append((number, raw))
        html = HTMLLinks()
        html.feed(content)
        links.extend(html.links)
        for number, target in links:
            try:
                resolved = local_target(root, page, target)
                if page == root / "SUMMARY.md":
                    if resolved is None or resolved.suffix != ".md":
                        raise ValueError("navigation must target a local Markdown page")
                    if resolved in seen:
                        raise ValueError("duplicate navigation target")
                    seen.add(resolved)
            except ValueError as exc:
                errors.append(f"{page.relative_to(root)}:{number}: {exc}: {target!r}")
    if not seen:
        errors.append("SUMMARY.md has no local navigation targets")
    return errors


if __name__ == "__main__":
    problems = validate(Path(__file__).resolve().parents[1])
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        sys.exit(1)
    print("Publication structure and safety: PASS (offline; index scanned; review still required)")
