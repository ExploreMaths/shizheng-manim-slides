# -*- coding: utf-8 -*-
p = r"C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\shizheng_pptx.py"
s = open(p, encoding="utf-8").read()

# 1. 把 FadeOut+next_slide 块替换成只 next_slide
old_block = "        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)\n        self.next_slide()"
s = s.replace(old_block, "        self.next_slide()")

# 2. 在 construct 后加 _transition 方法
old_construct = (
    "    def construct(self):\n"
    "        self.slide1()\n"
    "        self.slide2()\n"
    "        self.slide3()\n"
    "        self.slide4()\n"
    "        self.slide5()\n"
    "        self.slide6()\n"
    "        self.slide7()\n"
    "        self.slide8()"
)

transition_method = (
    "\n\n"
    "    def _transition(self):\n"
    "        # 炫酷页间转场：所有对象错落向上淡出 + 轻微缩小\n"
    "        if not self.mobjects:\n"
    "            return\n"
    "        self.play(\n"
    "            LaggedStart(\n"
    "                *[FadeOut(m, shift=UP * 0.4, scale=0.92) for m in self.mobjects],\n"
    "                lag_ratio=0.02,\n"
    "            ),\n"
    "            run_time=0.6,\n"
    "        )"
)

s = s.replace(old_construct, old_construct + transition_method)

# 3. 在 slide2-slide8 开头加 _transition()
for n in range(2, 9):
    old = "    def slide%d(self):\n        self.camera.background_color = ManimColor(BG_CREAM)" % n
    new = "    def slide%d(self):\n        self._transition()\n        self.camera.background_color = ManimColor(BG_CREAM)" % n
    s = s.replace(old, new)

open(p, "w", encoding="utf-8").write(s)
print("FadeOut(m) remaining:", s.count("FadeOut(m)"))
print("next_slide count:", s.count("next_slide"))
print("_transition() calls:", s.count("self._transition()"))
