# -*- coding: utf-8 -*-
"""
132 模式 — 从左向右枚举「2」、找左侧第一个更大的「3」、再看「3」左侧前缀最小「1」（Manim）

本文件（与脚本同名的唯一 Manim 源文件）:
  daily_temperatures_monotonic_stack.py
场景类名必须写对（否则渲染的是别的工程里的旧文件 / 或报错）:
  Pattern132Demo

样例 nums = [5, 3, 6, 1, 4, 0, 7, 2, 8]（长度 9）。黑底；上层 nums 逐格红箭下落生长柱后淡出；下层柱状图水平居中；
蓝色扫描箭头从左向右。成功时柱描边为蓝/红/绿（「1」「2」「3」文字同色）；**首次成功后仍继续枚举直至 k=n-1**。比较式在整排柱「水平正中、最高柱上方」。

视频：逻辑画幅 16:9；config 为 1080p（1920×1080）。导出 mp4 默认路径（相对本文件所在目录）:
  media/videos/daily_temperatures_monotonic_stack/1080p60/Pattern132Demo.mp4
若看起来「没更新」，请确认播放器打开的是上述路径下的新文件；并建议加 --disable_caching 强制重算。

渲染（在「出题\\lc」目录下执行）:
  py -m manim daily_temperatures_monotonic_stack.py Pattern132Demo -qh --disable_caching
"""

from __future__ import annotations

import numpy as np

from manim import *
from manim.utils.rate_functions import smooth

# 1080p @ 60fps
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


def _stroke_cross_mark(color: str, scale: float = 0.28, stroke: float = 4.5) -> VGroup:
    s = scale
    d = 0.2 * s
    return VGroup(
        Line([-d, d, 0], [d, -d, 0], color=color, stroke_width=stroke),
        Line([-d, -d, 0], [d, d, 0], color=color, stroke_width=stroke),
    ).set_z_index(23)


def _check_mark_green(scale: float = 0.32, stroke: float = 4.2) -> VGroup:
    """简易绿色勾（粗线）。"""
    s = scale
    p1 = np.array([-0.22 * s, 0.0, 0.0])
    p2 = np.array([-0.05 * s, -0.14 * s, 0.0])
    p3 = np.array([0.26 * s, 0.18 * s, 0.0])
    return VGroup(
        Line(p1, p2, color=GREEN, stroke_width=stroke),
        Line(p2, p3, color=GREEN, stroke_width=stroke),
    ).set_z_index(24)


class Pattern132Demo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        nums = [5, 3, 6, 1, 4, 0, 7, 2, 8]
        n = len(nums)
        max_v = max(nums) if max(nums) > 0 else 1

        RED_P = "#ff4444"
        BLUE_P = "#5599ff"
        RED_BAD = "#ff5555"
        GREEN_BORDER = "#44dd66"
        GREEN_OK = "#44dd66"

        slow = 0.95
        geom_scale = 1.14
        cell_w, cell_h = 0.48 * geom_scale, 0.44 * geom_scale
        val_fs = 22
        stroke_box = 2.4

        y_nums_center = 2.58

        BAR_MAX_H = 1.52 * geom_scale
        BAR_BOTTOM = -1.52

        ARROW_DEPTH = 0.42
        ARROW_STROKE = 6.2
        ARROW_TIP_RATIO = 0.24
        ARROW_TAIL_PAD = 0.12

        total_w = n * cell_w
        left = -total_w / 2
        bar_panel_shift_x = 0.0

        def x_top(k: int) -> float:
            return left + k * cell_w + cell_w / 2

        def x_bar(k: int) -> float:
            return x_top(k) + bar_panel_shift_x

        def cell_bottom_nums_y() -> float:
            return y_nums_center - cell_h / 2

        def bar_height(k: int) -> float:
            v = nums[k]
            r = v / max_v
            if v == 0:
                r = max(r, 0.1)
            return r * BAR_MAX_H

        def bar_top_y(k: int) -> float:
            return BAR_BOTTOM + bar_height(k)

        bar_w = cell_w * 0.88

        # ---------- 上层：单行 nums ----------
        top_boxes: list[Rectangle] = []
        top_nums: list[Text] = []
        for k in range(n):
            r = Rectangle(
                width=cell_w,
                height=cell_h,
                color=WHITE,
                stroke_width=stroke_box,
                fill_opacity=0,
            )
            r.move_to([x_top(k), y_nums_center, 0])
            r.set_z_index(8)
            top_boxes.append(r)
            t = Text(
                str(nums[k]),
                font_size=val_fs,
                color=WHITE,
                font="Arial",
                disable_ligatures=True,
            )
            t.move_to([x_top(k), y_nums_center, 0])
            t.set_z_index(9)
            top_nums.append(t)

        nums_label = Text(
            "nums",
            font_size=int(val_fs * 0.98),
            color=WHITE,
            font="Arial",
            disable_ligatures=True,
        )
        nums_label.next_to(top_boxes[0], LEFT, buff=0.1)
        nums_label.shift(LEFT * 0.12)
        nums_label.set_z_index(9)

        self.add(*top_boxes, *top_nums, nums_label)

        # ---------- 开场：上层 nums ----------
        t_intro = 0.5 * slow
        self.play(
            FadeIn(nums_label, shift=RIGHT * 0.08),
            LaggedStart(*[FadeIn(top_boxes[k], scale=0.96) for k in range(n)], lag_ratio=0.03, run_time=t_intro * 1.15),
            rate_func=smooth,
        )
        self.play(
            LaggedStart(*[FadeIn(t, scale=0.92) for t in top_nums], lag_ratio=0.0, run_time=0.18 * slow),
            rate_func=smooth,
        )
        self.wait(0.12 * slow)

        y_bot_cell = cell_bottom_nums_y()
        t_grow = 0.68 * slow

        bar_trackers: list[ValueTracker] = []
        bar_growing: list[Mobject] = []
        for k in range(n):
            h0 = 0.04
            vt = ValueTracker(h0)

            def make_bar_rect(kk: int = k, vt_ref: ValueTracker = vt) -> Rectangle:
                hh = max(0.04, vt_ref.get_value())
                rr = Rectangle(
                    width=bar_w,
                    height=hh,
                    color=WHITE,
                    stroke_width=stroke_box,
                    fill_opacity=0,
                )
                rr.move_to([x_bar(kk), BAR_BOTTOM + hh / 2, 0])
                return rr

            br = always_redraw(lambda kk=k, vt_ref=vt: make_bar_rect(kk, vt_ref))
            br.set_z_index(2)
            bar_growing.append(br)
            bar_trackers.append(vt)

        self.add(*bar_growing)

        for k in range(n):
            tip_y = BAR_BOTTOM + 0.02
            arr_down = Arrow(
                [x_top(k), y_bot_cell, 0],
                [x_bar(k), tip_y, 0],
                color=RED_P,
                stroke_width=4.6,
                buff=0.0,
                max_tip_length_to_length_ratio=0.22,
            )
            arr_down.set_z_index(18)
            self.play(FadeIn(arr_down, scale=0.9), run_time=0.14 * slow, rate_func=smooth)

            vt = bar_trackers[k]
            target_h = bar_height(k)
            self.play(
                AnimationGroup(
                    FadeOut(arr_down, run_time=0.06),
                    vt.animate.set_value(target_h),
                    lag_ratio=0.0,
                ),
                run_time=t_grow,
                rate_func=smooth,
            )
            self.wait(0.04 * slow)

        self.wait(0.2 * slow)

        # 条状图就位后：上层 nums 整行消失
        self.play(
            FadeOut(nums_label),
            FadeOut(VGroup(*top_boxes, *top_nums)),
            run_time=0.45 * slow,
            rate_func=smooth,
        )

        for br in bar_growing:
            self.remove(br)
        bar_rects: list[VGroup] = []
        bar_val_fs = int(val_fs * 0.62)
        for k in range(n):
            h = bar_height(k)
            rr = Rectangle(
                width=bar_w,
                height=h,
                color=WHITE,
                stroke_width=stroke_box,
                fill_opacity=0,
            )
            cy = BAR_BOTTOM + h / 2
            rr.move_to([x_bar(k), cy, 0])
            tv = Text(
                str(nums[k]),
                font_size=bar_val_fs,
                color=WHITE,
                font="Arial",
                disable_ligatures=True,
            )
            tv.move_to([x_bar(k), cy, 0])
            tv.set_z_index(3)
            rr.set_z_index(2)
            col = VGroup(rr, tv)
            col.set_z_index(2)
            bar_rects.append(col)
        self.add(*bar_rects)

        def make_scan_arrow(idx: int, color: str) -> Arrow:
            x = x_bar(idx)
            return Arrow(
                [x, BAR_BOTTOM - ARROW_DEPTH - ARROW_TAIL_PAD - 0.28, 0],
                [x, BAR_BOTTOM - 0.02, 0],
                color=color,
                stroke_width=ARROW_STROKE,
                buff=0.0,
                max_tip_length_to_length_ratio=ARROW_TIP_RATIO,
            ).set_z_index(20)

        def curved_arrow_up(k_idx: int, j_idx: int, color: str) -> CurvedArrow:
            xi = x_bar(k_idx)
            yti = bar_top_y(k_idx)
            xj = x_bar(j_idx)
            ytj = bar_top_y(j_idx)
            p0 = np.array([xi, yti + 0.08, 0.0])
            p1 = np.array([xj, ytj + 0.08, 0.0])
            half = float(np.linalg.norm(p1 - p0)) / 2.0
            rad = max(half * 1.22, 0.42)
            # 正半径：弧朝「左」侧凸出；此处 p0 在右、p1 在左，凸向画面上方
            return CurvedArrow(
                p0,
                p1,
                color=color,
                stroke_width=4.0,
                radius=rad,
            ).set_z_index(22)

        def cmp_text_chart_center_above(dy_pad: float = 0.55) -> np.ndarray:
            """整体柱状图水平正中、最高柱顶再向上 dy_pad（比较式统一放这里）。"""
            x_c = (x_bar(0) + x_bar(n - 1)) / 2.0
            y_top = max(bar_top_y(i) for i in range(n))
            return np.array([float(x_c), float(y_top) + dy_pad, 0.0])

        def first_larger_left(k: int) -> int:
            for t in range(k - 1, -1, -1):
                if nums[t] > nums[k]:
                    return t
            return -1

        def prefix_min_index(j: int) -> tuple[float, int]:
            """[0, j) 上最小值及最左达到最小的下标。"""
            if j <= 0:
                return float("inf"), -1
            best = nums[0]
            best_i = 0
            for t in range(1, j):
                if nums[t] < best:
                    best = nums[t]
                    best_i = t
            return float(best), best_i

        def brace_prefix_under(j: int) -> tuple[Mobject, Text]:
            """[0..j-1] 各柱底下方：仅花括号（无横线）+ min=。"""
            if j <= 0:
                raise ValueError("j must be > 0")
            y_attach = BAR_BOTTOM - 0.04
            p0 = np.array([x_bar(0) - bar_w * 0.5, y_attach, 0.0])
            p1 = np.array([x_bar(j - 1) + bar_w * 0.5, y_attach, 0.0])
            br = BraceBetweenPoints(p0, p1, direction=DOWN, color=WHITE)
            br.set_z_index(11)
            mn, _ = prefix_min_index(j)
            tx = Text(
                f"min={int(mn)}",
                font_size=18,
                color=WHITE,
                font="Microsoft YaHei",
                disable_ligatures=True,
            )
            tx.next_to(br, DOWN, buff=0.07)
            tx.set_z_index(12)
            return br, tx

        arrow_scan = make_scan_arrow(0, BLUE_P)
        self.play(FadeIn(arrow_scan, scale=0.9), run_time=0.26 * slow, rate_func=smooth)

        for k in range(n):
            na = make_scan_arrow(k, BLUE_P)
            self.play(ReplacementTransform(arrow_scan, na), run_time=0.28 * slow, rate_func=smooth)
            arrow_scan = na

            j = first_larger_left(k)
            overlay: list[Mobject] = []

            if j < 0:
                cross = _stroke_cross_mark(RED_BAD, scale=0.3, stroke=4.0)
                cross.move_to([x_bar(k), bar_top_y(k) + 0.38, 0])
                self.play(
                    bar_rects[k][0].animate.set_stroke(RED_BAD, width=5.0),
                    FadeIn(cross, scale=0.85),
                    run_time=0.32 * slow,
                    rate_func=smooth,
                )
                self.wait(0.2 * slow)
                self.play(
                    FadeOut(cross),
                    bar_rects[k][0].animate.set_stroke(WHITE, width=stroke_box),
                    run_time=0.36 * slow,
                    rate_func=smooth,
                )
                continue

            mn, i_star = prefix_min_index(j)
            ca = curved_arrow_up(k, j, RED_P)
            arc_mid = ca.point_from_proportion(0.5) + UP * 0.35

            self.play(
                bar_rects[k][0].animate.set_stroke(RED_BAD, width=5.2),
                bar_rects[j][0].animate.set_stroke(GREEN_BORDER, width=5.2),
                Create(ca, run_time=0.4 * slow),
                rate_func=smooth,
            )
            overlay.append(ca)

            if j > 0:
                brace_mob, min_txt = brace_prefix_under(j)
                self.play(
                    FadeIn(brace_mob, shift=DOWN * 0.05),
                    FadeIn(min_txt, shift=DOWN * 0.03),
                    run_time=0.34 * slow,
                )
                overlay.extend([brace_mob, min_txt])

            if i_star >= 0:
                self.play(
                    bar_rects[i_star][0].animate.set_stroke(BLUE_P, width=5.0),
                    run_time=0.26 * slow,
                    rate_func=smooth,
                )

            ok = i_star >= 0 and mn < nums[k]
            if not ok:
                fail_vis: list[Mobject] = []
                if i_star >= 0 and mn == nums[k]:
                    eq = Text(
                        f"{int(nums[k])}={int(mn)}",
                        font_size=int(val_fs * 0.78),
                        color=RED_BAD,
                        font="Arial",
                        disable_ligatures=True,
                    )
                    eq.move_to(cmp_text_chart_center_above(0.55))
                    eq.set_z_index(27)
                    fail_vis.append(eq)
                elif i_star >= 0 and mn > nums[k]:
                    gt = Text(
                        f"{int(mn)}>{int(nums[k])}",
                        font_size=int(val_fs * 0.78),
                        color=RED_BAD,
                        font="Arial",
                        disable_ligatures=True,
                    )
                    gt.move_to(cmp_text_chart_center_above(0.55))
                    gt.set_z_index(27)
                    fail_vis.append(gt)
                x_arc = _stroke_cross_mark(RED_BAD, scale=0.26, stroke=3.8)
                x_arc.move_to(arc_mid)
                fail_vis.append(x_arc)
                if len(fail_vis) == 2:
                    self.play(
                        FadeIn(fail_vis[0], shift=UP * 0.05),
                        FadeIn(fail_vis[1], scale=0.85),
                        run_time=0.3 * slow,
                    )
                else:
                    self.play(FadeIn(fail_vis[0], scale=0.85), run_time=0.3 * slow)
                overlay.extend(fail_vis)
                self.wait(0.28 * slow)

                fade_strokes = [
                    bar_rects[k][0].animate.set_stroke(WHITE, width=stroke_box),
                    bar_rects[j][0].animate.set_stroke(WHITE, width=stroke_box),
                ]
                if i_star >= 0:
                    fade_strokes.append(bar_rects[i_star][0].animate.set_stroke(WHITE, width=stroke_box))
                self.play(
                    *[FadeOut(m) for m in overlay],
                    *fade_strokes,
                    run_time=0.4 * slow,
                    rate_func=smooth,
                )
                continue

            # 成功：「1」蓝、「2」红、「3」绿 + 绿勾、三柱抖动
            t1 = Text('"1"', font_size=int(val_fs * 0.95), color=BLUE_P, font="Arial", disable_ligatures=True)
            t2 = Text('"2"', font_size=int(val_fs * 0.95), color=RED_P, font="Arial", disable_ligatures=True)
            t3 = Text('"3"', font_size=int(val_fs * 0.95), color=GREEN_BORDER, font="Arial", disable_ligatures=True)
            t1.move_to([x_bar(i_star), bar_top_y(i_star) + 0.48, 0])
            t2.move_to([x_bar(k), bar_top_y(k) + 0.48, 0])
            t3.move_to([x_bar(j), bar_top_y(j) + 0.48, 0])
            for t in (t1, t2, t3):
                t.set_z_index(26)
            chk = _check_mark_green(scale=0.34, stroke=4.4)
            chk.move_to(arc_mid + UP * 0.08)
            cmp_ok = Text(
                f"{int(mn)}<{int(nums[k])}",
                font_size=int(val_fs * 0.82),
                color=GREEN_OK,
                font="Arial",
                disable_ligatures=True,
            )
            cmp_ok.move_to(cmp_text_chart_center_above(0.58))
            cmp_ok.set_z_index(27)

            self.play(
                FadeIn(t1, shift=DOWN * 0.06),
                FadeIn(t2, shift=DOWN * 0.06),
                FadeIn(t3, shift=DOWN * 0.06),
                FadeIn(cmp_ok, shift=UP * 0.04),
                FadeIn(chk, scale=0.9),
                run_time=0.42 * slow,
                rate_func=smooth,
            )
            trio = VGroup(bar_rects[i_star], bar_rects[k], bar_rects[j])
            self.play(Wiggle(trio, scale_value=1.04, rotation_angle=0.03 * TAU), run_time=0.82 * slow)
            self.wait(0.55 * slow)
            self.play(
                FadeOut(VGroup(t1, t2, t3, cmp_ok, chk)),
                *[FadeOut(m) for m in overlay],
                bar_rects[k][0].animate.set_stroke(WHITE, width=stroke_box),
                bar_rects[j][0].animate.set_stroke(WHITE, width=stroke_box),
                bar_rects[i_star][0].animate.set_stroke(WHITE, width=stroke_box),
                run_time=0.45 * slow,
                rate_func=smooth,
            )
            continue

        self.play(FadeOut(arrow_scan), run_time=0.3 * slow, rate_func=smooth)
        self.wait(0.45 * slow)
