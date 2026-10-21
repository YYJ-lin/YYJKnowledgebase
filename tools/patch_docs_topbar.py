#!/usr/bin/env python3
"""文档：补顶栏与移动端说明。"""

p = "README.md"
s = open(p, encoding="utf-8").read()
old = "- 想让侧边栏重新显示全部目录：删掉 `quartz.config.yaml` 里 explorer 的 `filterFn` 即可。"
add = old + """
- **顶栏**：本地组件 `plugins/yyj-nav`（知识库 / 博客 / 关于我们 / GitHub）+ 站点名 + 工具条，位于 `quartz/components/frames/DefaultFrame.tsx` 里的 `.topbar`（`grid-header` 区域横跨三列）。这是对上游 frame 的唯一改动。
- **手机端（≤800px）**：grid 顺序为 顶栏 → 左栏 → 正文 → 右栏 → 页脚；顶栏两行（站点名 + 工具条 / 导航），左栏拉满宽度避免目录浮层溢出。"""
if old in s:
    s = s.replace(old, add, 1)
open(p, "w", encoding="utf-8").write(s)
print("README updated")

p = "MIGRATION.md"
s = open(p, encoding="utf-8").read()
old = "10. **Mermaid 是浏览器端渲染**"
add = """10. **手机端目录浮层会溢出 16px**：`.explorer-content` 是 `position:absolute; width:100vw`，而 `#quartz-body` 在移动端有 `padding:0 1rem`，左栏因此偏移 1rem。修法是给移动端的 `.sidebar.left` 加 `margin:0 -1rem; padding-left/right:1rem` 让它拉满。
11. **移动端 grid 顺序**：`$mobileGrid` 里 `grid-header` 要放在第一行，否则顶栏会跑到「探索」按钮下面。
12. **Mermaid 是浏览器端渲染**"""
if old in s and "手机端目录浮层会溢出" not in s:
    s = s.replace(old, add, 1)
    s = s.replace("11. **GitHub Pages 第一次必须手动启用**", "13. **GitHub Pages 第一次必须手动启用**", 1)
open(p, "w", encoding="utf-8").write(s)
print("MIGRATION updated")
