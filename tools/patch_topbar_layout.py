#!/usr/bin/env python3
"""顶栏：搜索居中、间距、材质改用伪元素（修搜索弹层偏移）；阅读模式/暗色状态；页脚换序。"""
P = "quartz/styles/custom.scss"
s = open(P, encoding="utf-8").read()

old_topbar = """// ---------- 通栏顶栏（站点名 + 主导航 + 工具条） ----------
.topbar {
  grid-area: grid-header;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid var(--yyj-line);
  background: color-mix(in srgb, var(--light) 92%, transparent);
  backdrop-filter: blur(10px);
}

.topbar-inner {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0.65rem 1.5rem;
}

.topbar header {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 0;
  gap: 1.25rem;
  flex-wrap: nowrap;
}

.topbar header > * {
  flex: 0 0 auto;
}

.topbar header > .yyj-nav {
  flex: 1 1 auto;
}
"""

new_topbar = """// ---------- 通栏顶栏（站点名 + 主导航 + 搜索 + 工具条） ----------
.topbar {
  grid-area: grid-header;
  position: sticky;
  top: 0;
  z-index: 100;
  padding-top: env(safe-area-inset-top, 0px);
  border-bottom: 1px solid var(--yyj-line);
  background: color-mix(in srgb, var(--light) 92%, transparent);
  // 注意：backdrop-filter 不能直接加在 .topbar 上。
  // filter/backdrop-filter 会成为 position:fixed 子元素的包含块，
  // 搜索弹层就会从顶栏左上角开始铺，而不是整个视口（用户看到的「弹窗偏了」）。
  // 把材质放到 ::before 上，既不改变包含块，又保留毛玻璃。
}

.topbar::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}

.topbar-inner {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0.7rem 1.75rem;
}

.topbar header {
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 0;
  gap: 1.6rem;
  flex-wrap: nowrap;
  min-height: 36px;
}

.topbar header > * {
  flex: 0 0 auto;
}

.topbar header > .yyj-nav {
  flex: 1 1 auto;
}

// 搜索框居中：绝对定位到顶栏中线，两侧是站点名/导航与工具条
.topbar .search {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: min(30vw, 360px);
  min-width: 220px;
  max-width: none;
}

@media all and (max-width: 1100px) {
  .topbar .search {
    position: static;
    transform: none;
    width: auto;
    min-width: 0;
  }
}
"""
if old_topbar not in s:
    raise SystemExit("topbar block not found")
s = s.replace(old_topbar, new_topbar, 1)

# 顶栏按钮的「已开启」状态
state_css = """
// 阅读模式 / 暗色模式的开启状态（用户能看到自己点开了）
.topbar .readermode,
.topbar .darkmode {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  transition:
    color 140ms var(--yyj-ease-out),
    background-color 140ms var(--yyj-ease-out);
}

.topbar .readermode:hover,
.topbar .darkmode:hover {
  background: var(--yyj-brand-soft);
}

:root[reader-mode="on"] .topbar .readermode {
  color: var(--yyj-brand);
  background: var(--yyj-brand-soft);
}

:root[saved-theme="dark"] .topbar .darkmode {
  color: var(--yyj-brand);
  background: var(--yyj-brand-soft);
}
"""
s = s.rstrip() + "\n" + state_css

# 页脚：品牌区放前面 + 图标行
s = s.replace(
    """.yyj-footer-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr)) 1.3fr;
  gap: 2rem 1.5rem;
  align-items: start;
}""",
    """.yyj-footer-grid {
  display: grid;
  grid-template-columns: 1.3fr repeat(3, minmax(0, 1fr));
  gap: 2rem 1.5rem;
  align-items: start;
}""",
    1,
)

s = s.rstrip() + """

.yyj-footer-actions {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-top: 0.9rem;
}

.yyj-icon {
  display: inline-flex;
  align-items: center;
  color: var(--yyj-muted);
  transition: color 140ms var(--yyj-ease-out);
}

.yyj-icon:hover {
  color: var(--yyj-brand);
}
"""

# 卡片：底部「进入」对齐；Hero overline 光学居中
s = s.replace(
    """.card-more {
  margin-top: 0.7rem;""",
    """.card-more {
  margin-top: auto;
  padding-top: 0.7rem;""",
    1,
)
s = s.rstrip() + """

// 卡片在网格里等高，「进入」贴底，三张卡的文字行才对得齐
.card {
  height: 100%;
}

// letter-spacing 会在最后一个字后面留空隙，居中时会整体偏左
.hero-overline {
  text-indent: 0.18em;
}
"""

open(P, "w", encoding="utf-8").write(s)
print("css updated")
