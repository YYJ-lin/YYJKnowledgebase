#!/usr/bin/env python3
"""第四阶段：面包屑中文、页脚外链、首页不出现在侧栏等收尾配置。"""
import re
import sys

P = "quartz.config.yaml"
with open(P, "r", encoding="utf-8") as f:
    s = f.read()

# 1) 面包屑根节点：Home -> 首页
old_bc = '''  - source: "@quartz-community/breadcrumbs"
    enabled: true
    layout:
'''
new_bc = '''  - source: "@quartz-community/breadcrumbs"
    enabled: true
    options:
      rootName: 首页
    layout:
'''
if old_bc not in s:
    sys.exit("breadcrumbs 块未找到")
s = s.replace(old_bc, new_bc, 1)

# 2) 页脚只保留外链（站内绝对路径在 GitHub Pages 子路径下会 404，
#    四区自定义页脚留给后续的自定义组件）
s = re.sub(
    r'    options:\n      links:\n(?:        .*\n)+',
    '    options:\n      links:\n'
    '        GitHub: https://github.com/YYJ-lin\n'
    '        反馈与联系: https://github.com/YYJ-lin/YYJ-wiki/issues\n',
    s,
    count=1,
)

with open(P, "w", encoding="utf-8") as f:
    f.write(s)
print("ok")
