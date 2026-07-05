from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
README_ZH = ROOT_DIR / "README.md"
README_EN = ROOT_DIR / "README.en.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ReadmeDocsTest(unittest.TestCase):
    def test_chinese_readme_links_to_english(self) -> None:
        self.assertTrue(README_ZH.exists(), f"Missing README: {README_ZH}")
        readme = read_text(README_ZH)

        self.assertRegex(readme, r"\[English\]\((?:\./)?README\.en\.md\)")
        self.assertIn("简体中文", readme)
        self.assertNotIn("typora/", readme.lower())
        self.assertNotIn("typora", readme.lower())

    def test_english_readme_links_to_chinese(self) -> None:
        self.assertTrue(README_EN.exists(), f"Missing README: {README_EN}")
        readme = read_text(README_EN)

        self.assertRegex(readme, r"\[简体中文\]\((?:\./)?README\.md\)")
        self.assertIn("English", readme)
        self.assertNotIn("typora/", readme.lower())
        self.assertNotIn("typora", readme.lower())


if __name__ == "__main__":
    unittest.main()
