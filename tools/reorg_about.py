#!/usr/bin/env python3
"""把「关于」这一类页面收进 /about/，/kb 改回「知识库」。"""
import re


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def set_fm(path, updates):
    s = read(path)
    m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
    if not m:
        raise SystemExit(f"no frontmatter: {path}")
    lines = m.group(1).splitlines()
    keys = [ln.split(":", 1)[0].strip() for ln in lines if ":" in ln]
    for k, v in updates.items():
        if k in keys:
            lines = [f"{k}: {v}" if ln.startswith(f"{k}:") else ln for ln in lines]
        else:
            lines.append(f"{k}: {v}")
    write(path, "---\n" + "\n".join(lines) + "\n---\n" + s[m.end() :])
    print("fm updated", path)


# 1) 旧 URL 重定向
set_fm("content/about/contact.md", {"aliases": '["contact/index"]'})
set_fm("content/about/privacy.md", {"aliases": '["privacy/index"]'})
set_fm("content/about/license.md", {"aliases": '["license/index"]'})

# 2) 页内相对链接修正
for path in ("content/about/privacy.md", "content/about/license.md"):
    s = read(path)
    s = s.replace("(../contact/)", "(./contact)")
    s = s.replace("(../../contact/)", "(./contact)")
    write(path, s)
    print("links fixed", path)

# 3) kb -> 知识库
s = read("content/kb.md")
s = s.replace("title: 业务与行业", "title: 知识库")
s = s.replace("navLabel: 业务与行业", "navLabel: 知识库")
s = s.replace("description: 业务分享与行业知识的总入口", "description: 业务笔记、行业常识与各类文档的入口")
# 去掉「资源与工具」卡片（它自己是顶栏一项）
s = re.sub(r'\n<a class="card" href="\.\./tools/">.*?</a>', "", s, flags=re.S)
s = s.replace(
    "业务里的判断、行业里的常识，按主题整理成可以回看的内容。挑一个入口开始：",
    "按主题整理的业务笔记与行业常识。挑一个入口开始：",
)
s = s.replace(
    "- **看更新**：技术类内容在 [技术手记](../tech/)，站点本身的说明在 [关于云屿集](../about/)。",
    "- **看更新**：技术类内容在 [技术手记](../tech/)，站点说明、联系方式在 [关于](../about/)。",
)
write("content/kb.md", s)
print("kb renamed")

# 4) 关于页：加「本站说明」入口
s = read("content/about/index.md")
old = """## 联系

- GitHub：[github.com/YYJ-lin](https://github.com/YYJ-lin)"""
new = """## 本站说明

- [联系](contact) —— 怎么找到我
- [隐私说明](privacy) —— 本站收集什么、不收集什么
- [版权与许可](license) —— 文章和代码分别怎么用

## 联系

- GitHub：[github.com/YYJ-lin](https://github.com/YYJ-lin)"""
if old in s and "本站说明" not in s:
    s = s.replace(old, new, 1)
    write("content/about/index.md", s)
    print("about page links added")

# 5) 页脚：法务行只留 RSS；关于与反馈加「联系」
p = "quartz.config.yaml"
s = read(p)
s = s.replace(
    """            - { label: 关于本站, to: /about/ }
            - { label: 反馈与联系, href: "https://github.com/YYJ-lin/YYJKnowledgebase/issues" }""",
    """            - { label: 关于本站, to: /about/ }
            - { label: 联系, to: /about/contact }
            - { label: 反馈与联系, href: "https://github.com/YYJ-lin/YYJKnowledgebase/issues" }""",
    1,
)
s = s.replace(
    """      legal:
        - { label: 联系, to: /contact/ }
        - { label: 隐私说明, to: /privacy/ }
        - { label: 版权与许可, to: /license/ }
        - { label: RSS, to: /index.xml }
        - { label: 站点地图, to: /sitemap.xml }""",
    """      legal:
        - { label: RSS, to: /index.xml }""",
    1,
)
write(p, s)
print("footer updated")
