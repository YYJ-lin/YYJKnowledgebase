#!/usr/bin/env python3
"""结构调整：/blog → /tech，/kb → 业务与行业，/tools → 资源与工具，并给分类加 nav 元数据。"""
import os
import re


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, s):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def set_fm(path, updates):
    s = read(path)
    m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
    if not m:
        raise SystemExit(f"no frontmatter: {path}")
    body = s[m.end() :]
    fm = m.group(1)
    lines = fm.splitlines()
    keys = [ln.split(":", 1)[0].strip() for ln in lines if ":" in ln]
    for k, v in updates.items():
        if k in keys:
            lines = [f"{k}: {v}" if ln.startswith(f"{k}:") else ln for ln in lines]
        else:
            lines.append(f"{k}: {v}")
    write(path, "---\n" + "\n".join(lines) + "\n---\n" + body)
    print("updated", path)


# 1) blog -> tech
if os.path.isdir("content/blog"):
    os.rename("content/blog", "content/tech")
    print("moved content/blog -> content/tech")

set_fm(
    "content/tech/index.md",
    {
        "title": "技术手记",
        "description": "ERPNext、WordPress、自建项目与开源工具里的真实实践",
        "nav": "true",
        "navOrder": 1,
        "aliases": '["blog/index"]',
    },
)
set_fm("content/tech/2026-10-19-hello.md", {"aliases": '["blog/2026-10-19-hello"]'})

# 2) kb -> 业务与行业
set_fm(
    "content/kb.md",
    {
        "title": "业务与行业",
        "description": "业务分享与行业知识的总入口",
        "nav": "true",
        "navOrder": 2,
    },
)

# 3) tools 改名
set_fm(
    "content/tools/index.md",
    {"title": "资源与工具", "nav": "true", "navOrder": 3},
)

# 4) about 进导航
set_fm("content/about/index.md", {"nav": "true", "navOrder": 4})
