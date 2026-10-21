import { i18n } from "../../i18n"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"

const NotFound: QuartzComponent = ({ cfg, ctx }: QuartzComponentProps) => {
  const url = new URL(`https://${cfg.baseUrl ?? "example.com"}`)
  const baseDir = ctx.argv.serve ? "/" : url.pathname

  return (
    <article class="popover-hint yyj-404">
      <h1>404</h1>
      <p>这一页不在了 —— 可能链接写错了，或者文章改过名字。</p>
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
          if (typeof fetchData !== "undefined") {
            fetchData.then(function(index) {
              var basePath = document.body.dataset.basepath || "";
              if (basePath.length > 1 && basePath.endsWith("/")) {
                basePath = basePath.slice(0, -1);
              }
              var pathname = window.location.pathname;
              var hasBasePrefix = basePath.length > 1 && pathname.startsWith(basePath);
              if (hasBasePrefix) {
                pathname = pathname.slice(basePath.length);
              }
              if (pathname.startsWith("/")) {
                pathname = pathname.slice(1);
              }
              if (pathname.endsWith("/")) {
                pathname = pathname.slice(0, -1);
              }
              if (pathname.endsWith(".html")) {
                pathname = pathname.slice(0, -5);
              }
              if (pathname.endsWith("/index")) {
                pathname = pathname.slice(0, -6);
              }
              var lowered = pathname.toLowerCase();
              if (lowered !== pathname && index[lowered] != null) {
                var prefix = hasBasePrefix ? basePath : "";
                var target = prefix + (prefix.endsWith("/") ? "" : "/") + lowered;
                window.location.replace(target);
              }
            });
          }
          `,
        }}
      />
    </article>
  )
}

export default (() => NotFound) satisfies QuartzComponentConstructor
