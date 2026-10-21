#!/usr/bin/env python3
"""把站点名/搜索/主题/阅读模式挪到顶栏，并注册云屿集导航组件。"""
import sys

P = "quartz.config.yaml"
s = open(P, encoding="utf-8").read()

# 1) page-title -> header
s = s.replace(
    '''  - source: "@quartz-community/page-title"
    enabled: true
    layout:
      position: left
      priority: 10
''',
    '''  - source: "@quartz-community/page-title"
    enabled: true
    layout:
      position: header
      priority: 5
''',
    1,
)

# 2) search -> header
s = s.replace(
    '''  - source: "@quartz-community/search"
    enabled: true
    layout:
      position: left
      priority: 20
      group: toolbar
      groupOptions:
        grow: true
''',
    '''  - source: "@quartz-community/search"
    enabled: true
    layout:
      position: header
      priority: 30
      group: toolbar
      groupOptions:
        grow: true
''',
    1,
)

# 3) darkmode -> header
s = s.replace(
    '''  - source: "@quartz-community/darkmode"
    enabled: true
    layout:
      position: left
      priority: 30
      group: toolbar
''',
    '''  - source: "@quartz-community/darkmode"
    enabled: true
    layout:
      position: header
      priority: 20
      group: toolbar
''',
    1,
)

# 4) reader-mode -> header
s = s.replace(
    '''  - source: "@quartz-community/reader-mode"
    enabled: true
    layout:
      position: left
      priority: 35
      group: toolbar
''',
    '''  - source: "@quartz-community/reader-mode"
    enabled: true
    layout:
      position: header
      priority: 25
      group: toolbar
''',
    1,
)

# 5) 注册云屿集导航（插在 page-title 之前）
nav = '''  - source: "./plugins/yyj-nav"
    enabled: true
    options:
      links:
        - { label: 知识库, to: /kb }
        - { label: 博客, to: /blog/ }
        - { label: 关于我们, to: /about/ }
        - { label: GitHub, href: "https://github.com/YYJ-lin/YYJKnowledgebase" }
    layout:
      position: header
      priority: 10
'''
anchor = '  - source: "@quartz-community/page-title"'
if anchor not in s:
    sys.exit("page-title 块未找到")
s = s.replace(anchor, nav + anchor, 1)

open(P, "w", encoding="utf-8").write(s)
print("config patched: header 组件 + yyj-nav")
