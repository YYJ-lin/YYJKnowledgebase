#!/usr/bin/env python3
"""站内链接体检：抓取页面里的站内链接，逐个请求，报告非 200。

用法:
  python3 tools/check_links.py                                  # 线上
  python3 tools/check_links.py http://127.0.0.1:8095/YYJKnowledgebase/
"""
import re
import subprocess
import sys
import time
from urllib.parse import urljoin, quote

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://yyj-lin.github.io/YYJKnowledgebase/"
if not BASE.endswith("/"):
    BASE += "/"

SEEDS = ["", "kb", "tech/", "tech/index", "tools/", "about/", "about/contact",
         "about/privacy", "about/license", "about/writing-guide", "kb/", "kb/business/", "kb/industry/"]


def fetch(url):
    """返回 (status, bytes)；失败重试三次。"""
    for attempt in range(3):
        proc = subprocess.run(
            ["curl", "-sSL", "--max-time", "25", "-w", "\n%{http_code}", url],
            capture_output=True,
        )
        if proc.returncode == 0:
            out = proc.stdout.decode("utf-8", "replace")
            body, _, code = out.rpartition("\n")
            return int(code or 0), body
        time.sleep(1 + attempt)
    return 0, ""


links, pages = set(), 0
for seed in SEEDS:
    url = urljoin(BASE, seed)
    status, html = fetch(url)
    if status != 200:
        print(f"✗ 页面打不开 {url} -> {status}")
        continue
    pages += 1
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith("#") or href.startswith("mailto:"):
            continue
        absolute = urljoin(url, href)
        if absolute.startswith(BASE):
            links.add(absolute)

print(f"抓取 {pages} 个页面，发现 {len(links)} 个站内链接")

bad = []
for link in sorted(links):
    status, _ = fetch(quote(link, safe=":/?&=#%"))
    if status != 200:
        bad.append((status, link))
    time.sleep(0.2)

if bad:
    print("以下链接不可达：")
    for status, link in bad:
        print(" ", status, link)
    sys.exit(1)
print("全部站内链接 200 ✅")
