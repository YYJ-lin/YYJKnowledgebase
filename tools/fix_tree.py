#!/usr/bin/env python3
"""修 buildTree：统一按一级目录分组，再按当前分类过滤；嵌套 index 保留为链接。"""
P = "plugins/yyj-nav/index.js"
s = open(P, encoding="utf-8").read()

start = s.find("/**\n * 菜单「目录」的数据")
end = s.find("function Nav(opts) {")
if start < 0 or end < 0:
    raise SystemExit("buildTree block not found")

new_block = '''/**
 * 菜单「目录」的数据：按一级目录分组，每组带篇数。
 * - 首页 / 知识库这类没有具体分类的页面：列出全部分组
 * - 在某个分类里：只保留当前那一组
 * 组内只把「本组的 index」当标题，嵌套的子分类首页（kb/erpnext 等）保留为链接。
 */
function buildTree(allFiles, currentSlug) {
  const entries = (allFiles ?? [])
    .filter((f) => {
      const slug = f.slug
      return slug && slug !== "index" && slug !== "404" && !slug.startsWith("tags")
    })
    .map((f) => ({
      slug: f.slug,
      title: f.frontmatter?.title ?? f.slug,
      isIndex: f.slug.endsWith("/index"),
      segments: f.slug.split("/"),
    }))

  const bySection = new Map()
  for (const e of entries) {
    const key = e.segments.length > 1 ? e.segments[0] : "__pages"
    if (!bySection.has(key)) bySection.set(key, [])
    bySection.get(key).push(e)
  }

  const all = [...bySection.entries()]
    .map(([key, items]) => {
      const sorted = sortItems(items)
      const ownSlug = key === "__pages" ? null : `${key}/index`
      const own = ownSlug ? (sorted.find((i) => i.slug === ownSlug) ?? null) : null
      return {
        key,
        title: key === "__pages" ? "页面" : (own?.title ?? key),
        indexItem: own,
        rank: key === "__pages" ? 99 : (SECTION_RANK[key] ?? 90),
        items: sorted.filter((i) => i.slug !== ownSlug),
        count: sorted.length,
      }
    })
    .sort((a, b) => a.rank - b.rank || String(a.title).localeCompare(String(b.title), "zh"))

  const section = currentSlug.includes("/") ? currentSlug.split("/")[0] : null
  const groups = section ? all.filter((g) => g.key === section) : all

  return { groups, section, defaultTab: section ? "nav" : groups.length > 0 ? "tree" : "nav" }
}

'''
s = s[:start] + new_block + s[end:]
open(P, "w", encoding="utf-8").write(s)
print("buildTree rewritten")
