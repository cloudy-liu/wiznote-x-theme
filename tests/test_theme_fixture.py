from __future__ import annotations

import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
THEME_FIXTURE_PATH = ROOT_DIR / "tests" / "test-theme.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ThemeFixtureTest(unittest.TestCase):
    def test_fixture_covers_heading_levels_and_rich_tables(self) -> None:
        fixture = read_text(THEME_FIXTURE_PATH)

        required_markers = [
            "# Wiznote X Theme Test",
            "## Heading Scale",
            "# Heading Level 1",
            "## Heading Level 2",
            "### Heading Level 3",
            "#### Heading Level 4",
            "##### Heading Level 5",
            "###### Heading Level 6",
            "## Table",
            "## Rich HTML Table",
            "<table>",
            "<td>",
            "<ul>",
            "<ol>",
            "<pre><code>",
        ]

        missing = [marker for marker in required_markers if marker not in fixture]
        self.assertEqual(missing, [], "\n".join(missing))

    def test_fixture_covers_heading_scoped_tasks_and_nested_rich_cells(self) -> None:
        fixture = read_text(THEME_FIXTURE_PATH)

        required_markers = [
            "### Heading Followed By Tasks",
            "- [ ] Heading-scoped pending task",
            "- [x] Heading-scoped completed task",
            "  - [ ] Nested heading-scoped follow-up",
            "<td>",
            "<ul>",
            "<li>Nested cell bullet</li>",
            "<pre><code>nested cell code",
        ]

        missing = [marker for marker in required_markers if marker not in fixture]
        self.assertEqual(missing, [], "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
