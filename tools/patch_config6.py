#!/usr/bin/env python3
"""第六阶段：关掉 Obsidian 属性面板（会在正文顶部重复展示 description/tags）。"""
P = "quartz.config.yaml"
s = open(P, encoding="utf-8").read()
old = '  - source: "@quartz-community/note-properties"\n    enabled: true\n'
new = '  - source: "@quartz-community/note-properties"\n    enabled: false\n'
if old not in s:
    raise SystemExit("note-properties 块未找到")
s = s.replace(old, new, 1)
open(P, "w", encoding="utf-8").write(s)
print("note-properties disabled")
