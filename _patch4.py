# -*- coding: utf-8 -*-
import re

p = r"C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\shizheng_pptx.py"
s = open(p, encoding="utf-8").read()

# 1. mk_text 加 stroke_width=0
s = s.replace(
    '    t = Text(\n        text, font=font, font_size=size, color=color,\n        weight=BOLD if bold else NORMAL, slant=slant,\n        line_spacing=0.6,\n    )',
    '    t = Text(\n        text, font=font, font_size=size, color=color,\n        weight=BOLD if bold else NORMAL, slant=slant,\n        line_spacing=0.6, stroke_width=0,\n    )'
)

# 2. 删除所有 run_time=... 参数（包括逗号）
s = re.sub(r',\s*run_time=[\d.]+', '', s)
s = re.sub(r'run_time=[\d.]+,\s*', '', s)
s = re.sub(r'\(run_time=[\d.]+\)', '()', s)
# 处理 play(xxx, run_time=0.5) 这种尾巴
s = re.sub(r',\s*run_time=[\d.]+', '', s)
s = re.sub(r'run_time=[\d.]+,?\s*', '', s)

# 3. 在每个 next_slide() 前加 wait(1)
s = s.replace(
    '        self.next_slide()',
    '        self.wait(1)\n        self.next_slide()'
)

# 4. construct 里加 slide9
s = s.replace(
    '        self.slide8()',
    '        self.slide8()\n        self.slide9()'
)

open(p, "w", encoding="utf-8").write(s)
print("done")
print("run_time remaining:", s.count("run_time"))
print("wait(1) count:", s.count("self.wait(1)"))
print("next_slide count:", s.count("next_slide()"))
print("slide9 refs:", s.count("slide9"))
