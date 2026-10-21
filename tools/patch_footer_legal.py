#!/usr/bin/env python3
"""页脚：加法务行（版权 + 次级链接 + 回到顶部）。"""
P = "plugins/yyj-footer/index.js"
s = open(P, encoding="utf-8").read()

# 1) 读取 legal 配置
s = s.replace(
    "  const actions = opts?.actions ?? []\n",
    "  const actions = opts?.actions ?? []\n  const legal = opts?.legal ?? []\n",
    1,
)

# 2) 品牌列里去掉版权（移到法务行）
s = s.replace(
    '          h("p", { class: "yyj-footer-copy" }, `© ${year} ${brand.title ?? "云屿集"}`),\n',
    "",
    1,
)

# 3) 网格后面加法务行
old_tail = """        ),
      ),
    ])
  }
"""
new_tail = """        ),
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
"""
if old_tail not in s:
    raise SystemExit("footer tail not found")
s = s.replace(old_tail, new_tail, 1)

# 4) 回到顶部：滚动 400px 后显示
s = s.replace(
    """  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll("details.yyj-qr[open]").forEach((d) => d.removeAttribute("open"));
    }
  });
})();""",
    """  document.addEventListener("keydown", (e) => {
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
})();""",
    1,
)

open(P, "w", encoding="utf-8").write(s)
print("footer legal row added")
