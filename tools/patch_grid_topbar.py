#!/usr/bin/env python3
"""把 grid 的 header 区域改成横跨所有列（通栏顶栏）。"""
P = "quartz/styles/variables.scss"
s = open(P, encoding="utf-8").read()

old_tablet = '''$tabletGrid: (
  templateRows: "auto auto auto auto",
  templateColumns: "#{$sidePanelWidth} auto",
  rowGap: "5px",
  columnGap: "5px",
  templateAreas:
    \'"grid-sidebar-left grid-header"\\
      "grid-sidebar-left grid-center"\\
      "grid-sidebar-left grid-sidebar-right"\\
      "grid-sidebar-left grid-footer"\',
);'''
new_tablet = '''$tabletGrid: (
  templateRows: "auto auto auto auto",
  templateColumns: "#{$sidePanelWidth} auto",
  rowGap: "5px",
  columnGap: "5px",
  templateAreas:
    \'"grid-header grid-header"\\
      "grid-sidebar-left grid-center"\\
      "grid-sidebar-left grid-sidebar-right"\\
      "grid-sidebar-left grid-footer"\',
);'''

old_desktop = '''$desktopGrid: (
  templateRows: "auto auto auto",
  templateColumns: "#{$sidePanelWidth} auto #{$sidePanelWidth}",
  rowGap: "5px",
  columnGap: "5px",
  templateAreas:
    \'"grid-sidebar-left grid-header grid-sidebar-right"\\
      "grid-sidebar-left grid-center grid-sidebar-right"\\
      "grid-sidebar-left grid-footer grid-sidebar-right"\',
);'''
new_desktop = '''$desktopGrid: (
  templateRows: "auto auto auto",
  templateColumns: "#{$sidePanelWidth} auto #{$sidePanelWidth}",
  rowGap: "5px",
  columnGap: "5px",
  templateAreas:
    \'"grid-header grid-header grid-header"\\
      "grid-sidebar-left grid-center grid-sidebar-right"\\
      "grid-sidebar-left grid-footer grid-sidebar-right"\',
);'''

for old, new, name in ((old_tablet, new_tablet, "tablet"), (old_desktop, new_desktop, "desktop")):
    if old not in s:
        raise SystemExit(f"{name} grid block not found")
    s = s.replace(old, new, 1)

open(P, "w", encoding="utf-8").write(s)
print("grid areas updated")
