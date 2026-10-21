import { h } from "preact"

/**
 * 云屿集页脚。
 *
 * 为什么要自己写：Quartz 内置页脚只接受写死的 href，站内链接在
 * GitHub Pages 项目页（部署在 /YYJKnowledgebase/ 子路径）下会 404。
 * 这里根据 cfg.baseUrl 拼出带子路径的绝对路径，域名根和子路径都成立。
 *
 * 顺序：品牌区（含 GitHub / 微信 / QQ 图标）→ 三列链接。
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

function renderIcon(name) {
  const icon = ICONS[name]
  if (!icon) return null
  return h(
    "svg",
    {
      width: 18,
      height: 18,
      viewBox: icon.viewBox,
      fill: "currentColor",
      "aria-hidden": "true",
      focusable: "false",
    },
    h("path", { d: icon.path }),
  )
}

function Footer(opts) {
  const columns = opts?.columns ?? []
  const brand = opts?.brand ?? null
  const actions = opts?.actions ?? []
  const legal = opts?.legal ?? []

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
          { href, ...(external ? { target: "_blank", rel: "noopener noreferrer" } : {}) },
          it.label,
        ),
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

    const brandNode = brand
      ? h("div", { class: "yyj-footer-brand", key: "brand" }, [
          h("a", { class: "yyj-footer-brand-name", href: `${root}/` }, brand.title ?? "云屿集"),
          brand.tagline ? h("p", { class: "yyj-footer-tagline" }, brand.tagline) : null,
          actions.length > 0
            ? h("div", { class: "yyj-footer-actions" }, actions.map(action))
            : null,
        ])
      : null

    return h("footer", { class: displayClass || undefined }, [
      h(
        "div",
        { class: "yyj-footer-grid" },
        [brandNode].concat(
          columns.map((col) =>
            h("div", { class: "yyj-footer-col", key: col.title }, [
              h("h4", null, col.title),
              h("ul", null, (col.items ?? []).map(item)),
            ]),
          ),
        ),
      ),
      h("div", { class: "yyj-footer-legal" }, [
        h("p", { class: "yyj-footer-copy" }, `© ${year} ${brand?.title ?? "云屿集"}`),
        h(
          "ul",
          { class: "yyj-footer-legal-links" },
          legal.map((it) => {
            const external = typeof it.href === "string" && it.href.length > 0
            return h(
              "li",
              { key: it.label },
              h(
                "a",
                {
                  href: external ? it.href : `${root}${it.to ?? "/"}`,
                  ...(external ? { target: "_blank", rel: "noopener noreferrer" } : {}),
                },
                it.label,
              ),
            )
          }),
        ),
        h(
          "button",
          { class: "yyj-to-top", type: "button", "aria-label": "回到顶部" },
          "回到顶部 ↑",
        ),
      ]),
    ])
  }

  // 点空白处 / Esc 收起二维码面板
  Comp.afterDOMLoaded = `
(() => {
  if (window.__yyjQrBound) return;
  window.__yyjQrBound = true;
  document.addEventListener("click", (e) => {
    document.querySelectorAll("details.yyj-qr[open]").forEach((d) => {
      if (!d.contains(e.target)) d.removeAttribute("open");
    });
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll("details.yyj-qr[open]").forEach((d) => d.removeAttribute("open"));
    }
  });

  // 回到顶部
  if (!window.__yyjTopBound) {
    window.__yyjTopBound = true;
    const sync = () => {
      document.querySelectorAll(".yyj-to-top").forEach((b) => {
        b.classList.toggle("is-visible", window.scrollY > 400);
      });
    };
    window.addEventListener("scroll", sync, { passive: true });
    document.addEventListener("click", (e) => {
      const btn = e.target.closest && e.target.closest(".yyj-to-top");
      if (!btn) return;
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    document.addEventListener("nav", sync);
    sync();
  }
})();
`

  return Comp
}

export { Footer }
