import { h } from "preact"

/**
 * 云屿集页脚。
 *
 * 为什么要自己写：Quartz 内置页脚只接受写死的 href，站内链接在
 * GitHub Pages 项目页（部署在 /yyj-quartz/ 子路径）下会 404。
 * 这里根据 cfg.baseUrl 拼出带子路径的绝对路径，域名根和子路径都成立。
 */

/** 由 baseUrl 推导站点根路径：`u.github.io/repo` -> `/repo`；`example.com` -> `` */
function siteRoot(cfg) {
  const baseUrl = cfg?.baseUrl ?? ""
  try {
    const path = new URL(`https://${baseUrl}`).pathname
    return path.replace(/\/+$/, "")
  } catch {
    return ""
  }
}

function Footer(opts) {
  const columns = opts?.columns ?? []
  const brand = opts?.brand ?? null

  const Comp = ({ displayClass, cfg }) => {
    const root = siteRoot(cfg)
    const year = new Date().getFullYear()

    const item = (it) => {
      const external = typeof it.href === "string" && it.href.length > 0
      const href = external ? it.href : `${root}${it.to ?? "/"}`
      return h(
        "li",
        null,
        h(
          "a",
          {
            href,
            ...(external ? { target: "_blank", rel: "noopener noreferrer" } : {}),
          },
          it.label,
        ),
      )
    }

    return h("footer", { class: displayClass || undefined }, [
      h(
        "div",
        { class: "yyj-footer-grid" },
        columns.map((col) =>
          h("div", { class: "yyj-footer-col", key: col.title }, [
            h("h4", null, col.title),
            h("ul", null, (col.items ?? []).map(item)),
          ]),
        ),
        brand
          ? h("div", { class: "yyj-footer-brand", key: "brand" }, [
              h(
                "a",
                { class: "yyj-footer-brand-name", href: `${root}/` },
                brand.title ?? "云屿集",
              ),
              brand.tagline ? h("p", { class: "yyj-footer-tagline" }, brand.tagline) : null,
              h("p", { class: "yyj-footer-copy" }, `© ${year} ${brand.title ?? "云屿集"}`),
            ])
          : null,
      ),
    ])
  }

  Comp.css = ""
  return Comp
}

export { Footer }
