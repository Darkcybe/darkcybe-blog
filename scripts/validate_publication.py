"""Offline structural checks for this small GitBook repository (stdlib only).

Checks inline Markdown links/images and HTML href/src links outside code/comments.
Reference-style links and GitBook-generated heading anchors need render review;
this is deliberately not a full Markdown renderer, YAML parser or URL checker.
"""

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


REQUIRED = (
    "README.md", "SUMMARY.md", "AGENTS.md", ".gitbook.yaml",
    "start-here/README.md", "investigate/README.md", "detect/README.md",
    "build/README.md", "reference/README.md", "dispatches/README.md",
    "about/README.md", "docs/DESIGN-SYSTEM.md",
    "templates/technical-guide.md", "templates/tool-note.md",
    "templates/investigation-report.md", "templates/field-note.md",
)
LINK = re.compile(r'!?\[[^\]\n]*\]\((<[^>\n]*>|[^()\n]*(?:\([^()\n]*\)[^()\n]*)*)\)')


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
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"missing foundational file: {name}")
    seen = set()
    for page in sorted(root.rglob("*.md")):
        if ".git" in page.relative_to(root).parts:
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
    print("Publication structure: PASS (offline; rendering and technical claims not checked)")
