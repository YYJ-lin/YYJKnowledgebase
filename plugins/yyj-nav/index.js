import { h } from "preact"

/**
 * 云屿集顶部导航。
 *
 * 和页脚同样的道理：站内链接要按 cfg.baseUrl 拼出子路径，
 * 才能同时适配「域名根」和 GitHub Pages 项目页（/YYJKnowledgebase/）。
 */

function siteRoot(cfg) {
  const baseUrl = cfg?.baseUrl ?? ""
  try {
    return new URL(`https://${baseUrl}`).pathname.replace(/\/+$/, "")
  } catch {
    return ""
  }
}

function Nav(opts) {
  const links = opts?.links ?? []

  const Comp = ({ displayClass, cfg, fileData }) => {
    const root = siteRoot(cfg)
    const current = fileData?.slug ? `/${fileData.slug}` : "/"

    return h(
      "nav",
      { class: `yyj-nav ${displayClass ?? ""}`.trim(), "aria-label": "主导航" },
      links.map((it) => {
        const external = typeof it.href === "string" && it.href.length > 0
        const href = external ? it.href : `${root}${it.to ?? "/"}`
        const active =
          !external &&
          (it.to === "/"
            ? current === "/"
            : current === it.to || current.startsWith(it.to.replace(/\/$/, "") + "/"))
        return h(
          "a",
          {
            key: it.label,
            href,
            class: active ? "yyj-nav-link is-active" : "yyj-nav-link",
            ...(external ? { target: "_blank", rel: "noopener noreferrer" } : {}),
          },
          it.label,
        )
      }),
    )
  }

  Comp.css = ""
  return Comp
}

export { Nav }
