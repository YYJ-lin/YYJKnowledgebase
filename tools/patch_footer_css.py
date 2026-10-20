#!/usr/bin/env python3
"""把 custom.scss 里的旧页脚样式换成四区页脚样式。"""
P = "quartz/styles/custom.scss"
s = open(P, encoding="utf-8").read()

start = s.find("// ---------- 页脚 ----------")
end = s.find("// ---------- 代码 ----------")
if start < 0 or end < 0:
    raise SystemExit("markers not found")

new = """// ---------- 页脚（自定义组件 plugins/yyj-footer） ----------
footer {
  border-top: 1px solid var(--yyj-line);
  margin-top: 3.5rem;
  padding: 2.5rem 0 1rem;
}

.yyj-footer-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr)) 1.3fr;
  gap: 2rem 1.5rem;
  align-items: start;
}

.yyj-footer-col {
  h4 {
    margin: 0 0 0.7rem;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: var(--yyj-muted);
  }

  ul {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    margin: 0;
    padding: 0;
    list-style: none;
  }

  a {
    font-size: 0.9rem;
    color: var(--darkgray);
    text-decoration: none;

    &:hover {
      color: var(--yyj-brand);
    }
  }
}

.yyj-footer-brand-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--dark);
  text-decoration: none;
}

.yyj-footer-tagline {
  margin: 0.4rem 0 0;
  font-size: 0.85rem;
  color: var(--yyj-muted);
}

.yyj-footer-copy {
  margin: 0.8rem 0 0;
  font-size: 0.78rem;
  color: var(--yyj-muted);
}

@media all and ($mobile) {
  .yyj-footer-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.5rem 1rem;
  }
}

"""

s = s[:start] + new + s[end:]
open(P, "w", encoding="utf-8").write(s)
print("footer styles replaced")
