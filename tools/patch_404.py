#!/usr/bin/env python3
"""404 页：人话 + 搜索入口 + 主要栏目。"""
P = "quartz/components/pages/404.tsx"
s = open(P, encoding="utf-8").read()

old_start = """    <article class="popover-hint">
      <h1>404</h1>
      <p>{i18n(cfg.locale).pages.error.notFound}</p>
      <a href={baseDir}>{i18n(cfg.locale).pages.error.home}</a>
"""
new_start = """    <article class="popover-hint yyj-404">
      <h1>404</h1>
      <p>这一页不在了 —— 可能链接写错了，或者文章改过名字。</p>
      <button class="yyj-404-search" type="button">
        搜索一下（Ctrl K）
      </button>
      <ul class="yyj-404-links">
        <li>
          <a href={baseDir}>首页</a>
        </li>
        <li>
          <a href={`${baseDir}/kb`}>知识库</a>
        </li>
        <li>
          <a href={`${baseDir}/business/`}>业务分享</a>
        </li>
        <li>
          <a href={`${baseDir}/industry/`}>行业知识</a>
        </li>
        <li>
          <a href={`${baseDir}/tools/`}>工具资源</a>
        </li>
        <li>
          <a href={`${baseDir}/blog/`}>博客</a>
        </li>
        <li>
          <a href={`${baseDir}/about/`}>关于</a>
        </li>
      </ul>
      <script
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
if old_start not in s:
    raise SystemExit("404 header block not found")
s = s.replace(old_start, new_start, 1)
open(P, "w", encoding="utf-8").write(s)
print("404 page upgraded")
