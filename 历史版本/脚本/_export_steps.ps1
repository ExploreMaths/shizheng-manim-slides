# 用 PowerPoint COM 把每页按"分步状态"导出成高清 PNG
$ErrorActionPreference = "Stop"

$pptxPath = "C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\assets\shizheng_working.pptx"
$outDir   = "C:\Users\kylez\Doubao\chats\2026-10-17\new-chat\shizheng_manim\assets\slides"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# 分步映射：key = "s{slideIndex}_step{step}"，value = 该步"还没出现"的形状名数组
# always 可见的形状不列在任何 hide 数组里
$stepMap = @{
    # ---- Slide 1 (index 0) ----
    "s1_step0" = @("top-label","title-bar","main-title","sub-title","bottom-info")
    "s1_step1" = @("main-title","sub-title","bottom-info")
    "s1_step2" = @("sub-title","bottom-info")
    "s1_step3" = @("bottom-info")
    "s1_step4" = @()

    # ---- Slide 2 (index 1) ----
    "s2_step0" = @("info-label-1","info-value-1","info-label-2","info-value-2","v-divider","info-label-3","info-value-3","stat-num-1","stat-cap-1","stat-num-2","stat-cap-2","quote-band","quote-mark","quote-text","why-line")
    "s2_step1" = @("info-label-2","info-value-2","v-divider","info-label-3","info-value-3","stat-num-1","stat-cap-1","stat-num-2","stat-cap-2","quote-band","quote-mark","quote-text","why-line")
    "s2_step2" = @("info-label-3","info-value-3","stat-num-1","stat-cap-1","stat-num-2","stat-cap-2","quote-band","quote-mark","quote-text","why-line")
    "s2_step3" = @("stat-num-1","stat-cap-1","stat-num-2","stat-cap-2","quote-band","quote-mark","quote-text","why-line")
    "s2_step4" = @("stat-num-2","stat-cap-2","quote-band","quote-mark","quote-text","why-line")
    "s2_step5" = @("quote-band","quote-mark","quote-text","why-line")
    "s2_step6" = @("why-line")
    "s2_step7" = @()

    # ---- Slide 3 (index 2) ----
    "s3_step0" = @("r1-num","r1-name","r1-desc","r1-line","r2-num","r2-name","r2-desc","r2-line","r3-num","r3-name","r3-desc","r3-line","r4-num","r4-name","r4-desc","r4-line","r5-num","r5-name","r5-desc","r5-line","note","memory-hook")
    "s3_step1" = @("r2-num","r2-name","r2-desc","r2-line","r3-num","r3-name","r3-desc","r3-line","r4-num","r4-name","r4-desc","r4-line","r5-num","r5-name","r5-desc","r5-line","note","memory-hook")
    "s3_step2" = @("r3-num","r3-name","r3-desc","r3-line","r4-num","r4-name","r4-desc","r4-line","r5-num","r5-name","r5-desc","r5-line","note","memory-hook")
    "s3_step3" = @("r4-num","r4-name","r4-desc","r4-line","r5-num","r5-name","r5-desc","r5-line","note","memory-hook")
    "s3_step4" = @("r5-num","r5-name","r5-desc","r5-line","note","memory-hook")
    "s3_step5" = @("note","memory-hook")
    "s3_step6" = @("memory-hook")
    "s3_step7" = @()

    # ---- Slide 4 (index 3) ----
    "s4_step0" = @("left-lead","left-p1","left-p2","left-p3","left-p4","v-divider","right-lead","right-p1","right-p2","right-p3","bottom-line")
    "s4_step1" = @("left-p2","left-p3","left-p4","v-divider","right-lead","right-p1","right-p2","right-p3","bottom-line")
    "s4_step2" = @("left-p3","left-p4","v-divider","right-lead","right-p1","right-p2","right-p3","bottom-line")
    "s4_step3" = @("left-p4","v-divider","right-lead","right-p1","right-p2","right-p3","bottom-line")
    "s4_step4" = @("right-lead","right-p1","right-p2","right-p3","bottom-line")
    "s4_step5" = @("right-p1","right-p2","right-p3","bottom-line")
    "s4_step6" = @("right-p2","right-p3","bottom-line")
    "s4_step7" = @("right-p3","bottom-line")
    "s4_step8" = @("bottom-line")
    "s4_step9" = @()

    # ---- Slide 5 (index 4) ----
    "s5_step0" = @("r1-num","r1-body","r1-line","r2-num","r2-body","r2-line","r3-num","r3-body","r3-line","r4-num","r4-body","note")
    "s5_step1" = @("r2-num","r2-body","r2-line","r3-num","r3-body","r3-line","r4-num","r4-body","note")
    "s5_step2" = @("r3-num","r3-body","r3-line","r4-num","r4-body","note")
    "s5_step3" = @("r4-num","r4-body","note")
    "s5_step4" = @("note")
    "s5_step5" = @()

    # ---- Slide 6 (index 5) ----
    # 表格整体作为一个 shape 控制可见性；分步高亮在 Manim 里叠加
    "s6_step0" = @("mapping-table","note")
    "s6_step1" = @("note")
    "s6_step2" = @("note")
    "s6_step3" = @("note")
    "s6_step4" = @("note")
    "s6_step5" = @()

    # ---- Slide 7 (index 6) ----
    "s7_step0" = @("p1-num","p1-body","p1-line","p2-num","p2-body","p2-line","p3-num","p3-body","closing-strip","closing-text")
    "s7_step1" = @("p2-num","p2-body","p2-line","p3-num","p3-body","closing-strip","closing-text")
    "s7_step2" = @("p3-num","p3-body","closing-strip","closing-text")
    "s7_step3" = @("closing-strip","closing-text")
    "s7_step4" = @()

    # ---- Slide 8 (index 7) ----
    "s8_step0" = @("a1-icon","a1-text","a2-icon","a2-text","a3-icon","a3-text","a4-icon","a4-text","v-divider","end-panel","end-quote-mark","end-quote","end-sign")
    "s8_step1" = @("a2-icon","a2-text","a3-icon","a3-text","a4-icon","a4-text","v-divider","end-panel","end-quote-mark","end-quote","end-sign")
    "s8_step2" = @("a3-icon","a3-text","a4-icon","a4-text","v-divider","end-panel","end-quote-mark","end-quote","end-sign")
    "s8_step3" = @("a4-icon","a4-text","v-divider","end-panel","end-quote-mark","end-quote","end-sign")
    "s8_step4" = @("v-divider","end-panel","end-quote-mark","end-quote","end-sign")
    "s8_step5" = @("end-sign")
    "s8_step6" = @()
}

# 每页对应的 slide index (0-based)
$slideIndexMap = @{
    "s1" = 0; "s2" = 1; "s3" = 2; "s4" = 3
    "s5" = 4; "s6" = 5; "s7" = 6; "s8" = 7
}

Write-Host "Opening PowerPoint..."
$pp = New-Object -ComObject PowerPoint.Application
# 不显示窗口
try { $pp.Visible = [Microsoft.Office.Core.MsoTriState]::msoFalse } catch {}

$pres = $pp.Presentations.Open($pptxPath, $true, $false, $false)  # ReadOnly, Untitled, WithWindow=false

# 先收集所有形状的原始 Visible 状态
$origVisible = @{}
foreach ($slide in $pres.Slides) {
    foreach ($shape in $slide.Shapes) {
        $key = "$($slide.SlideIndex)_$($shape.Name)"
        $origVisible[$key] = $shape.Visible
    }
}

# 按 stepMap 顺序导出
$sortedKeys = $stepMap.Keys | Sort-Object
foreach ($key in $sortedKeys) {
    $slidePrefix = $key.Split("_")[0]    # "s1"
    $slideIdx = $slideIndexMap[$slidePrefix]  # 0
    $slide = $pres.Slides.Item($slideIdx + 1)  # COM is 1-based
    $hideList = $stepMap[$key]

    # 先恢复所有形状为原始可见状态
    foreach ($shape in $slide.Shapes) {
        $shape.Visible = $origVisible["$($slide.SlideIndex)_$($shape.Name)"]
    }
    # 再隐藏本步要隐藏的形状
    foreach ($name in $hideList) {
        try {
            $shape = $slide.Shapes.Item($name)
            $shape.Visible = $false
        } catch {
            Write-Host "  WARN: shape not found on slide $slideIdx : $name"
        }
    }

    $outFile = Join-Path $outDir "$key.png"
    $slide.Export($outFile, "PNG", 2560, 1440)
    Write-Host "exported: $key.png"
}

$pres.Close()
$pp.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($pp) | Out-Null
Write-Host "`nAll done. Output:"
Get-ChildItem $outDir | Select-Object Name, Length
