from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
ROOT_THEME_PATH = ROOT_DIR / "theme.css"
ROOT_MANIFEST_PATH = ROOT_DIR / "manifest.json"
VERSIONS_PATH = ROOT_DIR / "versions.json"
RELEASE_WORKFLOW_PATH = ROOT_DIR / ".github" / "workflows" / "release.yml"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, object]:
    return json.loads(read_text(path))


class ObsidianSubmissionTest(unittest.TestCase):
    def test_root_obsidian_release_files_exist(self) -> None:
        self.assertTrue(ROOT_THEME_PATH.exists(), f"Missing root theme.css: {ROOT_THEME_PATH}")
        self.assertTrue(ROOT_MANIFEST_PATH.exists(), f"Missing root manifest.json: {ROOT_MANIFEST_PATH}")
        self.assertTrue(VERSIONS_PATH.exists(), f"Missing versions.json: {VERSIONS_PATH}")

    def test_root_obsidian_files_are_the_canonical_source(self) -> None:
        manifest = read_json(ROOT_MANIFEST_PATH)
        css = read_text(ROOT_THEME_PATH)

        self.assertEqual(manifest.get("name"), "Wiznote X")
        self.assertTrue(manifest.get("version"))
        self.assertTrue(manifest.get("minAppVersion"))
        self.assertTrue(manifest.get("author"))
        self.assertIn(".theme-light", css)
        self.assertIn(".theme-dark", css)

    def test_duplicate_obsidian_source_directory_is_removed(self) -> None:
        self.assertFalse(
            (ROOT_DIR / "obsidian").exists(),
            "Obsidian assets should live at the repository root instead of a duplicate obsidian/ directory",
        )

    def test_versions_json_maps_current_theme_version(self) -> None:
        manifest = read_json(ROOT_MANIFEST_PATH)
        versions = read_json(VERSIONS_PATH)

        version = manifest["version"]
        min_app_version = manifest["minAppVersion"]
        self.assertEqual(
            versions.get(version),
            min_app_version,
            "versions.json should map the current theme version to minAppVersion",
        )

    def test_release_workflow_packages_root_obsidian_files(self) -> None:
        workflow = read_text(RELEASE_WORKFLOW_PATH)

        self.assertIn(
            '      - "wiznote-x-v*"',
            workflow,
            "Release workflow should only trigger for wiznote-x-v* tags",
        )
        self.assertIn(
            "cp theme.css manifest.json dist/obsidian/",
            workflow,
            "Release workflow should package the root Obsidian theme files",
        )
        self.assertIn(
            "zip -q ../obsidian-wiznote-x.zip theme.css manifest.json",
            workflow,
            "Obsidian release package should only contain the two theme files",
        )
        self.assertIn(
            "This release ships an updated Wiznote X theme package for Obsidian.",
            workflow,
            "Release notes should describe the Obsidian package",
        )
        self.assertIn(
            "name: Wiznote X ${{ steps.build.outputs.version }}",
            workflow,
            "GitHub release names should keep the Wiznote X project prefix",
        )
        self.assertNotIn("typora", workflow.lower())


if __name__ == "__main__":
    unittest.main()
