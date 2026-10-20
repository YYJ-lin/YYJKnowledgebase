#!/usr/bin/env python3
"""把部署目标从 yyj-quartz 切到刚建好的 YYJKnowledge-base 仓库。"""

import re
import sys

REPL = [
    # baseUrl / 线上地址
    ("yyj-lin.github.io/yyj-quartz", "yyj-lin.github.io/YYJKnowledge-base"),
    # 仓库地址
    ("git@github.com:YYJ-lin/yyj-quartz.git", "git@github.com:YYJ-lin/YYJKnowledge-base.git"),
    ("YYJ-lin/yyj-quartz`", "YYJ-lin/YYJKnowledge-base`"),
    ("Repository name: yyj-quartz", "Repository name: YYJKnowledge-base"),
    # 预览子路径
    ("`/yyj-quartz/`", "`/YYJKnowledge-base/`"),
    ("`/yyj-quartz`", "`/YYJKnowledge-base`"),
    ("/yyj-quartz/ 子路径", "/YYJKnowledge-base/ 子路径"),
    ("/tmp/preview/yyj-quartz", "/tmp/preview/YYJKnowledge-base"),
    ("/yyj-quartz/\"", "/YYJKnowledge-base/\""),
    ("'^href=\"/yyj-quartz'", "'^href=\"/YYJKnowledge-base'"),
]

FILES = [
    "quartz.config.yaml",
    "tools/deploy.sh",
    "tools/preview.sh",
    "tools/verify.sh",
    "README.md",
    "MIGRATION.md",
]

for path in FILES:
    s = open(path, encoding="utf-8").read()
    before = s
    for a, b in REPL:
        s = s.replace(a, b)
    if s != before:
        open(path, "w", encoding="utf-8").write(s)
        print(f"updated {path}")
    else:
        print(f"unchanged {path}")

# 工作流：改为 main 分支 + 允许 configure-pages 自动启用 Pages
p = ".github/workflows/deploy.yml"
s = open(p, encoding="utf-8").read()
s = s.replace("      - v5\n", "      - main\n", 1)
s = s.replace(
    "      - name: Configure Pages\n        uses: actions/configure-pages@v5\n",
    "      - name: Configure Pages\n        uses: actions/configure-pages@v5\n        with:\n          enablement: true\n",
    1,
)
open(p, "w", encoding="utf-8").write(s)
print("updated .github/workflows/deploy.yml")

left = []
for path in FILES + [".github/workflows/deploy.yml"]:
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        if "yyj-quartz" in line and "sites/yyj-quartz" not in line and "yyj-quartz-preview" not in line:
            left.append(f"{path}:{i}: {line.strip()[:110]}")
print("\n--- 仍含旧仓库名的行 ---")
print("\n".join(left) if left else "(none)")
