# -*- coding: utf-8 -*-
"""
每日温度 — 暴力 O(n²) 演示（Manim）

样例 [5,2,2,3,7,2,6]；黑底、无旁白字幕与题面大段说明。

渲染（项目根目录）:
  1080p: manim-env2\\Scripts\\python.exe -m manim daily_temperatures_bruteforce.py DailyTemperaturesBruteForce -qh
  480p: 同上，末尾改为 -ql
"""

from __future__ import annotations

import numpy as np

from manim import *
from manim.utils.rate_functions import smooth

# 1080p @ 60fps（与 -qh 一致）
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


def _stroke_check_mark(color: str, scale: float = 0.28, stroke: float = 4.5) -> VGroup:
    """线段绘制 ✓，避免 Text/Unicode 在部分字体下出现白底杂图。"""
    s = scale
    leg = Line(
        [-0.22 * s, 0.02 * s, 0],
        [-0.06 * s, -0.14 * s, 0],
        color=color,
        stroke_width=stroke,
    )
    rise = Line(
        [-0.06 * s, -0.14 * s, 0],
        [0.24 * s, 0.18 * s, 0],
        color=color,
        stroke_width=stroke,
    )
    g = VGroup(leg, rise)
    g.set_z_index(23)
    return g


def _stroke_cross_mark(color: str, scale: float = 0.28, stroke: float = 4.5) -> VGroup:
    """线段绘制 ×，避免字体渲染异常。"""
    s = scale
    d = 0.2 * s
    return VGroup(
        Line([-d, d, 0], [d, -d, 0], color=color, stroke_width=stroke),
        Line([-d, -d, 0], [d, d, 0], color=color, stroke_width=stroke),
    ).set_z_index(23)


class DailyTemperaturesBruteForce(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        temps = [5, 2, 2, 3, 7, 2, 6]
        n = len(temps)
        max_v = max(temps)

        RED_P = "#ff4444"
        BLUE_P = "#5599ff"
        YELLOW_HL = "#ffcc00"
        GREEN_OK = "#44dd66"
        RED_BAD = "#ff5555"

        slow = 0.88
        cell_w, cell_h = 0.78, 0.52
        val_fs = 30
        stroke_box = 2.6

        # 上层两排矩阵：略上移，与条状图分离，避免拥挤
        y_temp_center = 2.42
        y_ans_center = y_temp_center - cell_h

        # 条状图：整体上移（不再贴死画面底边），柱单位高度与先前固定版一致
        BAR_MAX_H = 2.35
        # 柱底略低于画面中线偏下，保证柱底红/蓝箭头完全落在画面内、下方仍留空
        BAR_BOTTOM = -1.68

        # 红/蓝柱底箭头
        ARROW_DEPTH = 0.44
        ARROW_STROKE = 7.8
        ARROW_TIP_RATIO = 0.26
        ARROW_TAIL_PAD = 0.16

        total_w = n * cell_w
        left = -total_w / 2

        def x_center(k: int) -> float:
            return left + k * cell_w + cell_w / 2

        def cell_bottom_temp_y() -> float:
            return y_temp_center - cell_h / 2

        def bar_height(k: int) -> float:
            return (temps[k] / max_v) * BAR_MAX_H

        def bar_top_y(k: int) -> float:
            return BAR_BOTTOM + bar_height(k)

        bar_w = cell_w * 0.9

        # ---------- 第一排：温度 ----------
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
            r.move_to([x_center(k), y_temp_center, 0])
            r.set_z_index(8)
            top_boxes.append(r)
            t = Text(
                str(temps[k]),
                font_size=val_fs,
                color=WHITE,
                font="Arial",
                disable_ligatures=True,
            )
            t.move_to([x_center(k), y_temp_center, 0])
            t.set_z_index(9)
            top_nums.append(t)

        temp_label = Text(
            "temperatures",
            font_size=int(val_fs * 0.82),
            color=WHITE,
            font="Arial",
            disable_ligatures=True,
        )
        temp_label.next_to(top_boxes[0], LEFT, buff=0.12)
        temp_label.shift(LEFT * 0.22)
        temp_label.set_z_index(9)

        # ---------- 第二排：ans（与第一排同宽同高、逐列对齐） ----------
        ans_boxes: list[Rectangle] = []
        ans_texts: list[Text] = []
        for k in range(n):
            r = Rectangle(
                width=cell_w,
                height=cell_h,
                color=WHITE,
                stroke_width=stroke_box,
                fill_opacity=0,
            )
            r.move_to([x_center(k), y_ans_center, 0])
            r.set_z_index(8)
            ans_boxes.append(r)
            ph = Text("0", font_size=val_fs, color=WHITE, font="Arial", disable_ligatures=True)
            ph.move_to([x_center(k), y_ans_center, 0])
            ph.set_opacity(0)
            ph.set_z_index(9)
            ans_texts.append(ph)

        ans_label = Text(
            "ans",
            font_size=int(val_fs * 0.82),
            color=WHITE,
            font="Arial",
            disable_ligatures=True,
        )
        ans_label.next_to(ans_boxes[0], LEFT, buff=0.2)
        ans_label.set_z_index(9)

        yellow_frame = Rectangle(
            width=cell_w * 0.98,
            height=cell_h * 0.98,
            color=YELLOW_HL,
            stroke_width=4.2,
            fill_opacity=0,
        )
        yellow_frame.set_z_index(12)

        # ---------- 条状图（最底层） ----------
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
                rr.move_to([x_center(kk), BAR_BOTTOM + hh / 2, 0])
                return rr

            br = always_redraw(lambda kk=k, vt_ref=vt: make_bar_rect(kk, vt_ref))
            br.set_z_index(2)
            bar_growing.append(br)
            bar_trackers.append(vt)

        self.add(
            *top_boxes,
            *top_nums,
            temp_label,
            *ans_boxes,
            *ans_texts,
            ans_label,
            *bar_growing,
        )

        # ---------- 开场：两排方框 + temperatures / ans 标签同时出现 ----------
        t_intro = 0.55 * slow
        box_pairs: list[FadeIn] = []
        for k in range(n):
            box_pairs.append(FadeIn(top_boxes[k], scale=0.96))
            box_pairs.append(FadeIn(ans_boxes[k], scale=0.96))
        self.play(
            FadeIn(temp_label, shift=RIGHT * 0.12),
            FadeIn(ans_label, shift=RIGHT * 0.12),
            LaggedStart(
                *box_pairs,
                lag_ratio=0.04,
                run_time=t_intro * 1.35,
            ),
            rate_func=smooth,
        )
        self.play(
            LaggedStart(*[FadeIn(t, scale=0.92) for t in top_nums], lag_ratio=0.0, run_time=0.2 * slow),
            rate_func=smooth,
        )
        self.wait(0.2 * slow)

        # ---------- 从左到右：红箭头 + 条状生长（箭头自第一排底边指向柱） ----------
        y_bot_cell = cell_bottom_temp_y()
        t_grow = 0.78 * slow

        for k in range(n):
            xk = x_center(k)
            tip_y = BAR_BOTTOM + 0.02
            arr_down = Arrow(
                [xk, y_bot_cell, 0],
                [xk, tip_y, 0],
                color=RED_P,
                stroke_width=5.2,
                buff=0.0,
                max_tip_length_to_length_ratio=0.22,
            )
            arr_down.set_z_index(18)
            self.play(FadeIn(arr_down, scale=0.9), run_time=0.18 * slow, rate_func=smooth)

            vt = bar_trackers[k]
            target_h = bar_height(k)
            self.play(
                AnimationGroup(
                    FadeOut(arr_down, run_time=0.08),
                    vt.animate.set_value(target_h),
                    lag_ratio=0.0,
                ),
                run_time=t_grow,
                rate_func=smooth,
            )
            self.wait(0.06 * slow)

        self.wait(0.35 * slow)

        for br in bar_growing:
            self.remove(br)
        bar_rects: list[Rectangle] = []
        for k in range(n):
            h = bar_height(k)
            rr = Rectangle(
                width=bar_w,
                height=h,
                color=WHITE,
                stroke_width=stroke_box,
                fill_opacity=0,
            )
            rr.move_to([x_center(k), BAR_BOTTOM + h / 2, 0])
            rr.set_z_index(2)
            bar_rects.append(rr)
        self.add(*bar_rects)

        # 柱下方 1-based 下标 [1]..[n]（在柱底箭头之下）
        idx_fs = 21
        idx_y = BAR_BOTTOM - ARROW_DEPTH - ARROW_TAIL_PAD - 0.22
        idx_labels: list[Text] = []
        for k in range(n):
            lb = Text(
                f"[{k + 1}]",
                font_size=idx_fs,
                color=WHITE,
                font="Arial",
                disable_ligatures=True,
            )
            lb.move_to([x_center(k), idx_y, 0])
            lb.set_z_index(6)
            idx_labels.append(lb)
        self.play(
            LaggedStart(
                *[FadeIn(m, scale=0.92) for m in idx_labels],
                lag_ratio=0.05,
                run_time=0.48 * slow,
            ),
            rate_func=smooth,
        )
        self.wait(0.15 * slow)

        def make_up_arrow(idx: int, color: str) -> Arrow:
            x = x_center(idx)
            return Arrow(
                [x, BAR_BOTTOM - ARROW_DEPTH - ARROW_TAIL_PAD, 0],
                [x, BAR_BOTTOM - 0.02, 0],
                color=color,
                stroke_width=ARROW_STROKE,
                buff=0.0,
                max_tip_length_to_length_ratio=ARROW_TIP_RATIO,
            ).set_z_index(20)

        def curved_match_arrow(i_idx: int, j_idx: int) -> CurvedArrow:
            xi, xj = x_center(i_idx), x_center(j_idx)
            yti, ytj = bar_top_y(i_idx), bar_top_y(j_idx)
            p0 = np.array([xi, yti + 0.12, 0.0])
            p1 = np.array([xj, ytj + 0.12, 0.0])
            half = float(np.linalg.norm(p1 - p0)) / 2.0
            rad = max(half * 1.35, 0.55)
            return CurvedArrow(
                p0,
                p1,
                color=RED_P,
                stroke_width=5.0,
                radius=-rad,
            ).set_z_index(22)

        def digit_txt(s: str) -> Text:
            return Text(
                s,
                font_size=val_fs,
                color=WHITE,
                font="Arial",
                disable_ligatures=True,
            )

        t_flash = 0.45 * slow
        t_arc = 0.5 * slow

        # 外层 i：从后往前（蓝箭头）；内层 j：从左往右 i+1..n-1（红箭头）
        arrow_i = make_up_arrow(n - 1, BLUE_P)

        for i in range(n - 1, -1, -1):
            yellow_frame.move_to([x_center(i), y_temp_center, 0])
            self.play(FadeIn(yellow_frame, scale=0.96), run_time=0.28 * slow, rate_func=smooth)

            if i == n - 1:
                self.play(FadeIn(arrow_i, scale=0.9), run_time=0.22 * slow, rate_func=smooth)

            found = False
            arrow_j: Arrow | None = None

            for j in range(i + 1, n):
                ra = make_up_arrow(j, RED_P)
                if arrow_j is None:
                    arrow_j = ra
                    self.play(FadeIn(arrow_j, scale=0.9), run_time=0.24 * slow, rate_func=smooth)
                else:
                    self.play(ReplacementTransform(arrow_j, ra), run_time=0.28 * slow, rate_func=smooth)
                    arrow_j = ra

                self.wait(0.2 * slow)

                if temps[j] > temps[i]:
                    found = True
                    arc = curved_match_arrow(i, j)
                    xj = x_center(j)
                    ytj = bar_top_y(j)

                    check = _stroke_check_mark(GREEN_OK, scale=0.32, stroke=5.0)
                    check.move_to([xj, ytj + 0.52, 0])

                    self.play(Create(arc, run_time=t_arc * 0.85), rate_func=smooth)
                    self.play(
                        bar_rects[j].animate.set_stroke(GREEN_OK, width=5.5),
                        FadeIn(check, scale=0.85),
                        run_time=0.28 * slow,
                        rate_func=smooth,
                    )
                    self.wait(0.22 * slow)

                    # 答案：下一个更高温所在柱的 1-based 下标
                    ans_val = str(j + 1)
                    new_ans = digit_txt(ans_val)
                    new_ans.move_to([x_center(i), y_ans_center, 0])
                    new_ans.set_z_index(9)

                    self.play(
                        FadeOut(arc),
                        FadeOut(check),
                        FadeOut(arrow_j),
                        bar_rects[j].animate.set_stroke(WHITE, width=stroke_box),
                        ReplacementTransform(ans_texts[i], new_ans),
                        run_time=t_flash * 0.75,
                        rate_func=smooth,
                    )
                    ans_texts[i] = new_ans
                    arrow_j = None
                    break

                self.play(FadeOut(arrow_j, run_time=0.14 * slow), rate_func=smooth)
                arrow_j = None
                self.wait(0.12 * slow)

            if not found:
                cross = _stroke_cross_mark(RED_BAD, scale=0.34, stroke=5.0)
                cross.move_to([x_center(i), bar_top_y(i) + 0.5, 0])
                new_zero = digit_txt("0")
                new_zero.move_to([x_center(i), y_ans_center, 0])
                new_zero.set_z_index(9)
                self.play(
                    bar_rects[i].animate.set_stroke(RED_BAD, width=5.5),
                    FadeIn(cross, scale=0.85),
                    run_time=0.3 * slow,
                    rate_func=smooth,
                )
                self.wait(0.28 * slow)
                self.play(
                    FadeOut(cross),
                    bar_rects[i].animate.set_stroke(WHITE, width=stroke_box),
                    ReplacementTransform(ans_texts[i], new_zero),
                    run_time=t_flash * 0.85,
                    rate_func=smooth,
                )
                ans_texts[i] = new_zero

            self.play(FadeOut(yellow_frame, scale=0.96), run_time=0.24 * slow, rate_func=smooth)

            if i > 0:
                na = make_up_arrow(i - 1, BLUE_P)
                self.play(ReplacementTransform(arrow_i, na), run_time=0.32 * slow, rate_func=smooth)
                arrow_i = na

        self.play(FadeOut(arrow_i), run_time=0.35 * slow, rate_func=smooth)
        self.wait(0.6 * slow)
