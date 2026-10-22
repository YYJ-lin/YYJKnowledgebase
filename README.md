# 云屿集

用 [Quartz 5](https://quartz.jzhao.xyz) 搭的个人站点：技术手记 + 业务笔记，内容就是 `content/` 里的 Markdown，用 Obsidian 直接打开这个目录写作。

- 线上：https://yyj-lin.github.io/YYJKnowledgebase/
- 本地预览：http://192.168.1.102:8095/YYJKnowledgebase/（模拟 GitHub Pages 子路径）
- 仓库：`git@github.com:YYJ-lin/YYJKnowledgebase.git`（Pages 已启用，日常只需 `git push`）

## 结构

```
content/           Obsidian vault，所有内容
├── index.md       首页（Hero + 三卡）
├── tech/          技术手记
├── kb/            知识库（教程与文档）
│   ├── index.md
│   ├── erpnext/   ERPNext 教程
│   ├── wordpress/ WordPress 教程
│   ├── apps/      应用介绍与使用
│   └── industry/  行业常识
├── tools/         资源与工具
├── about/         关于 / 联系 / 隐私 / 许可 / 写作指南 / 开站记
└── attachments/   图片附件

plugins/           本地 Quartz 插件（改完要删 .quartz/plugins/<name> 缓存）
├── yyj-nav        顶栏（导航 + 搜索/主题/阅读 + 微信/QQ 二维码 + 手机菜单）
├── yyj-footer     页脚（品牌 + 三列 + 法务行 + 回到顶部）
└── yyj-crumbs     面包屑（首页 › 分类 › 文章，层级取自 frontmatter）

tools/             构建与自检脚本
quartz/            Quartz 框架（只改了 3 个文件，见下）
quartz.config.yaml 站点配置（标题、配色、插件、布局、页脚、导航兜底）
```

## 日常写作

1. 用 Obsidian 打开 `content/`；
2. 技术文章放 `content/tech/`，命名 `2026-10-21-xxx.md`（**文件名就是 URL**）；
3. front matter 至少写 `title`、`description`，技术手记建议加 `date`；
4. 正文不要再写 `#` 一级标题（h1 由 title 生成）；
5. 发布：

```bash
cd ~/sites/yyj-quartz
./tools/preview.sh                 # 本地看一眼
git add . && git commit -m "写一篇 xxx" && git push
```

推送后 GitHub Actions 自动构建发布，约 1–2 分钟。

### 新增一个分类

建目录 + `index.md`，写：

```yaml
---
title: Docker
description: 容器化部署相关
nav: true # 进顶栏
navOrder: 5 # 排序
parent: kb # 可选：面包屑挂到 /kb 下
---
```

顶栏、手机菜单目录、面包屑、搜索索引都会自动跟着变（分类顺序见 `plugins/yyj-nav/index.js` 里的 `SECTION_RANK`）。

## 对上游 Quartz 的改动（共 3 处）

| 文件                                        | 改了什么                                        | 为什么                             |
| ------------------------------------------- | ----------------------------------------------- | ---------------------------------- |
| `quartz/components/frames/DefaultFrame.tsx` | header 组件抽到 `.topbar`，grid-header 横跨整行 | 要做通栏顶栏                       |
| `quartz/components/Head.tsx`                | viewport-fit、theme-color、RSS alternate        | 手机安全区 / 状态栏颜色 / RSS 发现 |
| `quartz/components/pages/404.tsx`           | 中文文案 + 主入口链接                           | GitHub Pages 默认 404 太裸         |

升级上游时这三处可能要手工合并。

## 自检

```bash
./tools/verify.sh                          # 构建产物不变量（标题/字体/页脚/面包屑/索引）
python3 tools/check_links.py               # 线上或本地预览的站内链接体检（可传 URL）
./tools/make_icon.mjs                      # 从 logo.svg 生成站点图标
```

## 部署

GitHub Pages（Actions 构建）。域名或仓库名变了，只改 `quartz.config.yaml` 的 `baseUrl`（形如 `用户名.github.io/仓库名`，不带 `https://`）。

有自定义域名后：仓库 Settings → Pages 填域名 + 仓库根加 `CNAME` 文件，再把 `baseUrl` 改成域名。

## 待办

- [ ] 自定义域名
- [ ] `/services/` 单页（轻量获客，等有服务可写）
- [ ] `/archive/` 归档页（文章过 20 篇再做）
- [ ] giscus 评论 / Umami 统计（按需）
