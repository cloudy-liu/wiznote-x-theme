from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
THEME_PATH = ROOT_DIR / "theme.css"
MANIFEST_PATH = ROOT_DIR / "manifest.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_missing_items() -> list[str]:
    missing: list[str] = []

    readme_path = ROOT_DIR / "README.md"

    if not THEME_PATH.exists():
        missing.append(f"Theme file missing: {THEME_PATH}")
        return missing

    if not MANIFEST_PATH.exists():
        missing.append(f"Manifest file missing: {MANIFEST_PATH}")
        return missing

    if not readme_path.exists():
        missing.append(f"README missing: {readme_path}")
        return missing

    css = read_text(THEME_PATH)
    readme = read_text(readme_path)
    manifest = json.loads(read_text(MANIFEST_PATH))

    if manifest.get("name") != "Wiznote X":
        missing.append('Manifest "name" should be "Wiznote X"')
    if not manifest.get("version"):
        missing.append('Manifest "version" should not be empty')
    if not manifest.get("author"):
        missing.append('Manifest "author" should not be empty')

    required_css_markers = [
        ".theme-light",
        ".theme-dark",
        "--wiz-accent-rgb",
        "--background-primary",
        "--text-normal",
        "--color-accent",
        "--font-text-theme",
        '"PingFang SC"',
        ".workspace-ribbon",
        ".workspace-tab-header",
        ".nav-file-title",
        ".tree-item-self",
        ".search-input-container",
        ".markdown-rendered blockquote",
        ".markdown-rendered pre",
        ".markdown-rendered table",
        ".callout",
        ".cm-link",
        "#448aff",
        "#07142a",
    ]
    for marker in required_css_markers:
        if marker not in css:
            missing.append(f"Theme CSS marker missing: {marker}")

    required_readme_markers = [
        "python install.py obsidian --vault",
        ".obsidian/themes/Wiznote X/",
        "theme.css",
        "manifest.json",
        "Wiznote X",
    ]
    for marker in required_readme_markers:
        if marker not in readme:
            missing.append(f"README marker missing: {marker}")

    return missing


def main() -> int:
    missing = collect_missing_items()
    if missing:
        for item in missing:
            print(item, file=sys.stderr)
        return 1

    print("Obsidian Wiznote X theme checks passed.")
    return 0


class ObsidianThemeTest(unittest.TestCase):
    def test_obsidian_theme_assets(self) -> None:
        missing = collect_missing_items()
        self.assertEqual(missing, [], "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
