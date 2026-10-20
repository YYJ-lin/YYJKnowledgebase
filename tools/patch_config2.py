#!/usr/bin/env python3
"""配置第二阶段：字体改为本地自托管，关掉会注入 Google Fonts <link> 的字体插件。"""
import re

P = "quartz.config.yaml"
with open(P, "r", encoding="utf-8") as f:
    s = f.read()

# 1) 核心主题：不再向 Google 请求字体
s = s.replace("    fontOrigin: googleFonts\n", "    fontOrigin: local\n", 1)

# 2) quartz-fonts 插件关闭（它会在 <head> 里插 Google Fonts 链接；
#    自托管模式下又会写死 /static/... 绝对路径，GitHub Pages 子路径下会 404）
before = s
s = s.replace(
    '  - source: "@quartz-community/quartz-fonts"\n    enabled: true\n',
    '  - source: "@quartz-community/quartz-fonts"\n    enabled: false\n',
    1,
)
if s == before:
    raise SystemExit("quartz-fonts 插件块未找到，配置可能已变更")

with open(P, "w", encoding="utf-8") as f:
    f.write(s)
print("ok: fontOrigin=local, quartz-fonts disabled")
