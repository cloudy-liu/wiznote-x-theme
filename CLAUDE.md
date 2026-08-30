# WizNote X Theme for Obsidian

Pixel-perfect replication of [WizNote](https://www.wiz.cn/xapp) markdown editor for Obsidian.

## Architecture

```
wizx-theme/
├── theme.css          # Single-file theme: tokens → Obsidian mapping → components
├── manifest.json      # Obsidian theme manifest (name, version, minAppVersion)
├── install.py         # Automated installer: symlinks theme into Obsidian vault
├── docs/              # Visual references captured from live WizNote web app (dev-only, not linked from README)
├── tests/             # Parity + install + discovery tests
└── README.md          # User-facing documentation (zh/en)
```

## Design Tokens — Source of Truth

All CSS variables are **extracted from the live WizNote web app** (`wiz.cn/xapp`) via Chrome DevTools.
The WizNote desktop app (Electron, `renderer.dev.js`/`.css`) is used as a second, code-level source
of truth for values the web app can't reveal precisely — see `docs/reference/EXTRACTION.md`, which
records the extracted values. The raw extracted CSS is deliberately not committed. Where the two
sources conflict, the desktop app's
literal CSS/JS wins (it's the actual rendering code, not a visual approximation).

### Token Architecture (theme.css)

```
body {}                    → WizNote design tokens (colors, fonts, spacing)
.theme-light {}            → Obsidian variable mapping for light mode
.theme-dark {}             → Obsidian variable mapping for dark mode
body, .app-container, ...  → Shell/layout styling
.markdown-rendered ...     → Content rendering rules
.cm-* / .HyperMD-*        → Source/live-preview editor rules
```

### Critical Values (from live extraction)

| Token | Light | Dark |
|-------|-------|------|
| Editor bg | `#ffffff` | `#333333` |
| Editor text | `#07142a` | `#f0f0f0` |
| Link color | `#448aff` | `#448aff` |
| Left pane bg | `#222530` | `#121212` |
| Note-list (middle pane) bg | `#f5f8fb` | `#28292a` |
| Body font-size | `15px` | `15px` |
| Body line-height | `24px` (1.6×) | `24px` |
| Letter-spacing | `0.3px` body / `1px` headings | same |
| Bold weight | `bold` (700, headings stay `500`) | same |
| Selection | `#448aff66` (0.4 alpha) | same |
| Code block bg / header | `#cdcdcd40`, header = same var as body | `#96969640`, header = same var as body |
| Table cell bg | `transparent` | `#2a2a2a` |
| Table head/zebra bg | `#f5f8fb` | `rgba(85,85,85,.2)` |
| Checkbox border | `#b9bfc8` | unchanged (`#b9bfc8`) |
| Syntax highlight tokens | Prism default light palette | same as light, never overridden |
| Image brightness | `1` | `0.8` (`filter: brightness()`) |
| HR | `2px dashed #ccc` | same |
| Text highlight (`==mark==`) | flat `rgba(255,246,122,.8)` span, no border/radius | same |

### Heading Scale

| Level | Size | Line-height | Margin-top |
|-------|------|-------------|------------|
| H1 | 28px | 42px (1.5×) | 24px |
| H2 | 26px | 39px (1.5×) | 24px |
| H3 | 24px | 36px (1.5×) | 20px |
| H4 | 22px | 33px (1.5×) | 20px |
| H5 | 20px | 32px (1.6×) | 16px |
| H6 | 18px | 28.8px (1.6×) | 16px |

### Font Stack

```
Content: -apple-system, BlinkMacSystemFont, "Helvetica Neue", "PingFang SC",
         "Microsoft YaHei", "Source Han Sans SC", "Noto Sans CJK SC",
         "Noto Sans SC", "WenQuanYi Micro Hei", sans-serif
UI:      "Noto Sans SC", [same system stack]
Mono:    Menlo, Monaco, Consolas, ... monospace, [system CJK fallback]
```

## Development Rules

- **No backward compatibility burden** — each release targets current Obsidian
- **Single file** — all theme CSS lives in `theme.css`, no preprocessor
- **Token-driven** — change `--wiz-*` variables, not individual selectors
- **Dark mode** — `.theme-dark` overrides only the tokens, selectors stay shared
