#!/usr/bin/env python3
"""第七阶段：恢复 note-properties（它同时负责 front matter 解析），只隐藏属性面板。"""
P = "quartz.config.yaml"
s = open(P, encoding="utf-8").read()

old = '''  - source: "@quartz-community/note-properties"
    enabled: false
    options:
      includeAll: false
      includedProperties:
        - description
        - tags
        - aliases
      excludedProperties: []
      hidePropertiesView: false
'''
new = '''  - source: "@quartz-community/note-properties"
    enabled: true
    options:
      includeAll: false
      includedProperties: []
      excludedProperties: []
      hidePropertiesView: true
'''
if old not in s:
    raise SystemExit("note-properties 块未找到")
s = s.replace(old, new, 1)
open(P, "w", encoding="utf-8").write(s)
print("note-properties re-enabled (properties view hidden)")
