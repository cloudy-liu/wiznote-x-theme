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
        # The raw step is compensated for the parent `li`'s padding; see
        # test_preview_nesting_step_matches_wiz_flat_level_indent.
        self.assertIn("margin-left: calc(var(--wiz-list-level-step)", block)
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

    def test_preview_nesting_step_matches_wiz_flat_level_indent(self) -> None:
        # Wiz indents list lines flat from the root: `.block-content.level2`
        # gets `margin-left: 24px`, level3 48px, ... level8 168px - a constant
        # 24px per level. The editor's CM6 lines are flat too, so they match for
        # free; reading mode is nested DOM and compounds unless compensated.
        css = read_text(THEME_PATH)
        nested_block = extract_rule_block(
            css, ".markdown-rendered li > ul,\n.markdown-rendered li > ol"
        )
        obsidian_block = extract_rule_block(
            css,
            ".markdown-rendered ul ul > li,\n"
            ".markdown-rendered ul ol > li,\n"
            ".markdown-rendered ol ul > li,\n"
            ".markdown-rendered ol ol > li",
        )
        task_block = extract_rule_block(
            css,
            ".markdown-rendered li.task-list-item > ul,\n"
            ".markdown-rendered li.task-list-item > ol",
        )

        # A child list starts at its parent `li`'s content edge, so the step has
        # to subtract that padding back out to land on a flat 24px.
        self.assertIn(
            "margin-left: calc(var(--wiz-list-level-step) - var(--wiz-list-item-padding-left));",
            nested_block,
        )
        self.assertIn(
            "margin-left: calc(var(--wiz-list-level-step) - var(--wiz-task-indent));",
            task_block,
        )
        # Obsidian's `.markdown-rendered ul ul > li { margin-inline-start }`
        # outranks our own `li` rule, so it needs a same-shape selector to
        # cancel - covering the mixed pairs Obsidian's rule itself misses.
        self.assertIn("margin-inline-start: 0;", obsidian_block)
        self.assertNotIn("--wiz-list-preview-nested-compensation", css)

    def test_preview_suppresses_every_obsidian_marker_channel(self) -> None:
        # The theme draws its own markers, so it owns suppressing *every*
        # channel Obsidian paints one through. Scoping a suppression rule to
        # the surface where a bug was observed - rather than to the mechanism -
        # is what makes these regressions recur.
        css = read_text(THEME_PATH)

        # Channel 1: the native `::marker`. `list-style` must be declared on the
        # `li` itself; Obsidian's `.markdown-rendered ul.has-list-bullet` sets
        # `list-style-type` at a specificity we cannot outrank from the `ul`,
        # and a declaration on the element beats an inherited one.
        item_block = extract_rule_block(
            css, ".markdown-rendered ol > li,\n.markdown-rendered ul > li"
        )
        self.assertIn("list-style: none;", item_block)

        # Channel 2: the `.list-bullet` span widget, whose `::after` paints a
        # round dot via `background-color`. Obsidian injects it in reading mode
        # *and* live preview, so the selector must not be scoped to either.
        bullet_block = extract_rule_block(css, ".markdown-rendered .list-bullet")
        pseudo_block = extract_rule_block(css, ".markdown-rendered .list-bullet::after")

        self.assertIn("color: transparent !important;", bullet_block)
        self.assertIn("-webkit-text-fill-color: transparent;", bullet_block)
        self.assertIn("background-color: transparent;", bullet_block)
        self.assertIn("box-shadow: none;", bullet_block)
        # `li.is-collapsed .list-bullet:after` outranks us, so the paint
        # properties have to stay `!important`.
        self.assertIn("background-color: transparent !important;", pseudo_block)
        self.assertIn("box-shadow: none !important;", pseudo_block)
        self.assertIn("border: 0;", pseudo_block)
        self.assertIn("content: none;", pseudo_block)
        self.assertIn("display: none;", pseudo_block)

    def test_editor_self_drawn_markers_restore_wiz_geometry(self) -> None:
        css = read_text(THEME_PATH)
        formatting_block = extract_rule_block(
            css,
            ".markdown-source-view.mod-cm6 .HyperMD-list-line .cm-formatting-list {",
        )
        list_bullet_block = extract_rule_block(
            css,
            ".markdown-source-view.mod-cm6 .HyperMD-list-line .list-bullet",
        )
        list_bullet_pseudo_block = extract_rule_block(
            css,
            ".markdown-source-view.mod-cm6 .HyperMD-list-line .list-bullet::after",
        )
        pseudo_block = extract_rule_block(
            css,
            ".markdown-source-view.mod-cm6 .HyperMD-list-line .cm-formatting-list-ol::after,\n"
            ".markdown-source-view.mod-cm6 .HyperMD-list-line .cm-formatting-list-ul::after",
        )

        for marker in [
            "counter-reset: wiz-ol-1",
            "counter-increment: wiz-ol-1",
            ".cm-formatting-list-ol::after",
            ".cm-formatting-list-ul::after",
        ]:
            self.assertIn(marker, css)

        self.assertIn("color: transparent !important;", formatting_block)
        self.assertIn("-webkit-text-fill-color: transparent;", formatting_block)
        self.assertIn("display: inline-block;", formatting_block)
        # Since Obsidian's caret is the native browser caret, it defaults to
        # `color`. Hiding the marker text must not also hide the caret.
        self.assertIn("caret-color: var(--text-normal);", formatting_block)
        # Must stay non-zero so the caret doesn't collapse right after the marker.
        self.assertIn("font-size: var(--font-text-size, 15px);", formatting_block)
        self.assertNotIn("font-size: 0;", formatting_block)
        self.assertIn("color: var(--wiz-list-marker-color);", pseudo_block)
        self.assertIn("-webkit-text-fill-color: var(--wiz-list-marker-color);", pseudo_block)
        self.assertIn("font-size: var(--font-text-size, 15px);", pseudo_block)
        self.assertIn("line-height: var(--wiz-list-line-height);", pseudo_block)
        # Obsidian's native `.list-bullet` widget draws its dot through an
        # `::after` box. Left alone that pseudo-element renders next to our
        # own bullet character, producing a visible double marker. It must be
        # disabled, but must not draw a second glyph of its own.
        self.assertIn("color: transparent !important;", list_bullet_block)
        self.assertIn("-webkit-text-fill-color: transparent;", list_bullet_block)
        self.assertIn("background-color: transparent;", list_bullet_block)
        self.assertIn("box-shadow: none;", list_bullet_block)
        self.assertIn("background-color: transparent !important;", list_bullet_pseudo_block)
        self.assertIn("border: 0;", list_bullet_pseudo_block)
        self.assertIn("box-shadow: none !important;", list_bullet_pseudo_block)
        self.assertIn("content: none;", list_bullet_pseudo_block)
        self.assertIn("display: none;", list_bullet_pseudo_block)
        self.assertIn("-webkit-text-fill-color: transparent;", list_bullet_pseudo_block)
        self.assertNotIn(".cm-line.HyperMD-list-line .cm-formatting-list {", css)
        self.assertNotIn(".cm-line.HyperMD-list-line .list-bullet", css)
        self.assertNotIn('.list-bullet::after { content: "\\2022"; }', css)
        self.assertNotIn('.list-bullet::after { content: "\\25E6"; }', css)
        self.assertNotIn('.list-bullet::after { content: "\\25AA"; }', css)

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

    def test_scrollbar_sizing_goes_through_obsidian_scrollbar_vars(self) -> None:
        # Obsidian paints scrollbars from its own rules, scoped
        # `body.styled-scrollbars ::-webkit-scrollbar` (0,1,2), and those rules
        # read `--scrollbar-width` / `--scrollbar-height` / `--scrollbar-radius`.
        # A bare `::-webkit-scrollbar` (0,0,1) loses to them, so the theme's 7px
        # silently rendered as Obsidian's 12px default (app.css: `--scrollbar-
        # width: 12px`). Feeding the vars needs no cascade fight, and stays
        # correctly inert on macOS, where app.js adds the body class only when
        # `rd.isMacOS` is false and Obsidian defers to native scrollbars.
        #
        # An earlier revision of this test expected a
        # `body:not(.native-scrollbars)` scope. That class does not exist in
        # Obsidian - 0 occurrences in app.css - so the selector would only have
        # "worked" because `:not()` on a never-present class always matches.
        css = read_text(THEME_PATH)

        for declaration in [
            "--scrollbar-width: 7px;",
            "--scrollbar-height: 7px;",
            "--scrollbar-radius: 7px;",
            "--scrollbar-bg: transparent;",
            "--scrollbar-thumb-bg: var(--wiz-scrollbar-thumb-bg);",
            "--scrollbar-active-thumb-bg: var(--wiz-scrollbar-thumb-bg-active);",
        ]:
            self.assertIn(declaration, css)

        # No hand-rolled scrollbar selectors, and no phantom class.
        self.assertNotIn("::-webkit-scrollbar {", css)
        self.assertNotIn("native-scrollbars", css)


if __name__ == "__main__":
    unittest.main()
