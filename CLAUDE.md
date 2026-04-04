# WizNote X Theme for Obsidian

Pixel-perfect replication of [WizNote](https://www.wiz.cn/xapp) markdown editor for Obsidian.

## Architecture

```
wizx-theme/
├── theme.css          # Single-file theme: tokens → Obsidian mapping → components
├── manifest.json      # Obsidian theme manifest (name, version, minAppVersion)
├── install.py         # Automated installer: symlinks theme into Obsidian vault
├── docs/              # Visual references captured from live WizNote web app
├── tests/             # Parity + install + discovery tests
├── screenshot.png     # Theme preview for Obsidian community directory
└── README.md          # User-facing documentation (zh/en)
```

## Design Tokens — Source of Truth

All CSS variables are **extracted from the live WizNote web app** (`wiz.cn/xapp`) via Chrome DevTools.
Historical desktop assets are fallback reference only — the web app is canonical.

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
| Left pane bg | `#222530` | `#1c1f27` |
| Body font-size | `15px` | `15px` |
| Body line-height | `24px` (1.6×) | `24px` |
| Letter-spacing | `0.3px` body / `1px` headings | same |

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
