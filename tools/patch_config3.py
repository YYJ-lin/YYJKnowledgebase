#!/usr/bin/env python3
"""第三阶段：正文颜色、侧栏排序、页脚、关掉图谱、首页隐藏自动标题。"""
import re
import sys

P = "quartz.config.yaml"
with open(P, "r", encoding="utf-8") as f:
    s = f.read()

# 1) 正文用可读的深灰，标题用近黑
s = s.replace('        darkgray: "#6b6b73"\n        dark: "#18181b"',
              '        darkgray: "#3f3f46"\n        dark: "#18181b"', 1)

# 2) 关掉右侧图谱（右栏只留目录 / 反向链接）
s = s.replace('  - source: "@quartz-community/graph"\n    enabled: true\n',
              '  - source: "@quartz-community/graph"\n    enabled: false\n', 1)

# 3) 首页不渲染自动标题（首页自己写 Hero）
old_at = '''  - source: "@quartz-community/article-title"
    enabled: true
    layout:
      position: beforeBody
      priority: 10
'''
new_at = '''  - source: "@quartz-community/article-title"
    enabled: true
    layout:
      position: beforeBody
      priority: 10
      condition: not-index
'''
if old_at not in s:
    sys.exit("article-title 块未找到")
s = s.replace(old_at, new_at, 1)

# 4) 侧栏排序：固定「业务/行业/工具/关于/博客」，其余按名字
old_ex = '''  - source: "@quartz-community/explorer"
    enabled: true
    layout:
      position: left
      priority: 50
'''
new_ex = '''  - source: "@quartz-community/explorer"
    enabled: true
    options:
      sortFn: |-
        (a, b) => {
          const rank = { "业务分享": 1, "行业知识": 2, "工具资源": 3, "关于云屿集": 4, "博客": 5, "写作指南": 6, "组件演示": 7 };
          const ra = rank[a.displayName], rb = rank[b.displayName];
          if (ra !== undefined && rb !== undefined) return ra - rb;
          if (ra !== undefined) return -1;
          if (rb !== undefined) return 1;
          if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1;
          return (a.displayName || "").localeCompare(b.displayName || "", void 0, { numeric: true });
        }
    layout:
      position: left
      priority: 50
'''
if old_ex not in s:
    sys.exit("explorer 块未找到")
s = s.replace(old_ex, new_ex, 1)

# 5) 页脚链接
s = re.sub(
    r'    options:\n      links:\n(?:        .*\n)+',
    '    options:\n      links:\n'
    '        业务分享: /business/\n'
    '        行业知识: /industry/\n'
    '        工具资源: /tools/\n'
    '        博客: /blog/\n'
    '        关于: /about/\n'
    '        GitHub: https://github.com/YYJ-lin\n',
    s,
    count=1,
)

with open(P, "w", encoding="utf-8") as f:
    f.write(s)
print("ok")
