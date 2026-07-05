<p align="center">
  <img src="https://img.shields.io/badge/App-Obsidian-448aff?style=flat-square" alt="App: Obsidian" />
  <img src="https://img.shields.io/badge/Version-0.1.0-07142a?style=flat-square" alt="Version: 0.1.0" />
  <img src="https://img.shields.io/badge/Style-Wiznote%20X-f5f8fb?style=flat-square" alt="Style: Wiznote X" />
</p>

[简体中文](README.md) | English

# Wiznote X Theme

Wiznote X Theme is a full Obsidian theme package that ports the current Wiz X web Markdown experience into a local Obsidian vault.

It styles more than the editor surface. The theme also aligns Obsidian's file tree, search, tabs, outline, buttons, form fields, status bar, Reading View, and Live Preview around the same visual system:

- bright white content canvas with pale blue-gray side panels
- deep navy text and vivid blue accents
- compact heading rhythm and lightweight separators
- low-shadow, low-noise application chrome
- coordinated light and dark variants built from the same token set

## Supported App

| App | Theme | Status | Path |
|-----|-------|--------|------|
| Obsidian | Wiznote X | ✅ Maintained | [`theme.css`](theme.css) + [`manifest.json`](manifest.json) |

## Automatic Install

The repository root includes a lightweight installer script at [`install.py`](install.py):

```bash
python install.py obsidian
```

The script detects configured or currently opened vaults and installs the theme into every detected vault.

To target a single vault:

```bash
python install.py obsidian --vault "/path/to/your/vault"
```

## Manual Install

Copy [`theme.css`](theme.css) and [`manifest.json`](manifest.json) into `<vault>/.obsidian/themes/Wiznote X/`, then select **Wiznote X** in **Settings → Appearance → Themes**.

## Theme Coverage

- full app chrome styling for navigation, tabs, search, sidebar panels, outline, buttons, and inputs
- consistent Markdown coverage for headings, links, lists, tasks, quotes, tables, code blocks, footnotes, Mermaid, and callouts
- aligned Reading View and Live Preview tokens to reduce mode-switch friction
- root-level Obsidian assets for straightforward packaging and release automation

## Repository Layout

```text
wizx-theme/
├── .github/workflows/release.yml
├── docs/
├── tests/
├── install.py
├── manifest.json
├── README.en.md
├── README.md
├── theme.css
└── versions.json
```

## Verification

```bash
python -m unittest discover -s tests -v
```
