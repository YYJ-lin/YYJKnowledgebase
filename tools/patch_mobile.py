#!/usr/bin/env python3
"""移动端适配：grid 顺序（顶栏在前）+ 顶栏两行布局。"""
P = "quartz/styles/variables.scss"
s = open(P, encoding="utf-8").read()

old = '''$mobileGrid: (
  templateRows: "auto auto auto auto auto",
  templateColumns: "auto",
  rowGap: "5px",
  columnGap: "5px",
  templateAreas:
    \'"grid-sidebar-left"\\
      "grid-header"\\
      "grid-center"\\
      "grid-sidebar-right"\\
      "grid-footer"\',
);'''
new = '''$mobileGrid: (
  templateRows: "auto auto auto auto auto",
  templateColumns: "auto",
  rowGap: "5px",
  columnGap: "5px",
  templateAreas:
    \'"grid-header"\\
      "grid-sidebar-left"\\
      "grid-center"\\
      "grid-sidebar-right"\\
      "grid-footer"\',
);'''
if old not in s:
    raise SystemExit("mobile grid block not found")
s = s.replace(old, new, 1)
open(P, "w", encoding="utf-8").write(s)
print("mobile grid order updated")

# ---------- 顶栏移动端两行 ----------
P = "quartz/styles/custom.scss"
s = open(P, encoding="utf-8").read()
old_mq = '''@media all and ($mobile) {
  .topbar-inner {
    padding: 0.6rem 1rem;
  }

  .yyj-nav {
    gap: 0.85rem;
    overflow-x: auto;
  }

  .yyj-nav-link {
    font-size: 0.9rem;
  }
}'''
new_mq = '''@media all and ($mobile) {
  .topbar-inner {
    padding: 0.55rem 1rem;
  }

  // 手机端顶栏两行：站点名 + 工具条 / 导航链接
  .topbar header {
    flex-wrap: wrap;
    gap: 0.45rem 0.75rem;
  }

  .topbar header > .page-title {
    order: 1;
  }

  .topbar header > .flex-component {
    order: 2;
    margin-left: auto;
  }

  .topbar header > .yyj-nav {
    order: 3;
    flex: 1 1 100%;
    gap: 1rem;
    overflow-x: auto;
    scrollbar-width: none;

    &::-webkit-scrollbar {
      display: none;
    }
  }

  .yyj-nav-link {
    font-size: 0.9rem;
  }
}'''
if old_mq not in s:
    raise SystemExit("topbar mobile block not found")
s = s.replace(old_mq, new_mq, 1)
open(P, "w", encoding="utf-8").write(s)
print("topbar mobile layout updated")
