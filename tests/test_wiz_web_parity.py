from __future__ import annotations

import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
THEME_PATH = ROOT_DIR / "theme.css"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_rule_block(css: str, selector: str) -> str:
    start = css.find(selector)
    if start == -1:
        raise AssertionError(f"Selector not found: {selector}")

    brace_start = css.find("{", start)
    if brace_start == -1:
        raise AssertionError(f"Opening brace not found for selector: {selector}")

    depth = 0
    for index in range(brace_start, len(css)):
        char = css[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return css[brace_start + 1:index]

    raise AssertionError(f"Closing brace not found for selector: {selector}")


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
            "--wiz-table-width: 99%;",
            "--wiz-table-wrapper-padding-right: 1px;",
            "--wiz-list-marker-color: #448aff;",
            "--wiz-list-block-gap: 4px;",
            "--wiz-list-padding-left: 8px;",
            "--wiz-list-padding-right: 4px;",
            "--wiz-list-item-padding-left: 22px;",
            "--wiz-list-ol-marker-width: 24px;",
            "--wiz-list-ul-marker-width: 22px;",
            "--wiz-list-level-step: 24px;",
            "--wiz-list-line-height: 24px;",
            "--wiz-task-indent: 29.5px;",
            "--wiz-task-box-size: 12px;",
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
            "--wiz-code-block-bg: #cdcdcd40;",
            "--wiz-code-header-bg: var(--wiz-code-block-bg);",
            "--wiz-code-header-fg: #07142a;",
            "--wiz-code-header-height: 32px;",
            "--wiz-code-body-padding-top: 6px;",
            "--wiz-code-body-padding-x: 16px;",
            "--wiz-code-body-padding-bottom: 24px;",
            "--wiz-code-token-comment: slategray;",
            "--wiz-code-token-punctuation: rgb(153, 153, 153);",
            "--wiz-code-token-literal: rgb(153, 0, 85);",
            "--wiz-code-token-string: rgb(102, 153, 0);",
            "--wiz-code-token-operator: rgb(154, 110, 58);",
            "--wiz-code-token-keyword: rgb(0, 119, 170);",
            "--wiz-code-token-function: rgb(221, 74, 104);",
            "--wiz-code-token-variable: rgb(238, 153, 0);",
            ".workspace-split.mod-left-split",
            ".markdown-rendered blockquote",
            ".markdown-rendered :not(pre) > code",
            ".markdown-rendered pre",
            ".markdown-rendered pre::before",
            ".markdown-rendered .code-block-flair",
            ".markdown-rendered table",
            ".markdown-rendered .table-wrapper",
        ]

        missing = [marker for marker in required_markers if marker not in css]
        self.assertEqual(missing, [], "\n".join(missing))

    def test_preview_list_container_matches_wiz_web_geometry(self) -> None:
        css = read_text(THEME_PATH)
        block = extract_rule_block(css, ".markdown-rendered ul,\n.markdown-rendered ol")

        self.assertIn("list-style: none;", block)
        self.assertIn("margin: 0 0 var(--wiz-list-block-gap);", block)
        self.assertIn("padding-left: var(--wiz-list-padding-left);", block)
        self.assertIn("padding-right: var(--wiz-list-padding-right);", block)
        self.assertIn("line-height: var(--wiz-list-line-height);", block)
        self.assertNotIn("padding-inline-start: var(--list-indent);", block)

    def test_preview_nested_lists_use_wiz_level_step(self) -> None:
        css = read_text(THEME_PATH)
        block = extract_rule_block(css, ".markdown-rendered li > ul,\n.markdown-rendered li > ol")

        self.assertIn("margin-bottom: 0;", block)
        self.assertIn("margin-left: var(--wiz-list-level-step);", block)
        self.assertIn("margin-top: 0;", block)
        self.assertIn("padding-left: 0;", block)
        self.assertIn("padding-right: 0;", block)

    def test_preview_self_draws_unordered_markers_with_wiz_cycle(self) -> None:
        css = read_text(THEME_PATH)
        block = extract_rule_block(css, ".markdown-rendered ul > li::before")

        self.assertIn("color: var(--wiz-list-marker-color);", block)
        self.assertIn('content: "\\2022";', block)
        self.assertIn("font-family: var(--wiz-list-ul-marker-font);", block)
        self.assertIn("margin-left: calc(var(--wiz-list-ul-marker-width) * -1);", block)
        self.assertIn("position: absolute;", block)
        self.assertIn("width: var(--wiz-list-ul-marker-width);", block)

        self.assertIn('.markdown-rendered ul ul > li::before             { content: "\\25E6"; }', css)
        self.assertIn('.markdown-rendered ul ul ul > li::before          { content: "\\25AA"; }', css)
        self.assertIn('.markdown-rendered ul ul ul ul > li::before       { content: "\\2022"; }', css)

    def test_preview_self_draws_ordered_markers_with_wiz_counters(self) -> None:
        css = read_text(THEME_PATH)
        list_block = extract_rule_block(css, ".markdown-rendered ol")
        marker_block = extract_rule_block(css, ".markdown-rendered ol > li::before")
        item_block = extract_rule_block(css, ".markdown-rendered ol > li,\n.markdown-rendered ul > li")

        self.assertIn("counter-reset: wiz-r-ol;", list_block)
        self.assertIn("counter-increment: wiz-r-ol;", item_block)
        self.assertIn("color: var(--wiz-list-marker-color);", marker_block)
        self.assertIn("font-family: var(--wiz-list-ol-marker-font);", marker_block)
        self.assertIn("margin-left: calc(var(--wiz-list-ol-marker-width) * -1);", marker_block)
        self.assertIn("min-width: var(--wiz-list-ol-marker-width);", marker_block)
        self.assertIn("padding-left: 2px;", marker_block)
        self.assertIn("white-space: nowrap;", marker_block)

        self.assertIn('.markdown-rendered ol > li::before                                     { content: counter(wiz-r-ol, decimal) "."; }', css)
        self.assertIn('.markdown-rendered ol ol > li::before                                  { content: counter(wiz-r-ol, lower-alpha) "."; }', css)
        self.assertIn('.markdown-rendered ol ol ol > li::before                               { content: counter(wiz-r-ol, lower-roman) "."; }', css)

    def test_editor_self_drawn_markers_restore_wiz_geometry(self) -> None:
        css = read_text(THEME_PATH)
        formatting_block = extract_rule_block(
            css,
            ".markdown-source-view.mod-cm6 .HyperMD-list-line .cm-formatting-list-ol,\n.markdown-source-view.mod-cm6 .HyperMD-list-line .cm-formatting-list-ul",
        )
        pseudo_block = extract_rule_block(
            css,
            ".markdown-source-view.mod-cm6 .HyperMD-list-line .cm-formatting-list-ol::after,\n.markdown-source-view.mod-cm6 .HyperMD-list-line .cm-formatting-list-ul::after",
        )

        for marker in [
            "counter-reset: wiz-ol-1",
            "counter-increment: wiz-ol-1",
            ".cm-formatting-list-ol::after",
            ".cm-formatting-list-ul::after",
        ]:
            self.assertIn(marker, css)

        self.assertIn("color: transparent !important;", formatting_block)
        self.assertIn("display: inline-block;", formatting_block)
        self.assertIn("font-size: 0;", formatting_block)
        self.assertIn("color: var(--wiz-list-marker-color);", pseudo_block)
        self.assertIn("font-size: var(--font-text-size, 15px);", pseudo_block)
        self.assertIn("line-height: var(--wiz-list-line-height);", pseudo_block)

        self.assertIn('.markdown-source-view.mod-cm6 .HyperMD-list-line-1 .cm-formatting-list-ul::after { content: "\\2022"; }', css)
        self.assertIn('.markdown-source-view.mod-cm6 .HyperMD-list-line-2 .cm-formatting-list-ul::after { content: "\\25E6"; }', css)
        self.assertIn('.markdown-source-view.mod-cm6 .HyperMD-list-line-3 .cm-formatting-list-ul::after { content: "\\25AA"; }', css)
        self.assertIn('.markdown-source-view.mod-cm6 .HyperMD-list-line-1 .cm-formatting-list-ol::after { content: counter(wiz-ol-1, decimal) "."; }', css)
        self.assertIn('.markdown-source-view.mod-cm6 .HyperMD-list-line-2 .cm-formatting-list-ol::after { content: counter(wiz-ol-2, lower-alpha) "."; }', css)
        self.assertIn('.markdown-source-view.mod-cm6 .HyperMD-list-line-3 .cm-formatting-list-ol::after { content: counter(wiz-ol-3, lower-roman) "."; }', css)

    def test_task_lists_use_wiz_indent_model(self) -> None:
        css = read_text(THEME_PATH)
        item_block = extract_rule_block(
            css,
            ".markdown-rendered li.task-list-item,\n.markdown-rendered ul > li.task-list-item,\n.markdown-rendered ol > li.task-list-item",
        )
        checkbox_block = extract_rule_block(
            css,
            ".markdown-rendered li.task-list-item > input[type=\"checkbox\"],\n.markdown-rendered li.task-list-item > .task-list-item-checkbox",
        )

        self.assertIn("padding-left: var(--wiz-task-indent);", item_block)
        self.assertIn("content: none;", css)
        self.assertIn("left: 8px;", checkbox_block)
        self.assertIn("position: absolute;", checkbox_block)
        self.assertIn("top: 50%;", checkbox_block)
        self.assertIn("width: var(--wiz-task-box-size);", checkbox_block)

    def test_reading_and_editor_body_width_use_the_same_inset_model(self) -> None:
        css = read_text(THEME_PATH)
        block = extract_rule_block(
            css,
            ".markdown-reading-view .markdown-preview-sizer,\n.is-readable-line-width .markdown-source-view.mod-cm6 .cm-sizer",
        )

        self.assertIn("box-sizing: border-box;", block)
        self.assertIn("margin: 0 auto;", block)
        self.assertIn("max-width: calc(var(--wiz-editor-column-width) + 64px);", block)
        self.assertIn("padding: 0 32px 32px 32px;", block)
        self.assertIn("width: 100%;", block)
        self.assertNotIn("padding-right: 32px;", css)

    def test_preview_code_block_uses_dedicated_wiz_block_chrome(self) -> None:
        css = read_text(THEME_PATH)
        pre_block = extract_rule_block(css, ".markdown-rendered pre")
        before_block = extract_rule_block(css, ".markdown-rendered pre::before")
        flair_block = extract_rule_block(css, ".markdown-rendered .code-block-flair")

        self.assertIn("background: var(--wiz-code-block-bg);", pre_block)
        self.assertIn("border-radius: 4px;", pre_block)
        self.assertIn("padding:", pre_block)
        self.assertIn("position: relative;", pre_block)

        self.assertIn("background: var(--wiz-code-header-bg);", before_block)
        self.assertIn("border-top-left-radius: 4px;", before_block)
        self.assertIn("border-top-right-radius: 4px;", before_block)
        self.assertIn("content: \"\";", before_block)
        self.assertIn("height: var(--wiz-code-header-height);", before_block)

        self.assertIn("color: var(--wiz-code-header-fg);", flair_block)
        self.assertIn("height: var(--wiz-code-header-height);", flair_block)
        self.assertIn("padding: 0 var(--wiz-code-body-padding-x);", flair_block)

    def test_editor_code_block_uses_distinct_header_body_and_footer_rules(self) -> None:
        css = read_text(THEME_PATH)
        shared_block = extract_rule_block(
            css,
            ".markdown-source-view.mod-cm6 .cm-line.HyperMD-codeblock-begin,\n.markdown-source-view.mod-cm6 .cm-line.HyperMD-codeblock-end,\n.markdown-source-view.mod-cm6 .cm-line.HyperMD-codeblock",
        )
        begin_block = extract_rule_block(css, ".markdown-source-view.mod-cm6 .cm-line.HyperMD-codeblock-begin")
        body_block = extract_rule_block(css, ".markdown-source-view.mod-cm6 .cm-line.HyperMD-codeblock")
        end_block = extract_rule_block(css, ".markdown-source-view.mod-cm6 .cm-line.HyperMD-codeblock-end")

        self.assertIn("background-color: var(--wiz-code-block-bg);", shared_block)
        self.assertIn("background: var(--wiz-code-header-bg);", begin_block)
        self.assertIn("color: var(--wiz-code-header-fg);", begin_block)
        self.assertIn("min-height: var(--wiz-code-header-height);", begin_block)
        self.assertIn("padding: 0 var(--wiz-code-body-padding-x);", begin_block)
        self.assertIn("padding: 0 var(--wiz-code-body-padding-x);", body_block)
        self.assertIn("padding-bottom: var(--wiz-code-body-padding-bottom);", end_block)

    def test_code_block_syntax_palette_matches_wiz_for_preview_and_editor(self) -> None:
        css = read_text(THEME_PATH)

        required_markers = [
            ".markdown-rendered code .token.comment",
            ".markdown-rendered code .token.punctuation",
            ".markdown-rendered code .token.keyword",
            ".markdown-rendered code .token.number",
            ".markdown-rendered code .token.string",
            ".markdown-rendered code .token.operator",
            ".markdown-rendered code .token.function",
            ".markdown-rendered code .token.variable",
            ".cm-s-obsidian span.cm-comment",
            ".cm-s-obsidian span.cm-punctuation",
            ".cm-s-obsidian span.cm-keyword",
            ".cm-s-obsidian span.cm-number",
            ".cm-s-obsidian span.cm-string",
            ".cm-s-obsidian span.cm-operator",
            ".cm-s-obsidian span.cm-def",
            ".cm-s-obsidian span.cm-variable",
        ]

        missing = [marker for marker in required_markers if marker not in css]
        self.assertEqual(missing, [], "\n".join(missing))

    def test_markdown_tables_do_not_force_fixed_full_width(self) -> None:
        css = read_text(THEME_PATH)
        block = extract_rule_block(css, ".markdown-rendered table")
        declarations = {line.strip() for line in block.splitlines() if line.strip()}

        self.assertIn("table-layout: auto;", block)
        self.assertIn("width: var(--wiz-table-width);", block)
        self.assertIn("max-width: 100%;", block)
        self.assertNotIn("table-layout: fixed;", declarations)
        self.assertNotIn("width: 100%;", declarations)

    def test_table_wrapper_matches_wiz_scroll_model(self) -> None:
        css = read_text(THEME_PATH)
        block = extract_rule_block(css, ".markdown-rendered .table-wrapper")

        self.assertIn("margin: var(--wiz-table-block-margin-top) 0 8px;", block)
        self.assertIn("overflow-x: auto;", block)
        self.assertIn("overflow-y: hidden;", block)
        self.assertIn("padding: 0 var(--wiz-table-wrapper-padding-right) 0 0;", block)


if __name__ == "__main__":
    unittest.main()
