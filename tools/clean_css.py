#!/usr/bin/env python3
"""custom.scss 整理：去掉死样式、去掉完全重复的段落、加目录。不改任何有效声明。"""
import hashlib
import re

P = "quartz/styles/custom.scss"
s = open(P, encoding="utf-8").read()

# 1) 头部说明之后的第一个分段起点
lines = s.splitlines()
head_end = 0
for i, ln in enumerate(lines):
    if ln.startswith("// ---------- 字体"):
        head_end = i
        break
head = "\n".join(lines[:head_end]).rstrip() + "\n"
body = "\n".join(lines[head_end:])

# 2) 按分段标记切块
parts = re.split(r"(?m)^// ---------- (.+?) ----------\s*$", body)
# parts: ['', title1, content1, title2, content2, ...]
chunks = []
for i in range(1, len(parts), 2):
    chunks.append({"title": parts[i].strip(), "content": parts[i + 1].rstrip() + "\n"})

# 3) 去掉死样式段
before = len(chunks)
chunks = [c for c in chunks if c["title"] != "404"]
for c in chunks:
    c["content"] = re.sub(
        r"\n\.yyj-404-search \{.*?\n\}\n", "\n", c["content"], flags=re.S
    )

# 4) 去重（正文完全相同才丢）
seen = {}
kept = []
for c in chunks:
    key = hashlib.md5(re.sub(r"\s+", " ", c["content"]).strip().encode()).hexdigest()
    if key in seen:
        print("drop duplicate section:", c["title"], "(same as", seen[key] + ")")
        continue
    seen[key] = c["title"]
    kept.append(c)

# 5) 目录
toc = ["// =========================================================",
       "// 云屿集自定义样式（按区块组织，顺序 = 层叠顺序）",
       "// 目录："]
for i, c in enumerate(kept, 1):
    toc.append(f"//   {i:02d}. {c['title']}")
toc.append("// =========================================================")
toc.append("")

out = head.rstrip() + "\n\n" + "\n".join(toc) + "\n"
for c in kept:
    out += f"// ---------- {c['title']} ----------\n" + c["content"].lstrip("\n") + "\n"

open(P, "w", encoding="utf-8").write(out)
print(f"sections: {before} -> {len(kept)}; lines: {len(out.splitlines())}")
