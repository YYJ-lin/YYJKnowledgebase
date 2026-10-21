#!/usr/bin/env python3
"""mobile-native 基线 + emil 手感 + 首页居中（对齐旧站）。"""
P = "quartz/styles/custom.scss"
s = open(P, encoding="utf-8").read()

block = '''
// =========================================================
// 触控与手感（mobile-native / emil-design-eng）
// =========================================================
:root {
  --yyj-ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --yyj-ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
}

// 去掉 iOS/Android 点按的灰色高亮（最响的「这是网页」信号）
html {
  -webkit-tap-highlight-color: transparent;
  -webkit-text-size-adjust: 100%;
}

// 点按不再等双击缩放，反馈即时
button,
a,
[role="button"],
.card,
.btn {
  touch-action: manipulation;
}

// 控件文字不该被长按选中（正文要保持可选）
button,
[role="button"],
.btn {
  user-select: none;
  -webkit-user-select: none;
}

button,
.btn,
.yyj-nav-link,
.card {
  transition:
    transform 140ms var(--yyj-ease-out),
    background-color 140ms var(--yyj-ease-out),
    border-color 140ms var(--yyj-ease-out),
    color 140ms var(--yyj-ease-out);
}

// 按下反馈（150ms 内、scale 0.97）
button:active,
.btn:active,
.yyj-nav-link:active {
  transform: scale(0.97);
}

.card:active {
  transform: scale(0.985);
}

// 触屏没有真正的 hover：点过后不要保留 hover 态
@media (hover: none) {
  .card:hover {
    transform: none;
    box-shadow: none;
    border-color: var(--yyj-line);
  }
  .btn-primary:hover {
    background: var(--yyj-brand);
  }
  .btn-ghost:hover {
    border-color: var(--yyj-line);
    color: var(--darkgray);
  }
  .yyj-nav-link:hover,
  footer a:hover,
  .yyj-footer-col a:hover {
    color: var(--yyj-muted);
  }
  .hero-search:hover {
    border-color: var(--yyj-line);
    color: var(--yyj-muted);
  }
}

// iOS 会在 input 字号 <16px 时强制放大页面
@media (pointer: coarse) {
  input,
  textarea,
  select {
    font-size: 16px;
  }
}

// 刘海 / 底部指示条安全区（需要 Head 里的 viewport-fit=cover）
.topbar {
  padding-top: env(safe-area-inset-top, 0px);
}

footer {
  padding-bottom: calc(1.25rem + env(safe-area-inset-bottom, 0px));
}

@media all and ($mobile) {
  .topbar-inner {
    padding-left: calc(1rem + env(safe-area-inset-left, 0px));
    padding-right: calc(1rem + env(safe-area-inset-right, 0px));
  }

  .explorer-content {
    padding-bottom: calc(32px + env(safe-area-inset-bottom, 0px));
  }
}

// 顶栏材质：半透明 + 饱和度提升（apple-design §12）
.topbar {
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}

// 减少动效：保留透明度/颜色，去掉位移
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  .card:hover,
  .card:active,
  button:active,
  .btn:active {
    transform: none;
  }
}

// =========================================================
// 首页居中版式（对齐旧站 Hero）
// =========================================================
body[data-slug="index"] {
  .hero {
    text-align: center;
  }

  .hero-sub {
    margin-left: auto;
    margin-right: auto;
    max-width: 620px;
  }

  .hero-actions {
    margin-left: auto;
    margin-right: auto;
    max-width: 560px;
  }

  .hero-cta {
    justify-content: center;
  }

  .section-head {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.2rem;
    margin: 2.8rem 0 1.4rem;
  }

  .section-title {
    margin: 0;
    font-size: 1.4rem;
  }

  .section-note {
    font-size: 0.85rem;
    color: var(--yyj-muted);
  }
}

// 卡片图标
.card-icon {
  display: flex;
  margin-bottom: 0.4rem;
  color: var(--yyj-brand);
}
'''

s = s.rstrip() + "\n" + block
open(P, "w", encoding="utf-8").write(s)
print("scss appended")
