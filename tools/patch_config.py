#!/usr/bin/env python3
"""一次性脚本：把 quartz.config.yaml 改成云屿集品牌配置。幂等，可重复执行。"""
import re
import shutil
import sys

P = "quartz.config.yaml"
BACKUP = "quartz.config.yaml.orig"

try:
    with open(BACKUP, "r", encoding="utf-8"):
        pass
except FileNotFoundError:
    shutil.copyfile(P, BACKUP)

with open(P, "r", encoding="utf-8") as f:
    s = f.read()

s = re.sub(r"^  pageTitle: .*$", "  pageTitle: 云屿集", s, count=1, flags=re.M)
s = re.sub(r'^  pageTitleSuffix: .*$', '  pageTitleSuffix: " · 业务分享与行业知识"', s, count=1, flags=re.M)
s = re.sub(r"^  locale: .*$", "  locale: zh-CN", s, count=1, flags=re.M)
s = re.sub(r"^  baseUrl: .*$", "  baseUrl: yyj-lin.github.io/yyj-quartz", s, count=1, flags=re.M)
s = re.sub(r"  analytics:\n    provider: .*\n", "  analytics:\n    provider: null\n", s, count=1)

theme = """  theme:
    fontOrigin: googleFonts
    cdnCaching: false
    typography:
      header: IBM Plex Sans
      body: IBM Plex Sans
      code: JetBrains Mono
    colors:
      lightMode:
        light: "#fafaf9"
        lightgray: "#f5f5f4"
        gray: "#e4e4e7"
        darkgray: "#6b6b73"
        dark: "#18181b"
        secondary: "#1d4ed8"
        tertiary: "#3b5bdb"
        highlight: rgba(59, 91, 219, 0.10)
        textHighlight: "#fff23688"
      darkMode:
        light: "#0c0a09"
        lightgray: "#1c1917"
        gray: "#27272a"
        darkgray: "#a1a1aa"
        dark: "#f5f5f4"
        secondary: "#60a5fa"
        tertiary: "#93c5fd"
        highlight: rgba(96, 165, 250, 0.12)
        textHighlight: "#b3aa0288"
"""
s, n = re.subn(r"  theme:\n(?:.*\n)*?(?=plugins:)", theme, s, count=1)
if n != 1:
    print("ERROR: theme block not replaced", file=sys.stderr)
    sys.exit(1)

with open(P, "w", encoding="utf-8") as f:
    f.write(s)
print("config patched")
