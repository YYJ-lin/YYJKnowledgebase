#!/usr/bin/env python3
"""云屿集样式：首页落地页 + Hero 搜索/CTA + 章节标题。"""
P = "quartz/styles/custom.scss"
s = open(P, encoding="utf-8").read()

anchor = "// ---------- 首页卡片 ----------"
add = """// ---------- 首页（对齐旧站：无侧栏的落地页） ----------
body[data-slug="index"] {
  .page > #quartz-body {
    grid-template-columns: minmax(0, 1fr);
    grid-template-areas:
      "grid-header"
      "grid-center"
      "grid-footer";
    padding: 0 1.5rem;
  }

  // 首页不显示左目录树、右目录、返回顶部等侧栏内容
  .sidebar {
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

// Hero 里的搜索框与按钮（外观对齐旧站首页）
.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.9rem;
  max-width: 520px;
}

.hero-search {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  width: 100%;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--yyj-line);
  border-radius: 8px;
  background: var(--light);
  color: var(--yyj-muted);
  font: inherit;
  font-size: 0.95rem;
  text-align: left;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease;

  svg {
    flex: none;
  }

  kbd {
    margin-left: auto;
    padding: 0.1rem 0.38rem;
    border: 1px solid var(--yyj-line);
    border-radius: 4px;
    background: var(--lightgray);
    font-family: var(--codeFont);
    font-size: 0.72rem;
    color: var(--yyj-muted);
  }

  &:hover {
    border-color: var(--yyj-brand);
    color: var(--darkgray);
  }
}

.hero-cta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.55rem 1.15rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  text-decoration: none;
}

.btn-primary {
  background: var(--yyj-brand);
  color: #fff;

  &:hover {
    background: var(--yyj-brand-strong);
    color: #fff;
  }
}

.btn-ghost {
  border: 1px solid var(--yyj-line);
  color: var(--darkgray);

  &:hover {
    border-color: var(--yyj-brand);
    color: var(--yyj-brand);
  }
}

.section-title {
  display: flex;
  align-items: baseline;
  gap: 0.55rem;
  margin: 2.6rem 0 1.3rem;
  font-size: 1.35rem;
  border-bottom: none;
}

.section-note {
  font-size: 0.8rem;
  font-weight: 400;
  color: var(--yyj-muted);
}

"""
if anchor not in s:
    raise SystemExit("anchor not found")
s = s.replace(anchor, add + anchor, 1)
open(P, "w", encoding="utf-8").write(s)
print("scss patched")
