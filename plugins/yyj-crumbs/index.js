import { h } from "preact"

/**
 * 云屿集面包屑。
 *
 * 层级按「分类 index.md 的 frontmatter」推出来，和顶栏用的是同一套元数据：
 *   nav: true 的分类 = 顶级栏目（技术手记 / 资源与工具 / 关于…）
 *   没有 nav 的分类（业务分享、行业知识）= 挂在「业务与行业」(/kb) 下
 *
 * 结果：首页 › 技术手记 › 文章  /  首页 › 业务与行业 › 业务分享 › 文章
 */

function siteRoot(cfg) {
  const baseUrl = cfg?.baseUrl ?? ""
  try {
    return new URL(`https://${baseUrl}`).pathname.replace(/\/+$/, "")
  } catch {
    return ""
  }
}

function toHref(slug) {
  return slug.endsWith("/index") ? `/${slug.slice(0, -"/index".length)}/` : `/${slug}`
}

function Crumbs(opts) {
  return ({ cfg, fileData, allFiles }) => {
    const slug = fileData?.slug ?? ""
    if (!slug || slug === "index") return null

    const root = siteRoot(cfg)
    const parts = slug.split("/")
    const section = parts.length > 1 ? parts[0] : null
    const items = [{ label: "首页", href: `${root}/` }]

    const sectionIndex = section
      ? (allFiles ?? []).find((f) => f.slug === `${section}/index`)
      : null
    const sectionTitle = sectionIndex?.frontmatter?.title ?? section
    const sectionIsTopLevel = sectionIndex?.frontmatter?.nav === true

    if (!section) {
      // 顶层单页（/kb、/services 等）
      items.push({ label: fileData?.frontmatter?.title ?? slug, current: true })
    } else {
      // 父级：分类 index.md 里写 parent: kb，就能挂到 /kb 下
      const parentSlug = sectionIndex?.frontmatter?.parent
        ? String(sectionIndex.frontmatter.parent).replace(/^\//, "")
        : null
      if (!sectionIsTopLevel && parentSlug) {
        const parentFile = (allFiles ?? []).find((f) => f.slug === parentSlug)
        items.push({
          label: parentFile?.frontmatter?.title ?? parentSlug,
          href: `${root}${toHref(parentSlug)}`,
        })
      }
      const isSectionIndex = slug === `${section}/index`
      if (isSectionIndex) {
        items.push({ label: sectionTitle, current: true })
      } else {
        items.push({ label: sectionTitle, href: `${root}${toHref(`${section}/index`)}` })
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
