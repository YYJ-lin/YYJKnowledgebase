#!/usr/bin/env python3
"""把组件演示里「行高亮」一节改成如实说明（Quartz 不支持 {2,4}）。"""
p = "content/about/components.md"
s = open(p, encoding="utf-8").read()

old = """### 指定高亮行

```python {2,4}
def greet(name):
    print("Hello")          # 高亮这一行
    print("World")
    print(name)             # 也高亮这一行
```
"""
new = """### 高亮某几行（暂时不支持）

旧站 Docusaurus 用的 `{2,4}` 行高亮标记，Quartz 目前不支持：写了不会报错，只是这几行不会被高亮。
"""
if old not in s:
    raise SystemExit("block not found")
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(s)
print("components.md updated")
