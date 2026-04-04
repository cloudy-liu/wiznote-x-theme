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
            "--wiz-table-head-bg: #f5f8fb;",
            "--wiz-table-zebra-bg: #f5f8fb;",
            "--wiz-table-cell-padding-y: 2px;",
            "--wiz-table-cell-padding-x: 12px;",
            "--wiz-table-block-margin-top: 24px;",
            "--wiz-list-marker-color: #448aff;",
            "--wiz-list-block-gap: 4px;",
            "--wiz-list-padding-left: 8px;",
            "--wiz-list-padding-right: 4px;",
            "--wiz-list-item-padding-left: 22px;",
            "--wiz-list-ol-marker-width: 24px;",
            "--wiz-list-ul-marker-width: 22px;",
            "--wiz-list-level-step: 24px;",
            "--wiz-list-preview-nested-compensation: -6px;",
            "--wiz-task-indent: 29.5px;",
            "--wiz-task-box-size: 12px;",
            "--list-indent: 24px;",
            "--wiz-heading-font-family:",
            "--wiz-heading-letter-spacing: 1px;",
            "--wiz-heading-1-size: 28px;",
            "--wiz-heading-1-line-height: 42px;",
            "--wiz-heading-2-size: 26px;",
            "--wiz-heading-2-line-height: 39px;",
            "--wiz-heading-3-size: 24px;",
            "--wiz-heading-3-line-height: 36px;",
            "--wiz-heading-4-size: 22px;",
            "--wiz-heading-4-line-height: 33px;",
            "--wiz-heading-5-size: 20px;",
            "--wiz-heading-5-line-height: 32px;",
            "--wiz-heading-6-size: 18px;",
            "--wiz-heading-6-line-height: 28.8px;",
            "--wiz-title-size: 28px;",
            "--wiz-title-line-height: 32px;",
            ".workspace-split.mod-left-split",
            ".markdown-rendered blockquote",
            ".markdown-rendered :not(pre) > code",
            ".markdown-rendered pre code",
            ".markdown-rendered table",
        ]

        missing = [marker for marker in required_markers if marker not in css]
        self.assertEqual(missing, [], "\n".join(missing))

    def test_list_markers_use_stable_unicode_escapes(self) -> None:
        css = read_text(THEME_PATH)

        for marker in ['content: "\\2022";', 'content: "\\25E6";', 'content: "\\25AA";']:
            self.assertIn(marker, css)

        for broken in ["鈥", "鈼", "鈻"]:
            self.assertNotIn(broken, css)


if __name__ == "__main__":
    unittest.main()
