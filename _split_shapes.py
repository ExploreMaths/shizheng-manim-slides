# -*- coding: utf-8 -*-
"""
把原 pptx 中 slide 4 的 left-body / right-body 多段文本框拆成独立文本框，
方便后续按段落分步导出。同时把 slide 6 的表格按行拆成独立形状（便于逐行显示）。
输出：shizheng_working.pptx
"""
import copy
from pptx import Presentation
from pptx.util import Cm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree

SRC = r"C:\Users\kylez\Documents\kimi\tasks\2026-10-17\10-27-45-51e615b7\shizheng_ppt\shizheng.pptx"
DST = r"C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\assets\shizheng_working.pptx"

import os
os.makedirs(os.path.dirname(DST), exist_ok=True)

prs = Presentation(SRC)

# ---------------- Slide 4 (index 3): 拆 left-body / right-body ----------------
s4 = prs.slides[3]
for shape in list(s4.shapes):
    if shape.name == "left-body":
        # 原框位置
        left, top, width = shape.left, shape.top, shape.width
        height = shape.height
        tf = shape.text_frame
        paras = []
        for p in tf.paragraphs:
            text = "".join(r.text for r in p.runs)
            if text.strip():
                paras.append(text)
        # 删除原框
        sp = shape._element
        sp.getparent().remove(sp)
        # 按行高估算：原框高 8.47cm，4 段 -> 每段约 2.1cm
        # 实际 PowerPoint 行高约 字体大小 * 1.3
        line_h = Cm(2.05)
        for i, text in enumerate(paras):
            tb = s4.shapes.add_textbox(left, top + line_h * i, width, line_h)
            t = tb.text_frame
            t.word_wrap = True
            run = t.paragraphs[0].add_run()
            run.text = text
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(0x4A, 0x42, 0x39)
            run.font.name = "MiSans"
            tb.name = f"left-p{i+1}"
        print(f"[slide4] split left-body into {len(paras)} paragraphs")

    elif shape.name == "right-body":
        left, top, width = shape.left, shape.top, shape.width
        tf = shape.text_frame
        paras = []
        for p in tf.paragraphs:
            text = "".join(r.text for r in p.runs)
            if text.strip():
                paras.append(text)
        sp = shape._element
        sp.getparent().remove(sp)
        line_h = Cm(2.4)
        for i, text in enumerate(paras):
            tb = s4.shapes.add_textbox(left, top + line_h * i, width, line_h)
            t = tb.text_frame
            t.word_wrap = True
            run = t.paragraphs[0].add_run()
            run.text = text
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(0x4A, 0x42, 0x39)
            run.font.name = "MiSans"
            tb.name = f"right-p{i+1}"
        print(f"[slide4] split right-body into {len(paras)} paragraphs")

# ---------------- Slide 6 (index 5): 表格按行拆 ----------------
# 表格整体导出在一步里就够了（表头+第1行一起，然后逐行），这里把表格保留为整体，
# 但在导出脚本里通过"临时复制行"的方式控制可见性。python-pptx 拆表格太复杂，
# 改成在 PowerShell 导出脚本里用 shape.Visible 控制整个表格，然后用 Manim 叠加行截图。

prs.save(DST)
print("saved:", DST)

# 验证：打印 slide 4 的形状名
prs2 = Presentation(DST)
s4 = prs2.slides[3]
print("\nSlide 4 shapes after split:")
for sh in s4.shapes:
    print(f"  {sh.name}: top={round(sh.top/360000,2)}cm  text={sh.text_frame.text[:50] if sh.has_text_frame else ''!r}")
