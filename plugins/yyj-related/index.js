import { h } from "preact"

/**
 * 相关文章：不用手写链接，自动按「共同标签 + 同目录」打分推荐。
 *
 * 打分：每共用一个标签 +3，同目录层级每多一层 +1。
 * 只在文章页显示（分类首页、关于页等不显示）；没有候选项时整块不渲染。
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

function tagsOf(file) {
  const raw = file?.frontmatter?.tags ?? []
  const list = Array.isArray(raw) ? raw : [raw]
  return new Set(list.map((t) => String(t).trim().toLowerCase()).filter(Boolean))
}

export function Related(opts) {
  const max = Number(opts?.max) || 4

  return ({ cfg, fileData, allFiles }) => {
    const slug = fileData?.slug ?? ""
    if (!slug || slug === "index" || slug.endsWith("/index")) return null

    const root = siteRoot(cfg)
    const myTags = tagsOf(fileData)
    const mySegs = slug.split("/")

    const scored = (allFiles ?? [])
      .filter((f) => f.slug !== slug && f.slug !== "index" && !f.slug.endsWith("/index"))
      .map((f) => {
        const tags = tagsOf(f)
        let shared = 0
        for (const t of myTags) if (tags.has(t)) shared++
        const segs = f.slug.split("/")
        let common = 0
        while (
          common < segs.length - 1 &&
          common < mySegs.length - 1 &&
          segs[common] === mySegs[common]
        ) {
          common++
        }
        return { file: f, score: shared * 3 + common, shared }
      })
      .filter((x) => x.score > 0)
      .sort(
        (a, b) =>
          b.score - a.score ||
          String(a.file.frontmatter?.title ?? a.file.slug).localeCompare(
            String(b.file.frontmatter?.title ?? b.file.slug),
            "zh",
          ),
      )
      .slice(0, max)

    if (scored.length === 0) return null

    return h(
      "div",
      { class: "yyj-related" },
      h("h3", { class: "yyj-related-title" }, "相关文章"),
      h(
        "ul",
        { class: "yyj-related-list" },
        scored.map(({ file }) =>
          h(
            "li",
            { key: file.slug },
            h(
              "a",
              { href: `${root}${toHref(file.slug)}`, class: "internal" },
              file.frontmatter?.title ?? file.slug,
            ),
          ),
        ),
      ),
    )
  }
}
