# 时政演讲 · Manim Slides 交付包

> 题目：向"新"而行，以"创"致远
> 配套原文件：`shizheng.pptx`（8 页）、`时政演讲稿.docx`（约 1300 字 / 5 分钟）

## 文件清单

| 文件 | 用途 |
|---|---|
| `shizheng_slides.py` | **Manim Slides 源码**，可直接 `manim render` / `manim slides present` |
| `动画分镜脚本.md` | 每页逐拍动画设计表（46 个点击），绑定到演讲稿原句 |
| `时政演讲稿_动画标注版.md` | 演讲稿 Markdown 源，在每句关键位置插入蓝色【动画▶…】标注 |
| `时政演讲稿_动画标注版.docx` | 演讲稿 Word 版（手持用），动画标注用蓝色加粗显示 |

## 动画节奏总览

- 8 页共 **46 次点击**，平均 6.5 秒一次。
- 每页进入：页头三件套（kicker + 大标题 + 红线）一次淡入。
- 列表行（第 3、5、7、8 页）：一次点击出一行，从左滑入。
- 关键数字（5、19、40、14、26）：`GrowFromCenter` + 主题红放大。
- 底部色条（第 2、4、7 页引语 / 总结）：从下滑入。
- 整页切换：`FadeOut` 0.4s，不做花哨转场。

## 环境准备

```bash
# 已装 Manim CE v0.19+ 的环境直接装 manim-slides 即可
pip install manim manim-slides

# Windows 中文字体默认使用 "Microsoft YaHei"；
# macOS / Linux 请把 shizheng_slides.py 顶部的 CN_FONT 改成：
#   macOS:  "PingFang SC"
#   Linux:  "Noto Sans CJK SC"
```

## 渲染与演讲

```bash
# 1) 快速预览（低清，几秒出片）
manim -pql shizheng_slides.py ShizhengSlides

# 2) 演讲用 1080p 高清
manim -pqh shizheng_slides.py ShizhengSlides

# 3) 演讲者模式（键盘 / 翻页笔触发动画）
manim slides present shizheng_slides.py ShizhengSlides
```

演讲者模式按键：

| 按键 | 作用 |
|---|---|
| `Space` / `→` / `↓` | 下一个动画步（= 翻页笔一次点击） |
| `←` | 上一步 |
| 数字键 | 跳页 |
| `Esc` | 退出 |

## 与演讲稿的对应关系

演讲稿（`时政演讲稿_动画标注版.docx`）里每一行蓝色【动画▶…】标注，对应 `shizheng_slides.py` 里**一次** `self.play(...)` 之后的 `self.next_slide()`。

也就是说：演讲者讲到标注那半句的**开头**，按一次翻页笔，画面上对应元素淡入，与语言同步。

第 8 页结束后**不要再按**——代码里最后一段没有 `next_slide()`，画面停在"谢谢大家！"上，演讲者在此鞠躬即可。

## 自定义提示

- 替换"×××"：全局搜索 `×××`，改成真实姓名 / 班级。
- 换色：改 `shizheng_slides.py` 顶部的 `RED / INK / BG / LIGHT` 常量即可全局换肤。
- 想加快 / 减慢节奏：搜 `run_time=`，整体乘 0.8（快）或 1.3（慢）。
- 想把某段文字临时隐藏：把对应的 `self.play(...)` 行注释掉即可，不会破坏其他步。
