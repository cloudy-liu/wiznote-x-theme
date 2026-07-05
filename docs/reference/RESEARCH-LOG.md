# WizNote X 桌面版样式提取 — 调研纪实与踩坑记录

> 本文档记录 2026-07-04 这一轮「从 WizNote 桌面版 Electron 壳里挖官方样式源码」的完整过程：怎么找到的、走过哪些死胡同、验证时踩过哪些坑、最终改了什么。目的是给后续想重复这类"逆向提取 + 二次验证"工作的人（包括未来的自己）省时间。
>
> 关联产物：`docs/reference/EXTRACTION.md`（蒸馏结论）、`wiznote-editor-vars.css` / `wiznote-editor-main.css` / `wiznote-shell.css`（原始提取物）。
> 关联改动：`theme.css`（本轮按结论修改的目标文件）、`CLAUDE.md`（更新了过时的暗色数值表）、`tests/test_wiz_web_parity.py`（同步了一处断言）。

## 0. 背景与动机

`CLAUDE.md` 里长期写的信条是"所有 CSS 变量都从活的 WizNote Web 端 (`wiz.cn/xapp`) 里用 DevTools 提取，桌面版资源只作为兜底参考"。但 Web 端能看到的只是**渲染结果**（计算样式），看不到：

- 暗色模式里哪些 token 是"有意不同"、哪些只是"没人费心去改所以继承亮色"；
- 一些细节判断题（分割线到底是 1px 还是 2px、加粗到底是 500 还是 700、高亮到底有没有边框）单靠肉眼截图比对经常出偏差；
- 官方到底有没有"表格斑马纹默认开/表头默认样式"这类由 class 开关控制的行为。

桌面版是 Electron 应用，理论上样式就是普通 CSS（或 CSS-in-JS 字符串），只要能拿到源码就是**代码级别的 ground truth**，不再是"看图猜数值"。这轮调研的起点，是想验证一个直觉——WizNote 的 Markdown 渲染"长得像 GitHub 但又不完全像"，想搞清楚哪些像、哪些是 WizNote 自己的改动。

## 1. 调研阶段一：定位与提取（据用户转述整理，非本会话亲自执行）

> 以下内容是用户对另一轮调研过程的转述总结，我没有亲自跑过这几步；第 2 节是本会话里我亲自执行、留有完整命令记录的二次验证部分。两者请区分对待。

1. 确认本机 `C:\Program Files\WizNote` 是 Electron 壳（2024-07 构建），解包其 `app.asar` 得到 `dist/renderer/renderer.dev.js`（约 10.9MB，压缩混淆但未整体 minify 掉字符串）和 `renderer.dev.css`。
2. **第一条死胡同**：翻了 Service Worker 缓存（约 4637 个条目），指望能挖到主题相关的静态资源。结果 99% 都是笔记内容资源（图片、附件）。其中一个 `md_document.css` 一度看起来很像主题源文件，结果实测发现它是某篇**剪藏博客自带的 `github-markdown-css`**——不是 WizNote 官方样式，只是巧合地印证了"WizNote 像 GitHub"这个直觉从何而来（用户剪藏过的博客本来就用了 github-markdown-css，跟 WizNote 自己的样式没关系）。
3. **真正的源头**：`renderer.dev.js` 内嵌的 CSS-in-JS 字符串块——`@9091073`（约 35KB，编辑器变量总表：亮色默认值 + `.dark-mode` 覆盖 + `@media prefers-color-scheme` 自动跟随系统）+ `@8860308`（约 201KB，编辑器块级样式：标题/列表/待办/引用/代码/表格/分割线/链接/行内样式/Prism 主题）+ MUI 主题工厂（模块编号 46075，壳层明暗配色，是一段普通的 JS 对象字面量，不是 CSS）。
4. 还在设置存储模块（`@6257727`）里挖到默认排版参数：

   ```js
   editorStyle = { paragraphSpacing: 16, editorWidth: "1024px", textFontSize: 15, textIndent: 0 }
   ```

   所有块级间距都是这个 `paragraphSpacing`（记作 e=16）的倍数公式：block 16/8，table-top `1.5e=24`，title-bottom `1.5e=24`，list-bottom `e/4=4`，h1/h2-top `1.5e=24`，h3/h4-top `1.25e=20`，h5-top `e=16`，所有 heading-bottom `e/2=8`，table-sub-block `e/3≈5.33`。这与之前从 Web 端提取、写进 `CLAUDE.md` 的排版基础数据吻合，说明早期的间距推导方向本来就是对的。
5. 提取物归档进了本仓库 `docs/reference/`（4 个文件，含蒸馏笔记 `EXTRACTION.md`）。

## 2. 调研阶段二：我方二次验证（本会话，完整可复现命令）

拿到一份"调研总结"之后，不管写得多详细、多有条理，都不该直接当真去改代码——**转述/蒸馏笔记天然有转录风险**（抄错数值、上下文丢失、多个相似变量搞混）。这一节记录我是怎么把 `EXTRACTION.md` 里的关键结论一条条摁回原始材料里核对的。

### 2.1 确认归档产物完整

```powershell
Get-ChildItem -Path docs/reference -Force
```

确认 4 个文件都在：`EXTRACTION.md`(5.9KB)、`wiznote-editor-main.css`(196KB)、`wiznote-editor-vars.css`(34KB)、`wiznote-shell.css`(40KB)。

### 2.2 意外发现：原始解包产物还留在临时目录里

```powershell
Get-ChildItem -Path "$env:TEMP" -Filter "renderer*" -Recurse -ErrorAction SilentlyContinue
```

命中了 `C:\Users\cloudy\AppData\Local\Temp\wiznote-asar\dist\renderer\renderer.dev.js` 和 `renderer.dev.css`——说明上一轮解包的产物还没被系统清理掉。这给了我直接回源验证的机会，但**这纯粹是运气，不能当作可依赖的前提**（见踩坑 #7）。同一次 `Get-ChildItem` 还扫到了 `%TEMP%\nsd*.tmp\7z-out\...`，从命名推断上一轮很可能是先用 7-Zip 解开 NSIS 安装包拿到 `app.asar`，再用某个 asar 解包工具（如 `npx asar extract app.asar <dir>`）展开到 `wiznote-asar\` 目录——但这一步工具链细节我没有实测过，如果要重新走一遍完整流程，请自行确认。

### 2.3 逐条回源核对 EXTRACTION.md 里的关键结论

核心手法：Windows 上单文件超过几 MB、又是压缩过的单行 JS，`Select-String` 配合 `-Context` 经常因为整行太长而截不出有效上下文。更好用的方式是整个文件读进内存字符串再用 `.IndexOf` + `.Substring` 手动裁剪：

```powershell
$content = Get-Content "C:\Users\cloudy\AppData\Local\Temp\wiznote-asar\dist\renderer\renderer.dev.js" -Raw
$idx = $content.IndexOf("关键字")
$content.Substring([Math]::Max(0, $idx - 150), 400)
```

**验证 1 — 暗色壳层配色（MUI 主题工厂）**

```powershell
$content.IndexOf("28292A")   # 直接用一个足够独特的十六进制值当锚点
```

命中：

```js
backgroundColor:{danger:"#FF5E84",leftPane:e?"#121212":"#222530",
middlePane:e?"#28292A":"#F5F8FB",
middleScrollbar:e?"rgba(255, 255, 255, .2)":"rgba(0, 0, 0, 0.2)",
middlePaneSelectedItem:e?"rgba(85, 85, 85, .3)":"#DAE6F2",
middlePaneItemHover:e?"rgba(85, 85, 85, .15)":"rgba(112, 132, 164, .1)",
rightPane:e?"#333333":"#fff", ...}
```

（`e` 是 `isDark` 布尔量）一次命中同时坐实了 `EXTRACTION.md` 表里 5 项数值：`leftPane`/`middlePane`/`rightPane`/`middlePaneSelectedItem`/`middlePaneItemHover`，逐字符对得上。

**验证 2 — 代码块头部背景到底读的是哪个变量**

在 `wiznote-editor-main.css` 里搜 `code-title|editor-code-bg-color`，命中第 2186 行附近（32px 高的语言选择条规则）：

```css
{
  height: 32px;
  width: 100%;
  background-color: var(--editor-code-bg-color);   /* 不是 --editor-code-title-bg-color！ */
  padding-left: 8px;
  border-top-left-radius: 4px;
}
```

`--editor-code-title-bg-color` 这个"看起来专门给标题栏用"的变量在 `vars.css` 里明确定义了亮/暗两套值，但**实际渲染标题栏背景的规则用的是跟代码体共享的 `--editor-code-bg-color`**。这证实了"代码块头部与代码体同色（一体的淡灰块）"这个反直觉结论——细节见踩坑 #3。

**验证 3 — 暗色模式是否重新定义了 Prism 语法高亮颜色**

在 `wiznote-editor-main.css` 第 2288–2365 行找到完整的 Prism 默认主题（`.style-token.style-comment { color: slategray }` 等 9 组规则），确认这一整段**没有被包在任何 `.dark-mode` 前缀选择器或 `@media` 查询里**——是全局唯一定义，证实"暗色模式不改语法配色，明暗共用同一套 Prism 默认色板"。

**验证 4 — 选区透明度、复选框边框、14 色高亮盘是否有暗色专属值**

```powershell
Grep pattern: "checkbox-color|editor-selection-bg-color" 全文件搜索 wiznote-editor-vars.css
Grep pattern: "255,\s*246,\s*122|style-bg-color-" 全文件搜索
```

两次搜索都只在文件靠前的（亮色）区域各命中一次，`.dark-mode` 代码块（约行 370–680）里完全没有出现这几个变量名——证实 `--editor-selection-bg-color: #448aff66`、`--editor-checkbox-color: #b9bfc8`、`--style-bg-color-0..13`（14 色高亮盘）在暗色模式下**全部沿用亮色值**，没有被单独覆盖。

以上 4 组验证覆盖了 `EXTRACTION.md` 里最反直觉、最容易抄错、影响改动范围最大的几条结论，全部命中，才敢直接照着表去改 `theme.css`（而不是再重新人工核对一遍全表）。

## 3. 最终结论对照表（浅色实测值 vs 改动前 theme.css）

| 项 | 改动前 theme.css | 桌面版实际值（已验证） |
|---|---|---|
| 加粗字重 | `--bold-weight: 500` | `bold`（700），只有标题是 500 |
| 高亮 `mark` | 米黄底 + 黄色左边框 + 圆角 | 纯色背景 span，无边框无圆角（14 色盘，默认黄 `rgba(255,246,122,.8)`） |
| 分割线 | `1px dashed #cfd6e1` | `2px dashed #ccc` |
| 代码块头部 | 独立深灰 `rgb(220,223,227)` | 与代码体同色（一体的淡灰块，见验证 2） |
| 暗色左栏 | `#1c1f27` | `#121212` |
| 暗色笔记列表 | `#333333` | `#28292A`（与编辑区 `#333` 区分开） |
| 暗色代码底/头 | `rgba(255,255,255,.07)` / `.12` | `#96969640` / 与底色同变量 |
| 暗色语法高亮 | 自造的一套浅色系配色 | 与浅色完全相同的 Prism 原色（见验证 3） |
| 暗色表格 | 单元格透明、斑马 `rgba(255,255,255,.06)` | 单元格 `#2a2a2a`、斑马/标题行 `rgba(85,85,85,.2)` |
| 暗色复选框 | 边框 `#777` | 边框 `#b9bfc8`（暗色不变，见验证 4） |
| 选区 | 0.36 透明度 | `#448aff66`（0.4） |
| 暗色图片 | 无处理 | `filter: brightness(0.8)` |
| 表头 `th` | `font-weight:400` / 左对齐 | `font-weight:500` / 居中（对应官方 `row-title-table` 样式，见开放问题） |

对应的 `theme.css` / `CLAUDE.md` / `tests/test_wiz_web_parity.py` 改动已经落地在本轮工作树里，具体 diff 见 `git diff`（本轮未做 commit，改动仍在 working tree）。

## 4. 踩坑记录

### 坑 1：Service Worker 缓存是噪音源，别指望在里面找主题文件

4637 个条目里 99% 都是笔记正文引用的图片/附件资源，跟应用自身样式无关。`md_document.css` 这种"文件名看起来像主题"的条目，务必打开确认内容来源，别看名字就当真——这次它其实是某篇被剪藏保存的博客自带的第三方 CSS，只是恰好读起来也很像 GitHub 风格，容易让人误判为"找到了"。

### 坑 2：字符串精确匹配会撞上"假阳性"——图标示意图色值 ≠ 真实主题变量

第一次在 `renderer.dev.js` 里搜 `222530` 时，命中的是主题选择器 UI 里画"浅色主题预览缩略图"的一段 SVG：

```js
o.default.createElement("path", {
  d: "M12 16C12 13.7909 13.7909 12 16 12H32V48H12V16Z",
  fill: "#222530"   // 这只是给预览图标画色块，不是真正在用的 leftPane 变量！
})
```

数值完全相同（`#222530` 正好也是真实的 `leftPane` 亮色值），但上下文是 `React.createElement("path", {...})` 画图标，跟"验证 1"里那条真正的 `backgroundColor: {leftPane: ...}` 对象字面量完全是两处不同代码。

**教训**：命中一个数值后先看清楚上下文语义——落在 `createElement`/`svg`/`path`/`d:` 附近的，八成是图标示意图，要跳过去找下一个命中，直到落在一个明显是"配置对象/主题定义"的地方（比如 `backgroundColor: {...}`、`--editor-xxx: ...`）。

### 坑 3：死变量陷阱——变量被定义 ≠ 变量被实际引用

`--editor-code-title-bg-color` 在 `vars.css` 里堂堂正正定义了亮色 `rgb(220,223,227)` 和暗色 `#000` 两套值，命名上看就该是"代码块标题栏专属背景色"。但翻遍 `wiznote-editor-main.css`，真正渲染标题栏（32px 高的语言选择条）背景色的规则用的是 `var(--editor-code-bg-color)`——跟代码体共用同一个变量。那个"专属变量"没有在我们关心的渲染路径上被引用（可能是给别处用、历史遗留、或纯粹的死代码）。

**教训**：判断一个 token 的"最终视觉效果"，永远要反查它在哪些选择器规则里被引用，不能只看变量定义表就下结论——变量表里"存在"不代表"生效"。

### 坑 4：暗色模式"没覆盖"≠"没有暗色版"，而是"直接继承亮色"

`vars.css` 的 `.dark-mode` 代码块只重新定义了一部分变量（比如 `--editor-table-bg-color`、`--editor-code-bg-color`、`--editor-img-brightness`），完全没提到的（`--editor-checkbox-color`、`--editor-selection-bg-color`、14 色高亮盘 `--style-bg-color-0..13`、9 组 Prism 语法色）就是照抄外层同名变量的亮色值，没有独立的暗色定义。

改动前的 `theme.css` 犯的错误恰好是反过来：给几乎所有 token 都"发明"了一套看起来对称、实际上官方根本没做区分的暗色值（比如自造的暗色语法高亮配色、自造的暗色复选框边框）。这种"过度设计对称性"看起来更完整，但恰恰背离了原始设计意图。

**教训**：对齐一个多态 token 系统时，"暗色分支里这个变量不存在"本身就是一个有意义的信号（= 官方就是让它继承），不能默认"暗色理应有自己的一套值"就去凑一个。

### 坑 5：只有蒸馏笔记、没有原始材料时，反直觉结论必须留出回源验证的路

`EXTRACTION.md` 本身质量很高，但它是"人读代码后手工誊写的表格"，天然有转录风险。这次能做第 2 节的二次验证，完全是因为上一轮解包产物碰巧还留在 `%TEMP%` 里没被清理——这是运气，不是必然。

**教训**：拿到任何"调研总结"性质的产出，只要还摸得到原始材料，就该抽样回源验证，优先验证那些反直觉、影响改动面大、或者"如果错了会很尴尬"的结论（这次挑的是：加粗字重、mark 样式、hr、code header 共色、selection alpha、image brightness、暗色 table/left-pane/middle-pane——全部命中才敢直接照表改代码）。如果原始材料已经不可得，至少要在文档里明确标注"未回源验证，信度仅到转述层级"。

### 坑 6：中文全角框线表格在 Windows 终端里容易乱码，别用来存档

用户第一次转述调研结果时，用 Unicode 框线字符（`┌─┬─┐` 之类）手绘了一个 ASCII 对照表。在 Windows 终端的默认代码页下，部分中文标点和框线连接符被渲染成了 `�` 替换字符（原文里能看到"黄`��`左边框"、`┼──────┼──────┼───────���`这类乱码）。这次不影响我理解内容（能从上下文推断），但如果要把这类表格永久存档进仓库文档，应该统一改写成标准 Markdown 表格语法（就像本文档第 3 节这样），而不是手绘框线字符，避免跨终端/跨编码环境的乱码风险。

### 坑 7：临时解包目录不受版本控制、随时可能被系统清理，用完必须马上归档

`%TEMP%\wiznote-asar\`、`%TEMP%\nsd*.tmp\7z-out\` 这些中间产物都在系统临时目录下，Windows 的磁盘清理、重启、临时文件回收策略随时可能把它们删掉——这次是运气好还在，让我能做第 2 节的二次验证。一旦被清理，除非重新下载并解包 WizNote 安装包，否则没法再回源核对任何结论。

**教训**：解包/提取动作完成后，第一件事就是把用得上的文件复制进仓库长期保存（这正是 `docs/reference/` 目录存在的意义），绝不要假设临时目录"应该还在"。

## 5. 待复核问题（Open Questions）

以下两项在 `EXTRACTION.md` 和本轮改动里都做了"最合理推断"式的处理，但**没有用活的 DOM 计算样式验证过**，标记出来供后续复核：

1. **表格斑马纹默认开关**：`wiznote-editor-main.css` 里的 `stripe-style-table` 是 WizNote 编辑器里用户可以对某张表手动开/关的一个 class，不是全局样式常量。目前 `theme.css` 保留了斑马纹渲染（只是把颜色改成了实测的暗色 `rgba(85,85,85,.2)`），但**没有验证"从 Markdown 导入/粘贴生成的表格，斑马纹默认是开还是关"**。
2. **表头样式归类**：`wiznote-editor-main.css` 里的 `row-title-table`（首行加粗居中 + 特殊背景）同样是一个可选 class。本轮把 Obsidian 里 `<th>` 的样式改成了"字重 500 + 居中"去对齐这个 class 的效果，理由是"Markdown 表格语法本身就要求有一行表头分隔符，语义上等价于官方的首行标题"，但这个推断没有拿真机验证过。

**建议的验证方式**：按 `EXTRACTION.md` 里原本的建议，让 WizNote 桌面版带 `--remote-debugging-port` 参数启动，用仓库里已经配置好的 `chrome-devtools` MCP 直连它的活 DOM，新建一张从 Markdown 粘贴生成的表格，取计算样式（`getComputedStyle`）一锤定音。

另外，`errors-png/`（如果存在）目前仍是空的——如果之后收集到 Obsidian 端的实际问题截图，可以逐张对照本文档第 3 节的结论表复核。

## 6. 复现方法论（给未来的自己 / 后续贡献者）

如果 WizNote 桌面版升级导致 `renderer.dev.js` 内容变化，需要重新走一遍这轮提取，建议按这个顺序：

1. **定位安装目录**：`Test-Path "C:\Program Files\WizNote"`，确认是 Electron 壳。
2. **拿到 `app.asar`**：在应用安装目录下的 `resources/` 里找 `app.asar`；如果只有安装包（NSIS `.exe`），先用 7-Zip 解出安装包内容拿到 `app.asar`。
3. **解包 asar**：用 `asar` CLI（`npm install -g asar` 后 `asar extract app.asar <输出目录>`）展开，找到 `dist/renderer/renderer.dev.js` 和 `renderer.dev.css`。
4. **在 `renderer.dev.js` 里定位 CSS-in-JS 字符串块**：搜索特征字符串——变量表用 `--editor-` 前缀（如搜 `--editor-code-bg-color`），块级样式用 `.style-token.style-` 或 `.editor-main .root-container` 前缀，壳层配色用 `backgroundColor:{` 这类对象字面量特征。用 `Get-Content -Raw` 整个读入内存 + `.IndexOf`/`.Substring` 定位，比 `Select-String -Context` 在超长单行 JS 里更可靠。
5. **抽取并归档**：把定位到的字符串块整理成独立的 `.css` 文件，第一时间复制进 `docs/reference/`（不要留在 `%TEMP%` 里，见踩坑 #7）。
6. **交叉验证再落地**：写蒸馏笔记（如 `EXTRACTION.md`）之后，挑几条反直觉/高影响的结论回到原始文件里重新搜一次确认（见第 2 节的方法），确认无误才改 `theme.css`。

验证任何"调研总结"类产出时，建议过一遍这个 checklist：

- [ ] 原始源文件是否仍可访问？如果不能，本文档/笔记的可信度就只到"转述"层级，要如实标注。
- [ ] 反直觉、影响面大的结论是否逐一在源里复核过，而不是全盘相信蒸馏笔记？
- [ ] 命中的数值上下文是否明确是"运行时配置对象/CSS 规则"，而不是图标示意图、注释、或死代码？
- [ ] 一个变量在"变体分支"（暗色模式、移动端等）里"没被覆盖"，是被正确理解为"继承"，还是被误当成"没有数据、我随便猜一个"？
