# -*- coding: utf-8 -*-
"""
用 win32com 驱动 PowerPoint，按分步状态导出每页高清 PNG。
每个 step 对应一个 <prefix>_step<n>.png。
"""
import os
import win32com.client as win32

PPTX = r"C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\assets\shizheng_working.pptx"
OUT  = r"C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\assets\slides"
os.makedirs(OUT, exist_ok=True)

# { "输出文件名": (slide_index_0based, [要隐藏的形状名]) }
STEPS = [
    # ---- Slide 1 ----
    ("s1_step0", 0, ["top-label","title-bar","main-title","sub-title","bottom-info"]),
    ("s1_step1", 0, ["main-title","sub-title","bottom-info"]),
    ("s1_step2", 0, ["sub-title","bottom-info"]),
    ("s1_step3", 0, ["bottom-info"]),
    ("s1_step4", 0, []),

    # ---- Slide 2 ----
    ("s2_step0", 1, ["info-label-1","info-value-1","info-label-2","info-value-2","v-divider",
                     "info-label-3","info-value-3","stat-num-1","stat-cap-1","stat-num-2",
                     "stat-cap-2","quote-band","quote-mark","quote-text","why-line"]),
    ("s2_step1", 1, ["info-label-2","info-value-2","v-divider","info-label-3","info-value-3",
                     "stat-num-1","stat-cap-1","stat-num-2","stat-cap-2","quote-band",
                     "quote-mark","quote-text","why-line"]),
    ("s2_step2", 1, ["info-label-3","info-value-3","stat-num-1","stat-cap-1","stat-num-2",
                     "stat-cap-2","quote-band","quote-mark","quote-text","why-line"]),
    ("s2_step3", 1, ["stat-num-1","stat-cap-1","stat-num-2","stat-cap-2","quote-band",
                     "quote-mark","quote-text","why-line"]),
    ("s2_step4", 1, ["stat-num-2","stat-cap-2","quote-band","quote-mark","quote-text","why-line"]),
    ("s2_step5", 1, ["quote-band","quote-mark","quote-text","why-line"]),
    ("s2_step6", 1, ["why-line"]),
    ("s2_step7", 1, []),

    # ---- Slide 3 ----
    ("s3_step0", 2, ["r1-num","r1-name","r1-desc","r1-line",
                     "r2-num","r2-name","r2-desc","r2-line",
                     "r3-num","r3-name","r3-desc","r3-line",
                     "r4-num","r4-name","r4-desc","r4-line",
                     "r5-num","r5-name","r5-desc","r5-line",
                     "note","memory-hook"]),
    ("s3_step1", 2, ["r2-num","r2-name","r2-desc","r2-line",
                     "r3-num","r3-name","r3-desc","r3-line",
                     "r4-num","r4-name","r4-desc","r4-line",
                     "r5-num","r5-name","r5-desc","r5-line",
                     "note","memory-hook"]),
    ("s3_step2", 2, ["r3-num","r3-name","r3-desc","r3-line",
                     "r4-num","r4-name","r4-desc","r4-line",
                     "r5-num","r5-name","r5-desc","r5-line",
                     "note","memory-hook"]),
    ("s3_step3", 2, ["r4-num","r4-name","r4-desc","r4-line",
                     "r5-num","r5-name","r5-desc","r5-line",
                     "note","memory-hook"]),
    ("s3_step4", 2, ["r5-num","r5-name","r5-desc","r5-line","note","memory-hook"]),
    ("s3_step5", 2, ["note","memory-hook"]),
    ("s3_step6", 2, ["memory-hook"]),
    ("s3_step7", 2, []),

    # ---- Slide 4 ----
    ("s4_step0", 3, ["left-lead","left-p1","left-p2","left-p3","left-p4",
                     "v-divider","right-lead","right-p1","right-p2","right-p3","bottom-line"]),
    ("s4_step1", 3, ["left-p2","left-p3","left-p4","v-divider",
                     "right-lead","right-p1","right-p2","right-p3","bottom-line"]),
    ("s4_step2", 3, ["left-p3","left-p4","v-divider",
                     "right-lead","right-p1","right-p2","right-p3","bottom-line"]),
    ("s4_step3", 3, ["left-p4","v-divider",
                     "right-lead","right-p1","right-p2","right-p3","bottom-line"]),
    ("s4_step4", 3, ["right-lead","right-p1","right-p2","right-p3","bottom-line"]),
    ("s4_step5", 3, ["right-p1","right-p2","right-p3","bottom-line"]),
    ("s4_step6", 3, ["right-p2","right-p3","bottom-line"]),
    ("s4_step7", 3, ["right-p3","bottom-line"]),
    ("s4_step8", 3, ["bottom-line"]),
    ("s4_step9", 3, []),

    # ---- Slide 5 ----
    ("s5_step0", 4, ["r1-num","r1-body","r1-line",
                     "r2-num","r2-body","r2-line",
                     "r3-num","r3-body","r3-line",
                     "r4-num","r4-body","note"]),
    ("s5_step1", 4, ["r2-num","r2-body","r2-line",
                     "r3-num","r3-body","r3-line",
                     "r4-num","r4-body","note"]),
    ("s5_step2", 4, ["r3-num","r3-body","r3-line","r4-num","r4-body","note"]),
    ("s5_step3", 4, ["r4-num","r4-body","note"]),
    ("s5_step4", 4, ["note"]),
    ("s5_step5", 4, []),

    # ---- Slide 6 ----
    ("s6_step0", 5, ["mapping-table","note"]),
    ("s6_step1", 5, ["note"]),
    ("s6_step2", 5, ["note"]),
    ("s6_step3", 5, ["note"]),
    ("s6_step4", 5, ["note"]),
    ("s6_step5", 5, []),

    # ---- Slide 7 ----
    ("s7_step0", 6, ["p1-num","p1-body","p1-line",
                     "p2-num","p2-body","p2-line",
                     "p3-num","p3-body","closing-strip","closing-text"]),
    ("s7_step1", 6, ["p2-num","p2-body","p2-line",
                     "p3-num","p3-body","closing-strip","closing-text"]),
    ("s7_step2", 6, ["p3-num","p3-body","closing-strip","closing-text"]),
    ("s7_step3", 6, ["closing-strip","closing-text"]),
    ("s7_step4", 6, []),

    # ---- Slide 8 ----
    ("s8_step0", 7, ["a1-icon","a1-text","a2-icon","a2-text",
                     "a3-icon","a3-text","a4-icon","a4-text",
                     "v-divider","end-panel","end-quote-mark","end-quote","end-sign"]),
    ("s8_step1", 7, ["a2-icon","a2-text","a3-icon","a3-text","a4-icon","a4-text",
                     "v-divider","end-panel","end-quote-mark","end-quote","end-sign"]),
    ("s8_step2", 7, ["a3-icon","a3-text","a4-icon","a4-text",
                     "v-divider","end-panel","end-quote-mark","end-quote","end-sign"]),
    ("s8_step3", 7, ["a4-icon","a4-text",
                     "v-divider","end-panel","end-quote-mark","end-quote","end-sign"]),
    ("s8_step4", 7, ["v-divider","end-panel","end-quote-mark","end-quote","end-sign"]),
    ("s8_step5", 7, ["end-sign"]),
    ("s8_step6", 7, []),
]

print("Starting PowerPoint...")
ppt = win32.Dispatch("PowerPoint.Application")
# 不弹窗
try:
    ppt.Visible = 0  # msoFalse
except Exception:
    pass

pres = ppt.Presentations.Open(PPTX, WithWindow=False)

# 缓存原始 Visible
orig = {}
for slide in pres.Slides:
    for sh in slide.Shapes:
        orig[(slide.SlideIndex, sh.Name)] = sh.Visible

# 按顺序导出
for name, sidx, hide in STEPS:
    slide = pres.Slides.Item(sidx + 1)  # 1-based
    # 恢复
    for sh in slide.Shapes:
        sh.Visible = orig[(slide.SlideIndex, sh.Name)]
    # 隐藏
    missing = []
    for h in hide:
        try:
            slide.Shapes.Item(h).Visible = False
        except Exception:
            missing.append(h)
    out = os.path.join(OUT, name + ".png")
    slide.Export(out, "PNG", 2560, 1440)
    msg = f"  exported {name}.png"
    if missing:
        msg += f"  (MISSING: {missing})"
    print(msg)

pres.Close()
ppt.Quit()
print("\nDone. Files:")
for f in sorted(os.listdir(OUT)):
    print(" ", f, os.path.getsize(os.path.join(OUT, f)), "bytes")
