#!/usr/bin/env python3
"""顶栏样式 + 首页改为「顶栏 + 单栏内容」（搜索已挪到顶栏，侧栏可以整块隐藏）。"""
P = "quartz/styles/custom.scss"
s = open(P, encoding="utf-8").read()

start = s.find('body[data-slug="index"] {')
end = s.find('// Hero 里的搜索框与按钮')
if start < 0 or end < 0:
    raise SystemExit("homepage block markers not found")

new_home = '''body[data-slug="index"] {
  .page > #quartz-body {
    grid-template-columns: minmax(0, 1fr);
    grid-template-rows: auto auto auto;
    grid-template-areas:
      "grid-header"
      "grid-center"
      "grid-footer";
    padding: 0 1.5rem;
  }

  // 搜索/主题/阅读模式已经挪到顶栏，首页可以整块隐藏侧栏
  .sidebar.left,
  .sidebar.right {
    display: none;
  }

  .center > article {
    max-width: 920px;
  }

  .hero {
    border-bottom: none;
    padding: 3rem 0 2.5rem;
    margin-bottom: 0.5rem;
  }

  .hero-sub {
    font-size: 1.15rem;
    max-width: none;
  }
}

'''
s = s[:start] + new_home + s[end:]

# 顶栏样式插到「首页（对齐旧站）」之前
anchor = "// ---------- 首页（对齐旧站：无侧栏的落地页） ----------"
if anchor not in s:
    raise SystemExit("homepage section anchor not found")

topbar = '''// ---------- 通栏顶栏（站点名 + 主导航 + 工具条） ----------
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
  margin: 0;
  gap: 1.25rem;
  align-items: center;
}

.topbar header h1 {
  flex: none;
  margin: 0;
  font-size: 1.12rem;
  letter-spacing: -0.01em;
}

.yyj-nav {
  display: flex;
  align-items: center;
  gap: 1.1rem;
  flex: 1;
}

.yyj-nav-link {
  font-size: 0.95rem;
  color: var(--darkgray);
  text-decoration: none;
  white-space: nowrap;

  &:hover {
    color: var(--yyj-brand);
  }

  &.is-active {
    color: var(--yyj-brand);
    font-weight: 500;
  }
}

@media all and ($mobile) {
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
}

'''
s = s.replace(anchor, topbar + anchor, 1)
open(P, "w", encoding="utf-8").write(s)
print("css patched: topbar + homepage")
