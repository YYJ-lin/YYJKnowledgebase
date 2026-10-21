---
title: 写作指南
description: 这个站怎么组织内容、怎么在 Obsidian 里写、怎么发布
---

这一页写给未来的自己：新文章放哪、front matter 怎么写、怎么在本地看一眼再发布。

## 一、目录结构

站点直接读 `content/`，用 Obsidian 打开这个目录就能写：

```
content/
├── index.md              首页
├── tech/                 技术手记（顶栏「技术手记」）
│   └── index.md
├── kb.md                 知识库总入口（顶栏「知识库」）
├── business/             知识库 › 业务分享
├── industry/             知识库 › 行业知识
├── tools/                资源与工具
├── about/                关于（含 联系 / 隐私 / 许可 / 写作指南 / 开站记）
└── attachments/          图片附件
```

**文件名就是网址**：`content/tech/2026-10-21-docker.md` → `/tech/2026-10-21-docker`。改了文件名要给旧地址留一条 `aliases`，否则老链接会 404。

## 二、front matter

```yaml
---
title: Docker 里跑 ERPNext 的三个坑
description: 一句话说明这篇解决什么问题
date: 2026-10-21
tags: [docker, erpnext]
---
```

| 字段                            | 作用                                                    |
| ------------------------------- | ------------------------------------------------------- |
| `title`                         | 标题，同时渲染成页面 h1 和侧栏名字                      |
| `description`                   | 摘要，用于搜索与分享预览                                |
| `date`                          | 技术手记建议写；知识库可选                              |
| `tags`                          | 会生成标签页，并在文章顶部显示                          |
| `aliases`                       | 旧地址跳转，改文件名时必填                              |
| `nav` / `navOrder` / `navLabel` | 给**分类首页**用：进顶栏、排序、导航显示名              |
| `parent`                        | 给**分类首页**用：面包屑挂到某个上级（如 `parent: kb`） |

> [!warning] 正文不要再写一级标题
> 页面 h1 由 `title` 生成，正文里再写 `# 标题` 会出现两个大标题。

## 三、新增一个分类

在 `content/` 下建目录，放一个 `index.md`：

```yaml
---
title: Docker
description: 容器化部署相关
nav: true
navOrder: 5
parent: kb # 想挂在知识库下面才写；不写就是顶级栏目
---
```

提交后会自动发生这些事：顶栏多一项（如果写了 `nav: true`）、手机菜单「目录」里多一个可折叠分类并显示篇数、面包屑自动补上级、搜索索引更新。

## 四、常用写法

### 提示框

```md
> [!tip] 小标题
> 内容
```

类型：`note / tip / info / caution / warning / danger`。

### 代码块

````md
```bash
docker compose up -d
```
````

### 图片

图片放 `content/attachments/`，用相对路径：

```md
![截图](../attachments/docker-1.png)
```

### Wiki 链接

```md
[[tech/2026-10-21-docker]]
[[tech/2026-10-21-docker|Docker 那篇]]
```

按**文件名或路径**写，不要按标题写。

### 表格、任务列表、脚注、折叠块、Mermaid、数学公式

都支持，语法与 Obsidian 一致（`- [ ]` 任务、`[^1]` 脚注、`<details>` 折叠、` ```mermaid `、`$…$`）。

## 五、本地看效果

```bash
cd ~/sites/yyj-quartz
./tools/preview.sh        # 构建 + 同步 + 重启预览
```

预览地址 http://192.168.1.102:8095/YYJKnowledgebase/ ，挂在子路径下，和线上环境一致。

## 六、发布

```bash
git add . && git commit -m "写一篇 Docker 的文章" && git push
```

推送后 GitHub Actions 自动构建发布，约 1–2 分钟。构建失败的话去仓库 Actions 页面看那一次 run 的日志。

## 七、几条约定

1. 一篇一个主题，标题写清楚"解决什么问题"；
2. 长文多用小标题，代码块标语言；
3. 命令写清在哪台机器跑；
4. 图片放 `attachments/`，别用外链（会挂）；
5. 发布前跑一遍 `./tools/preview.sh` 和 `python3 tools/check_links.py`。
