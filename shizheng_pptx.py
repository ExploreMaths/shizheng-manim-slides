# -*- coding: utf-8 -*-
"""
时政演讲 Manim Slides —— 像素级复刻 + Manim 招牌动画版
======================================================
- 文本框按 PPT 左上角锚定（UL），多行文字位置与原 PPT 一致
- 动画：Write（打字机）/ Create（画线）/ GrowFromEdge（生长）/
        Circumscribe（圈重点）/ LaggedStart（错落）/ Indicate（高亮）
- 字体：MiSans（正文）、Noto Serif SC（标题/数字）
- 颜色：直接取 PPT HEX

运行：
  manim -pqh shizheng_pptx.py ShizhengSlides
  manim-slides present shizheng_pptx.py ShizhengSlides
  # 导出 PPTX：
  manim-slides convert --to=pptx ShizhengSlides shizheng.pptx
"""

import os
from manim import *
from manim_extensions import ExtendedLine
from manim import ManimColor
from manim_slides import Slide

# ---- 兼容 manim 0.22：老 manim-slides 与 0.22 的 API 差异 ----
import manim_slides.slide.manim as _msm
from manim import config as _cfg

def _slide_init_compat(self, *a, **kw):
    super(_msm.Slide, self).__init__(*a, **kw)
_msm.Slide.__init__ = _slide_init_compat

# manim 0.22 要求 max_files_cached 是整数或 -1；老版 render 写 float("inf") 会报错。
# 直接重写 render：把 inf 换成 -1，flush_cache 已在 0.22 删除直接跳过，其余逻辑原样保留。
def _slide_render_compat(self, *a, **kw):
    max_files_cached = _cfg["max_files_cached"]
    _cfg["max_files_cached"] = -1  # -1 = 不限制

    super(_msm.Slide, self).render(*a, **kw)

    _cfg["max_files_cached"] = max_files_cached

    self._save_slides(
        use_cache=not (_cfg.get("disable_caching", False) or self.disable_caching),
        flush_cache=False,
        skip_reversing=self.skip_reversing,
    )
_msm.Slide.render = _slide_render_compat

# ---------------------------------------------------------------------------
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
MEDIA  = os.path.join(ASSETS, "media")

BG_CREAM   = "#F8F4ED"
RED        = "#C03A2B"
INK        = "#211D18"
BODY       = "#4A4239"
GRAY       = "#7A7166"
BAND       = "#F1E9DC"
LINE_GRAY  = "#D9CFC0"
TABLE_HEAD = "#2B2420"

FONT_SANS  = "MiSans"
FONT_SERIF = "Noto Serif SC"

SCALE = 14.222 / 33.87
PPT_W = 33.87
PPT_H = 19.05


def P(left_cm, top_cm, w_cm, h_cm):
    """返回 (center_x, center_y, w_m, h_m)"""
    cx = left_cm + w_cm / 2
    cy = top_cm + h_cm / 2
    return (cx - PPT_W / 2) * SCALE, (PPT_H / 2 - cy) * SCALE, w_cm * SCALE, h_cm * SCALE


def ul_point(left_cm, top_cm):
    """PPT 文本框左上角在 Manim 中的坐标。"""
    return ((left_cm - PPT_W / 2) * SCALE, (PPT_H / 2 - top_cm) * SCALE, 0)


def mk_text(left, top, w, h, text, size, color=INK, font=FONT_SANS, bold=False, slant=NORMAL, z=2):
    """按 PPT 文本框左上角锚定（UL），文字从左上角开始排。"""
    t = Text(
        text, font=font, font_size=size, color=color,
        weight=BOLD if bold else NORMAL, slant=slant,
        line_spacing=0.6, stroke_width=1, stroke_color=color,
    )
    t.move_to(ul_point(left, top), aligned_edge=UL)
    t.set_z_index(z)
    return t


def mk_rect(left, top, w, h, fill_color, opacity=1.0, stroke_width=0, stroke_color=None, z=1):
    mx, my, mw, mh = P(left, top, w, h)
    r = Rectangle(
        width=mw, height=mh,
        fill_color=fill_color, fill_opacity=opacity,
        stroke_width=stroke_width,
        stroke_color=stroke_color if stroke_color else fill_color,
    )
    r.move_to([mx, my, 0])
    r.set_z_index(z)
    return r


def mk_hline(left, top, w, color=RED, stroke=2.0, z=1):
    mx, my, mw, _ = P(left, top, w, 0.04)
    ln = Line([-mw/2, 0, 0], [mw/2, 0, 0], color=color, stroke_width=stroke)
    ln.move_to([mx, my, 0])
    ln.set_z_index(z)
    return ln


def mk_vline(left, top, h, color=LINE_GRAY, stroke=1.5, z=1):
    mx, my, _, mh = P(left, top, 0.04, h)
    ln = Line([0, mh/2, 0], [0, -mh/2, 0], color=color, stroke_width=stroke)
    ln.move_to([mx, my, 0])
    ln.set_z_index(z)
    return ln


# ---------------------------------------------------------------------------
class ShizhengSlides(Slide):

    def construct(self):
        self.slide0()
        self.slide1()
        self.slide2()
        self.slide3()
        self.slide4()
        self.slide5()
        self.slide6()
        self.slide7()
        self.slide8()
        self.slide9()

    def _transition(self, target="up", rt=0.8):
        """切页转场：每页不同的飞出方式。
        target:
          "up"     → 全部向上飞出画面
          "down"   → 全部向下飞出画面
          "left"   → 全部向左飞出画面
          "right"  → 全部向右飞出画面
          "diag_tr"→ 全部飞向右上角
          "diag_bl"→ 全部飞向左下角
          "shrink" → 全部缩到中心淡出
          "spin"   → 旋转缩小淡出
        """
        if not self.mobjects:
            return
        H = 8.5
        W = 10.5
        dest_map = {
            "up":      np.array([0, H, 0]),
            "down":    np.array([0, -H, 0]),
            "left":    np.array([-W, 0, 0]),
            "right":   np.array([W, 0, 0]),
            "diag_tr": np.array([W, H, 0]),
            "diag_tl": np.array([-W, H, 0]),
            "diag_bl": np.array([-W, -H, 0]),
            "diag_br": np.array([W, -H, 0]),
        }
        if target in ("shrink", "spin"):
            target = "diag_br"
        d = dest_map[target]
        self.play(
            *[m.animate.shift(d).set_opacity(0) for m in self.mobjects],
            run_time=rt, rate_func=smooth,
        )

    # ================================================================ #
    # 第 0 页 · Manim 片头
    # ================================================================ #
    def slide0(self):
        self.camera.background_color = ManimColor("#000000")
        BUFF = 0.6
        SCALE = 0.4
        banner = ManimBanner()
        bannercopy = banner.copy().scale(SCALE)
        self.play(banner.create())
        text = (MathTex(r"\text{Made with}")
                .scale_to_fit_height(bannercopy.M.height)
                .next_to(bannercopy.M, LEFT, buff=BUFF)
                .align_to(bannercopy.M, UP)
                .set_z_index(-1)
                )
        textcopy = text.copy()
        VGroup(textcopy, bannercopy).move_to(ORIGIN)
        self.play(
            FadeIn(text.move_to(textcopy.get_center()), shift=LEFT),
            banner.animate.move_to(bannercopy.get_center()).scale(SCALE)
        )
        text.add_updater(lambda t: t
            .next_to(banner.M, LEFT, buff=BUFF)
            .scale_to_fit_height(banner.M.height)
            .align_to(banner.M, UP)
        )
        self.add(banner, text)
        self.play(banner.expand())
        self.wait(0.5)
        text.clear_updaters()
        self.next_slide()

    # ================================================================ #
    # 第 1 页 · 封面
    # ================================================================ #
    def slide1(self):
        self.play(FadeOut(*self.mobjects))
        bg = ImageMobject(os.path.join(MEDIA, "image1_0.png"))
        bg.set_width(14.222)
        bg.move_to(ORIGIN)
        bg.set_z_index(0)
        self.play(FadeIn(bg))
        self.camera.background_color = ManimColor(BG_CREAM)

        # 顶部小标签
        top_label = mk_text(2.26, 1.41, 14.11, 0.85,
                            "时政演讲 · 道德与法治", 13, RED, FONT_SANS, bold=True)
        self.play(Write(top_label))

        # 主标题两行
        t1 = mk_text(3.03, 4.94, 19.76, 2.8, "向\u201c新\u201d而行，", 50, INK, FONT_SERIF, bold=True)
        t2 = mk_text(3.03, 7.5, 19.76, 2.8, "以\u201c创\u201d致远", 50, INK, FONT_SERIF, bold=True)

        # 红色竖条：先画线（两端延长一点），再写文字
        bar_cx = ul_point(2.26, 4.94)[0]
        base_bar = Line(
            [bar_cx, t1.get_top()[1], 0],
            [bar_cx, t2.get_bottom()[1], 0],
            color=RED, stroke_width=8,
        )
        title_bar = ExtendedLine(base_bar, extend_distance=0.3)
        title_bar.set_z_index(1)
        self.play(GrowFromEdge(title_bar, UP))
        self.play(Write(t1))
        self.play(Write(t2))

        # 副标题
        sub = mk_text(3.03, 10.94, 21.87, 1.06,
                      "——从《关于发展新质生产力的意见》看\u201c创新驱动发展\u201d",
                      17, INK, FONT_SANS)
        self.play(FadeIn(sub, shift=UP * 0.2))

        # 底部两行
        info1 = mk_text(2.26, 16.3, 21.87, 0.8,
                        "教材链接：人教版《道德与法治》九年级上册 第二课《创新驱动发展》",
                        13, BODY, FONT_SANS)
        info2 = mk_text(2.26, 17.1, 21.87, 0.8,
                        "演讲人：朱崇璟、戴语骏    ｜    班级：八（2）班",
                        13, BODY, FONT_SANS)
        self.play(LaggedStart(FadeIn(info1, shift=UP * 0.15),
                              FadeIn(info2, shift=UP * 0.15),
                              lag_ratio=0.4))

        self.wait(1)
        self.next_slide()

    # ================================================================ #
    # 通用页头：kicker(Write) + 大标题(Write) + 红线(Create)
    # ================================================================ #
    def chrome(self, kicker_text, title_text, source_text, page_no):
        k = mk_text(2.26, 1.41, 15, 0.71, kicker_text, 13, RED, FONT_SANS, bold=True)
        t = mk_text(2.26, 2.19, 29, 1.41, title_text, 28, INK, FONT_SERIF, bold=True)
        ln = mk_hline(2.26, 3.95, 29.35)
        s = mk_text(2.26, 17.92, 24.69, 0.64, source_text, 11, GRAY, FONT_SANS)
        pn = mk_text(30.2, 17.92, 1.41, 0.64, page_no, 11, GRAY, FONT_SANS)
        return k, t, ln, s, pn

    def play_chrome(self, kicker_text, title_text, source_text, page_no):
        k, t, ln, s, pn = self.chrome(kicker_text, title_text, source_text, page_no)
        self.play(Write(k))
        self.play(Write(t))
        self.play(Write(ln), FadeIn(s), FadeIn(pn))
        return k, t, ln, s, pn

    # ================================================================ #
    # 第 2 页 · 时政速览
    # ================================================================ #
    def slide2(self):
        self._transition(target="up")  # 封面向上飞出
        self.camera.background_color = ManimColor(BG_CREAM)
        self.play_chrome("报道 · 01  时政速览",
                         "中共中央、国务院发布《关于发展新质生产力的意见》",
                         "来源：央视新闻《早啊！新闻来了》（2026-10-10），经新华社通稿报道",
                         "02 / 08")

        # 时间
        lbl1 = mk_text(2.26, 4.5, 4.23, 0.71, "时　间", 13, GRAY, FONT_SANS)
        val1 = mk_text(2.26, 5.2, 11.29, 0.92, "2026 年 10 月 9 日", 18, INK, FONT_SANS, bold=True)
        self.play(FadeIn(lbl1, shift=RIGHT * 0.2), Write(val1))

        # 发布主体 + 竖线
        lbl2 = mk_text(2.26, 7.5, 4.23, 0.71, "发布主体", 13, GRAY, FONT_SANS)
        val2 = mk_text(2.26, 8.2, 11.29, 0.92, "中共中央、国务院", 18, INK, FONT_SANS, bold=True)
        vd = mk_vline(18.34, 4.5, 7.2)
        self.play(FadeIn(lbl2, shift=RIGHT * 0.2), Write(val2), Write(vd))

        # 文件名称
        lbl3 = mk_text(2.26, 10.5, 4.23, 0.71, "文件名称", 13, GRAY, FONT_SANS)
        val3 = mk_text(2.26, 11.2, 14.82, 0.92, "《关于发展新质生产力的意见》", 18, INK, FONT_SANS, bold=True)
        self.play(FadeIn(lbl3, shift=RIGHT * 0.2), Write(val3))

        # 数字 5（相对竖线垂直居中）
        n5 = mk_text(19.76, 6.83, 4.94, 2.54, "5 个", 60, RED, FONT_SERIF, bold=True)
        c5 = mk_text(19.76, 9.5, 5.64, 1.41, "方面部署\n（科技创新摆在首位）", 14, GRAY, FONT_SANS)
        self.play(GrowFromCenter(n5), FadeIn(c5, shift=UP * 0.2))
        self.play(Circumscribe(n5, color=RED, time_width=0.5))

        # 数字 19
        n19 = mk_text(26.11, 6.83, 5.64, 2.54, "19 项", 60, RED, FONT_SERIF, bold=True)
        c19 = mk_text(26.11, 9.5, 5.64, 1.41, "重点举措", 14, GRAY, FONT_SANS)
        self.play(GrowFromCenter(n19), FadeIn(c19, shift=UP * 0.2))
        self.play(Circumscribe(n19, color=RED, time_width=0.5))

        # 引语条
        band = mk_rect(0, 13.0, 33.87, 2.4, BAND)
        qm = mk_text(2.26, 13.2, 2.12, 2.12, "\u201c", 52, RED, FONT_SERIF, bold=True)
        qt = mk_text(4.23, 13.4, 27.38, 2.0,
                     "围绕科技创新、产业创新、发展方式创新、体制机制创新、\n人才工作机制创新五方面，提出 19 项重点举措。",
                     18, INK, FONT_SERIF)
        self.play(GrowFromEdge(band, LEFT), FadeIn(qm), Write(qt))

        # why 一行（紧贴引语条下方，整体再往下移一点）
        why = mk_text(2.26, 16.1, 29.35, 0.85,
                      "为什么选这条新闻？——它正对应教材的核心考点：创新驱动发展。接下来按\u201c报道 → 教材 → 点评\u201d展开。",
                      14, GRAY, FONT_SANS, slant=ITALIC)
        self.play(FadeIn(why, shift=UP * 0.2))

        self.wait(1)
        self.next_slide()

    # ================================================================ #
    # 第 3 页 · 五方面要点
    # ================================================================ #
    def slide3(self):
        self._transition(target="left")  # 向左飞出
        self.camera.background_color = ManimColor(BG_CREAM)
        self.play_chrome("报道 · 01  要点梳理",
                         "《意见》部署五方面创新，科技创新居首",
                         "来源：央视新闻《早啊！新闻来了》（2026-10-10）",
                         "03 / 08")

        rows = [
            ("01", "科技创新",     "核心引擎——以科技突破引领产业变革",        4.60),
            ("02", "产业创新",     "主战场——让科技成果转化为现实生产力",      6.60),
            ("03", "发展方式创新", "方向标——推动发展向绿色化、智能化转型",     8.60),
            ("04", "体制机制创新", "制度保障——让各类创新活力充分涌流",       10.60),
            ("05", "人才工作机制创新", "第一资源——培养造就大批创新型人才",    12.60),
        ]
        for i, (num, name, desc, top) in enumerate(rows):
            row_h = 2.0
            row_mid = top + row_h / 2
            nm = mk_text(4.23, row_mid - 0.45, 6.7, 0.92, name, 18, INK, FONT_SANS, bold=True)
            n = mk_text(2.26, row_mid - 0.5, 1.55, 1.06, num, 22, RED, FONT_SERIF, bold=True)
            d = mk_text(11.64, row_mid - 0.4, 19.97, 0.85, desc, 15, BODY, FONT_SANS)
            # 三项整体垂直居中于上下两条线之间（不偏上、不偏下）
            row_mid_y = (PPT_H / 2 - row_mid) * SCALE
            nm.move_to([nm.get_center()[0], row_mid_y, 0])
            n.move_to([n.get_center()[0], nm.get_center()[1], 0])
            d.move_to([d.get_center()[0], nm.get_center()[1], 0])
            # 每项被上下两条线夹住：第一行画上线，每行画下线（相邻行共用中线）
            acts = [GrowFromCenter(n), Write(nm), FadeIn(d, shift=RIGHT * 0.2)]
            if i == 0:
                acts.append(Write(mk_hline(2.26, top, 29.35, color=LINE_GRAY, stroke=1)))
            acts.append(Write(mk_hline(2.26, top + row_h, 29.35, color=LINE_GRAY, stroke=1)))
            self.play(*acts)

        note = mk_text(2.26, 14.9, 29.35, 1.41,
                       "注：左列为《意见》部署的五个方面（据新华社报道）；右列为演讲者结合教材知识所作的要点解读，帮助理解记忆。",
                       13, GRAY, FONT_SANS)
        self.play(FadeIn(note))

        hook = mk_text(2.26, 16.5, 29.35, 0.92,
                       "记忆钩子：\u201c科技打头、产业落地、方式转型、机制护航、人才支撑\u201d。",
                       15, INK, FONT_SANS)
        self.play(Write(hook))
        self.play(Indicate(hook, color=RED))

        self.wait(1)
        self.next_slide()

    # ================================================================ #
    # 第 4 页 · 关联新闻
    # ================================================================ #
    def slide4(self):
        self._transition(target="right")  # 向右飞出
        self.camera.background_color = ManimColor(BG_CREAM)
        self.play_chrome("报道 · 02  关联新闻",
                         "一周内，40 项关键技术出口管制公开征求意见",
                         "来源：财新网（2026-10-16），《中国禁止出口限制出口技术目录》修订征求意见稿",
                         "04 / 08")

        lead_l = mk_text(2.26, 4.59, 17.64, 0.92, "新闻事实", 16, INK, FONT_SANS, bold=True)
        p1 = mk_text(2.26, 5.80, 17.64, 2.05,
                     "10 月 16 日，商务部、科技部发布 2026 年第 48 号公告，\n就修订《中国禁止出口限制出口技术目录》公开征求意见。",
                     15, BODY, FONT_SANS)
        self.play(Write(lead_l), Write(p1))

        p2 = mk_text(2.26, 7.85, 17.64, 2.05,
                     "拟增列人工智能、生物医药、光伏三个领域\n共 40 项关键技术。",
                     15, BODY, FONT_SANS)
        self.play(Write(p2))

        p3 = mk_text(2.26, 9.90, 17.64, 2.05,
                     "其中拟禁止出口 14 项，拟限制出口 26 项。",
                     15, BODY, FONT_SANS)
        self.play(Write(p3))

        p4 = mk_text(2.26, 11.95, 17.64, 2.05,
                     "商务部发言人：这是技术贸易管理的常态化工作，\n依法依规，不针对任何特定国家、地区或实体。",
                     15, BODY, FONT_SANS)
        vd = mk_vline(21.17, 4.59, 10.58)
        self.play(Write(p4), Write(vd))

        lead_r = mk_text(22.3, 4.59, 9.31, 0.92, "这条新闻释放什么信号？", 16, RED, FONT_SANS, bold=True)
        self.play(Write(lead_r))

        for txt, top in [
            ("· 科技实力已成为国际竞争的核心，\n各主要经济体都在加强关键技术管控。", 5.80),
            ("· 关键技术关系国家安全与发展利益，\n必须掌握在自己手里。", 8.20),
            ("· 管制不等于封闭：我国仍坚持扩大开放，\n推动国际科技合作。", 10.60),
        ]:
            rb = mk_text(22.3, top, 9.31, 2.3, txt, 14, BODY, FONT_SANS)
            self.play(FadeIn(rb, shift=LEFT * 0.3))

        bottom = mk_rect(2.26, 15.95, 29.35, 0.92, BAND)
        btxt = mk_text(2.26, 15.95, 29.35, 0.92,
                       "两条新闻合看：一端是\u201c促创新\u201d的顶层部署，一端是\u201c护安全\u201d的制度安排——发展与安全一体两面。",
                       15, INK, FONT_SANS, bold=True)
        self.play(GrowFromEdge(bottom, UP), Write(btxt))

        self.wait(1)
        self.next_slide()

    # ================================================================ #
    # 第 5 页 · 教材四观点
    # ================================================================ #
    def slide5(self):
        self._transition(target="diag_bl")  # 飞向左下角
        self.camera.background_color = ManimColor(BG_CREAM)
        k, t, ln, s, pn = self.play_chrome("教材 · 知识回顾",
                         "九上第二课《创新驱动发展》的四个核心观点",
                         "教材：人民教育出版社《道德与法治》九年级上册",
                         "05 / 08")
        tag = mk_text(2.26, 4.45, 29.35, 0.71,
                      "人教版《道德与法治》九年级上册 · 第一单元\u201c富强与创新\u201d",
                      13, GRAY, FONT_SANS)
        self.play(FadeIn(tag, shift=RIGHT * 0.2))

        rows = [
            ("01", "创新是引领发展的第一动力。",
             "创新是一个民族进步的灵魂，是国家兴旺发达的不竭源泉，也是中华民族最鲜明的民族禀赋。",
             5.70),
            ("02", "创新驱动是国家命运所系。",
             "我国实施创新驱动发展战略，推进以科技创新为核心的全面创新。",
             8.15),
            ("03", "建设世界科技创新强国，要增强自主创新能力。",
             "坚持自主创新、重点跨越、支撑发展、引领未来的方针，走中国特色自主创新道路。",
             10.60),
            ("04", "企业是社会创新的重要力量。",
             "提升创新能力是企业持续发展之基、市场制胜之道；核心技术不是别人赐予的，必须自强奋斗。",
             13.05),
        ]
        for i, (num, lead, body, top) in enumerate(rows):
            row_h = 2.45
            row_mid = top + row_h / 2
            # 内容(head单行 + bd单行，总高约1.35cm)整体垂直居中于上下两条线之间
            head_top = row_mid - 0.481
            n = mk_text(2.26, row_mid - 0.686, 1.55, 1.06, num, 22, RED, FONT_SERIF, bold=True)
            head = mk_text(4.23, head_top, 27.38, 0.8, lead, 15, INK, FONT_SANS, bold=True)
            bd = mk_text(4.23, head_top + 0.70, 27.38, 1.3, body, 15, BODY, FONT_SANS)
            # 每项被上下两条线夹住：第一行画上线，每行画下线
            acts = [GrowFromCenter(n), Write(head), FadeIn(bd, shift=RIGHT * 0.2)]
            if i == 0:
                acts.append(Write(mk_hline(2.26, top, 29.35, color=LINE_GRAY, stroke=1)))
            acts.append(Write(mk_hline(2.26, top + row_h, 29.35, color=LINE_GRAY, stroke=1)))
            self.play(*acts)

        note = mk_text(2.26, 16.90, 29.35, 0.71,
                       "以上表述综合自人教版《道德与法治》九年级上册第二课《创新驱动发展》。",
                       13, GRAY, FONT_SANS)
        self.play(FadeIn(note))

        self.wait(1)
        self.next_slide()

    # ================================================================ #
    # 第 6 页 · 考点对照表
    # ================================================================ #
    def slide6(self):
        self._transition(target="down")  # 向下飞出
        self.camera.background_color = ManimColor(BG_CREAM)
        self.play_chrome("教材 · 考点对照",
                         "一条新闻里的四个考点：新闻事实 ↔ 教材观点",
                         "来源：综合央视新闻（2026-10-10）、财新网（2026-10-16）及人教版教材",
                         "06 / 08")

        col1_w = 13.0
        row_h = 2.33
        hdr_top = 4.59

        # 表头
        hdr_bg1 = mk_rect(2.26, hdr_top, col1_w, row_h, TABLE_HEAD)
        hdr_bg2 = mk_rect(2.26 + col1_w, hdr_top, 29.35 - col1_w, row_h, TABLE_HEAD)
        hdr_t1 = mk_text(2.26 + 0.3, hdr_top + 0.5, col1_w - 0.6, row_h, "新闻中的事实", 17, WHITE, FONT_SANS, bold=True)
        hdr_t2 = mk_text(2.26 + col1_w + 0.3, hdr_top + 0.5, 29.35 - col1_w - 0.6, row_h, "教材中的观点（九年级上册）", 17, WHITE, FONT_SANS, bold=True)
        # 表头文字垂直居中于表头格内
        hdr_mid_y = (PPT_H / 2 - (hdr_top + row_h / 2)) * SCALE
        hdr_t1.move_to([hdr_t1.get_center()[0], hdr_mid_y, 0])
        hdr_t2.move_to([hdr_t2.get_center()[0], hdr_mid_y, 0])
        self.play(
            LaggedStart(
                Write(hdr_bg1), Write(hdr_bg2),
                Write(hdr_t1), Write(hdr_t2),
                lag_ratio=0.2,
            ),
        )

        rows = [
            ("《意见》把科技创新摆在五方面首位，\n部署 19 项举措",
             "创新是引领发展的第一动力；实施创新驱动发展战略，\n推进以科技创新为核心的全面创新"),
            ("《意见》专门部署人才工作机制创新",
             "落实科教兴国战略、人才强国战略；\n培养创新型人才，建设创新型国家"),
            ("拟对人工智能、生物医药、光伏等\n40 项关键技术实施出口管制",
             "增强自主创新能力；大国重器一定要掌握在自己手里，\n核心技术不是别人赐予的"),
            ("新质生产力覆盖光伏、生物医药等\n新兴产业",
             "转变发展方式、优化经济结构、转换增长动力，\n推动经济高质量发展"),
        ]
        for i, (fact, view) in enumerate(rows):
            top = hdr_top + row_h * (i + 1)
            bg1 = mk_rect(2.26, top, col1_w, row_h, WHITE, opacity=0.5, stroke_width=1, stroke_color=LINE_GRAY)
            bg2 = mk_rect(2.26 + col1_w, top, 29.35 - col1_w, row_h, WHITE, opacity=0.5, stroke_width=1, stroke_color=LINE_GRAY)
            t1 = mk_text(2.26 + 0.3, top + 0.4, col1_w - 0.6, row_h, fact, 15, BODY, FONT_SANS)
            t2 = mk_text(2.26 + col1_w + 0.3, top + 0.4, 29.35 - col1_w - 0.6, row_h, view, 15, BODY, FONT_SANS)
            # 文字垂直居中于格内（上下边框线之间）
            cell_mid_y = (PPT_H / 2 - (top + row_h / 2)) * SCALE
            t1.move_to([t1.get_center()[0], cell_mid_y, 0])
            t2.move_to([t2.get_center()[0], cell_mid_y, 0])
            self.play(
                Write(bg1), Write(bg2),
                Write(t1), Write(t2),
            )

        note = mk_text(2.26, 16.72, 29.35, 0.71,
                       "用法提示：先找新闻里的\u201c事实\u201d，再对教材里的\u201c观点\u201d——一分事实配一分观点，踩点得分。",
                       13, GRAY, FONT_SANS, slant=ITALIC)
        self.play(FadeIn(note))

        self.wait(1)
        self.next_slide()

    # ================================================================ #
    # 第 7 页 · 时政点评
    # ================================================================ #
    def slide7(self):
        self._transition(target="diag_tl")  # 飞向左上角
        self.camera.background_color = ManimColor(BG_CREAM)
        self.play_chrome("点评 · 怎么看",
                         "三重逻辑读懂这份《意见》：发展、竞争与安全",
                         "",
                         "07 / 08")

        rows = [
            ("①", "发展的选择：",
             "我国经济已由高速增长阶段转向高质量发展阶段，传统要素驱动难以为继，\n必须以创新催生新产业、新模式、新动能。",
             "教材链接：创新是引领发展的第一动力，创新驱动是国家命运所系。",
             4.60),
            ("②", "竞争的应对：",
             "新一轮科技革命加速突破，关键核心技术买不来、讨不来。\n只有把大国重器掌握在自己手里，才能赢得发展主动权。",
             "教材链接：建设世界科技创新强国，要增强自主创新能力，走中国特色自主创新道路。",
             8.10),
            ("③", "安全的统筹：",
             "对先进技术依法依规实施出口管制，与扩大高水平对外开放并行不悖，\n体现统筹发展和安全，守住国家利益底线。",
             "教材链接：坚持国家利益至上，维护国家安全，人人有责。",
             11.60),
        ]
        for i, (num, head, body, link, top) in enumerate(rows):
            row_h = 3.50
            row_mid = top + row_h / 2
            # 内容(hd单行 + bd两行 + lk单行，总高约2.63cm)整体垂直居中于上下两条线之间
            hd_top = row_mid - 1.130
            n = mk_text(2.26, hd_top - 0.31, 1.83, 1.27, num, 26, RED, FONT_SERIF, bold=True)
            hd = mk_text(4.45, hd_top, 27.16, 0.8, head, 15, INK, FONT_SANS, bold=True)
            bd = mk_text(4.45, hd_top + 0.75, 27.16, 1.5, body, 15, BODY, FONT_SANS)
            lk = mk_text(4.45, hd_top + 2.20, 27.16, 0.7, link, 13, RED, FONT_SANS, slant=ITALIC)
            # 每项被上下两条线夹住：第一行画上线，每行画下线
            acts = [GrowFromCenter(n), Write(hd), FadeIn(bd, shift=RIGHT * 0.2), FadeIn(lk)]
            if i == 0:
                acts.append(Write(mk_hline(2.26, top, 29.35, color=LINE_GRAY, stroke=1)))
            acts.append(Write(mk_hline(2.26, top + row_h, 29.35, color=LINE_GRAY, stroke=1)))
            self.play(*acts)

        # 底部米色条
        strip = mk_rect(0, 16.93, 33.87, 2.12, BAND)
        stxt = mk_text(2.26, 17.4, 29.35, 1.2,
                       "一句话点评：以创新破局、以制度护航，新质生产力正成为中国式现代化最鲜明的\u201c新引擎\u201d。",
                       16, INK, FONT_SERIF, bold=True)
        self.play(GrowFromEdge(strip, UP), Write(stxt))

        self.wait(1)
        self.next_slide()

    # ================================================================ #
    # 第 8 页 · 行动倡议 + 结束语
    # ================================================================ #
    def slide8(self):
        self._transition(target="diag_tr")  # 飞向右上角
        self.camera.background_color = ManimColor(BG_CREAM)
        self.play_chrome("点评 · 我们怎么做",
                         "强国建设，少年何为？四个行动现在做起",
                         "",
                         "08 / 08")

        actions = [
            ("勤学习", "学好科学文化知识，打牢创新的知识根基", 4.60),
            ("敢质疑", "不迷信权威、不盲从答案，培养批判性思维", 7.40),
            ("重实践", "参加科技小发明、小制作和研究性学习活动", 10.20),
            ("立大志", "把个人理想融入科技强国、民族复兴的伟大征程", 13.00),
        ]
        for title, desc, top in actions:
            icon = mk_rect(2.26, top + 0.21, 0.78, 0.78, RED)
            t = mk_text(3.6, top, 13.76, 0.8, title, 15, INK, FONT_SANS, bold=True)
            d = mk_text(3.6, top + 0.75, 13.76, 1.2, desc, 14, BODY, FONT_SANS)
            self.play(
                GrowFromCenter(icon),
                Write(t),
                FadeIn(d, shift=RIGHT * 0.2),
            )

        # 右栏
        vd = mk_vline(19.05, 4.94, 10.23)
        panel = mk_rect(20.46, 4.94, 11.15, 10.23, BAND)
        qm = mk_text(21.31, 5.57, 1.76, 1.62, "\u201c", 40, RED, FONT_SERIF, bold=True)
        quote = mk_text(21.31, 7.34, 9.45, 4.59,
                        "惟创新者进，\n惟创新者强，\n惟创新者胜。",
                        28, INK, FONT_SERIF, bold=True)
        self.play(
            Write(vd),
            GrowFromEdge(panel, RIGHT),
            FadeIn(qm),
            Write(quote),
        )

        self.wait(1)
        self.next_slide()

    # ================================================================ #
    # 第 9 页 · 结束页（同封面背景图）
    # ================================================================ #
    def slide9(self):
        self._transition(target="diag_br")  # 飞向右下角
        self.camera.background_color = ManimColor(BG_CREAM)
        bg = ImageMobject(os.path.join(MEDIA, "image1_0.png"))
        bg.set_width(14.222)
        bg.move_to(ORIGIN)
        bg.set_z_index(0)
        self.play(FadeIn(bg))

        title = mk_text(3.03, 4.94, 19.76, 2.8, "谢谢大家！", 50, INK, FONT_SERIF, bold=True)
        self.play(Write(title))

        info = mk_text(2.26, 16.3, 21.87, 0.8,
                       "演讲人：朱崇璟、戴语骏    ｜    班级：八（2）班",
                       13, BODY, FONT_SANS)
        self.play(FadeIn(info, shift=UP * 0.2))

