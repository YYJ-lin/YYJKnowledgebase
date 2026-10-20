#!/usr/bin/env python3
"""第八阶段：内置页脚换成云屿集自定义页脚（四区 + 子路径安全链接）。"""
import re
import sys

P = "quartz.config.yaml"
s = open(P, encoding="utf-8").read()

start = s.find('  - source: "@quartz-community/footer"')
if start < 0:
    sys.exit("footer 插件块未找到")
# 找到该插件块结束（下一个 "  - source:" 或 "layout:"）
end = s.find("\n  - source:", start + 10)
if end < 0:
    end = len(s)
block = s[start:end]

new_block = '''  - source: "./plugins/yyj-footer"
    enabled: true
    options:
      columns:
        - title: 内容导航
          items:
            - { label: 首页, to: / }
            - { label: 业务分享, to: /business/ }
            - { label: 行业知识, to: /industry/ }
            - { label: 工具资源, to: /tools/ }
            - { label: 博客, to: /blog/ }
        - title: 相关资源
          items:
            - { label: 写作指南, to: /about/writing-guide }
            - { label: 组件演示, to: /about/components }
            - { label: GitHub 仓库, href: "https://github.com/YYJ-lin/YYJ-wiki" }
        - title: 关于与反馈
          items:
            - { label: 关于本站, to: /about/ }
            - { label: 反馈与联系, href: "https://github.com/YYJ-lin/YYJ-wiki/issues" }
      brand:
        title: 云屿集
        tagline: 业务分享与行业知识
    layout:
      position: footer
      priority: 50
'''

s = s[:start] + new_block + s[end:]

# 删掉原来 footer 插件残留的 layout 段（若有）
s = re.sub(
    r'(position: footer\n      priority: 50\n)(\s*)(  - source:)',
    r"\1\3",
    s,
)

open(P, "w", encoding="utf-8").write(s)
print("footer swapped to local plugin")
print("--- 检查残留 ---")
for line in s.splitlines():
    if "footer" in line and "yyj" not in line:
        print(repr(line))
