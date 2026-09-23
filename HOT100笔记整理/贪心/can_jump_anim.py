# -*- coding: utf-8 -*-
"""
LeetCode 55 跳跃游戏 — 贪心维护最远可达 max_reach（Manim）

上层样例 [2,3,1,1,4]（可达）；下层 [3,2,1,0,4]（不可达）。黑底、白格、红指针与弧箭、黄框当前格、
虚线 right（仅向右延伸时移动）、成功绿勾 / 失败红叉与抖动。

逻辑画幅 16:9。成片 1080p（1920×1080，目录一般为 1080p60）:
  py -m manim can_jump_anim.py CanJumpDemo -qh --disable_caching

上层可达样例会遍历完整个数组（不因已能到终点而提前结束）；下层不可达样例逻辑不变。
"""

from __future__ import annotations

import numpy as np

from manim import *
from manim.utils.rate_functions import smooth

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


def _stroke_cross_red(scale: float = 0.42, stroke: float = 5.2) -> VGroup:
    s = scale
    d = 0.22 * s
    return VGroup(
        Line([-d, d, 0], [d, -d, 0], color="#ff3333", stroke_width=stroke),
        Line([-d, -d, 0], [d, d, 0], color="#ff3333", stroke_width=stroke),
    )


def _check_green(scale: float = 0.48, stroke: float = 5.0) -> VGroup:
    s = scale
    p1 = np.array([-0.28 * s, 0.02 * s, 0.0])
    p2 = np.array([-0.08 * s, -0.18 * s, 0.0])
    p3 = np.array([0.32 * s, 0.22 * s, 0.0])
    return VGroup(
        Line(p1, p2, color=GREEN_B, stroke_width=stroke),
        Line(p2, p3, color=GREEN_B, stroke_width=stroke),
    )


class CanJumpDemo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        RED_P = "#ff3333"
        YELLOW_P = "#ffcc22"
        DASH_COLOR = "#4499ee"
        RIGHT_LAB_COLOR = "#9ecfff"

        slow = 1.05
        cell_w, cell_h = 0.56, 0.5
        buff_x = 0.16
        val_fs = 26
        idx_fs = 20
        lbl_fs = 24
        stroke_box = 2.6

        y_top = 1.42
        y_bot = -1.42

        nums_good = [2, 3, 1, 1, 4]
        nums_bad = [3, 2, 1, 0, 4]

        def build_row(nums: list[int], y_center: float) -> dict:
            n = len(nums)
            unit_w = cell_w + buff_x
            total_w = n * cell_w + max(n - 1, 0) * buff_x
            left_x = -total_w / 2

            def cell_left_x(k: int) -> float:
                return left_x + k * unit_w

            def cell_center(k: int) -> np.ndarray:
                return np.array([cell_left_x(k) + cell_w / 2, y_center, 0])

            def top_mid(k: int) -> np.ndarray:
                return np.array([cell_left_x(k) + cell_w / 2, y_center + cell_h / 2, 0])

            boxes: list[Rectangle] = []
            vals: list[Text] = []
            cols: list[VGroup] = []
            for k in range(n):
                r = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    color=WHITE,
                    stroke_width=stroke_box,
                    fill_opacity=0,
                )
                r.move_to(cell_center(k))
                t = Text(
                    str(nums[k]),
                    font_size=val_fs,
                    color=WHITE,
                    font="Consolas",
                    disable_ligatures=True,
                )
                t.move_to(cell_center(k))
                boxes.append(r)
                vals.append(t)
                cols.append(VGroup(r, t))

            nums_lbl = Text("nums", font_size=lbl_fs, color=WHITE, font="Consolas")
            nums_lbl.next_to(boxes[0], LEFT, buff=0.38)

            idx_y = y_center - cell_h / 2 - 0.36
            idx_txts: list[Text] = []
            for k in range(n):
                it = Text(f"[{k}]", font_size=idx_fs, color=GREY_A, font="Consolas")
                it.move_to(np.array([cell_center(k)[0], idx_y, 0]))
                idx_txts.append(it)

            return {
                "nums": nums,
                "n": n,
                "y": y_center,
                "unit_w": unit_w,
                "left_x": left_x,
                "cell_left_x": cell_left_x,
                "cell_center": cell_center,
                "top_mid": top_mid,
                "boxes": boxes,
                "vals": vals,
                "cols": cols,
                "nums_lbl": nums_lbl,
                "idx_txts": idx_txts,
                "idx_y": idx_y,
            }

        row_a = build_row(nums_good, y_top)
        row_b = build_row(nums_bad, y_bot)

        # 开场：两行同时出现
        t_in = 0.55 * slow
        g_top = VGroup(row_a["nums_lbl"], *row_a["cols"], *row_a["idx_txts"])
        g_bot = VGroup(row_b["nums_lbl"], *row_b["cols"], *row_b["idx_txts"])
        self.play(
            FadeIn(g_top, shift=UP * 0.05),
            FadeIn(g_bot, shift=DOWN * 0.05),
            run_time=t_in,
            rate_func=smooth,
        )
        self.wait(0.45 * slow)

        def gap_x_after_max_reach(r: int, row: dict) -> float:
            n = row["n"]
            if r >= n - 1:
                return row["cell_left_x"](n - 1) + cell_w + buff_x * 0.65 + 0.08
            return row["cell_left_x"](r) + cell_w + buff_x / 2

        def make_right_marker(x: float, y_center: float) -> VGroup:
            h = 3 * cell_w
            line = DashedLine(
                [x, y_center - h / 2, 0],
                [x, y_center + h / 2, 0],
                color=DASH_COLOR,
                stroke_width=2.8,
                dash_length=0.1,
                dashed_ratio=0.55,
            )
            lab = Text("right", font_size=18, color=RIGHT_LAB_COLOR, font="Consolas")
            lab.move_to(np.array([x + 0.22, y_center + h / 2 + 0.12, 0]))
            g = VGroup(line, lab)
            g.set_z_index(6)
            return g

        def pointer_arrow(row: dict, i: int) -> Arrow:
            top = row["top_mid"](i)
            start = top + UP * 0.38
            arr = Arrow(
                start,
                top,
                color=RED_P,
                stroke_width=5.0,
                buff=0.0,
                max_tip_length_to_length_ratio=0.28,
            )
            arr.set_z_index(15)
            return arr

        def run_demo(row: dict, success: bool) -> None:
            nums = row["nums"]
            n = row["n"]
            yc = row["y"]

            max_reach = 0
            gx0 = gap_x_after_max_reach(max_reach, row)
            right_mob = make_right_marker(gx0, yc)
            self.play(FadeIn(right_mob, scale=0.95), run_time=0.42 * slow)

            ptr = pointer_arrow(row, 0)
            self.play(FadeIn(ptr, shift=UP * 0.12), run_time=0.38 * slow)

            t_arc = 0.55 * slow
            t_move_line = 0.62 * slow
            t_fade_y = 0.35 * slow

            check_shown = False

            for i in range(n):
                # 指针移到 i
                new_ptr = pointer_arrow(row, i)
                self.play(Transform(ptr, new_ptr), run_time=0.45 * slow, rate_func=smooth)

                if i > max_reach:
                    yb = Rectangle(
                        width=cell_w + 0.06,
                        height=cell_h + 0.06,
                        color=YELLOW_P,
                        stroke_width=4.0,
                        fill_opacity=0,
                    )
                    yb.move_to(row["cell_center"](i))
                    yb.set_z_index(10)
                    self.play(Create(yb), run_time=0.35 * slow)
                    self.wait(0.22 * slow)
                    col = row["cols"][i]
                    d = 0.07
                    self.play(col.animate.shift(RIGHT * d), run_time=0.1 * slow)
                    self.play(col.animate.shift(LEFT * 2 * d), run_time=0.1 * slow)
                    self.play(col.animate.shift(RIGHT * 2 * d), run_time=0.1 * slow)
                    self.play(col.animate.shift(LEFT * 2 * d), run_time=0.1 * slow)
                    self.play(col.animate.shift(RIGHT * d), run_time=0.1 * slow)
                    cross = _stroke_cross_red(scale=0.55, stroke=5.0)
                    cross.next_to(right_mob[1], RIGHT, buff=0.2)
                    cross.set_y(right_mob[1].get_y())
                    cross.set_z_index(20)
                    self.play(FadeIn(cross, scale=0.85), run_time=0.4 * slow)
                    self.wait(0.55 * slow)
                    self.play(FadeOut(yb), FadeOut(ptr), run_time=0.35 * slow)
                    return

                yb = Rectangle(
                    width=cell_w + 0.04,
                    height=cell_h + 0.04,
                    color=YELLOW_P,
                    stroke_width=3.8,
                    fill_opacity=0,
                )
                yb.move_to(row["cell_center"](i))
                yb.set_z_index(10)
                self.play(Create(yb), run_time=0.38 * slow)

                j = min(i + nums[i], n - 1)
                arc: Mobject | None = None
                if j != i:
                    a0 = row["top_mid"](i) + UP * 0.02 + RIGHT * 0.02
                    a1 = row["top_mid"](j) + UP * 0.02 + LEFT * 0.02
                    arc = CurvedArrow(
                        a0,
                        a1,
                        angle=-TAU / 5.0,
                        color=RED_P,
                        stroke_width=2.35,
                    )
                    arc.set_z_index(12)
                    self.play(Create(arc), run_time=t_arc, rate_func=smooth)
                    self.wait(0.18 * slow)
                else:
                    self.wait(0.22 * slow)

                new_mr = max(max_reach, i + nums[i])
                if new_mr > max_reach:
                    max_reach = new_mr
                    gx = gap_x_after_max_reach(max_reach, row)
                    new_rm = make_right_marker(gx, yc)
                    self.play(
                        ReplacementTransform(right_mob, new_rm),
                        run_time=t_move_line,
                        rate_func=smooth,
                    )
                    right_mob = new_rm

                if max_reach >= n - 1 and not check_shown:
                    chk = _check_green(scale=0.62, stroke=5.5)
                    chk.next_to(right_mob[1], RIGHT, buff=0.2)
                    chk.set_y(right_mob[1].get_y())
                    chk.set_z_index(20)
                    self.play(FadeIn(chk, scale=0.9), run_time=0.45 * slow)
                    self.wait(0.35 * slow)
                    check_shown = True

                self.wait(0.15 * slow)
                anims2 = [FadeOut(yb)]
                if arc is not None:
                    anims2.append(FadeOut(arc))
                self.play(*anims2, run_time=t_fade_y)

                if max_reach >= n - 1 and not success:
                    break

            if success and not check_shown:
                chk = _check_green(scale=0.62, stroke=5.5)
                chk.next_to(right_mob[1], RIGHT, buff=0.2)
                chk.set_y(right_mob[1].get_y())
                chk.set_z_index(20)
                self.play(FadeIn(chk, scale=0.9), run_time=0.45 * slow)
                self.wait(0.35 * slow)

            self.play(FadeOut(ptr), run_time=0.35 * slow)
            self.wait(0.4 * slow)

        # 上层
        run_demo(row_a, success=True)
        self.wait(0.5 * slow)

        # 下层
        run_demo(row_b, success=False)

        self.wait(0.85 * slow)
