# -*- coding: utf-8 -*-
"""
时政演讲 Manim Slides —— 向"新"而行，以"创"致远
=================================================
配套：shizheng.pptx / 时政演讲稿_动画标注版.docx / 动画分镜脚本.md

依赖：
    pip install manim manim-slides

运行（预览）：
    manim -pql shizheng_slides.py ShizhengSlides
    manim -pqh shizheng_slides.py ShizhengSlides      # 1080p 高清
    manim slides present shizheng_slides.py ShizhengSlides   # 演讲者模式（键盘 → 下一页）

操作：
    空格 / →：下一个动画步（= 翻页笔一次点击）
    ←：上一步
    数字键：跳页
    Esc：退出

字体：Windows 默认使用 "Microsoft YaHei"（微软雅黑），如在 macOS/Linux 运行请把
      CN_FONT 改成 "PingFang SC" / "Noto Sans CJK SC"。
"""

from manim import *
from manim_slides import Slide

# ---------------------------------------------------------------------------
# 配色（与原 PPT 保持一致）
# ---------------------------------------------------------------------------
BG       = "#FBF8F3"   # 暖白底
INK      = "#211D18"   # 主文字
RED      = "#C03A2B"   # 主题红
GOLD     = "#B8860B"   # 强调金
GRAY     = "#7A7166"   # 次要灰
LIGHT    = "#F1E9DC"   # 浅米色块
LINE     = "#D9CFC0"   # 分隔线

CN_FONT  = "Microsoft YaHei"
EN_FONT  = "Times New Roman"


def cn_text(text, size=24, color=INK, weight=NORMAL, slant=NORMAL):
    return Text(
        text,
        font=CN_FONT,
        font_size=size,
        color=color,
        weight=weight,
        slant=slant,
    )


def header(kicker, title):
    """统一的页头：小标签 + 大标题 + 红色细线。返回 VGroup。"""
    k = cn_text(kicker, size=20, color=RED, weight=BOLD)
    t = cn_text(title, size=34, color=INK, weight=BOLD)
    line = Line(LEFT * 6.2, RIGHT * 6.2, color=RED, stroke_width=2)
    grp = VGroup(k, t, line).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    k.to_edge(UP).shift(DOWN * 0.55)
    t.next_to(k, DOWN, aligned_edge=LEFT, buff=0.25)
    line.next_to(t, DOWN, aligned_edge=LEFT, buff=0.2)
    return grp


def footer(source, page_no):
    """页脚：来源（左） + 页码（右）。"""
    s = cn_text(source, size=14, color=GRAY)
    p = cn_text(page_no, size=14, color=GRAY)
    s.to_edge(DOWN).to_edge(LEFT).shift(DOWN * 0.35 + RIGHT * 0.5)
    p.to_edge(DOWN).to_edge(RIGHT).shift(DOWN * 0.35 + LEFT * 0.5)
    return VGroup(s, p)


# ---------------------------------------------------------------------------
# 主场景
# ---------------------------------------------------------------------------
class ShizhengSlides(Slide):

    def construct(self):
        self.camera.background_color = BG

        self.slide1_cover()
        self.slide2_news()
        self.slide3_five_pillars()
        self.slide4_export_control()
        self.slide5_textbook()
        self.slide6_mapping()
        self.slide7_commentary()
        self.slide8_actions()

    # ------------------------------------------------------------------ #
    # 第 1 页 · 封面
    # ------------------------------------------------------------------ #
    def slide1_cover(self):
        # 1.0 顶部小标签
        top = cn_text("时政演讲 · 道德与法治", size=22, color=GRAY)
        top.to_edge(UP).shift(DOWN * 0.8)
        bar = Rectangle(width=0.12, height=2.6, fill_color=RED, fill_opacity=1,
                        stroke_width=0)
        bar.next_to(top, DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 0.2)

        self.play(FadeIn(top, shift=DOWN * 0.2), run_time=0.5)
        self.next_slide()

        # 1.1 主标题
        title = cn_text('向"新"而行，', size=64, color=INK, weight=BOLD)
        title2 = cn_text('以"创"致远', size=64, color=RED, weight=BOLD)
        VGroup(title, title2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        title.next_to(bar, RIGHT, buff=0.5)
        title2.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        self.play(FadeIn(VGroup(title, title2), shift=RIGHT * 0.4), run_time=0.7)
        self.next_slide()

        # 1.2 副标题
        sub = cn_text("——从《关于发展新质生产力的意见》看\"创新驱动发展\"",
                      size=26, color=GRAY)
        sub.next_to(title2, DOWN, aligned_edge=LEFT, buff=0.6)
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.next_slide()

        # 1.3 底部信息
        info = cn_text("教材链接：人教版《道德与法治》九年级上册 第二课《创新驱动发展》",
                       size=20, color=INK)
        info2 = cn_text("演讲人：×××    ｜    班级：×××", size=20, color=INK)
        VGroup(info, info2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        info.to_edge(DOWN).shift(UP * 1.2 + LEFT * 0.5)
        info2.next_to(info, DOWN, aligned_edge=LEFT, buff=0.15)
        self.play(FadeIn(VGroup(info, info2), shift=UP * 0.2), run_time=0.5)
        self.next_slide()

        # 整页切走
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ------------------------------------------------------------------ #
    # 第 2 页 · 时政速览
    # ------------------------------------------------------------------ #
    def slide2_news(self):
        h = header("报道 · 01  时政速览",
                   "中共中央、国务院发布《关于发展新质生产力的意见》")
        f = footer("来源：央视新闻《早啊！新闻来了》（2026-10-10）", "02 / 08")
        self.play(FadeIn(h), FadeIn(f), run_time=0.5)
        self.next_slide()

        # 2.1 时间
        lbl1 = cn_text("时　间", size=20, color=GRAY, weight=BOLD)
        val1 = cn_text("2026 年 10 月 9 日", size=28, color=INK, weight=BOLD)
        VGroup(lbl1, val1).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lbl1.to_edge(LEFT).shift(RIGHT * 0.8 + UP * 1.6)
        val1.next_to(lbl1, DOWN, aligned_edge=LEFT, buff=0.1)
        self.play(FadeIn(VGroup(lbl1, val1), shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 2.2 发布主体
        lbl2 = cn_text("发布主体", size=20, color=GRAY, weight=BOLD)
        val2 = cn_text("中共中央、国务院", size=28, color=INK, weight=BOLD)
        VGroup(lbl2, val2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lbl2.next_to(val1, DOWN, aligned_edge=LEFT, buff=0.55)
        val2.next_to(lbl2, DOWN, aligned_edge=LEFT, buff=0.1)
        vdiv = Line(UP * 2.6, DOWN * 2.6, color=LINE, stroke_width=1.5)
        vdiv.move_to(RIGHT * 3.2)
        self.play(FadeIn(VGroup(lbl2, val2), shift=RIGHT * 0.2),
                  Create(vdiv), run_time=0.4)
        self.next_slide()

        # 2.3 文件名称
        lbl3 = cn_text("文件名称", size=20, color=GRAY, weight=BOLD)
        val3 = cn_text("《关于发展新质生产力的意见》", size=26, color=INK, weight=BOLD)
        VGroup(lbl3, val3).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lbl3.next_to(val2, DOWN, aligned_edge=LEFT, buff=0.55)
        val3.next_to(lbl3, DOWN, aligned_edge=LEFT, buff=0.1)
        self.play(FadeIn(VGroup(lbl3, val3), shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 2.4 数字 5
        n5 = cn_text("5 个", size=64, color=RED, weight=BOLD)
        c5 = cn_text("方面部署\n（科技创新摆在首位）", size=18, color=INK)
        VGroup(n5, c5).arrange(DOWN, aligned_edge=ORIGIN, buff=0.1)
        n5.move_to(RIGHT * 4.6 + UP * 1.0)
        c5.next_to(n5, DOWN, buff=0.15)
        self.play(GrowFromCenter(n5), FadeIn(c5, shift=UP * 0.15), run_time=0.6)
        self.next_slide()

        # 2.5 数字 19
        n19 = cn_text("19 项", size=64, color=RED, weight=BOLD)
        c19 = cn_text("重点举措", size=18, color=INK)
        VGroup(n19, c19).arrange(DOWN, aligned_edge=ORIGIN, buff=0.1)
        n19.move_to(RIGHT * 8.0 + UP * 1.0)
        c19.next_to(n19, DOWN, buff=0.15)
        self.play(GrowFromCenter(n19), FadeIn(c19, shift=UP * 0.15), run_time=0.6)
        self.next_slide()

        # 2.6 引语条
        band = Rectangle(width=12.8, height=1.4, fill_color=LIGHT, fill_opacity=1,
                         stroke_width=0)
        band.to_edge(DOWN).shift(UP * 1.7)
        qmark = cn_text("\u201c", size=48, color=RED, weight=BOLD)
        qmark.move_to(band.get_left() + RIGHT * 0.5 + UP * 0.2)
        qtext = cn_text("围绕科技创新、产业创新、发展方式创新、体制机制创新、人才工作机制创新\n"
                        "五方面，提出 19 项重点举措。",
                        size=20, color=INK)
        qtext.move_to(band.get_center()).shift(RIGHT * 0.6)
        self.play(FadeIn(band, shift=UP * 0.3),
                  FadeIn(qmark), FadeIn(qtext), run_time=0.6)
        self.next_slide()

        # 2.7 why line
        why = cn_text("为什么选这条新闻？——它正对应教材的核心考点：创新驱动发展。"
                      "接下来按\"报道 → 教材 → 点评\"展开。",
                      size=19, color=GRAY, slant=ITALIC)
        why.to_edge(DOWN).shift(UP * 0.7)
        self.play(FadeIn(why, shift=UP * 0.2), run_time=0.5)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ------------------------------------------------------------------ #
    # 第 3 页 · 五方面要点
    # ------------------------------------------------------------------ #
    def _five_row(self, num, name, desc, y):
        n = cn_text(num, size=28, color=RED, weight=BOLD)
        nm = cn_text(name, size=24, color=INK, weight=BOLD)
        d = cn_text(desc, size=19, color=GRAY)
        row = VGroup(n, nm, d)
        n.move_to(LEFT * 5.6 + y)
        nm.next_to(n, RIGHT, buff=0.3, aligned_edge=ORIGIN)
        d.next_to(nm, RIGHT, buff=0.6, aligned_edge=ORIGIN)
        line = Line(LEFT * 5.6, RIGHT * 6.2, color=LINE, stroke_width=1)
        line.next_to(row, DOWN, buff=0.18)
        return VGroup(row, line)

    def slide3_five_pillars(self):
        h = header("报道 · 01  要点梳理",
                   "《意见》部署五方面创新，科技创新居首")
        f = footer("来源：央视新闻《早啊！新闻来了》（2026-10-10）", "03 / 08")
        self.play(FadeIn(h), FadeIn(f), run_time=0.5)
        self.next_slide()

        rows_data = [
            ("01", "科技创新",     "核心引擎——以科技突破引领产业变革",        UP * 2.0),
            ("02", "产业创新",     "主战场——让科技成果转化为现实生产力",      UP * 0.7),
            ("03", "发展方式创新", "方向标——推动发展向绿色化、智能化转型",     DOWN * 0.6),
            ("04", "体制机制创新", "制度保障——让各类创新活力充分涌流",        DOWN * 1.9),
            ("05", "人才工作机制创新", "第一资源——培养造就大批创新型人才",    DOWN * 3.2),
        ]
        rows = []
        for num, name, desc, y in rows_data:
            r = self._five_row(num, name, desc, y)
            rows.append(r)
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.4)
            self.next_slide()

        # 注释
        note = cn_text("注：左列为《意见》部署的五个方面（据新华社报道）；"
                       "右列为演讲者结合教材知识所作的要点解读，帮助理解记忆。",
                       size=16, color=GRAY)
        note.to_edge(DOWN).shift(UP * 1.35)
        self.play(FadeIn(note), run_time=0.4)
        self.next_slide()

        # 记忆钩子
        hook = cn_text("记忆钩子：科技打头 · 产业落地 · 方式转型 · 机制护航 · 人才支撑",
                       size=24, color=RED, weight=BOLD)
        hook.to_edge(DOWN).shift(UP * 0.6)
        self.play(hook.animate.scale(1.1), FadeIn(hook, shift=UP * 0.2), run_time=0.5)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ------------------------------------------------------------------ #
    # 第 4 页 · 关联新闻
    # ------------------------------------------------------------------ #
    def slide4_export_control(self):
        h = header("报道 · 02  关联新闻",
                   "一周内，40 项关键技术出口管制公开征求意见")
        f = footer("来源：财新网（2026-10-16）", "04 / 08")
        self.play(FadeIn(h), FadeIn(f), run_time=0.5)
        self.next_slide()

        # 左栏标题 + 第 1 段
        lead_l = cn_text("新闻事实", size=22, color=RED, weight=BOLD)
        lead_l.to_edge(LEFT).shift(RIGHT * 0.8 + UP * 1.9)
        b1 = cn_text("10 月 16 日，商务部、科技部发布 2026 年第 48 号公告，\n"
                     "就修订《中国禁止出口限制出口技术目录》公开征求意见。",
                     size=18, color=INK, weight=NORMAL)
        b1.next_to(lead_l, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(VGroup(lead_l, b1), shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 左栏第 2 段（40 项）
        b2 = cn_text("拟增列 人工智能、生物医药、光伏 三个领域\n"
                     "共 ", size=18, color=INK)
        n40 = cn_text(" 40 项 ", size=22, color=RED, weight=BOLD)
        b2b = cn_text("关键技术。", size=18, color=INK)
        VGroup(b2, n40, b2b).arrange(RIGHT, buff=0.05)
        VGroup(b2, n40, b2b).next_to(b1, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(FadeIn(VGroup(b2, n40, b2b), shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 左栏第 3 段（14 / 26）
        b3 = cn_text("其中拟禁止出口 ", size=18, color=INK)
        n14 = cn_text(" 14 项 ", size=22, color=RED, weight=BOLD)
        b3b = cn_text("，拟限制出口 ", size=18, color=INK)
        n26 = cn_text(" 26 项 ", size=22, color=RED, weight=BOLD)
        b3c = cn_text("。", size=18, color=INK)
        VGroup(b3, n14, b3b, n26, b3c).arrange(RIGHT, buff=0.05)
        VGroup(b3, n14, b3b, n26, b3c).next_to(b2, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(FadeIn(VGroup(b3, n14, b3b, n26, b3c), shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        # 左栏第 4 段（发言人）+ 右栏分隔线
        b4 = cn_text("商务部发言人：这是技术贸易管理的常态化工作，\n"
                     "依法依规，不针对任何特定国家、地区或实体。",
                     size=18, color=GRAY)
        b4.next_to(b3, DOWN, aligned_edge=LEFT, buff=0.35)
        vdiv = Line(UP * 3.0, DOWN * 3.0, color=LINE, stroke_width=1.5)
        vdiv.move_to(RIGHT * 1.2)
        self.play(FadeIn(b4, shift=RIGHT * 0.2), Create(vdiv), run_time=0.4)
        self.next_slide()

        # 右栏标题
        lead_r = cn_text("这条新闻释放什么信号？", size=22, color=RED, weight=BOLD)
        lead_r.next_to(vdiv, RIGHT, buff=0.5).shift(UP * 1.9)
        self.play(FadeIn(lead_r, shift=LEFT * 0.2), run_time=0.4)
        self.next_slide()

        # 右栏三条
        sig1 = cn_text("· 科技实力已成为国际竞争的核心，\n  各主要经济体都在加强关键技术管控。",
                       size=17, color=INK)
        sig2 = cn_text("· 关键技术关系国家安全与发展利益，\n  必须掌握在自己手里。",
                       size=17, color=INK)
        sig3 = cn_text("· 管制不等于封闭：我国仍坚持扩大开放，\n  推动国际科技合作。",
                       size=17, color=INK)
        VGroup(sig1, sig2, sig3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        sig1.next_to(lead_r, DOWN, aligned_edge=LEFT, buff=0.35)
        for sig in (sig1, sig2, sig3):
            self.play(FadeIn(sig, shift=LEFT * 0.2), run_time=0.4)
            self.next_slide()

        # 底部总结
        bottom = Rectangle(width=12.8, height=0.9, fill_color=LIGHT,
                           fill_opacity=1, stroke_width=0)
        bottom.to_edge(DOWN).shift(UP * 1.0)
        txt = cn_text("两条新闻合看：一端是\"促创新\"的顶层部署，一端是\"护安全\"的制度安排"
                      "——发展与安全一体两面。",
                      size=19, color=INK, weight=BOLD)
        txt.move_to(bottom.get_center())
        self.play(FadeIn(bottom, shift=UP * 0.3), FadeIn(txt), run_time=0.6)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ------------------------------------------------------------------ #
    # 第 5 页 · 教材四观点
    # ------------------------------------------------------------------ #
    def _textbook_row(self, num, lead, rest, y):
        n = cn_text(num, size=30, color=RED, weight=BOLD)
        head = cn_text(lead, size=22, color=INK, weight=BOLD)
        body = cn_text(rest, size=17, color=GRAY)
        n.move_to(LEFT * 5.6 + y)
        head.next_to(n, RIGHT, buff=0.3, aligned_edge=ORIGIN)
        body.next_to(head, DOWN, aligned_edge=LEFT, buff=0.1)
        line = Line(LEFT * 5.6, RIGHT * 6.2, color=LINE, stroke_width=1)
        line.next_to(VGroup(head, body), DOWN, buff=0.2)
        return VGroup(n, head, body, line)

    def slide5_textbook(self):
        h = header("教材 · 知识回顾",
                   "九上第二课《创新驱动发展》的四个核心观点")
        f = footer("教材：人民教育出版社《道德与法治》九年级上册", "05 / 08")
        tag = cn_text("人教版《道德与法治》九年级上册 · 第一单元\"富强与创新\"",
                      size=18, color=GRAY)
        tag.to_edge(LEFT).shift(RIGHT * 0.8 + UP * 2.0)
        self.play(FadeIn(h), FadeIn(f), FadeIn(tag), run_time=0.5)
        self.next_slide()

        rows = [
            ("01", "创新是引领发展的第一动力。",
             "创新是一个民族进步的灵魂，是国家兴旺发达的不竭源泉，也是中华民族最鲜明的民族禀赋。",
             UP * 1.3),
            ("02", "创新驱动是国家命运所系。",
             "我国实施创新驱动发展战略，推进以科技创新为核心的全面创新。",
             DOWN * 0.2),
            ("03", "建设世界科技创新强国，要增强自主创新能力。",
             "坚持自主创新、重点跨越、支撑发展、引领未来的方针，走中国特色自主创新道路。",
             DOWN * 1.7),
            ("04", "企业是社会创新的重要力量。",
             "提升创新能力是企业持续发展之基、市场制胜之道；核心技术不是别人赐予的，必须自强奋斗。",
             DOWN * 3.2),
        ]
        for num, lead, rest, y in rows:
            r = self._textbook_row(num, lead, rest, y)
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.45)
            self.next_slide()

        note = cn_text("以上表述综合自人教版《道德与法治》九年级上册第二课《创新驱动发展》。",
                       size=15, color=GRAY)
        note.to_edge(DOWN).shift(UP * 0.85)
        self.play(FadeIn(note), run_time=0.4)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ------------------------------------------------------------------ #
    # 第 6 页 · 考点对照表
    # ------------------------------------------------------------------ #
    def slide6_mapping(self):
        h = header("教材 · 考点对照",
                   "一条新闻里的四个考点：新闻事实 ↔ 教材观点")
        f = footer("来源：综合央视新闻、财新网及人教版教材", "06 / 08")
        self.play(FadeIn(h), FadeIn(f), run_time=0.5)
        self.next_slide()

        # 表头
        col_w = [5.6, 6.0]
        header_row = VGroup(
            self._cell("新闻中的事实", col_w[0], is_header=True),
            self._cell("教材中的观点（九年级上册）", col_w[1], is_header=True),
        ).arrange(RIGHT, buff=0.0)
        header_row.move_to(UP * 1.8)
        self.play(FadeIn(header_row), run_time=0.4)
        self.next_slide()

        rows_data = [
            ("《意见》把科技创新摆在五方面首位，\n部署 19 项举措",
             "创新是引领发展的第一动力；实施创新驱动发展战略，\n推进以科技创新为核心的全面创新"),
            ("《意见》专门部署人才工作机制创新",
             "落实科教兴国战略、人才强国战略；\n培养创新型人才，建设创新型国家"),
            ("拟对人工智能、生物医药、光伏等\n40 项关键技术实施出口管制",
             "增强自主创新能力；大国重器一定要掌握在自己手里，\n核心技术不是别人赐予的"),
            ("新质生产力覆盖光伏、生物医药等\n新兴产业",
             "转变发展方式、优化经济结构、转换增长动力，\n推动经济高质量发展"),
        ]
        y_cursor = UP * 1.8
        for fact, view in rows_data:
            y_cursor -= 1.15
            row = VGroup(
                self._cell(fact, col_w[0]),
                self._cell(view, col_w[1]),
            ).arrange(RIGHT, buff=0.0)
            row.move_to(y_cursor)
            self.play(FadeIn(row, shift=DOWN * 0.2), run_time=0.45)
            self.next_slide()

        note = cn_text("用法提示：先找新闻里的\"事实\"，再对教材里的\"观点\"——一分事实配一分观点，踩点得分。",
                       size=18, color=GRAY, slant=ITALIC)
        note.to_edge(DOWN).shift(UP * 0.85)
        self.play(FadeIn(note), run_time=0.4)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    @staticmethod
    def _cell(text, width, is_header=False):
        box = Rectangle(width=width, height=1.05,
                        fill_color=LIGHT if is_header else WHITE,
                        fill_opacity=1, stroke_color=LINE, stroke_width=1)
        t = cn_text(text, size=16 if not is_header else 18,
                    color=INK if not is_header else RED,
                    weight=BOLD if is_header else NORMAL)
        t.move_to(box.get_center())
        return VGroup(box, t)

    # ------------------------------------------------------------------ #
    # 第 7 页 · 时政点评
    # ------------------------------------------------------------------ #
    def _comment_row(self, num, title, body, link, y):
        n = cn_text(num, size=36, color=RED, weight=BOLD)
        head = cn_text(title, size=24, color=INK, weight=BOLD)
        body_t = cn_text(body, size=18, color=INK)
        link_t = cn_text("教材链接：" + link, size=15, color=GRAY, slant=ITALIC)
        n.move_to(LEFT * 5.6 + y)
        head.next_to(n, RIGHT, buff=0.3, aligned_edge=ORIGIN)
        body_t.next_to(head, DOWN, aligned_edge=LEFT, buff=0.1)
        link_t.next_to(body_t, DOWN, aligned_edge=LEFT, buff=0.1)
        line = Line(LEFT * 5.6, RIGHT * 6.2, color=LINE, stroke_width=1)
        line.next_to(link_t, DOWN, buff=0.2)
        return VGroup(n, head, body_t, link_t, line)

    def slide7_commentary(self):
        h = header("点评 · 怎么看",
                   "三重逻辑读懂这份《意见》：发展、竞争与安全")
        f = footer("", "07 / 08")
        self.play(FadeIn(h), FadeIn(f), run_time=0.5)
        self.next_slide()

        rows = [
            ("①", "发展的选择",
             "经济由高速增长转向高质量发展，传统要素驱动难以为继，\n必须以创新催生新产业、新模式、新动能。",
             "创新是引领发展的第一动力，创新驱动是国家命运所系。",
             UP * 1.7),
            ("②", "竞争的应对",
             "新一轮科技革命加速突破，关键核心技术买不来、讨不来；\n把大国重器掌握在自己手里，才能赢得发展主动权。",
             "增强自主创新能力，走中国特色自主创新道路。",
             DOWN * 0.2),
            ("③", "安全的统筹",
             "对先进技术依法依规实施出口管制，与扩大高水平对外开放\n并行不悖，体现统筹发展和安全，守住国家利益底线。",
             "坚持国家利益至上，维护国家安全，人人有责。",
             DOWN * 2.2),
        ]
        for num, title, body, link, y in rows:
            r = self._comment_row(num, title, body, link, y)
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.5)
            self.next_slide()

        # 底部一句话点评
        strip = Rectangle(width=12.8, height=0.95, fill_color=RED,
                          fill_opacity=1, stroke_width=0)
        strip.to_edge(DOWN).shift(UP * 0.6)
        txt = cn_text("一句话点评：以创新破局、以制度护航，"
                      "新质生产力正成为中国式现代化最鲜明的\"新引擎\"。",
                      size=20, color=WHITE, weight=BOLD)
        txt.move_to(strip.get_center())
        self.play(FadeIn(strip, shift=UP * 0.4), FadeIn(txt), run_time=0.6)
        self.next_slide()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ------------------------------------------------------------------ #
    # 第 8 页 · 行动倡议 + 结束语
    # ------------------------------------------------------------------ #
    def slide8_actions(self):
        h = header("点评 · 我们怎么做",
                   "强国建设，少年何为？四个行动现在做起")
        f = footer("本页为演讲者倡议与结束语", "08 / 08")
        self.play(FadeIn(h), FadeIn(f), run_time=0.5)
        self.next_slide()

        actions = [
            ("勤学习", "学好科学文化知识，打牢创新的知识根基"),
            ("敢质疑", "不迷信权威、不盲从答案，培养批判性思维"),
            ("重实践", "参加科技小发明、小制作和研究性学习活动"),
            ("立大志", "把个人理想融入科技强国、民族复兴的伟大征程"),
        ]
        ys = [UP * 1.9, UP * 0.5, DOWN * 0.9, DOWN * 2.3]
        for (title, desc), y in zip(actions, ys):
            icon = Circle(radius=0.28, color=RED, fill_color=RED, fill_opacity=1)
            t = cn_text(title, size=24, color=INK, weight=BOLD)
            d = cn_text(desc, size=18, color=GRAY)
            icon.move_to(LEFT * 5.6 + y)
            t.next_to(icon, RIGHT, buff=0.3, aligned_edge=ORIGIN)
            d.next_to(t, DOWN, aligned_edge=LEFT, buff=0.08)
            self.play(FadeIn(VGroup(icon, t, d), shift=RIGHT * 0.3), run_time=0.45)
            self.next_slide()

        # 右栏引言卡片
        vdiv = Line(UP * 3.0, DOWN * 3.0, color=LINE, stroke_width=1.5)
        vdiv.move_to(RIGHT * 1.0)
        panel = Rectangle(width=4.6, height=3.6, fill_color=LIGHT,
                          fill_opacity=1, stroke_width=0)
        panel.move_to(RIGHT * 4.3 + UP * 0.2)
        qm = cn_text("\u201c", size=64, color=RED, weight=BOLD)
        qm.move_to(panel.get_top() + DOWN * 0.6 + LEFT * 1.6)
        quote = cn_text("惟创新者进，\n惟创新者强，\n惟创新者胜。",
                        size=26, color=INK, weight=BOLD)
        quote.move_to(panel.get_center() + UP * 0.2)
        self.play(Create(vdiv),
                  FadeIn(panel, shift=RIGHT * 0.4),
                  FadeIn(qm), FadeIn(quote), run_time=0.7)
        self.next_slide()

        # 结束语
        sign = cn_text("我的演讲到此结束，\n谢谢大家！",
                       size=26, color=RED, weight=BOLD)
        sign.move_to(panel.get_bottom() + DOWN * 0.95)
        self.play(FadeIn(sign, shift=UP * 0.2), run_time=0.6)
        # 最后一页停留，不再 next_slide（演讲者在此鞠躬）
