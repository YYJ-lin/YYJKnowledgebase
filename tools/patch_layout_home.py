#!/usr/bin/env python3
"""首页/侧边栏对齐旧站：
1) 首页不显示左侧目录树与右侧目录（condition: not-index）
2) 侧边栏只显示当前分类（filterFn 读取当前 URL 的第一段）
"""
import re
import sys

P = "quartz.config.yaml"
s = open(P, encoding="utf-8").read()

# ---- 1. explorer: 加 filterFn + not-index ----
old_tail = """          return (a.displayName || "").localeCompare(b.displayName || "", void 0, { numeric: true });
        }
    layout:
      position: left
      priority: 50
"""
new_tail = """          return (a.displayName || "").localeCompare(b.displayName || "", void 0, { numeric: true });
        }
      filterFn: |-
        (node) => {
          const base = (document.body.dataset.basepath || "").replace(/\\/+$/, "");
          let path = window.location.pathname;
          if (base && path.startsWith(base)) path = path.slice(base.length);
          const section = path.split("/").filter(Boolean)[0];
          // 首页、知识库页、标签页显示完整目录；其余页面只显示当前分类
          if (!section || section === "kb" || section === "tags") return true;
          const segs = node.slugSegments || [];
          if (segs.length === 0) return true;
          return segs[0] === section;
        }
    layout:
      position: left
      priority: 50
      condition: not-index
"""
if old_tail not in s:
    sys.exit("explorer 块尾部未找到")
s = s.replace(old_tail, new_tail, 1)

# ---- 2. table-of-contents: 首页不显示 ----
old_toc = """  - source: "@quartz-community/table-of-contents"
    enabled: true
    order: 50
    layout:
      position: right
      priority: 30
"""
new_toc = """  - source: "@quartz-community/table-of-contents"
    enabled: true
    order: 50
    layout:
      position: right
      priority: 30
      condition: not-index
"""
if old_toc not in s:
    sys.exit("toc 块未找到")
s = s.replace(old_toc, new_toc, 1)

open(P, "w", encoding="utf-8").write(s)
print("config patched")
