#!/usr/bin/env bash
# 构建产物自检：关键不变量，失败会以非 0 退出
set -uo pipefail
cd "$(dirname "$0")/.."

PUB=public
fail=0
ok() { printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad() { printf '  \033[31m✗\033[0m %s\n' "$1"; fail=1; }

echo "== 页面 =="
pages=$(find "$PUB" -name '*.html' | wc -l)
[ "$pages" -ge 10 ] && ok "生成 $pages 个页面" || bad "页面数量异常：$pages"

echo "== 标题（front matter 是否生效）=="
for pair in "index.html:云屿集" "about/index.html:关于云屿集" "kb/erpnext/index.html:ERPNext" "kb/index.html:知识库" "about/welcome.html:开站记"; do
  f="${pair%%:*}"; want="${pair#*:}"
  if grep -q "<title>$want" "$PUB/$f" 2>/dev/null; then ok "$f 标题含「$want」"; else bad "$f 标题不含「$want」"; fi
done

echo "== 字体 =="
if grep -rqs "fonts.googleapis\|fonts.gstatic" "$PUB" --include='*.html' --include='*.css'; then
  bad "产物里仍有 Google Fonts 引用"
else
  ok "无 Google Fonts 引用"
fi
n=$(ls "$PUB"/static/fonts/*.woff2 2>/dev/null | wc -l)
[ "$n" -ge 5 ] && ok "自托管字体 $n 个 woff2" || bad "字体文件缺失（$n）"

echo "== 页脚 =="
if grep -q "yyj-footer-grid" "$PUB/index.html" && grep -q "yyj-footer-grid" "$PUB/kb/erpnext/index.html"; then
  ok "页脚组件已渲染（首页 + 内页）"
else
  bad "页脚组件缺失"
fi
if grep -o 'href="/[^"]*"' "$PUB/index.html" | grep -qv '^href="/YYJKnowledgebase'; then
  bad "存在未带 baseUrl 前缀的站内绝对链接"
else
  ok "站内绝对链接均带 baseUrl 前缀"
fi

echo "== 内容渲染 =="
grep -q 'data-callout=' "$PUB/kb/erpnext/index.html" && ok "callout 渲染正常" || bad "callout 未渲染"
[ -f "$PUB/about/welcome.html" ] && ok "关于/开站记存在" || bad "about/welcome 缺失"
grep -q 'yyj-crumbs' "$PUB/kb/erpnext/index.html" && ok "面包屑已渲染" || bad "面包屑缺失"
grep -q 'yyj-footer-brand' "$PUB/index.html" && ok "页脚品牌区存在" || bad "页脚品牌区缺失"

echo "== 索引 =="
size=$(stat -c%s "$PUB/static/contentIndex.json" 2>/dev/null || echo 0)
[ "$size" -gt 3000 ] && ok "搜索索引 $size 字节" || bad "搜索索引异常（$size）"
grep -q "yyj-lin.github.io/YYJKnowledgebase" "$PUB/sitemap.xml" && ok "sitemap 指向正确 baseUrl" || bad "sitemap baseUrl 不对"
[ ! -e "$PUB/CNAME" ] && ok "无多余 CNAME 文件" || bad "存在 CNAME（会顶掉 GitHub Pages 域名）"

echo
if [ "$fail" -eq 0 ]; then echo "全部通过 ✅"; else echo "有检查失败 ❌"; fi
exit "$fail"
