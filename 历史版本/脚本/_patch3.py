# -*- coding: utf-8 -*-
p = r"C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\shizheng_pptx.py"
s = open(p, encoding="utf-8").read()

# 7 个转场用不同 target 交替
import re
targets = {
    2: "line",    # 封面→速览：拉伸成横线
    3: "dot",     # 速览→要点：聚合成点
    4: "square",  # 要点→新闻：收缩成方块
    5: "dot",     # 新闻→教材：聚合成点
    6: "line",    # 教材→表格：拉伸成横线
    7: "square",  # 表格→点评：收缩成方块
    8: "dot",     # 点评→行动：聚合成点
}

for n, tgt in targets.items():
    # 匹配 self._transition(...) 整行
    pattern = r"    def slide%d\(self\):\n        self\._transition\([^)]*\)" % n
    replacement = "    def slide%d(self):\n        self._transition(target=\"%s\")" % (n, tgt)
    new_s, cnt = re.subn(pattern, replacement, s)
    if cnt:
        s = new_s
        print(f"slide{n}: -> {tgt}")
    else:
        print(f"slide{n}: NOT FOUND")

open(p, "w", encoding="utf-8").write(s)
