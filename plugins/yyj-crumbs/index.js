import { h } from "preact"

/**
 * 云屿集面包屑。
 *
 * 按 slug 的祖先链自动拼：每一级只要存在 `<前缀>/index.md` 就成为一个面包屑，
 * 标题取那个 index 的 title。所以：
 *   kb/business/index  → 首页 › 知识库 › 业务分享
 *   kb/business/a      → 首页 › 知识库 › 业务分享 › A
 *   tech/a             → 首页 › 技术手记 › A
 *   about/writing-guide→ 首页 › 关于云屿集 › 写作指南
 *   kb                 → 首页 › 知识库
 */

function siteRoot(cfg) {
  const baseUrl = cfg?.baseUrl ?? ""
  try {
    return new URL(`https://${baseUrl}`).pathname.replace(/\/+$/, "")
  } catch {
    return ""
  }
}

function Crumbs() {
  return ({ cfg, fileData, allFiles }) => {
    const slug = fileData?.slug ?? ""
    if (!slug || slug === "index") return null

    const root = siteRoot(cfg)
    const bySlug = new Map((allFiles ?? []).map((f) => [f.slug, f]))
    const parts = slug.split("/")
    const isIndex = parts[parts.length - 1] === "index"
    const base = isIndex ? parts.slice(0, -1) : parts

    const items = [{ label: "首页", href: `${root}/` }]

    for (let i = 1; i <= base.length; i++) {
      const prefix = base.slice(0, i).join("/")
      const indexFile = bySlug.get(`${prefix}/index`)
      if (!indexFile) continue
      const label = indexFile.frontmatter?.title ?? prefix
      const current = isIndex && i === base.length
      items.push(current ? { label, current: true } : { label, href: `${root}/${prefix}/` })
    }

    if (!isIndex) {
      items.push({ label: fileData?.frontmatter?.title ?? parts[parts.length - 1], current: true })
    }

    const children = []
    items.forEach((item, i) => {
      if (i > 0) children.push(h("span", { class: "yyj-crumb-sep", "aria-hidden": "true" }, "›"))
      children.push(
        item.current
          ? h("span", { class: "yyj-crumb-current", "aria-current": "page" }, item.label)
          : h("a", { class: "yyj-crumb-link", href: item.href }, item.label),
      )
    })

    return h("nav", { class: "yyj-crumbs", "aria-label": "面包屑" }, children)
  }
}

export { Crumbs }
