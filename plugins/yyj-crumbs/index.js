import { h } from "preact"

/**
 * 云屿集面包屑。
 *
 * Quartz 自带的面包屑只按文件路径拆，`/business/` 只会显示「首页 › 业务分享」，
 * 中间缺了「知识库」这一层。这里按站点的真实层级拼：
 *   首页 › 知识库 › 分类 › 文章
 * 博客单独一条：首页 › 博客 › 文章
 */

function siteRoot(cfg) {
  const baseUrl = cfg?.baseUrl ?? ""
  try {
    return new URL(`https://${baseUrl}`).pathname.replace(/\/+$/, "")
  } catch {
    return ""
  }
}

function titleOf(allFiles, slug) {
  const file = (allFiles ?? []).find((f) => f.slug === slug)
  return file?.frontmatter?.title ?? null
}

function Crumbs(opts) {
  const libraryLabel = opts?.libraryLabel ?? "知识库"
  const libraryPath = opts?.libraryPath ?? "/kb"

  return ({ cfg, fileData, allFiles }) => {
    const slug = fileData?.slug ?? ""
    if (!slug || slug === "index") return null

    const root = siteRoot(cfg)
    const parts = slug.split("/")
    const section = parts.length > 1 ? parts[0] : null
    const items = [{ label: "首页", href: `${root}/` }]

    if (!section) {
      items.push({ label: fileData?.frontmatter?.title ?? slug, current: true })
    } else {
      const sectionTitle = titleOf(allFiles, `${section}/index`) ?? section
      if (section !== "blog") {
        items.push({ label: libraryLabel, href: `${root}${libraryPath}` })
      }
      const isSectionIndex = slug === `${section}/index`
      if (isSectionIndex) {
        items.push({ label: sectionTitle, current: true })
      } else {
        items.push({ label: sectionTitle, href: `${root}/${section}/` })
        items.push({
          label: fileData?.frontmatter?.title ?? parts[parts.length - 1],
          current: true,
        })
      }
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
