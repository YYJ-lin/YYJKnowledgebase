import { h } from "preact"

/**
 * 侧栏顶部的分类切换器。
 *
 * 三个入口（技术手记 / 知识库 / 资源与工具）直接链到各分类首页；
 * 顶栏滚出视野后，这一栏随时能点。
 *
 * 顺带做两件小事（afterDOMLoaded）：
 *   1. 给目录树里的折叠项补「下面有几篇」的小徽标；
 *   2. 给当前页面那一行加高亮（Quartz 自带的 explorer 不标当前项）。
 */

const EXCLUDE = new Set(["about"])

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

export function Switch(opts) {
  const maxItems = opts?.maxItems ?? 3

  const Comp = ({ cfg, fileData, allFiles }) => {
    const root = siteRoot(cfg)
    const currentSlug = fileData?.slug ?? ""
    const currentSection = currentSlug.includes("/") ? currentSlug.split("/")[0] : null

    const items = (allFiles ?? [])
      .filter((f) => f.frontmatter?.nav === true)
      .filter((f) => !EXCLUDE.has(f.slug.split("/")[0]))
      .sort(
        (a, b) => (Number(a.frontmatter?.navOrder) || 99) - (Number(b.frontmatter?.navOrder) || 99),
      )
      .slice(0, maxItems)
      .map((f) => ({
        label: f.frontmatter?.navLabel ?? f.frontmatter?.title ?? f.slug,
        to: toHref(f.slug),
        key: f.slug.split("/")[0],
      }))

    if (items.length === 0) return null

    return h(
      "div",
      { class: "yyj-switch", role: "tablist", "aria-label": "分类切换" },
      items.map((it) => {
        const active = currentSection === it.key
        return h(
          "a",
          {
            key: it.key,
            href: `${root}${it.to}`,
            class: active ? "yyj-switch-item is-active" : "yyj-switch-item",
            role: "tab",
            "aria-selected": active ? "true" : "false",
          },
          it.label,
        )
      }),
    )
  }

  Comp.afterDOMLoaded = `
(() => {
  if (window.__yyjSidebarBound) return;
  window.__yyjSidebarBound = true;

  const norm = (p) =>
    p.replace(/\\/index\\.html$/, "/").replace(/\\.html$/, "").replace(/\\/+$/, "") || "/";

  const decorate = () => {
    document.querySelectorAll(".explorer .folder-container").forEach((row) => {
      const outer = row.nextElementSibling;
      const count = outer ? outer.querySelectorAll("a").length : 0;
      if (count > 0 && !row.querySelector(".yyj-count")) {
        const badge = document.createElement("span");
        badge.className = "yyj-count";
        badge.textContent = String(count);
        row.appendChild(badge);
      }
    });

    const here = norm(location.pathname);
    document.querySelectorAll(".explorer-ul a").forEach((a) => {
      const link = norm(new URL(a.getAttribute("href"), location.href).pathname);
      const row = a.closest(".folder-container") || a.closest("li") || a;
      const isCurrent = link === here;
      a.classList.toggle("is-current", isCurrent);
      row.classList.toggle("is-current-row", isCurrent);
    });
  };

  const run = () => setTimeout(decorate, 60);
  document.addEventListener("nav", run);
  document.addEventListener("render", run);
  run();
})();
`

  return Comp
}
