#!/usr/bin/env python3
"""导航：从 frontmatter (nav/navOrder) 自动生成顶栏项，留 config 作为兜底。"""
P = "plugins/yyj-nav/index.js"
s = open(P, encoding="utf-8").read()

# 1) toHref 工具
if "function toHref(" not in s:
    s = s.replace(
        "function renderIcon(name, size = 18) {",
        """function toHref(slug) {
  return slug.endsWith("/index") ? `/${slug.slice(0, -"/index".length)}/` : `/${slug}`
}

function renderIcon(name, size = 18) {""",
        1,
    )

# 2) 在 Comp 里算 navItems
old = """    const { groups, defaultTab } = buildTree(allFiles, currentSlug)
    const isTree = defaultTab === "tree"
"""
new = """    const { groups, defaultTab } = buildTree(allFiles, currentSlug)
    const isTree = defaultTab === "tree"

    // 顶栏项来自各分类 index.md 的 frontmatter：nav: true + navOrder
    const navPages = (allFiles ?? [])
      .filter((f) => f.frontmatter?.nav === true)
      .sort(
        (a, b) =>
          (Number(a.frontmatter?.navOrder) || 99) - (Number(b.frontmatter?.navOrder) || 99),
      )
    const autoLinks = navPages.map((f) => ({
      label: f.frontmatter?.title ?? f.slug,
      to: toHref(f.slug),
    }))
    const navItems = autoLinks.length >= 2 ? autoLinks : links
"""
if old not in s:
    raise SystemExit("comp header block not found")
s = s.replace(old, new, 1)

# 3) 用 navItems 渲染
s = s.replace("links.map(navLink)", "navItems.map(navLink)")

open(P, "w", encoding="utf-8").write(s)
print("nav auto links")
