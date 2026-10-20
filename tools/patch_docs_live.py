#!/usr/bin/env python3
"""站点已上线：更新 README / MIGRATION 的状态与地址。"""

# ---------- README ----------
p = "README.md"
s = open(p, encoding="utf-8").read()
s = s.replace(
    "- 线上（规划）：https://yyj-lin.github.io/YYJKnowledgebase/",
    "- 线上：https://yyj-lin.github.io/YYJKnowledgebase/",
)
s = s.replace(
    "仓库：`git@github.com:YYJ-lin/YYJKnowledgebase.git`（需先在 GitHub 建空仓库）",
    "仓库：`git@github.com:YYJ-lin/YYJKnowledgebase.git`（GitHub Pages 已启用，日常只需 `git push`）",
)
old_deploy = s[s.find("首次部署：") : s.find("域名或仓库名变了")]
new_deploy = """上线已经完成，Pages 的 Source 已设为 **GitHub Actions**。日常发布就是：

```bash
git add . && git commit -m "写一篇新文章" && git push
```

Actions 跑完（约 1–2 分钟）自动更新线上站点。手动重跑：仓库 Actions 页 → 选最近一次 run → Re-run all jobs。

"""
s = s.replace(old_deploy, new_deploy)
s = s.replace(
    "- [ ] 首次 push 到 `git@github.com:YYJ-lin/YYJKnowledgebase.git`（需先在 GitHub 建空仓库），并把 Pages Source 设为 GitHub Actions",
    "- [x] 首次 push 到 `git@github.com:YYJ-lin/YYJKnowledgebase.git`，Pages Source 设为 GitHub Actions —— 已上线",
)
open(p, "w", encoding="utf-8").write(s)
print("README updated")

# ---------- MIGRATION ----------
p = "MIGRATION.md"
s = open(p, encoding="utf-8").read()
s = s.replace(
    "| 部署 | 🟡 工作流与脚本已就绪，**等 GitHub 仓库创建后首次 push** |",
    "| 部署 | ✅ 已上线 https://yyj-lin.github.io/YYJKnowledgebase/（Actions 自动构建 + Pages） |",
)
s = s.replace(
    "> 新会话从这里接着做，不依赖对话记忆。最后更新：2026-10-20。",
    "> 新会话从这里接着做，不依赖对话记忆。最后更新：2026-10-20（已上线）。",
)
old_next = s[s.find("## 六、下一步（按顺序）") : s.find("## 七、已知遗留")]
new_next = """## 六、日常发布

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

"""
s = s.replace(old_next, new_next)
s = s.replace(
    "- 新仓库 remote：`origin` → `git@github.com:YYJ-lin/YYJKnowledgebase.git`（**仓库尚未创建**）",
    "- 新仓库 remote：`origin` → `git@github.com:YYJ-lin/YYJKnowledgebase.git`（已建、已推、Pages 已启用）",
)
open(p, "w", encoding="utf-8").write(s)
print("MIGRATION updated")
