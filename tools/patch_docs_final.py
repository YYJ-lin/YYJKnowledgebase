#!/usr/bin/env python3
"""收尾文档：补 wiki 链接规则、自检工具、遗留项。"""

# ---------- README ----------
p = "README.md"
s = open(p, encoding="utf-8").read()
anchor = "## 自定义页脚"
add = """## 自检

```bash
./tools/verify.sh                                   # 构建产物不变量（标题/字体/页脚/渲染/索引）
python3 tools/check_links.py                        # 线上站内链接全量体检（也可传本地预览地址）
```

"""
if anchor in s and "## 自检" not in s:
    s = s.replace(anchor, add + anchor, 1)
open(p, "w", encoding="utf-8").write(s)
print("README updated")

# ---------- MIGRATION ----------
p = "MIGRATION.md"
s = open(p, encoding="utf-8").read()

old7 = "7. **背景进程**：ssh 命令结束后 `nohup ... &` 会被回收，长期预览要用 systemd 用户服务。"
new7 = old7 + """
8. **wiki 链接按文件名/路径写**：`[[写作指南]]`（页面标题）会变成死链，必须写 `[[writing-guide]]` 或 `[[about/writing-guide|写作指南]]`。
9. **Mermaid 是浏览器端渲染**：脚本从 `cdnjs.cloudflare.com` 懒加载（只在含图页面触发，约 26 个请求），静态 HTML 里只有 `<code class="mermaid">`，别在构建产物里找 SVG。
10. **GitHub Pages 第一次必须手动启用**：`configure-pages` 的 `enablement: true` 需要仓库管理员权限，`GITHUB_TOKEN` 没有，会 403。"""
if old7 in s:
    s = s.replace(old7, new7, 1)

old_known = "- KaTeX 的 CSS 仍从 `cdn.jsdelivr.net` 加载"
if old_known in s:
    s = s.replace("- KaTeX 的 CSS 仍从 `cdn.jsdelivr.net` 加载", "- （已解决）公式改用 MathJax 服务端 SVG，产物里已无 KaTeX/jsdelivr 引用\n- Mermaid 仍从 cdnjs 懒加载")
open(p, "w", encoding="utf-8").write(s)
print("MIGRATION updated")
