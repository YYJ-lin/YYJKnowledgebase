#!/usr/bin/env python3
"""方案二：business/industry 移入 kb/，补 301、修相对链接、去掉 parent。"""
import re


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def set_fm(path, updates, remove=()):
    s = read(path)
    m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
    if not m:
        raise SystemExit(f"no frontmatter: {path}")
    lines = [ln for ln in m.group(1).splitlines() if ln.split(":", 1)[0].strip() not in remove]
    keys = [ln.split(":", 1)[0].strip() for ln in lines if ":" in ln]
    for k, v in updates.items():
        if k in keys:
            lines = [f"{k}: {v}" if ln.startswith(f"{k}:") else ln for ln in lines]
        else:
            lines.append(f"{k}: {v}")
    write(path, "---\n" + "\n".join(lines) + "\n---\n" + s[m.end() :])
    print("fm", path)


# 1) 旧地址 301；parent 不再需要（现在是真嵌套）
set_fm("content/kb/business/index.md", {"aliases": '["business/index"]'}, remove=("parent",))
set_fm("content/kb/industry/index.md", {"aliases": '["industry/index"]'}, remove=("parent",))

# 2) 知识库首页卡片：../business → ./business
s = read("content/kb/index.md")
s = s.replace('href="../business/"', 'href="./business/"').replace('href="../industry/"', 'href="./industry/"')
s = s.replace('href="../tools/"', 'href="./../tools/"')
write("content/kb/index.md", s)
print("kb cards")

# 3) 子页面里的相对链接上移一层
for path in ("content/kb/business/index.md", "content/kb/industry/index.md"):
    s = read(path)
    s = s.replace("](../about/)", "](../../about/)")
    s = s.replace("](../tools/)", "](../../tools/)")
    s = s.replace("](../tech/)", "](../../tech/)")
    write(path, s)
    print("links", path)

# 4) 首页卡片指向新地址
s = read("content/index.md")
s = s.replace('href="business/"', 'href="kb/business/"').replace('href="industry/"', 'href="kb/industry/"')
write("content/index.md", s)
print("home cards")
