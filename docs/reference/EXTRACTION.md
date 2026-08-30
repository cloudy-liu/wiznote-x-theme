# WizNote X Desktop — Extracted Ground Truth

Source: installed desktop app `C:\Program Files\WizNote` (Electron, build 2024-07-25).
Extraction: `app.asar` → `dist/renderer/renderer.dev.js` (CSS-in-JS chunks) + `renderer.dev.css`.

> The raw extracted stylesheets are **not committed** — they are verbatim source from a commercial
> product. This file records the values distilled from them; regenerate the originals locally from
> your own WizNote install using the offsets below if you need to re-verify.

Files this document was distilled from (regenerate locally, do not commit):

| File | Origin | Content |
|------|--------|---------|
| `wiznote-editor-vars.css` | renderer.dev.js @9091073 | Canonical editor token table: light defaults + `.dark-mode` overrides + `@media prefers-color-scheme` auto-dark |
| `wiznote-editor-main.css` | renderer.dev.js @8860308 | Editor block styles: headings, lists, todo, quote, code, table, hr, links, inline styles, Prism theme |
| `wiznote-shell.css` | renderer.dev.css | App shell CSS (toasts, tree DnD, resizers, misc) |

## Editor defaults (settings store, renderer.dev.js @6257727)

```js
editorStyle = { paragraphSpacing: 16, editorWidth: "1024px", textFontSize: 15, textIndent: 0 }
```

Derived block margins (paragraphSpacing e=16): block 16/8, table-top 1.5e=24,
title-bottom 1.5e=24, list-bottom e/4=4, h1/h2-top 1.5e=24, h3/h4-top 1.25e=20,
h5-top e=16, all heading bottoms e/2=8, table-sub-block e/3=5.33.
`--text-line-height = floor(lineHeight × fontSize)` → floor(1.6×15)=24px.

Content column: `max-width: min(var(--editor-width,1024px), 100%)`, margin auto,
container padding `8px 32px 32px 52px` (52px left = block-handle gutter),
`.editor-main` margin-top/bottom 24px.

## Shell theme (MUI theme factory, renderer.dev.js module 46075; `e` = isDark)

| Key | Light | Dark |
|-----|-------|------|
| baseText | `#07142A` | `#F0F0F0` |
| editorBaseText | `#121212` | `#f0f0f0` |
| leftPane bg | `#222530` | `#121212` |
| middlePane bg (note list) | `#F5F8FB` | `#28292A` |
| rightPane bg (editor area) | `#fff` | `#333333` |
| middlePaneSelectedItem | `#DAE6F2` | `rgba(85,85,85,.3)` |
| middlePaneItemHover | `rgba(112,132,164,.1)` | `rgba(85,85,85,.15)` |
| leftPaneSelected/Active | `rgba(112,132,164,.4)` / `.2` | `rgba(85,85,85,.4)` |
| leftPane text | `#C0D2EB` (muted `#7084A4`) | `#D8D8D8` (muted `#555555`) |
| noteListTitle / secondary | `#07142A` / `#7084A4` | `#D8D8D8` / `#969696` |
| noteListUnderLine | `#DAE6F2` | `#555555` |
| primary / active | `#448AFF` | `#448AFF` |
| rightPaneToolbar bg | `#fff` | `#404040` |
| toolbar button active bg | `#EEF3F8` / `#EBF3FA` | `rgba(150,150,150,.2)` |
| searchBox bg / expanded | `#E8ECF3` / `#DFE8F0` | `#212121` |
| searchInput bg | `#EAEEF2` | `#333333` |
| activeTab / hoverTab | `#EBF3FA` / `rgba(112,132,164,.1)` | `#555555` / `rgba(85,85,85,.2)` |
| popper (menus) | `#ffffff` | `#404040` |
| menu item text / hover bg | `#07142A` / `#EEF3F8` | `#F0F0F0` / `rgba(150,150,150,.2)` |
| scrollbar thumb / track border | `rgba(7,20,42,.2)` / `#FFF` | `rgba(255,255,255,.2)` / `#424242` |
| error / danger | `#FF403C` / `#FF5E84` | same |
| success snackbar | `#17CB86` / icon `#28D17B` | same |
| warning | `#FFB806` | same |
| search-hit highlight | `#ADD0FF` | same |
| wizInput border / focus bg | `#CFD6E1` / `#EBF3FA` | `#555555` / `#2a2a2a` |
| placeholder | `#B2BCCD` | (dark input placeholder `#555555`) |
| noteWarningInfo banner | text `#07142A` bg `#FCF7EA` | text `#FFB806` bg `#4F4D47` |
| UI font (MUI typography) | `'Open Sans','PingFang SC','Microsoft Yahei',…` | same |
| menu radius / shadow | 10px / `0 3px 20px rgba(0,0,0,.15)` | same |
| body bg/text (window) | `white` / `#333333` | `#101115` / `white` |

## Key editor facts worth remembering

- Headings H1–H6: 28/26/24/22/20/18px, line-height 1.5/1.5/1.5/1.5/1.6/1.6,
  **font-weight 500**, letter-spacing 1px. (H7 16px / H8 14px exist internally.)
- Body: 15px, line-height 1.6 (24px), **letter-spacing 0.02em**, color `#07142A`.
- Note title block: 28px / 500 / line-height 32px / margin-bottom 24px.
- Bold = `font-weight: bold` (700). Underline = `border-bottom: 1px solid` placeholder color, not text-decoration.
- Links: `#448AFF`, `text-decoration: underline`.
- Inline code: `.2em .4em` padding, radius 4px, font-size 85%, bg `#cdcdcd40` (dark `#96969640`), Menlo stack.
- Code block: uniform bg `--editor-code-bg-color` (header bar is the SAME color, 32px tall,
  language select revealed on hover), body padding `6px 16px 24px`, code 13px,
  radius 4px top+bottom. Syntax = **Prism default light theme** (`#905`/`#690`/slategray/`#07a`…),
  NOT overridden in dark mode (only bg changes; dark code title bg `#000`).
- Blockquote: border-left **4px** `#E0E6EE` (dark `#555`), padding-left 8px, text `#7084A4`
  (dark `#969696`); consecutive quote blocks merge (`margin-top: -4px`, `margin-bottom: 0`).
- Lists: markers **blue `#448aff`**; ul cycle by level •/◦/▪ (PingFang SC, weight 700, scale(1));
  ol `N.` in `Helvetica Neue, Consolas`, min-width 24px, padding-left 2px;
  li padding-left 22px; list block margin-bottom 4px.
- Todo: 12×12px box (bigger in headings: h1 20px/h2 18px/h3 16px, border 2px), border 1px
  `#b9bfc8` (unchanged in dark), radius 4px, checked bg `#07142A` (dark `#F0F0F0`) + white (dark `#333`) check SVG.
- Table: cells `2px 12px` padding, border `#B9BFC8` (dark `#555555`), cell bg transparent
  (dark **`#2a2a2a`**); th 400/left by default, but title-row style = weight 500 + centered +
  bg `#F5F8FB` (dark `rgba(85,85,85,.2)`); zebra (`stripe-style-table`, opt-in) even rows
  `#F5F8FB` (dark `rgba(85,85,85,.2)`); markdown-mode td min-width 100px; table block margin-top 24px.
- HR: `border-top: 2px dashed #ccc`.
- Text highlight (mark): plain `background-color` span, NO border/radius/padding.
  Palette `--style-bg-color-0..13` (e.g. yellow `rgba(255,246,122,.8)`, green `rgba(183,237,177,.8)`,
  blue `rgba(186,206,253,.7)`); text-color palette `--style-color-0..6`.
- Selection: `#448aff66`. Placeholder: `#b9bfc8` (dark `#555555`). Line-number gutter: `#aaaaaa`, 12px.
- Dark mode: editor bg `#333`, text `#f0f0f0`, images `filter brightness(0.8)` (`--editor-img-brightness: 0.8`).
- Mobile editor font-size: 18px.
