"""Regression tests for broken navigation and native-card link handling."""

from pathlib import Path
import tempfile
import subprocess
import unittest

from scripts.validate_publication import REQUIRED, validate


class PublicationValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        for name in REQUIRED:
            self.write(name, "# Page\n")
        self.write("SUMMARY.md", "# Summary\n\n* [Home](README.md)\n")
        self.git('add', '.')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_valid_markdown_html_and_examples(self):
        self.write("README.md", '''# Home
[Start](start-here/README.md "Start here")
[Fragment](#home)
[External](https://example.invalid/page)
<table data-view="cards"><tr><td><a href="about/README.md">About</a></td></tr></table>
`[example](missing.md)`
<!-- [example](missing.md) -->
~~~markdown
[example](missing.md)
~~~
''')
        self.assertEqual(validate(self.root), [])

    def test_missing_foundation(self):
        (self.root / "AGENTS.md").unlink()
        self.assertTrue(any("missing foundational" in e for e in validate(self.root)))

    def test_missing_site_sync_configuration(self):
        (self.root / "gitbook-docs.yaml").unlink()
        self.assertIn("missing foundational file: gitbook-docs.yaml",
                      validate(self.root))

    def test_missing_navigation(self):
        self.write("SUMMARY.md", "* [Missing](missing.md)\n")
        self.assertTrue(any("does not exist" in e for e in validate(self.root)))

    def test_duplicate_normalised_navigation(self):
        self.write("SUMMARY.md", "* [Home](README.md)\n* [Again](./README.md#home)\n")
        self.assertTrue(any("duplicate navigation" in e for e in validate(self.root)))

    def test_broken_card_target(self):
        self.write("README.md", '<a href="absent.md">Missing card</a>\n')
        self.assertTrue(any("does not exist" in e for e in validate(self.root)))

    def test_malformed_links(self):
        for link in ("[Broken](README.md", "[Blank]()", "[Space](bad path.md)",
                     "[Escape](../outside.md)", "[Root](/README.md)",
                     "[Percent](bad%ZZ.md)", "[Query](README.md?x=1)"):
            with self.subTest(link=link):
                self.write("README.md", link + "\n")
                self.assertTrue(validate(self.root))

    def test_nested_relative_link_and_encoded_filename(self):
        self.write("assets/example (1).md", "# Example\n")
        self.write("about/README.md", "[Home](../README.md)\n[Example](../assets/example%20%281%29.md)\n")
        self.assertEqual(validate(self.root), [])

    def test_empty_and_malformed_navigation(self):
        for content in ("# Summary\n", "* not a page\n"):
            self.write("SUMMARY.md", content)
            self.assertTrue(validate(self.root))

    def test_unsafe_tracked_files(self):
        for name in ('.env', '.env.local', 'config/production.env',
                     'assets/server.key', 'assets/client.pfx', '.ssh/id_ed25519',
                     'credentials.json', 'access-token.txt', 'secrets.yaml',
                     'data.sqlite3', 'data.db-wal', 'capture.PCAPNG',
                     'capture.pcap', 'events.evtx', 'raw.log', 'memory.dmp',
                     'bundle.zip', 'bundle.7z', 'bundle.tar.gz'):
            with self.subTest(name=name):
                self.write(name, 'synthetic fixture\n')
                self.git('add', '--', name)
                self.assertTrue(any('unsafe public file' in e for e in validate(self.root)))
                self.git('rm', '-f', '--', name)

    def test_secret_markers_in_text_including_examples(self):
        markers = ['-----BEGIN ' + kind + 'PRIVATE KEY-----'
                   for kind in ('', 'RSA ', 'EC ', 'OPENSSH ', 'ENCRYPTED ')]
        markers += ['gh' + 'p_' + 'A' * 36,
                    'github_' + 'pat_' + 'A' * 82,
                    'AK' + 'IA' + 'A' * 16,
                    'xox' + 'b-' + '1' * 24]
        for marker in markers:
            with self.subTest(prefix=marker[:8]):
                self.write('assets/example.txt', '<!--\n```\n' + marker + '\n```\n-->')
                self.git('add', '.')
                errors = validate(self.root)
                self.assertTrue(any('secret marker' in e for e in errors))
                self.assertNotIn(marker, '\n'.join(errors))

    def test_utf16_secret_marker(self):
        (self.root / 'example.txt').write_bytes(
            ('-----BEGIN ' + 'PRIVATE KEY-----').encode('utf-16'))
        self.git('add', '.')
        self.assertTrue(any('secret marker' in e for e in validate(self.root)))

    def test_scans_index_even_if_worktree_is_cleaned(self):
        self.write('example.txt', 'gh' + 'p_' + 'A' * 36)
        self.git('add', '.')
        self.write('example.txt', 'sanitised worktree, unsafe index')
        self.assertTrue(any('secret marker' in e for e in validate(self.root)))

    def test_untracked_files_are_not_publication_inputs(self):
        self.write('untracked.env', 'synthetic fixture')
        self.assertEqual(validate(self.root), [])

    def test_legitimate_security_prose_and_assets(self):
        self.write('credential-analysis.md', '# Lab\n10.0.0.1, 172.16.0.1, 192.168.1.1\n'
                   'SQLite, PCAP, EVTX, private keys, tokens and credentials.\n'
                   'Use ghp_REDACTED as a placeholder.\n')
        (self.root / 'diagram.png').write_bytes(b'\x89PNG\r\n\x1a\n')
        self.git('add', '.')
        self.assertEqual(validate(self.root), [])

    def test_missing_git_index_fails_closed(self):
        import shutil
        shutil.rmtree(self.root / '.git')
        self.assertTrue(any('cannot inspect Git index' in e for e in validate(self.root)))

    def test_symlink_is_rejected_without_reading_target(self):
        (self.root / 'outside.txt').symlink_to('/nonexistent-publication-fixture')
        self.git('add', '.')
        self.assertTrue(any('non-regular tracked file' in e for e in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
