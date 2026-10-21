# 交接文档

> 新会话从这里接着做，不依赖对话记忆。最后更新：2026-10-21。

## 一、现状

站点从 Docusaurus 迁到 **Quartz 5**，已上线：https://yyj-lin.github.io/YYJKnowledgebase/

| 项     | 状态                                                                |
| ------ | ------------------------------------------------------------------- |
| 框架   | Quartz 5（Gitee 镜像克隆，`upstream` 指向镜像，`origin` 是 GitHub） |
| 内容   | `content/` 下 11 篇 md，4 个分类 + 关于                             |
| 品牌   | 自托管 IBM Plex Sans / JetBrains Mono，知识蓝配色，日夜两套         |
| 布局   | 通栏顶栏 + 左目录 + 居中正文 + 右目录/图谱 + 四列页脚               |
| 手机端 | 顶栏收成一行，「导航 / 目录」两个页签，目录按分类折叠带篇数         |
| 部署   | GitHub Actions → Pages，push `main` 即发布                          |

## 二、结构决策（别轻易改）

1. **顶栏项由 frontmatter 驱动**：分类 `index.md` 写 `nav: true` + `navOrder`（+ `navLabel`），`plugins/yyj-nav` 从 `allFiles` 里挑；`quartz.config.yaml` 里的 `links` 只是兜底。
2. **面包屑层级**同理：`parent: kb` 表示挂在知识库下，不写就是顶级栏目（`plugins/yyj-crumbs`）。
3. **搜索/主题/阅读模式在顶栏**，不在左栏；左栏只放目录树。
4. **手机端没有独立侧栏**：目录并进了菜单，`.sidebar.left` 在 ≤800px 直接隐藏。
5. **页脚/面包屑/导航都是本地插件**，因为内置组件只会拼死链，子路径部署会 404。

## 三、踩过的坑

1. **`note-properties` 插件不能关**：front matter 解析挂在它身上，关掉后全站标题变「无题」。要隐藏属性面板用 `hidePropertiesView: true`。
2. **字体别用 `@quartz-community/quartz-fonts`**：默认注入 Google Fonts 链接；自托管模式又写死 `/static/...` 子路径会 404。现在用 `fontOrigin: local` + `custom.scss` 里相对路径 `@font-face`。
3. **md 里的 `<a>` 里不要放 `<h3>`**：标题锚点会插进来截断 `<a>`。
4. **正文不要再写 `#` 标题**：h1 由 frontmatter 生成。
5. **`.sidebar` 不能整块 `display:none`**（在还需要搜索弹层的页面）：`position: fixed` 的弹层会跟着隐藏。我们用条件渲染 + 移动端单独处理。
6. **祖先有 `transform` / `backdrop-filter` 时，`position: fixed` 弹层会以它为包含块**：搜索弹层「偏了」就是这个原因；顶栏毛玻璃放在 `::before`，居中不能用 transform，改用负 margin。
7. **`.yyj-nav` 的 `overflow-x: auto` 会连带 `overflow-y`**：手机菜单面板会被裁在 40px 容器里，点了像没反应。
8. **`height: 100%` 放在 grid item（.card）上**：auto 行高会先解成较小值，内容溢出压到下一张卡。
9. **改了 `plugins/*/` 必须删 `.quartz/plugins/<name>` 缓存**，否则构建继续用旧副本。
10. **GitHub Pages 第一次要手动启用 Pages**（Source: GitHub Actions）；`configure-pages` 的 `enablement: true` 需要管理员权限，GITHUB_TOKEN 没有。
11. **wiki 链接按文件名/路径写**，按标题写会死链。
12. **Mermaid 是浏览器端渲染**（cdnjs 懒加载），静态 HTML 里只有 `<code class="mermaid">`。
13. **背景进程会被 ssh 回收**：长期预览用 systemd 用户服务 `yyj-quartz-preview`。

## 四、运维

```bash
cd ~/sites/yyj-quartz
./tools/preview.sh            # 构建 + 同步 + 重启预览服务
./tools/verify.sh             # 产物自检
python3 tools/check_links.py  # 站内链接体检（默认线上）
systemctl --user status yyj-quartz-preview
journalctl --user -u yyj-quartz-preview -n 50
```

部署：`git push` → Actions → Pages。`tools/deploy.sh` 是首次部署用的检查脚本，平时用不到。

## 五、待办

- [ ] 自定义域名（改 `baseUrl` + `CNAME`）
- [ ] `/services/` 单页（技术博客为主，获客只留一个触点）
- [ ] `/archive/` 归档页（文章 ≥20 篇再做）
- [ ] giscus 评论、Umami 统计（按需，需要外部账号）
- [ ] 二级分类（`tech/erpnext/` 这类）：菜单目录目前只按一级分组，需要再加一层折叠

## 六、回滚

旧站 `~/sites/my-website`（Docusaurus）与仓库 `YYJ-wiki` 全程未动；新站出问题把入口指回旧站即可。
