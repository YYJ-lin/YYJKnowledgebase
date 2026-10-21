# 云屿集 · 从 Docusaurus 迁移到 Quartz（交接文档）

> 新会话从这里接着做，不依赖对话记忆。最后更新：2026-10-20（已上线）。

## 一、目标

把站点从 **Docusaurus（MDX）** 迁到 **Quartz 5（纯 Markdown / Obsidian vault）**：

- 在 Obsidian 里写，实时预览，所见即所得
- 线上站点与 Obsidian 用同一套 Markdown 语法
- 保留云屿集品牌视觉（配色、字体、排版）

## 二、当前进度

| 项            | 状态                                                                              |
| ------------- | --------------------------------------------------------------------------------- |
| Quartz 5 源码 | ✅ `~/sites/yyj-quartz`（v5.0.0，来自 Gitee 镜像）                                |
| 依赖安装      | ✅ `npm install` 完成                                                             |
| 站点配置      | ✅ 标题 / `zh-CN` / baseUrl / 品牌配色 / 布局与侧栏排序                           |
| 内容迁移      | ✅ 7 篇 MDX → Obsidian Markdown（callout、Tabs、图片全部处理）                    |
| 字体          | ✅ 自托管 IBM Plex Sans + JetBrains Mono（不走 Google CDN）                       |
| 主题定制      | ✅ 760px 版心、首页 Hero + 三卡、四区页脚、暗色模式                               |
| 构建验证      | ✅ 本地构建 + `git archive` 干净检出构建均通过（78 文件）                         |
| 本地预览      | ✅ `./tools/preview.sh` + systemd 服务（模拟 `/YYJKnowledgebase/` 子路径）        |
| 部署          | ✅ 已上线 https://yyj-lin.github.io/YYJKnowledgebase/（Actions 自动构建 + Pages） |

## 三、环境事实

- 工作机：Ubuntu 24.04，Node v22.20.0（`~/.local/node/bin`），npm 10.9.3
- **GitHub HTTPS 超时，SSH 正常**（`ssh -T git@github.com` 返回 `Hi YYJ-lin!`）
- 拉开源代码用 Gitee 镜像：`https://gitee.com/linxiansheng0409/quartz`（已设为 `upstream`）
- 新仓库 remote：`origin` → `git@github.com:YYJ-lin/YYJKnowledgebase.git`（已建、已推、Pages 已启用）
- 旧站：`~/sites/my-website`（Docusaurus，仓库 `YYJ-wiki`），后台编辑器 `yyj-editor`（3002），**全程未改动**
- 端口占用：3000 / 3001 被旧后台占用，所以 `quartz build --serve` 要加 `--wsPort 3011`
- 本地预览：`http://192.168.1.102:8095/yyj-quartz/`（systemd 用户服务 `yyj-quartz-preview`）

## 四、目录与关键文件

```
content/                 Obsidian vault（首页 / about / business / industry / tools / blog / attachments）
quartz.config.yaml       站点配置：标题、locale、baseUrl、配色、45 个插件、布局
quartz/styles/custom.scss  品牌样式：字体 @font-face、Hero、卡片、四区页脚、暗色
quartz/styles/variables.scss  断点与栏宽（$sidePanelWidth 已改 280px）
quartz/static/fonts/     自托管 woff2（5 个文件）
quartz/static/icon.png   由 content/attachments/logo.svg 生成的站点图标（tools/make_icon.mjs）
plugins/yyj-footer/      自定义页脚插件（Preact，纯 JS，无需编译）
tools/preview.sh         构建 + 同步 + 重启预览
tools/deploy.sh          首次部署：检查远端仓库并 push
.github/workflows/deploy.yml  push v5 分支 → 构建 → Pages
```

## 五、这轮踩过的坑（改动前务必先读）

1. **`note-properties` 插件不能关**：front matter 解析挂在这个插件上，关掉后全站标题变「无题」、正文把 front matter 当文本渲染。要隐藏属性面板用 `hidePropertiesView: true`。
2. **字体别用 `@quartz-community/quartz-fonts`**：默认在 `<head>` 注入 Google Fonts 链接（国内会阻塞渲染）；自托管模式又把路径写死成 `/static/...`，项目页子路径下 404。现在的做法是 `fontOrigin: local` + 插件关闭 + `custom.scss` 里相对路径 `static/fonts/…` 的 `@font-face`。
3. **md 里的 HTML `<a>` 里不要放 `<h3>`**：标题锚点会插进来把 `<a>` 截断，卡片会拆成多个链接。首页卡片用 `<span class="card-title">`。
4. **内置页脚不能放站内链接**：只吃写死 href，子路径部署会 404。已换成本地插件，用 `cfg.baseUrl` 推导根路径。
5. **正文不要再写 `#` 一级标题**：页面 h1 由 front matter `title` 生成，否则出现两个大标题。
6. **`{2,4}` 行高亮**：Quartz 不支持，写了不报错也不生效。
7. **背景进程**：ssh 命令结束后 `nohup ... &` 会被回收，长期预览要用 systemd 用户服务。
8. **wiki 链接按文件名/路径写**：`[[写作指南]]`（页面标题）会变成死链，必须写 `[[writing-guide]]` 或 `[[about/writing-guide|写作指南]]`。
9. **不要给 `.sidebar` 加 `display:none`**：搜索弹层（`.search-container`）是 sidebar 的子元素，整栏隐藏会连搜索一起隐藏（点了没反应、输入框宽度为 0）。首页的做法是把 grid 改成单栏 + `grid-template-areas` 里保留 `grid-sidebar-left`，再让 `.sidebar.left` 横排贴右上，只隐藏其中的 `.page-title` / `.explorer`。
10. **手机端目录浮层会溢出 16px**：`.explorer-content` 是 `position:absolute; width:100vw`，而 `#quartz-body` 在移动端有 `padding:0 1rem`，左栏因此偏移 1rem。修法是给移动端的 `.sidebar.left` 加 `margin:0 -1rem; padding-left/right:1rem` 让它拉满。
11. **搜索弹层「偏了」= 祖先元素有 transform / backdrop-filter**：它们会成为 的包含块，弹层就从那个元素左上角开始铺。顶栏毛玻璃因此改到 上，居中也不能用 ，改用 。
12. **改了本地插件要清缓存**： 是构建时拷进去的副本，改完 不删它会继续用旧代码（现象：CSS 变了但组件结构没变）。 再 build。
13. **移动端 grid 顺序**：`$mobileGrid` 里 `grid-header` 要放在第一行，否则顶栏会跑到「探索」按钮下面。
14. **Mermaid 是浏览器端渲染**：脚本从 `cdnjs.cloudflare.com` 懒加载（只在含图页面触发，约 26 个请求），静态 HTML 里只有 `<code class="mermaid">`，别在构建产物里找 SVG。
15. **GitHub Pages 第一次必须手动启用**：`configure-pages` 的 `enablement: true` 需要仓库管理员权限，`GITHUB_TOKEN` 没有，会 403。

## 六、日常发布

```bash
cd ~/sites/yyj-quartz
# 写内容：用 Obsidian 打开 content/，或直接改 md
git add . && git commit -m "写一篇新文章" && git push
```

约 1–2 分钟后线上自动更新。排查构建失败：仓库 Actions 页面看那一次 run 的日志。

验收 checklist（上线时已全部通过，改版后再跑一遍）：

- [x] 首页 Hero、三卡样式正常，卡片可点
- [x] 侧栏顺序：业务分享 / 行业知识 / 工具资源 / 关于云屿集 / 博客
- [x] 字体是 IBM Plex Sans（Network 里无 Google Fonts 请求）
- [x] 组件演示页 callout、mermaid、数学公式（MathJax）、脚注、wiki 链接正常
- [x] 搜索能搜到「写作」
- [x] 暗色模式切换正常
- [x] 页脚四区链接全部可达（无 404）
- [x] 404 页面中文

## 七、已知遗留

- （已解决）公式改用 MathJax 服务端 SVG，产物里已无 KaTeX/jsdelivr 引用
- Mermaid 仍从 cdnjs 懒加载（插件写死），国内可能偏慢；目前只在有公式时才有字体请求。要彻底去掉需给 latex 插件打补丁或换渲染器。
- 页脚在桌面端位于中间栏网格内（宽度约 930px），未做成通栏；如需通栏要改 Quartz 的 grid 布局。
- 站点还没有自定义域名，`baseUrl` 目前是 `yyj-lin.github.io/YYJKnowledgebase`。

## 八、回滚

旧站与旧仓库完全没动：`~/sites/my-website`、`git@github.com:YYJ-lin/YYJ-wiki.git`。新站验证不通过时，把 DNS/入口指回旧站即可，删除新仓库也不影响旧站。
