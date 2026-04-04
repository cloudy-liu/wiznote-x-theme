from __future__ import annotations

import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
THEME_PATH = ROOT_DIR / "theme.css"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class WizWebParityTest(unittest.TestCase):
    def test_theme_contains_verified_wiz_web_tokens(self) -> None:
        css = read_text(THEME_PATH)

        required_markers = [
            "--wiz-left-pane-bg: #222530;",
            "--wiz-middle-pane-bg: #f5f8fb;",
            "--wiz-middle-selected-bg: #dae6f2;",
            "--wiz-editor-column-width: 1024px;",
            "--wiz-editor-content-font",
            '"Noto Sans SC"',
            "--wiz-editor-ui-font",
            "--wiz-link-color: #448aff;",
            "--wiz-inline-code-bg: #cdcdcd40;",
            "--wiz-inline-code-color: #07142a;",
            "--wiz-quote-color: #7084a4;",
            "--wiz-quote-border: #e0e6ee;",
            "--wiz-table-border: #b9bfc8;",
            "--wiz-list-marker-color: #448aff;",
            ".workspace-split.mod-left-split",
            ".markdown-rendered blockquote",
            ".markdown-rendered :not(pre) > code",
            ".markdown-rendered pre code",
            ".markdown-rendered table",
        ]

        missing = [marker for marker in required_markers if marker not in css]
        self.assertEqual(missing, [], "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
