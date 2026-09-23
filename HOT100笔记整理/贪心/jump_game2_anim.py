# -*- coding: utf-8 -*-
"""
LeetCode 45 跳跃游戏 II — 最少跳跃次数（Manim）

样例 n=12, nums=[2,4,3,4,1,2,4,3,5,1,2,6]（输入格式：首行 n，次行 n 个数）；单行居中；蓝虚线旁 end、红虚线旁 right（蓝=curEnd、红=maxReach）；
绿框仅在 ans 更新时重画，表示下一跳搜索区间 [旧 curEnd+1, 新 curEnd]；绿框上方白色层号，与 ans 同步（1,2,3…）并随框移动。
绿框表示 (i+1)..maxReach 搜索区间；红指针 + 红色上凸弧箭；下方 ans。

成片 1080p（1920×1080）:
  py -m manim jump_game2_anim.py JumpGame2Demo -qh --disable_caching

480p 预览:
  py -m manim jump_game2_anim.py JumpGame2Demo -ql --disable_caching
"""

from __future__ import annotations

import numpy as np

from manim import *
from manim.utils.rate_functions import smooth

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


class JumpGame2Demo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        RED_P = "#ff3333"
        GREEN_P = "#44cc66"
        RIGHT_DASH = "#4499ee"
        RIGHT_LAB = "#9ecfff"
        END_DASH = "#ff5555"
        END_LAB = "#ff9999"

        slow = 1.12
        cell_w, cell_h = 0.5, 0.48
        buff_x = 0.17
        val_fs = 22
        idx_fs = 14
        lbl_fs = 20
        stroke_box = 2.5

        nums = [2, 4, 3, 4, 1, 2, 4, 3, 5, 1, 2, 6]
        n = len(nums)
        y_nums = 0.34

        unit_w = cell_w + buff_x
        total_w = n * cell_w + max(n - 1, 0) * buff_x
        left_x = -total_w / 2

        def cell_left_x(k: int) -> float:
            return left_x + k * unit_w

        def cell_center(k: int) -> np.ndarray:
            return np.array([cell_left_x(k) + cell_w / 2, y_nums, 0])

        def top_mid(k: int) -> np.ndarray:
            return np.array([cell_left_x(k) + cell_w / 2, y_nums + cell_h / 2, 0])

        def gap_x_after(r: int) -> float:
            if r >= n - 1:
                return cell_left_x(n - 1) + cell_w + buff_x * 0.55 + 0.06
            return cell_left_x(r) + cell_w + buff_x / 2

        # 两条虚线同逻辑位置时略微错开，避免完全重合
        split = 0.034

        def x_right_line(cur_end: int) -> float:
            return gap_x_after(cur_end) - split

        def x_end_line(max_reach: int) -> float:
            return gap_x_after(max_reach) + split

        dash_h = 3 * cell_w

        def dash_at(x: float, *, cur_end: bool) -> VGroup:
            """cur_end=True：蓝虚线 + 单词 end；cur_end=False：红虚线 + 单词 right。"""
            if cur_end:
                lc, txt, tc, z = RIGHT_DASH, "end", RIGHT_LAB, 6
                where = UP
                buff = 0.1
                shift = RIGHT * 0.06
            else:
                lc, txt, tc, z = END_DASH, "right", END_LAB, 7
                where = DOWN
                buff = 0.1
                shift = RIGHT * 0.05
            line = DashedLine(
                [x, y_nums - dash_h / 2, 0],
                [x, y_nums + dash_h / 2, 0],
                color=lc,
                stroke_width=2.5,
                dash_length=0.09,
                dashed_ratio=0.55 if cur_end else 0.5,
            )
            lab = Text(txt, font_size=16, color=tc, font="Consolas")
            lab.next_to(line, where, buff=buff).shift(shift)
            g = VGroup(line, lab)
            g.set_z_index(z)
            return g

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
        nums_lbl.next_to(boxes[0], LEFT, buff=0.32)

        idx_y = y_nums - cell_h / 2 - 0.34
        idx_txts: list[Text] = []
        for k in range(n):
            it = Text(f"[{k}]", font_size=idx_fs, color=GREY_A, font="Consolas")
            it.move_to(np.array([cell_center(k)[0], idx_y, 0]))
            idx_txts.append(it)

        ans_y = idx_y - 0.52
        arr_center_x = (cell_left_x(0) + cell_left_x(n - 1) + cell_w) / 2
        ans_lbl = Text("ans", font_size=lbl_fs, color=WHITE, font="Consolas")
        ans_num = Text("0", font_size=lbl_fs, color=WHITE, font="Consolas")

        def align_ans_row() -> None:
            row = VGroup(ans_lbl, ans_num)
            row.arrange(RIGHT, buff=0.16)
            row.move_to(np.array([arr_center_x, ans_y, 0]))

        align_ans_row()

        g_static = VGroup(nums_lbl, *cols, *idx_txts, ans_lbl, ans_num)
        self.play(FadeIn(g_static, shift=UP * 0.06), run_time=0.55 * slow, rate_func=smooth)
        self.wait(0.4 * slow)

        def rect_green(lo: int, hi: int) -> Rectangle | None:
            """绿框覆盖 [lo, hi] 下标格；右缘不超过最后一格的右缘。"""
            hi_v = min(hi, n - 1)
            lo_v = max(0, min(lo, hi_v))
            if lo_v > hi_v:
                return None
            le = cell_left_x(lo_v)
            re_cap = cell_left_x(n - 1) + cell_w
            re = min(cell_left_x(hi_v) + cell_w, re_cap)
            w = max(re - le, 0.06)
            rr = Rectangle(
                width=w,
                height=cell_h + 0.06,
                color=GREEN_P,
                stroke_width=3.0,
                fill_opacity=0,
            )
            rr.move_to(np.array([(le + re) / 2, y_nums, 0]))
            rr.set_z_index(3)
            return rr

        def green_with_label(lo: int, hi: int, layer: int) -> VGroup | None:
            """绿框 + 其正上方白色层号（随 ReplacementTransform 与框一起动）。"""
            rr = rect_green(lo, hi)
            if rr is None:
                return None
            lab = Text(
                str(layer),
                font_size=int(val_fs * 0.92),
                color=WHITE,
                font="Consolas",
                disable_ligatures=True,
            )
            lab.next_to(rr, UP, buff=0.11)
            lab.set_z_index(11)
            rr.set_z_index(10)
            g = VGroup(rr, lab)
            g.set_z_index(10)
            return g

        def pointer_arrow(i: int) -> Arrow:
            top = top_mid(i)
            start = top + UP * 0.34
            arr = Arrow(
                start,
                top,
                color=RED_P,
                stroke_width=4.5,
                buff=0.0,
                max_tip_length_to_length_ratio=0.28,
            )
            arr.set_z_index(15)
            return arr

        cur_end = 0
        max_reach = 0
        ans = 0

        right_mob = dash_at(x_right_line(cur_end), cur_end=True)
        end_mob = dash_at(x_end_line(max_reach), cur_end=False)
        self.play(
            FadeIn(right_mob, scale=0.95),
            FadeIn(end_mob, scale=0.95),
            run_time=0.45 * slow,
        )

        ptr = pointer_arrow(0)
        self.play(FadeIn(ptr, shift=UP * 0.1), run_time=0.36 * slow)

        green_mob: Mobject | None = None
        t_arc = 0.52 * slow
        t_line = 0.58 * slow
        t_green = 0.5 * slow
        t_fade_arc = 0.32 * slow

        for i in range(n - 1):
            self.play(Transform(ptr, pointer_arrow(i)), run_time=0.42 * slow, rate_func=smooth)

            j = min(i + nums[i], n - 1)
            arc: Mobject | None = None
            if j != i:
                a0 = top_mid(i) + UP * 0.02 + RIGHT * 0.02
                a1 = top_mid(j) + UP * 0.02 + LEFT * 0.02
                arc = CurvedArrow(
                    a0,
                    a1,
                    angle=-TAU / 5.0,
                    color=RED_P,
                    stroke_width=2.2,
                )
                arc.set_z_index(12)
                self.play(Create(arc), run_time=t_arc, rate_func=smooth)
                self.wait(0.16 * slow)

            old_mr = max_reach
            max_reach = max(max_reach, i + nums[i])

            if max_reach > old_mr:
                new_end = dash_at(x_end_line(max_reach), cur_end=False)
                self.play(
                    ReplacementTransform(end_mob, new_end),
                    run_time=t_line,
                    rate_func=smooth,
                )
                end_mob = new_end

            if i == cur_end:
                old_ce = cur_end
                ans += 1
                new_ans_txt = Text(str(ans), font_size=lbl_fs, color=WHITE, font="Consolas")
                new_ans_txt.move_to(ans_num.get_center())
                self.play(
                    ReplacementTransform(ans_num, new_ans_txt),
                    run_time=0.38 * slow,
                )
                ans_num = new_ans_txt
                align_ans_row()

                cur_end = max_reach
                gl = old_ce + 1
                gh = min(cur_end, n - 1)
                new_green = green_with_label(gl, gh, ans) if gl <= gh else None

                new_right = dash_at(x_right_line(cur_end), cur_end=True)
                if new_green is not None:
                    if green_mob is None:
                        self.play(
                            ReplacementTransform(right_mob, new_right),
                            Create(new_green),
                            run_time=t_line,
                            rate_func=smooth,
                        )
                        green_mob = new_green
                    else:
                        self.play(
                            ReplacementTransform(right_mob, new_right),
                            ReplacementTransform(green_mob, new_green),
                            run_time=t_line,
                            rate_func=smooth,
                        )
                        green_mob = new_green
                    right_mob = new_right
                else:
                    self.play(
                        ReplacementTransform(right_mob, new_right),
                        run_time=t_line,
                        rate_func=smooth,
                    )
                    right_mob = new_right

            if arc is not None:
                self.play(FadeOut(arc), run_time=t_fade_arc)

            self.wait(0.2 * slow)

        self.play(FadeOut(ptr), run_time=0.35 * slow)
        self.wait(0.75 * slow)
