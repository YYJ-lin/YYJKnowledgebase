#!/usr/bin/env python3
"""小修：导航标签可覆盖（navLabel）、面包屑父级由 frontmatter parent 决定。"""
import re

# 1) 关于页：导航显示「关于」
p = "content/about/index.md"
s = open(p, encoding="utf-8").read()
if "navLabel:" not in s:
    s = s.replace("nav: true\n", "nav: true\nnavLabel: 关于\n", 1)
open(p, "w", encoding="utf-8").write(s)
print("about navLabel")

# 2) 业务/行业：父级指向 /kb
for path in ("content/business/index.md", "content/industry/index.md"):
    s = open(path, encoding="utf-8").read()
    if "parent:" not in s:
        s = re.sub(r"^---\n(.*?)\n---\n", lambda m: "---\n" + m.group(1) + "\nparent: kb\n---\n", s, count=1, flags=re.S)
        open(path, "w", encoding="utf-8").write(s)
        print("parent kb ->", path)

# 3) 导航用 navLabel
p = "plugins/yyj-nav/index.js"
s = open(p, encoding="utf-8").read()
s = s.replace(
    """    const autoLinks = navPages.map((f) => ({
      label: f.frontmatter?.title ?? f.slug,""",
    """    const autoLinks = navPages.map((f) => ({
      label: f.frontmatter?.navLabel ?? f.frontmatter?.title ?? f.slug,""",
    1,
)
open(p, "w", encoding="utf-8").write(s)
print("nav uses navLabel")

# 4) 面包屑：父级来自 frontmatter.parent
p = "plugins/yyj-crumbs/index.js"
s = open(p, encoding="utf-8").read()
old = """      if (!sectionIsTopLevel) {
        items.push({ label: libraryLabel, href: `${root}${libraryPath}` })
      }"""
new = """      // 父级：分类 index.md 里写 parent: kb，就能挂到 /kb 下
      const parentSlug = sectionIndex?.frontmatter?.parent
        ? String(sectionIndex.frontmatter.parent).replace(/^\\//, "")
        : null
      if (!sectionIsTopLevel && parentSlug) {
        const parentFile = (allFiles ?? []).find((f) => f.slug === parentSlug)
        items.push({
          label: parentFile?.frontmatter?.title ?? parentSlug,
          href: `${root}${toHref(parentSlug)}`,
        })
      }"""
if old not in s:
    raise SystemExit("crumbs parent block not found")
s = s.replace(old, new, 1)
s = s.replace(
    """  const libraryLabel = opts?.libraryLabel ?? "业务与行业"
  const libraryPath = opts?.libraryPath ?? "/kb"
""",
    "",
    1,
)
open(p, "w", encoding="utf-8").write(s)
print("crumbs use parent frontmatter")
