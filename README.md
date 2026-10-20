# 云屿集（Quartz 5）

用 [Quartz 5](https://quartz.jzhao.xyz) 搭建的「云屿集」站点：内容就是 `content/` 里的 Markdown，用 Obsidian 直接打开这个目录即可写作。

- 线上（规划）：https://yyj-lin.github.io/yyj-quartz/
- 本地预览：http://192.168.1.102:8095/yyj-quartz/（模拟 GitHub Pages 子路径）
- 旧站（Docusaurus）：`~/sites/my-website`，仓库 `YYJ-wiki`，保持不动，随时可回滚

## 目录结构

```
content/              ← Obsidian vault，所有内容在这里
├── index.md          ← 首页（Hero + 三张入口卡）
├── about/            ← 关于、写作指南、组件演示
├── business/         ← 知识库：业务分享
├── industry/         ← 知识库：行业知识
├── tools/            ← 知识库：工具资源
├── blog/             ← 博客（文件名建议 日期-标题.md）
└── attachments/      ← 图片等附件
quartz.config.yaml    ← 站点配置（标题、baseUrl、配色、插件、布局）
quartz/styles/        ← 主题样式
├── custom.scss       ← 云屿集的自定义样式（字体 / Hero / 卡片 / 页脚）
└── variables.scss    ← 布局断点、栏宽
quartz/static/        ← 静态资源（icon.png 站点图标、fonts/ 自托管字体）
plugins/yyj-footer/   ← 自定义页脚组件（本地 Quartz 插件，四区 + 子路径安全链接）
tools/                ← 构建与预览辅助脚本
.github/workflows/deploy.yml  ← 推送到 v5 分支即自动部署
```

## 日常写作

1. 用 Obsidian 打开 `content/` 目录；
2. 新建文章，写 front matter（`title` / `description` / `date` / `tags`）；
3. 正文**不要再写 `#` 一级标题**，页面标题由 front matter 的 `title` 生成；
4. 图片拖进笔记，会自动落到 `content/attachments/`；
5. 提交推送，GitHub Actions 自动构建发布。

分类就是文件夹：在 `content/` 下新建目录并放一个 `index.md`（写 `title` 和介绍），侧边栏会自动出现该分组。

## 本地预览

```bash
./tools/preview.sh          # 构建 + 同步 + 重启预览
```

预览服务是 systemd 用户服务：

```bash
systemctl --user status  yyj-quartz-preview
systemctl --user restart yyj-quartz-preview
journalctl --user -u yyj-quartz-preview -n 50
```

预览地址 `http://192.168.1.102:8095/yyj-quartz/`，故意挂在 `/yyj-quartz/` 子路径下，用来验证 GitHub Pages 项目页的路径是否正确。

也可以直接用 Quartz 自带的热更新服务器：

```bash
export PATH=$HOME/.local/node/bin:$PATH
npx quartz build --serve --wsPort 3011   # http://localhost:8080，只监听本机
# 3000/3001 被旧后台编辑器占用，所以显式指定 WebSocket 端口；只在本机看就用这个
```

## 部署

仓库：`git@github.com:YYJ-lin/yyj-quartz.git`（需先在 GitHub 建空仓库）

首次部署：

1. GitHub 仓库 → Settings → Pages → Source 选 **GitHub Actions**；
2. 本地 `git push origin v5`；
3. Actions 跑完即上线 `https://yyj-lin.github.io/yyj-quartz/`。

域名或仓库名变了，只改一处：`quartz.config.yaml` 里的 `baseUrl`（形如 `用户名.github.io/仓库名`，不带 `https://`）。

## 从 Docusaurus 迁移的对照

| 旧写法 | 现在 |
| --- | --- |
| `::::tip[标题]` | `> [!tip] 标题`（Obsidian callout） |
| `<Tabs>` / `<TabItem>` | 并列小标题 |
| `import ... from ...` | 删掉 |
| `{/* truncate */}` | 删掉 |
| `/img/xxx.png` | `../attachments/xxx.png` |
| `[文字](/about)` | `[文字](../about/)` 或 `[[about/index]]` |

行高亮 `{2,4}` 目前不支持，写了不报错也不生效。

## 自定义页脚

内置页脚只接受写死的 href，站内链接在 `/yyj-quartz/` 子路径下会 404，所以换成了本地插件 `plugins/yyj-footer/`：

- 组件在 `plugins/yyj-footer/index.js`（纯 Preact，无需编译），`package.json` 里的 `quartz` 字段是 Quartz 的插件清单；
- 链接由 `cfg.baseUrl` 推导站点根（`/yyj-quartz`），域名根和子路径部署都成立；
- 四区内容和文案在 `quartz.config.yaml` 里该插件的 `options` 段配置，改文案不用动代码；
- 样式在 `quartz/styles/custom.scss` 的「页脚」一节。

## 已知待办

- [x] 页脚四区（内容导航 / 相关资源 / 关于与反馈 / 品牌）—— 已用本地插件实现
- [ ] 首次 push 到 `git@github.com:YYJ-lin/yyj-quartz.git`（需先在 GitHub 建空仓库），并把 Pages Source 设为 GitHub Actions
- [ ] 旧站 `~/sites/my-website` 与后台编辑器 `yyj-editor` 的退役（等新站验证稳定后再决定）
- [ ] 评论（Giscus）、访问统计（可选，需要时再开）
