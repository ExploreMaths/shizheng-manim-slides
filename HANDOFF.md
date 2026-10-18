# 时政演讲 Manim Slides 项目交接文档

> 给下一个继续开发的 AI 助手。读完这份文档你应该能立刻接手，不需要再问用户。

## 项目地址

- **GitHub**: https://github.com/ExploreMaths/shizheng-manim-slides
- **作者**: ExploreMaths（朱崇璟）
- **演讲人**: 朱崇璟、戴语骏，八（2）班

## 这是什么

把一份 8 页时政演讲 PPT《向"新"而行，以"创"致远——从〈关于发展新质生产力的意见〉看"创新驱动发展"》用 Manim Slides 重写成带动画的演示视频。每个文字、图片、形状都按原 PPT 坐标系独立复刻，不是整页贴图。

## 技术栈

- **Manim Community** v0.22.0（Python 3.14）
- **manim-slides** v5.7.0（Slides 框架，支持分步）
- **manim_extensions** v1.0.4（用了 `ExtendedLine`）
- **字体**: MiSans（无衬线）、Noto Serif SC（衬线）
- **OS**: Windows 11

## 目录结构

```
shizheng_manim/
├── shizheng_pptx.py          # 主文件（唯一需要改的）
├── assets/media/image1_0.png # 封面/结束页背景图（水印已去）
├── media/videos/...          # Manim 渲染输出
├── 时政演讲稿_双人版.md       # 双人分步演讲稿
├── 时政演讲稿_动画标注版.md
├── 动画分镜脚本.md
└── shizheng_v17.pptx 等       # 历史 PPTX 导出
```

## 主文件结构（shizheng_pptx.py）

### 开头补丁（manim 0.22 兼容）

文件开头重写了 `Slide.__init__` 和 `Slide.render`，去掉了 0.22 里已移除的 `write_to_movie` 配置和 `max_files_cached` 的 float 限制。**不要删这段**。

### 常量

```python
BG_CREAM = "#F8F4ED"   # 米色背景
RED      = "#C03A2B"
INK      = "#211D18"
BODY     = "#4A4239"
GRAY     = "#7A7166"
BAND     = "#F1E9DC"
LINE_GRAY= "#D9CFC0"
SCALE    = 14.222 / 33.87  # ≈0.420，PPT cm → Manim 单位
PPT_W    = 33.87
PPT_H    = 19.05
```

### 坐标映射

- `P(left, top, w, h)` → Manim 居中坐标
- `ul_point(left, top)` → 文本框左上角（UL 锚定）
- `mk_text(left, top, w, h, text, size, ...)` → 按 PPT 坐标放文字
- `mk_rect(left, top, w, h, color)` → 矩形
- `mk_hline / mk_vline(left, top, w/h, color)` → 线

### 10 个 slide

| slide | 内容 | 转场方向 |
|---|---|---|
| 0 | ManimBanner 片头（黑底） | — |
| 1 | 封面（标题+竖线+署名） | FadeOut（不是平移） |
| 2 | 新闻事实（时间/发布主体/文件名+5个/19项） | up |
| 3 | 五方面要点列表 | left |
| 4 | 关联新闻（出口管制） | right |
| 5 | 教材链接 | diag_bl |
| 6 | 创新驱动发展 | down |
| 7 | 点评/总结 | diag_tl |
| 8 | 金句/过渡 | diag_tr |
| 9 | 结束页（谢谢大家） | diag_br |

### 转场函数 `_transition(target)`

所有切页都是**整体平移飞出**（`shift`，不是 `move_to`），目标方向：
`up / down / left / right / diag_tr / diag_tl / diag_bl / diag_br`。

**不要再加 shrink/spin 到中心的动画**——用户明确要求所有元素保持相对位置整体平移。

## 渲染命令

```powershell
# 低清调试（快）
& "C:\Users\kylez\AppData\Local\Programs\Python\Python314\python.exe" -m manim -ql --disable_caching shizheng_pptx.py ShizhengSlides

# 高清（慢，约 5-10 分钟）
& "C:\Users\kylez\AppData\Local\Programs\Python\Python314\python.exe" -m manim -qh shizheng_pptx.py ShizhengSlides

# 导出 PPTX（可选）
& "C:\Users\kylez\AppData\Local\Programs\Python\Python314\python.exe" -m manim_slides convert --to=pptx ShizhengSlides output.pptx
```

视频输出在 `media/videos/shizheng_pptx/480p15/ShizhengSlides.mp4`（低清）或 `1080p60/`（高清）。

## 用户偏好（必须遵守）

1. **只要视频，不要 PPTX**——用户最近几轮明确说"我只要视频"
2. **每个元素独立复刻**，不要整页贴图
3. **动画用 Write / Create / GrowFromCenter / Circumscribe / FadeIn**，不要全 FadeIn
4. **转场全部平移飞出**，不要缩到中心
5. **不要加 run_time 或倍速**，用 Manim 默认速度
6. **文本 stroke_width=1, stroke_color=同文字色**（这样 Write 动画不会出现白色描边）
7. **z_index 分层**：背景图 z=0，形状/线 z=1，文字 z=2
8. **排版要紧凑**：列表项行距均匀，不要大块空白；用户会反复要求调间距
9. **片头在第1页开头 FadeOut**（不是飞出去），背景图先 FadeIn 再设背景色
10. **竖条用 ExtendedLine**（manim_extensions），两端延长 0.3

## 已知待办 / 可能继续做的方向

- [ ] 高清渲染经常因 ffmpeg 编码错误中断，需要重跑
- [ ] 各页排版可能还需要微调（用户审美要求高，对标 Awwwards 级别）
- [ ] 演讲稿 `时政演讲稿_双人版.md` 的翻页标注可能需要和最终视频同步
- [ ] 结束页目前没有副标题（用户要求删除了"敬请各位老师同学批评指正"）
- [ ] 第3页列表行距 2.0cm，顶部无横线，底部有分隔线
- [ ] 第2页三行行距 3.0cm，引语条 h=2.4 靠下，why 行紧贴引语条

## 关键坐标速查

### slide1 封面
- 背景图 `image1_0.png`，width=14.222，FadeIn 出现
- 竖线：`ExtendedLine(base_bar, extend_distance=0.3)`，从 t1.get_top() 到 t2.get_bottom()
- 标题 t1: "向"新"而行，"，t2: "以"创"致远"，font_size=50，Noto Serif SC bold
- 署名 bottom: "演讲人：朱崇璟、戴语骏 ｜ 班级：八（2）班"

### slide2 新闻事实
- 时间 top=4.5 / 发布主体 top=7.5 / 文件名称 top=10.5
- 竖线 vd: x=18.34, top=4.5, h=7.2
- "5个" top=6.83，"19项" top=6.83（相对竖线居中）
- 引语条 band: top=13.0, h=2.4
- why 行: top=15.6

### slide3 五方面列表
- 行 top: 4.60, 6.60, 8.60, 10.60, 12.60（行距 2.0）
- 每行底部一条横线，顶部无线
- 序号/名称/描述三者垂直居中对齐（用 `move_to([x, nm.get_center()[1], 0])`）

## 不要做的事

- 不要把背景换成深色（用户要米色 BG_CREAM）
- 不要用 FadeOut 做转场（除了片头）
- 不要加 PPTX 导出步骤（用户只要 mp4）
- 不要删开头的 manim 0.22 兼容补丁
