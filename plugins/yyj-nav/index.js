import { h } from "preact"

/**
 * 云屿集顶部导航。
 *
 * - links：站内文字链接（知识库 / 博客 / 关于我们）
 * - actions：图标或二维码按钮（GitHub 图标、微信 / QQ 二维码）
 *
 * 站内链接按 cfg.baseUrl 拼子路径，域名根和 GitHub Pages 项目页都成立。
 */

const GITHUB_PATH =
  "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"

function siteRoot(cfg) {
  const baseUrl = cfg?.baseUrl ?? ""
  try {
    return new URL(`https://${baseUrl}`).pathname.replace(/\/+$/, "")
  } catch {
    return ""
  }
}

function isExternal(item) {
  return typeof item.href === "string" && item.href.length > 0
}

function linkHref(item, root) {
  return isExternal(item) ? item.href : `${root}${item.to ?? "/"}`
}

function renderIcon(name) {
  if (name === "github") {
    return h(
      "svg",
      {
        width: 18,
        height: 18,
        viewBox: "0 0 16 16",
        fill: "currentColor",
        "aria-hidden": "true",
        focusable: "false",
      },
      h("path", { d: GITHUB_PATH }),
    )
  }
  return null
}

function Nav(opts) {
  const links = opts?.links ?? []
  const actions = opts?.actions ?? []

  const Comp = ({ displayClass, cfg, fileData }) => {
    const root = siteRoot(cfg)
    const current = fileData?.slug ? `/${fileData.slug}` : "/"

    const navLink = (it) => {
      const external = isExternal(it)
      const active =
        !external &&
        (it.to === "/"
          ? current === "/"
          : current === it.to || current.startsWith(it.to.replace(/\/$/, "") + "/"))
      return h(
        "a",
        {
          key: it.label,
          href: linkHref(it, root),
          class: active ? "yyj-nav-link is-active" : "yyj-nav-link",
          ...(external ? { target: "_blank", rel: "noopener noreferrer" } : {}),
        },
        it.label,
      )
    }

    const action = (it) => {
      // 二维码按钮：<details> 原生折叠，无需 JS
      if (it.image) {
        return h("details", { class: "yyj-qr", name: "yyj-qr", key: it.label }, [
          h("summary", { title: `${it.label}二维码` }, it.label),
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

      // 图标链接（GitHub）
      const icon = renderIcon(it.icon)
      if (icon) {
        return h(
          "a",
          {
            key: it.label,
            class: "yyj-nav-icon",
            href: linkHref(it, root),
            "aria-label": it.label,
            title: it.label,
            ...(isExternal(it) ? { target: "_blank", rel: "noopener noreferrer" } : {}),
          },
          icon,
        )
      }

      return h("a", { key: it.label, class: "yyj-nav-link", href: linkHref(it, root) }, it.label)
    }

    return h(
      "nav",
      { class: `yyj-nav ${displayClass ?? ""}`.trim(), "aria-label": "主导航" },
      [h("div", { class: "yyj-nav-links" }, links.map(navLink))].concat(
        actions.length > 0 ? [h("div", { class: "yyj-nav-actions" }, actions.map(action))] : [],
      ),
    )
  }

  // 点空白处 / Esc 收起二维码面板
  Comp.afterDOMLoaded = `
(() => {
  if (window.__yyjQrBound) return;
  window.__yyjQrBound = true;
  const closeAll = (except) => {
    document.querySelectorAll("details.yyj-qr[open]").forEach((d) => {
      if (d !== except) d.removeAttribute("open");
    });
  };
  document.addEventListener("click", (e) => {
    document.querySelectorAll("details.yyj-qr[open]").forEach((d) => {
      if (!d.contains(e.target)) d.removeAttribute("open");
    });
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeAll(null);
  });
})();
`

  return Comp
}

export { Nav }
