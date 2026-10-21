import { h } from "preact"

/**
 * 云屿集顶部导航。
 *
 * 桌面：文字链接 + 图标（GitHub / 微信 / QQ，二维码用 <details> 展开）
 * 手机：一个菜单按钮，两个标签页
 *   「导航」站点栏目 + 图标
 *   「目录」按分类折叠：分类标题是 <details>，点开才看到下面的文章（带篇数）
 */

const GITHUB_PATH =
  "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"

const WECHAT_PATH =
  "M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178A1.17 1.17 0 0 1 4.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178 1.17 1.17 0 0 1-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 0 1 .598.082l1.584.926a.272.272 0 0 0 .14.047c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 0 1-.023-.156.49.49 0 0 1 .201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-6.656-6.088V8.89c-.135-.01-.27-.027-.407-.03zm-2.53 3.274c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.969-.982z"

const QQ_PATH =
  "M21.395 15.035a40 40 0 0 0-.803-2.264l-1.079-2.695c.001-.032.014-.562.014-.836C19.526 4.632 17.351 0 12 0S4.474 4.632 4.474 9.241c0 .274.013.804.014.836l-1.08 2.695a39 39 0 0 0-.802 2.264c-1.021 3.283-.69 4.643-.438 4.673.54.065 2.103-2.472 2.103-2.472 0 1.469.756 3.387 2.394 4.771-.612.188-1.363.479-1.845.835-.434.32-.379.646-.301.778.343.578 5.883.369 7.482.189 1.6.18 7.14.389 7.483-.189.078-.132.132-.458-.301-.778-.483-.356-1.233-.646-1.846-.836 1.637-1.384 2.393-3.302 2.393-4.771 0 0 1.563 2.537 2.103 2.472.251-.03.581-1.39-.438-4.673"

const ICONS = {
  github: { path: GITHUB_PATH, viewBox: "0 0 16 16" },
  wechat: { path: WECHAT_PATH, viewBox: "0 0 24 24" },
  qq: { path: QQ_PATH, viewBox: "0 0 24 24" },
}

// 分类顺序（和侧栏 sortFn 一致），新分类按名字排在后面
const SECTION_RANK = { business: 1, industry: 2, tools: 3, about: 4, blog: 5 }

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

function renderIcon(name, size = 18) {
  const icon = ICONS[name]
  if (!icon) return null
  return h(
    "svg",
    {
      width: size,
      height: size,
      viewBox: icon.viewBox,
      fill: "currentColor",
      "aria-hidden": "true",
      focusable: "false",
    },
    h("path", { d: icon.path }),
  )
}

function burgerIcon() {
  return h(
    "svg",
    {
      width: 20,
      height: 20,
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      "stroke-width": 2,
      "stroke-linecap": "round",
      "aria-hidden": "true",
      focusable: "false",
    },
    [h("path", { d: "M4 7h16" }), h("path", { d: "M4 12h16" }), h("path", { d: "M4 17h16" })],
  )
}

function sortItems(items) {
  return [...items].sort((a, b) => {
    if (a.isIndex !== b.isIndex) return a.isIndex ? -1 : 1
    return String(a.title).localeCompare(String(b.title), "zh-Hans-CN")
  })
}

/**
 * 菜单「目录」的数据：按分类分组，每组带篇数。
 * 分类页里只保留当前分类；首页/知识库列出全部分类。
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

  const section = currentSlug.includes("/") ? currentSlug.split("/")[0] : null

  if (section) {
    const items = sortItems(entries.filter((e) => e.segments[0] === section))
    if (items.length === 0) return { groups: [], section: null, defaultTab: "nav" }
    return {
      groups: [
        {
          key: section,
          title: items.find((i) => i.isIndex)?.title ?? section,
          indexItem: items.find((i) => i.isIndex) ?? null,
          items: items.filter((i) => !i.isIndex),
          count: items.length,
        },
      ],
      section,
      defaultTab: "nav",
    }
  }

  const bySection = new Map()
  for (const e of entries) {
    const key = e.segments.length > 1 ? e.segments[0] : "__pages"
    if (!bySection.has(key)) bySection.set(key, [])
    bySection.get(key).push(e)
  }

  const groups = [...bySection.entries()]
    .map(([key, items]) => {
      const sorted = sortItems(items)
      const indexItem = sorted.find((i) => i.isIndex) ?? null
      return {
        key,
        title: key === "__pages" ? "页面" : (indexItem?.title ?? key),
        indexItem,
        rank: key === "__pages" ? 99 : (SECTION_RANK[key] ?? 90),
        items: sorted.filter((i) => !i.isIndex),
        count: sorted.length,
      }
    })
    .sort((a, b) => a.rank - b.rank || String(a.title).localeCompare(String(b.title), "zh"))

  return { groups, section: null, defaultTab: groups.length > 0 ? "tree" : "nav" }
}

function Nav(opts) {
  const links = opts?.links ?? []
  const actions = opts?.actions ?? []

  const Comp = ({ displayClass, cfg, fileData, allFiles }) => {
    const root = siteRoot(cfg)
    const current = fileData?.slug ? `/${fileData.slug}` : "/"
    const currentSlug = fileData?.slug ?? ""
    const { groups, defaultTab } = buildTree(allFiles, currentSlug)
    const isTree = defaultTab === "tree"

    // 顶栏项来自各分类 index.md 的 frontmatter：nav: true + navOrder
    const navPages = (allFiles ?? [])
      .filter((f) => f.frontmatter?.nav === true)
      .sort(
        (a, b) => (Number(a.frontmatter?.navOrder) || 99) - (Number(b.frontmatter?.navOrder) || 99),
      )
    const autoLinks = navPages.map((f) => ({
      label: f.frontmatter?.navLabel ?? f.frontmatter?.title ?? f.slug,
      to: toHref(f.slug),
    }))
    const navItems = autoLinks.length >= 2 ? autoLinks : links

    const navLink = (it) => {
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
    }

    const action = (it) => {
      const icon = renderIcon(it.icon)

      if (it.image && icon) {
        return h("details", { class: "yyj-qr", name: "yyj-qr", key: it.label }, [
          h("summary", { "aria-label": `${it.label}二维码`, title: `${it.label}二维码` }, icon),
          h("div", { class: "yyj-qr-panel" }, [
            h("img", {
              src: `${root}${it.image}`,
              alt: `${it.label}二维码`,
              width: 180,
              height: 180,
              loading: "lazy",
            }),
            h("span", null, it.label),
          ]),
        ])
      }

      const external = typeof it.href === "string" && it.href.length > 0
      return h(
        "a",
        {
          key: it.label,
          class: "yyj-icon",
          href: external ? it.href : `${root}${it.to ?? "/"}`,
          "aria-label": it.label,
          title: it.label,
          ...(external ? { target: "_blank", rel: "noopener noreferrer" } : {}),
        },
        icon,
      )
    }

    const treeLink = (item, label) =>
      h(
        "a",
        {
          key: item.slug,
          href: `${root}/${item.slug}`,
          class: item.slug === currentSlug ? "yyj-tree-link is-active" : "yyj-tree-link",
        },
        label ?? item.title,
      )

    const treeBody =
      groups.length === 0
        ? null
        : h(
            "div",
            { class: "yyj-tree", "data-panel": "tree", hidden: !isTree },
            groups.map((g) =>
              h(
                "details",
                {
                  class: "yyj-tree-group",
                  key: g.key,
                  // 分类内页默认展开当前分类；首页全部收起
                  open: groups.length === 1,
                },
                [
                  h("summary", { class: "yyj-tree-heading" }, [
                    h("span", { class: "yyj-tree-title" }, g.title),
                    h("span", { class: "yyj-tree-count" }, `${g.count}`),
                  ]),
                  h(
                    "div",
                    { class: "yyj-tree-items" },
                    (g.indexItem ? [treeLink(g.indexItem, "概览")] : []).concat(
                      g.items.map((i) => treeLink(i)),
                    ),
                  ),
                ],
              ),
            ),
          )

    const tabs =
      groups.length > 0
        ? h("div", { class: "yyj-tabs", role: "tablist" }, [
            h(
              "button",
              {
                type: "button",
                class: isTree ? "yyj-tab" : "yyj-tab is-active",
                role: "tab",
                "aria-selected": isTree ? "false" : "true",
                "data-target": "nav",
              },
              "导航",
            ),
            h(
              "button",
              {
                type: "button",
                class: isTree ? "yyj-tab is-active" : "yyj-tab",
                role: "tab",
                "aria-selected": isTree ? "true" : "false",
                "data-target": "tree",
              },
              "目录",
            ),
          ])
        : null

    return h("nav", { class: `yyj-nav ${displayClass ?? ""}`.trim(), "aria-label": "主导航" }, [
      h("details", { class: "yyj-mobile-menu", name: "yyj-mobile-menu" }, [
        h("summary", { "aria-label": "菜单", title: "菜单" }, burgerIcon()),
        h("div", { class: "yyj-mobile-menu-panel" }, [
          tabs,
          h(
            "div",
            { class: "yyj-mobile-links", "data-panel": "nav", hidden: isTree },
            navItems.map(navLink),
          ),
          actions.length > 0
            ? h(
                "div",
                { class: "yyj-mobile-actions", "data-panel": "nav", hidden: isTree },
                actions.map(action),
              )
            : null,
          treeBody,
        ]),
      ]),
      h("div", { class: "yyj-nav-links" }, navItems.map(navLink)),
      actions.length > 0 ? h("div", { class: "yyj-nav-actions" }, actions.map(action)) : null,
    ])
  }

  // 交互：标签页切换、点空白/Esc 收起、跳转后收起
  Comp.afterDOMLoaded = `
(() => {
  if (window.__yyjNavBound) return;
  window.__yyjNavBound = true;

  const closeOthers = (target) => {
    document.querySelectorAll("details.yyj-qr[open], details.yyj-mobile-menu[open]").forEach((d) => {
      if (!d.contains(target)) d.removeAttribute("open");
    });
  };

  document.addEventListener("click", (e) => {
    const tab = e.target.closest && e.target.closest(".yyj-tab");
    if (tab) {
      const panel = tab.closest(".yyj-mobile-menu-panel");
      const target = tab.getAttribute("data-target");
      panel.querySelectorAll(".yyj-tab").forEach((t) => {
        const on = t === tab;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      panel.querySelectorAll("[data-panel]").forEach((p) => {
        p.hidden = p.getAttribute("data-panel") !== target;
      });
      return;
    }
    closeOthers(e.target);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll("details.yyj-qr[open], details.yyj-mobile-menu[open]").forEach((d) =>
        d.removeAttribute("open"),
      );
    }
  });

  document.addEventListener("nav", () => {
    document.querySelectorAll("details.yyj-mobile-menu[open]").forEach((d) =>
      d.removeAttribute("open"),
    );
  });
})();
`

  return Comp
}

export { Nav }
