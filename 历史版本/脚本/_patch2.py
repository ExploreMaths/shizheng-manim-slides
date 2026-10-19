# -*- coding: utf-8 -*-
p = r"C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\shizheng_pptx.py"
s = open(p, encoding="utf-8").read()

transitions = {
    2: "self._transition(shift=UP * 2.5, scale=0.7, rt=0.8)  # 封面向上拉走",
    3: "self._transition(shift=LEFT * 2, rt=0.6)  # 左滑出",
    4: "self._transition(shift=DOWN * 1.5, scale=0.8, rt=0.6)  # 下沉",
    5: "self._transition(shift=RIGHT * 2, rt=0.6)  # 右滑出",
    6: "self._transition(shift=ORIGIN, scale=0.2, rotate=TAU/6, rt=0.8)  # 缩小旋转消失",
    7: "self._transition(shift=DL * 2, scale=0.85, rt=0.6)  # 左下斜飞",
    8: "self._transition(shift=UP * 1.5, lag=0.03, rt=0.8)  # 错落上推",
}

for n, call in transitions.items():
    old = "    def slide%d(self):\n        self._transition()" % n
    new = "    def slide%d(self):\n        %s" % (n, call)
    if old in s:
        s = s.replace(old, new)
        print(f"slide{n}: OK")
    else:
        print(f"slide{n}: PATTERN NOT FOUND")

open(p, "w", encoding="utf-8").write(s)
