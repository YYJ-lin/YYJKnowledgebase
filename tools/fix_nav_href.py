#!/usr/bin/env python3
"""修复被 shell 吃掉的模板字符串。"""
P = "plugins/yyj-nav/index.js"
s = open(P, encoding="utf-8").read()

bad = "                          href: ,\n"
good = "                          href: `${root}/${g.indexItem.slug}`,\n"
if bad not in s:
    raise SystemExit("pattern not found")
s = s.replace(bad, good, 1)
open(P, "w", encoding="utf-8").write(s)
print("fixed href template")
