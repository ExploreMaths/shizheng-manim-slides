# -*- coding: utf-8 -*-
"""
时政演讲 Manim Slides —— 逐元素像素级复刻版
==========================================
每个文字 / 形状 / 图片都按原 PPT 坐标（cm）映射到 Manim 坐标系，
字体用 PPT 原字体（MiSans / Noto Serif SC），颜色用原 HEX 值。

坐标映射：
  PPT 页面 33.87cm × 19.05cm（16:9）
  Manim 帧 14.222 × 8 units
  scale = 14.222 / 33.87 ≈ 0.420
  mx = (center_x_cm - 16.935) * scale
  my = (9.525 - center_y_cm) * scale

依赖：
  pip install manim manim-slides
运行：
  manim -pqh shizheng_slides_pixel.py ShizhengSlides
  manim-slides present shizheng_slides_pixel.py ShizhengSlides
"""

import os
from manim import *
from manim import ManimColor
from manim_slides import Slide

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
MEDIA  = os.path.join(ASSETS, "media")

# 配色（从 PPT 直接提取）
BG_CREAM   = "#F8F4ED"   # 页面底色（s2-s8）
RED        = "#C03A2B"   # 主题红
INK        = "#211D18"   # 主标题/深字
BODY       = "#4A4239"   # 正文
GRAY       = "#7A7166"   # 次要灰
BAND       = "#F1E9DC"   # 米色块
LINE_GRAY  = "#D9CFC0"   # 分隔线
LINK_BLUE  = "#0563C1"   # 超链接蓝
TABLE_HEAD = "#2B2420"   # 表头深棕黑

FONT_SANS  = "MiSans"
FONT_SERIF = "Noto Serif SC"

# 坐标换算
SCALE = 14.222 / 33.87
PPT_W = 33.87
PPT_H = 19.05

def P(left_cm, top_cm, w_cm, h_cm):
    """给定 PPT 形状左上角和宽高（cm），返回 (center_x, center_y, width, height) 的 Manim 坐标。"""
    cx = left_cm + w_cm / 2
    cy = top_cm + h_cm / 2
    mx = (cx - PPT_W / 2) * SCALE
    my = (PPT_H / 2 - cy) * SCALE
    return mx, my, w_cm * SCALE, h_cm * SCALE


def mk_text(left, top, w, h, text, size, color=INK, font=FONT_SANS, bold=False, slant=NORMAL):
    """按 PPT 坐标创建一段 Text。"""
    mx, my, _, _ = P(left, top, w, h)
    t = Text(
        text,
        font=font,
        font_size=size,
        color=color,
        weight=BOLD if bold else NORMAL,
        slant=slant,
        line_spacing=0.5,
    )
    t.move_to([mx, my, 0])
    return t


def mk_rect(left, top, w, h, fill_color, opacity=1.0, stroke_width=0):
    """按 PPT 坐标创建矩形。"""
    mx, my, mw, mh = P(left, top, w, h)
    r = Rectangle(
        width=mw, height=mh,
        fill_color=fill_color, fill_opacity=opacity,
        stroke_width=stroke_width,
    )
    r.move_to([mx, my, 0])
    return r


def mk_hline(left, top, w, color=LINE_GRAY, stroke=1.5):
    """按 PPT 坐标创建水平细线（高 0.04cm）。"""
    mx, my, mw, _ = P(left, top, w, 0.04)
    ln = Line([-mw/2, 0, 0], [mw/2, 0, 0], color=color, stroke_width=stroke)
    ln.move_to([mx, my, 0])
    return ln


def mk_vline(left, top, h, color=LINE_GRAY, stroke=1.5):
    """按 PPT 坐标创建竖直细线（宽 0.04cm）。"""
    mx, my, _, mh = P(left, top, 0.04, h)
    ln = Line([0, mh/2, 0], [0, -mh/2, 0], color=color, stroke_width=stroke)
    ln.move_to([mx, my, 0])
    return ln


# ---------------------------------------------------------------------------
# 主场景
# ---------------------------------------------------------------------------
class ShizhengSlides(Slide):

    def construct(self):
        # 封面用背景图，其余页用米色底
        self.slide1()
        self.slide2()
        self.slide3()
        self.slide4()
        self.slide5()
        self.slide6()
        self.slide7()
        self.slide8()

    # ================================================================ #
    # 第 1 页 · 封面（背景图 image1_0.png）
    # ================================================================ #
    def slide1(self):
        # 背景图铺满
        bg = ImageMobject(os.path.join(MEDIA, "image1_0.png"))
        bg.set_width(14.222)
        bg.move_to(ORIGIN)
        self.add(bg)

        # 1.0 顶部小标签 + 红色竖条
        top_label = mk_text(2.26, 1.41, 14.11, 0.85,
                            "时政演讲 · 道德与法治", 12, RED, FONT_SANS, bold=True)
        title_bar = mk_rect(2.26, 5.29, 0.21, 4.66, RED)
        self.play(FadeIn(top_label), GrowFromEdge(title_bar, UP), run_time=0.5)
        self.next_slide()

        # 1.1 主标题（两行，Noto Serif SC 48pt）
        title = VGroup(
            mk_text(3.03, 4.94, 19.76, 2.8, "向\u201c新\u201d而行，", 48, INK, FONT_SERIF, bold=True),
            mk_text(3.03, 7.5, 19.76, 2.8, "以\u201c创\u201d致远", 48, INK, FONT_SERIF, bold=True),
        )
        # 第二行稍微调整 y
        title[1].shift(DOWN * 1.15)
        self.play(FadeIn(title, shift=RIGHT * 0.3), run_time=0.7)
        self.next_slide()

        # 1.2 副标题
        sub = mk_text(3.03, 10.94, 21.87, 1.06,
                      "——从《关于发展新质生产力的意见》看\u201c创新驱动发展\u201d",
                      16, INK, FONT_SANS)
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.next_slide()

        # 1.3 底部信息
        info = VGroup(
            mk_text(2.26, 16.3, 21.87, 0.8,
                    "教材链接：人教版《道德与法治》九年级上册 第二课《创新驱动发展》",
                    12, BODY, FONT_SANS),
            mk_text(2.26, 17.1, 21.87, 0.8,
                    "演讲人：×××    ｜    班级：×××",
                    12, BODY, FONT_SANS),
        )
        info[1].shift(DOWN * 0.55)
        self.play(FadeIn(info, shift=UP * 0.2), run_time=0.5)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ================================================================ #
    # 通用页头 / 页脚
    # ================================================================ #
    def chrome(self, kicker_text, title_text, source_text, page_no):
        """返回 (VGroup)，包含 kicker + 大标题 + 分隔线 + 来源 + 页码。"""
        g = VGroup(
            mk_text(2.26, 1.41, 15, 0.71, kicker_text, 12, RED, FONT_SANS, bold=True),
            mk_text(2.26, 2.19, 29, 1.41, title_text, 27, INK, FONT_SERIF, bold=True),
            mk_hline(2.26, 3.95, 29.35, color=RED, stroke=2),
            mk_text(2.26, 17.92, 24.69, 0.64, source_text, 10, GRAY, FONT_SANS),
            mk_text(30.2, 17.92, 1.41, 0.64, page_no, 10, GRAY, FONT_SANS),
        )
        return g

    # ================================================================ #
    # 第 2 页 · 时政速览
    # ================================================================ #
    def slide2(self):
        self.camera.background_color = ManimColor(BG_CREAM)
        ch = self.chrome("报道 · 01  时政速览",
                         "中共中央、国务院发布《关于发展新质生产力的意见》",
                         "来源：央视新闻《早啊！新闻来了》（2026-10-10），经新华社通稿报道",
                         "02 / 08")
        self.play(FadeIn(ch), run_time=0.5)
        self.next_slide()

        # 时间
        lbl1 = mk_text(2.26, 4.8, 4.23, 0.71, "时　间", 12, GRAY, FONT_SANS)
        val1 = mk_text(2.26, 5.5, 11.29, 0.92, "2026 年 10 月 9 日", 17, INK, FONT_SANS, bold=True)
        self.play(FadeIn(VGroup(lbl1, val1), shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 发布主体 + 竖线
        lbl2 = mk_text(2.26, 7.06, 4.23, 0.71, "发布主体", 12, GRAY, FONT_SANS)
        val2 = mk_text(2.26, 7.76, 11.29, 0.92, "中共中央、国务院", 17, INK, FONT_SANS, bold=True)
        vd = mk_vline(18.34, 4.8, 6.0)
        self.play(FadeIn(VGroup(lbl2, val2), shift=RIGHT * 0.2), Create(vd), run_time=0.4)
        self.next_slide()

        # 文件名称
        lbl3 = mk_text(2.26, 9.31, 4.23, 0.71, "文件名称", 12, GRAY, FONT_SANS)
        val3 = mk_text(2.26, 10.02, 14.82, 0.92, "《关于发展新质生产力的意见》", 17, INK, FONT_SANS, bold=True)
        self.play(FadeIn(VGroup(lbl3, val3), shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 5 个
        n5 = mk_text(19.76, 4.59, 4.94, 2.54, "5 个", 56, RED, FONT_SERIF, bold=True)
        c5 = mk_text(19.76, 7.27, 5.64, 1.41, "方面部署\n（科技创新摆在首位）", 13, GRAY, FONT_SANS)
        self.play(GrowFromCenter(n5), FadeIn(c5, shift=UP * 0.15), run_time=0.6)
        self.next_slide()

        # 19 项
        n19 = mk_text(26.11, 4.59, 5.64, 2.54, "19 项", 56, RED, FONT_SERIF, bold=True)
        c19 = mk_text(26.11, 7.27, 5.64, 1.41, "重点举措", 13, GRAY, FONT_SANS)
        self.play(GrowFromCenter(n19), FadeIn(c19, shift=UP * 0.15), run_time=0.6)
        self.next_slide()

        # 引语条
        band = mk_rect(0, 11.85, 33.87, 3.88, BAND)
        qm = mk_text(2.26, 12.28, 2.12, 2.12, "\u201c", 52, RED, FONT_SERIF, bold=True)
        qt = mk_text(4.23, 12.49, 27.38, 2.75,
                     "围绕科技创新、产业创新、发展方式创新、体制机制创新、\n人才工作机制创新五方面，提出 19 项重点举措。",
                     17, INK, FONT_SERIF)
        self.play(FadeIn(band, shift=UP * 0.3), FadeIn(qm), FadeIn(qt), run_time=0.6)
        self.next_slide()

        # why 一行
        why = mk_text(2.26, 16.44, 29.35, 0.85,
                      "为什么选这条新闻？——它正对应教材的核心考点：创新驱动发展。接下来按\u201c报道 → 教材 → 点评\u201d展开。",
                      13, GRAY, FONT_SANS, slant=ITALIC)
        self.play(FadeIn(why, shift=UP * 0.2), run_time=0.5)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ================================================================ #
    # 第 3 页 · 五方面要点
    # ================================================================ #
    def slide3(self):
        self.camera.background_color = ManimColor(BG_CREAM)
        ch = self.chrome("报道 · 01  要点梳理",
                         "《意见》部署五方面创新，科技创新居首",
                         "来源：央视新闻《早啊！新闻来了》（2026-10-10）",
                         "03 / 08")
        self.play(FadeIn(ch), run_time=0.5)
        self.next_slide()

        rows = [
            ("01", "科技创新",     "核心引擎——以科技突破引领产业变革",        4.66),
            ("02", "产业创新",     "主战场——让科技成果转化为现实生产力",      6.42),
            ("03", "发展方式创新", "方向标——推动发展向绿色化、智能化转型",     8.18),
            ("04", "体制机制创新", "制度保障——让各类创新活力充分涌流",        9.95),
            ("05", "人才工作机制创新", "第一资源——培养造就大批创新型人才",    11.71),
        ]
        for num, name, desc, top in rows:
            n = mk_text(2.26, top, 1.55, 1.06, num, 20, RED, FONT_SERIF, bold=True)
            nm = mk_text(4.23, top + 0.07, 6.7, 0.92, name, 17, INK, FONT_SANS, bold=True)
            d = mk_text(11.64, top + 0.14, 19.97, 0.85, desc, 14, BODY, FONT_SANS)
            ln = mk_hline(2.26, top + 1.41, 29.35)
            self.play(FadeIn(VGroup(n, nm, d, ln), shift=RIGHT * 0.3), run_time=0.4)
            self.next_slide()

        note = mk_text(2.26, 14.11, 29.35, 1.41,
                       "注：左列为《意见》部署的五个方面（据新华社报道）；右列为演讲者结合教材知识所作的要点解读，帮助理解记忆。",
                       12, GRAY, FONT_SANS)
        self.play(FadeIn(note), run_time=0.4)
        self.next_slide()

        hook = mk_text(2.26, 16.09, 29.35, 0.92,
                       "记忆钩子：\u201c科技打头、产业落地、方式转型、机制护航、人才支撑\u201d。",
                       14, INK, FONT_SANS, bold=False)
        self.play(FadeIn(hook, shift=UP * 0.2), run_time=0.5)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ================================================================ #
    # 第 4 页 · 关联新闻（文本框已在 working.pptx 里拆成 left-p1..4 / right-p1..3）
    # ================================================================ #
    def slide4(self):
        self.camera.background_color = ManimColor(BG_CREAM)
        ch = self.chrome("报道 · 02  关联新闻",
                         "一周内，40 项关键技术出口管制公开征求意见",
                         "来源：财新网（2026-10-16），《中国禁止出口限制出口技术目录》修订征求意见稿",
                         "04 / 08")
        self.play(FadeIn(ch), run_time=0.5)
        self.next_slide()

        # 左栏标题 + 第 1 段
        lead_l = mk_text(2.26, 4.59, 17.64, 0.92, "新闻事实", 15, INK, FONT_SANS, bold=True)
        p1 = mk_text(2.26, 5.79, 17.64, 2.05,
                     "10 月 16 日，商务部、科技部发布 2026 年第 48 号公告，\n就修订《中国禁止出口限制出口技术目录》公开征求意见。",
                     14, BODY, FONT_SANS)
        self.play(FadeIn(VGroup(lead_l, p1), shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 第 2 段（40 项）
        p2 = mk_text(2.26, 7.84, 17.64, 2.05,
                     "拟增列人工智能、生物医药、光伏三个领域\n共 40 项关键技术。",
                     14, BODY, FONT_SANS)
        self.play(FadeIn(p2, shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 第 3 段（14/26）
        p3 = mk_text(2.26, 9.89, 17.64, 2.05,
                     "其中拟禁止出口 14 项，拟限制出口 26 项。",
                     14, BODY, FONT_SANS)
        self.play(FadeIn(p3, shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 第 4 段（发言人）+ 竖线
        p4 = mk_text(2.26, 11.94, 17.64, 2.05,
                     "商务部发言人：这是技术贸易管理的常态化工作，\n依法依规，不针对任何特定国家、地区或实体。",
                     14, BODY, FONT_SANS)
        vd = mk_vline(21.17, 4.59, 10.58)
        self.play(FadeIn(p4, shift=RIGHT * 0.2), Create(vd), run_time=0.4)
        self.next_slide()

        # 右栏标题
        lead_r = mk_text(22.3, 4.59, 9.31, 0.92, "这条新闻释放什么信号？", 15, RED, FONT_SANS, bold=True)
        self.play(FadeIn(lead_r, shift=LEFT * 0.2), run_time=0.4)
        self.next_slide()

        # 右栏三条
        r1 = mk_text(22.3, 5.79, 9.31, 2.3,
                     "· 科技实力已成为国际竞争的核心，\n各主要经济体都在加强关键技术管控。",
                     13, BODY, FONT_SANS)
        self.play(FadeIn(r1, shift=LEFT * 0.2), run_time=0.4); self.next_slide()

        r2 = mk_text(22.3, 8.19, 9.31, 2.3,
                     "· 关键技术关系国家安全与发展利益，\n必须掌握在自己手里。",
                     13, BODY, FONT_SANS)
        self.play(FadeIn(r2, shift=LEFT * 0.2), run_time=0.4); self.next_slide()

        r3 = mk_text(22.3, 10.59, 9.31, 2.3,
                     "· 管制不等于封闭：我国仍坚持扩大开放，\n推动国际科技合作。",
                     13, BODY, FONT_SANS)
        self.play(FadeIn(r3, shift=LEFT * 0.2), run_time=0.4); self.next_slide()

        # 底部总结
        bottom = mk_rect(2.26, 15.95, 29.35, 0.92, BAND)
        btxt = mk_text(2.26, 15.95, 29.35, 0.92,
                       "两条新闻合看：一端是\u201c促创新\u201d的顶层部署，一端是\u201c护安全\u201d的制度安排——发展与安全一体两面。",
                       14, INK, FONT_SANS, bold=True)
        self.play(FadeIn(bottom, shift=UP * 0.3), FadeIn(btxt), run_time=0.6)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ================================================================ #
    # 第 5 页 · 教材四观点
    # ================================================================ #
    def slide5(self):
        self.camera.background_color = ManimColor(BG_CREAM)
        ch = self.chrome("教材 · 知识回顾",
                         "九上第二课《创新驱动发展》的四个核心观点",
                         "教材：人民教育出版社《道德与法治》九年级上册",
                         "05 / 08")
        tag = mk_text(2.26, 4.45, 29.35, 0.71,
                      "人教版《道德与法治》九年级上册 · 第一单元\u201c富强与创新\u201d",
                      12, GRAY, FONT_SANS)
        self.play(FadeIn(ch), FadeIn(tag), run_time=0.5)
        self.next_slide()

        rows = [
            ("01", "创新是引领发展的第一动力。",
             "创新是一个民族进步的灵魂，是国家兴旺发达的不竭源泉，也是中华民族最鲜明的民族禀赋。",
             5.71),
            ("02", "创新驱动是国家命运所系。",
             "我国实施创新驱动发展战略，推进以科技创新为核心的全面创新。",
             8.61),
            ("03", "建设世界科技创新强国，要增强自主创新能力。",
             "坚持自主创新、重点跨越、支撑发展、引领未来的方针，走中国特色自主创新道路。",
             11.5),
            ("04", "企业是社会创新的重要力量。",
             "提升创新能力是企业持续发展之基、市场制胜之道；核心技术不是别人赐予的，必须自强奋斗。",
             14.39),
        ]
        for num, lead, body, top in rows:
            n = mk_text(2.26, top + 0.08, 1.55, 1.06, num, 20, RED, FONT_SERIF, bold=True)
            head = mk_text(4.23, top, 27.38, 0.8, lead, 14, INK, FONT_SANS, bold=True)
            bd = mk_text(4.23, top + 0.75, 27.38, 1.3, body, 14, BODY, FONT_SANS)
            ln = mk_hline(2.26, top + 2.47, 29.35)
            self.play(FadeIn(VGroup(n, head, bd, ln), shift=RIGHT * 0.2), run_time=0.45)
            self.next_slide()

        note = mk_text(2.26, 16.93, 29.35, 0.71,
                       "以上表述综合自人教版《道德与法治》九年级上册第二课《创新驱动发展》。",
                       12, GRAY, FONT_SANS)
        self.play(FadeIn(note), run_time=0.4)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ================================================================ #
    # 第 6 页 · 考点对照表
    # ================================================================ #
    def slide6(self):
        self.camera.background_color = ManimColor(BG_CREAM)
        ch = self.chrome("教材 · 考点对照",
                         "一条新闻里的四个考点：新闻事实 ↔ 教材观点",
                         "来源：综合央视新闻（2026-10-10）、财新网（2026-10-16）及人教版教材",
                         "06 / 08")
        self.play(FadeIn(ch), run_time=0.5)
        self.next_slide()

        # 表格区域：left=2.26, top=4.59, w=29.35, h=11.64
        # 5 行（1 表头 + 4 数据），每行约 2.33cm
        col1_w = 13.0   # 左列宽 cm
        row_h  = 2.33

        def cell_text(left_cm, top_cm, w_cm, h_cm, text, size, color, bold):
            return mk_text(left_cm, top_cm, w_cm, h_cm, text, size, color, FONT_SANS, bold=bold)

        # 表头
        hdr_top = 4.59
        hdr = VGroup(
            mk_rect(2.26, hdr_top, col1_w, row_h, TABLE_HEAD),
            mk_rect(2.26 + col1_w, hdr_top, 29.35 - col1_w, row_h, TABLE_HEAD),
            cell_text(2.26 + 0.3, hdr_top, col1_w - 0.6, row_h, "新闻中的事实", 16, WHITE, True),
            cell_text(2.26 + col1_w + 0.3, hdr_top, 29.35 - col1_w - 0.6, row_h, "教材中的观点（九年级上册）", 16, WHITE, True),
        )
        self.play(FadeIn(hdr), run_time=0.4)
        self.next_slide()

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
            row = VGroup(
                mk_rect(2.26, top, col1_w, row_h, WHITE, opacity=0.6, stroke_width=1),
                mk_rect(2.26 + col1_w, top, 29.35 - col1_w, row_h, WHITE, opacity=0.6, stroke_width=1),
                cell_text(2.26 + 0.3, top, col1_w - 0.6, row_h, fact, 14, BODY, False),
                cell_text(2.26 + col1_w + 0.3, top, 29.35 - col1_w - 0.6, row_h, view, 14, BODY, False),
            )
            self.play(FadeIn(row, shift=DOWN * 0.2), run_time=0.45)
            self.next_slide()

        note = mk_text(2.26, 16.72, 29.35, 0.71,
                       "用法提示：先找新闻里的\u201c事实\u201d，再对教材里的\u201c观点\u201d——一分事实配一分观点，踩点得分。",
                       12, GRAY, FONT_SANS, slant=ITALIC)
        self.play(FadeIn(note), run_time=0.4)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ================================================================ #
    # 第 7 页 · 时政点评
    # ================================================================ #
    def slide7(self):
        self.camera.background_color = ManimColor(BG_CREAM)
        ch = self.chrome("点评 · 怎么看",
                         "三重逻辑读懂这份《意见》：发展、竞争与安全",
                         "",
                         "07 / 08")
        self.play(FadeIn(ch), run_time=0.5)
        self.next_slide()

        rows = [
            ("①", "发展的选择：",
             "我国经济已由高速增长阶段转向高质量发展阶段，传统要素驱动难以为继，\n必须以创新催生新产业、新模式、新动能。",
             "教材链接：创新是引领发展的第一动力，创新驱动是国家命运所系。",
             4.66),
            ("②", "竞争的应对：",
             "新一轮科技革命加速突破，关键核心技术买不来、讨不来。\n只有把大国重器掌握在自己手里，才能赢得发展主动权。",
             "教材链接：建设世界科技创新强国，要增强自主创新能力，走中国特色自主创新道路。",
             8.89),
            ("③", "安全的统筹：",
             "对先进技术依法依规实施出口管制，与扩大高水平对外开放并行不悖，\n体现统筹发展和安全，守住国家利益底线。",
             "教材链接：坚持国家利益至上，维护国家安全，人人有责。",
             13.12),
        ]
        for num, head, body, link, top in rows:
            n = mk_text(2.26, top, 1.83, 1.27, num, 24, RED, FONT_SERIF, bold=True)
            hd = mk_text(4.45, top, 27.16, 0.8, head, 14, INK, FONT_SANS, bold=True)
            bd = mk_text(4.45, top + 0.75, 27.16, 1.5, body, 14, BODY, FONT_SANS)
            lk = mk_text(4.45, top + 2.2, 27.16, 0.7, link, 12, RED, FONT_SANS, slant=ITALIC)
            ln = mk_hline(2.26, top + 3.52, 29.35)
            self.play(FadeIn(VGroup(n, hd, bd, lk, ln), shift=RIGHT * 0.2), run_time=0.5)
            self.next_slide()

        # 底部米色条 + 一句话点评
        strip = mk_rect(0, 16.93, 33.87, 2.12, BAND)
        stxt = mk_text(2.26, 16.93, 29.35, 2.12,
                       "一句话点评：以创新破局、以制度护航，新质生产力正成为中国式现代化最鲜明的\u201c新引擎\u201d。",
                       15, INK, FONT_SERIF, bold=True)
        self.play(FadeIn(strip, shift=UP * 0.4), FadeIn(stxt), run_time=0.6)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ================================================================ #
    # 第 8 页 · 行动倡议 + 结束语
    # ================================================================ #
    def slide8(self):
        self.camera.background_color = ManimColor(BG_CREAM)
        ch = self.chrome("点评 · 我们怎么做",
                         "强国建设，少年何为？四个行动现在做起",
                         "本页为演讲者倡议与结束语",
                         "08 / 08")
        self.play(FadeIn(ch), run_time=0.5)
        self.next_slide()

        actions = [
            ("勤学习", "学好科学文化知识，打牢创新的知识根基", 4.66),
            ("敢质疑", "不迷信权威、不盲从答案，培养批判性思维", 7.48),
            ("重实践", "参加科技小发明、小制作和研究性学习活动", 10.3),
            ("立大志", "把个人理想融入科技强国、民族复兴的伟大征程", 13.12),
        ]
        for title, desc, top in actions:
            # 小红方块（a1-icon 0.78cm x 0.78cm）
            icon = mk_rect(2.26, top + 0.21, 0.78, 0.78, RED)
            t = mk_text(3.6, top, 13.76, 0.8, title, 13, INK, FONT_SANS, bold=True)
            d = mk_text(3.6, top + 0.75, 13.76, 1.2, desc, 13, BODY, FONT_SANS)
            self.play(FadeIn(VGroup(icon, t, d), shift=RIGHT * 0.3), run_time=0.45)
            self.next_slide()

        # 右栏：竖线 + 米色面板 + 引言
        vd = mk_vline(19.05, 4.94, 10.23)
        panel = mk_rect(20.46, 4.94, 11.15, 10.23, BAND)
        qm = mk_text(21.31, 5.57, 1.76, 1.62, "\u201c", 40, RED, FONT_SERIF, bold=True)
        quote = mk_text(21.31, 7.34, 9.45, 4.59,
                        "惟创新者进，\n惟创新者强，\n惟创新者胜。",
                        26, INK, FONT_SERIF, bold=True)
        self.play(Create(vd),
                  FadeIn(panel, shift=RIGHT * 0.4),
                  FadeIn(qm), FadeIn(quote), run_time=0.7)
        self.next_slide()

        # 结束语
        sign = mk_text(21.31, 12.42, 9.45, 1.98,
                       "我的演讲到此结束，\n谢谢大家！",
                       20, RED, FONT_SERIF, bold=True)
        self.play(FadeIn(sign, shift=UP * 0.2), run_time=0.6)
        # 最后一页停留，不 next_slide

ShizhengSlides().render()