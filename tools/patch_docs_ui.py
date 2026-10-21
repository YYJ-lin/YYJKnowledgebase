#!/usr/bin/env python3
"""文档：记录首页/侧边栏的改造方式。"""

p = "README.md"
s = open(p, encoding="utf-8").read()
anchor = "## 自检"
add = """## 首页与侧边栏

- **首页是单栏落地页**：`content/index.md` 里的 Hero（搜索框 + 两个入口）+「从这里开始」三卡；左目录树和右目录在首页不渲染（`quartz.config.yaml` 里 explorer / table-of-contents 的 `condition: not-index`），顶端保留搜索/主题/阅读模式工具条。
- **侧边栏只显示当前分类**：explorer 的 `filterFn` 读当前 URL 的第一段来决定显示哪一类；首页和 `/kb` 显示完整目录；`tags` 永不进目录。
- **`/kb` 是知识库汇总页**（`content/kb.md`），首页 Hero 的「进入知识库」指向它。
- 想让侧边栏重新显示全部目录：删掉 `quartz.config.yaml` 里 explorer 的 `filterFn` 即可。

"""
if anchor in s and "## 首页与侧边栏" not in s:
    s = s.replace(anchor, add + anchor, 1)
open(p, "w", encoding="utf-8").write(s)
print("README updated")

p = "MIGRATION.md"
s = open(p, encoding="utf-8").read()
old = "9. **Mermaid 是浏览器端渲染**"
add = """9. **不要给 `.sidebar` 加 `display:none`**：搜索弹层（`.search-container`）是 sidebar 的子元素，整栏隐藏会连搜索一起隐藏（点了没反应、输入框宽度为 0）。首页的做法是把 grid 改成单栏 + `grid-template-areas` 里保留 `grid-sidebar-left`，再让 `.sidebar.left` 横排贴右上，只隐藏其中的 `.page-title` / `.explorer`。
10. **Mermaid 是浏览器端渲染**"""
if old in s and "不要给 `.sidebar` 加" not in s:
    s = s.replace(old, add, 1)
    # 原来的 10 号顺延为 11
    s = s.replace("10. **GitHub Pages 第一次必须手动启用**", "11. **GitHub Pages 第一次必须手动启用**", 1)
open(p, "w", encoding="utf-8").write(s)
print("MIGRATION updated")
