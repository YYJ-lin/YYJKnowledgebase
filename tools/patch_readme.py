#!/usr/bin/env python3
"""README 更新：页脚已完成 + 记录本地插件目录。"""
P = "README.md"
s = open(P, encoding="utf-8").read()

s = s.replace(
    """tools/                ← 构建与预览辅助脚本""",
    """plugins/yyj-footer/   ← 自定义页脚组件（本地 Quartz 插件，四区 + 子路径安全链接）
tools/                ← 构建与预览辅助脚本""",
)

old_todo = """## 已知待办

- [ ] 页脚四区（内容导航 / 相关资源 / 关于与反馈 / 品牌）：现在用内置页脚，只放外链；站内绝对路径在子路径部署下会 404，需要自定义页脚组件
- [ ] 旧站 `~/sites/my-website` 与后台编辑器 `yyj-editor` 的退役（等新站验证稳定后再决定）
- [ ] 评论（Giscus）、访问统计（可选，需要时再开）"""
new_todo = """## 自定义页脚

内置页脚只接受写死的 href，站内链接在 `/yyj-quartz/` 子路径下会 404，所以换成了本地插件 `plugins/yyj-footer/`：

- 组件在 `plugins/yyj-footer/index.js`（纯 Preact，无需编译），`package.json` 里的 `quartz` 字段是 Quartz 的插件清单；
- 链接由 `cfg.baseUrl` 推导站点根（`/yyj-quartz`），域名根和子路径部署都成立；
- 四区内容和文案在 `quartz.config.yaml` 里该插件的 `options` 段配置，改文案不用动代码；
- 样式在 `quartz/styles/custom.scss` 的「页脚」一节。

## 已知待办

- [x] 页脚四区（内容导航 / 相关资源 / 关于与反馈 / 品牌）—— 已用本地插件实现
- [ ] 首次 push 到 `git@github.com:YYJ-lin/yyj-quartz.git`（需先在 GitHub 建空仓库），并把 Pages Source 设为 GitHub Actions
- [ ] 旧站 `~/sites/my-website` 与后台编辑器 `yyj-editor` 的退役（等新站验证稳定后再决定）
- [ ] 评论（Giscus）、访问统计（可选，需要时再开）"""
if old_todo not in s:
    raise SystemExit("README 待办段未找到")
s = s.replace(old_todo, new_todo, 1)

open(P, "w", encoding="utf-8").write(s)
print("README updated")
