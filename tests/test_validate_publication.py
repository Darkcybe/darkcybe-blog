"""Regression tests for broken navigation and native-card link handling."""

from pathlib import Path
import tempfile
import unittest

from scripts.validate_publication import REQUIRED, validate


class PublicationValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in REQUIRED:
            self.write(name, "# Page\n")
        self.write("SUMMARY.md", "# Summary\n\n* [Home](README.md)\n")

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


if __name__ == "__main__":
    unittest.main()
