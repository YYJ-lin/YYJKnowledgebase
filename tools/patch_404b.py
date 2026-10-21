#!/usr/bin/env python3
"""404 页：去掉用不了的搜索按钮（404 不走普通 frame，页面里没有搜索组件）。"""
P = "quartz/components/pages/404.tsx"
s = open(P, encoding="utf-8").read()

old = """      <button class="yyj-404-search" type="button">
        搜索一下（Ctrl K）
      </button>
"""
if old in s:
    s = s.replace(old, "", 1)

old_script = """      <script
        dangerouslySetInnerHTML={{
          __html: `
          document.addEventListener("click", function (e) {
            if (!e.target.closest || !e.target.closest(".yyj-404-search")) return;
            var btn = document.querySelector("button.search-button");
            if (btn) btn.click();
          });
          `,
        }}
      />
"""
if old_script in s:
    s = s.replace(old_script, "", 1)

open(P, "w", encoding="utf-8").write(s)
print("404 search button removed")
