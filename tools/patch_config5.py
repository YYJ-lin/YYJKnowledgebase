#!/usr/bin/env python3
"""第五阶段：关掉 CNAME 插件（项目页用不到自定义域名文件，写错会顶掉用户主页）。"""
P = "quartz.config.yaml"
with open(P, "r", encoding="utf-8") as f:
    s = f.read()
old = '  - source: "@quartz-community/cname"\n    enabled: true\n'
new = '  - source: "@quartz-community/cname"\n    enabled: false\n'
if old not in s:
    raise SystemExit("cname 块未找到")
s = s.replace(old, new, 1)
with open(P, "w", encoding="utf-8") as f:
    f.write(s)
print("cname disabled")
