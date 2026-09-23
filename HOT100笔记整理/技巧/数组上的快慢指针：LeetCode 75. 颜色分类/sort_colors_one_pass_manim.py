"""一趟三指针「颜色分类 / 荷兰国旗」可视化。

算法（与常见 LeetCode 单趟解一致）：
  j, k = 0, n-1; i = 0
  while i <= k:
      if nums[i] == 0: swap(i,j); j++; i++
      elif nums[i] == 2: swap(i,k); k--
      else: i++

样例：nums = [2,0,2,1,1,0,0,1,2,1,0]

视觉：格子/交换高亮与 move_nonzero、sort_colors_two_pass 一致（灰框无填充）；
前缀已处理 [0..j-1] 绿框 + 指针 j（红箭，上排）；后缀已处理 [k+1..n-1] 红框 + 指针 k（橙箭，与 j 同排同长度）；j 与 k 同列时 k 略微水平错位；
扫描指针 i（蓝箭，下方）。一趟结束后前缀绿框 / 后缀红框下方绿色「✓」与 sort_colors_two_pass 相同（font_size=30、Write）。

低清预览：
  manim -ql sort_colors_one_pass_manim.py SortColorsOnePass
"""

from __future__ import annotations

import numpy as np

from manim import *

config.pixel_height = 1080
config.pixel_width = 1920
config.background_color = BLACK
config.frame_rate = 60


def _green_check_text() -> Text:
    """与 sort_colors_two_pass_manim.py 一致：Text ✓，font_size=30，color=GREEN。"""
    return Text("✓", font_size=30, color=GREEN)


class SortColorsOnePass(Scene):
    def construct(self):
        nums = [2, 0, 2, 1, 1, 0, 0, 1, 2, 1, 0]
        n = len(nums)
        a = list(nums)

        cell_w, cell_h = 0.75, 0.9
        gap = 0.06
        spacing = cell_w + gap
        start_x = -(n - 1) * spacing / 2

        cells = VGroup()
        texts = VGroup()
        for t_idx in range(n):
            box = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.08,
                color=GRAY_B,
                stroke_width=2,
            )
            t = Text(str(a[t_idx]), font_size=32)
            box.move_to(RIGHT * (start_x + t_idx * spacing))
            t.move_to(box.get_center())
            cells.add(box)
            texts.add(t)

        array_g = VGroup(cells, texts)
        array_g.move_to(ORIGIN)

        j_y = array_g.get_top()[1] + 0.75
        i_y = array_g.get_bottom()[1] - 0.75

        def col_x(idx: int) -> float:
            return array_g.get_center()[0] + start_x + idx * spacing

        def j_pointer_at(idx: int) -> VGroup:
            tip = np.array([col_x(idx), cells[idx].get_top()[1] + 0.1, 0.0])
            base = np.array([col_x(idx), j_y, 0.0])
            ar = Arrow(
                base,
                tip,
                buff=0.0,
                color=RED,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            )
            lab = Text("j", font_size=36, color=RED).next_to(ar.get_start(), UP, buff=0.08)
            return VGroup(lab, ar)

        def k_pointer_at(idx: int, x_shift: float = 0.0) -> VGroup:
            """与 j 同基线 j_y，箭长一致；x_shift 在 j、k 同列时错开标签。"""
            xh = col_x(idx) + x_shift
            tip = np.array([xh, cells[idx].get_top()[1] + 0.1, 0.0])
            base = np.array([xh, j_y, 0.0])
            ar = Arrow(
                base,
                tip,
                buff=0.0,
                color=ORANGE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            )
            lab = Text("k", font_size=36, color=ORANGE).next_to(ar.get_start(), UP, buff=0.08)
            return VGroup(lab, ar)

        def i_pointer_at(idx: int) -> VGroup:
            tip = np.array([col_x(idx), cells[idx].get_bottom()[1] - 0.1, 0.0])
            base = np.array([col_x(idx), i_y, 0.0])
            ar = Arrow(
                base,
                tip,
                buff=0.0,
                color=BLUE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            )
            lab = Text("i", font_size=36, color=BLUE).next_to(ar.get_start(), DOWN, buff=0.08)
            return VGroup(lab, ar)

        def triple_at(i_idx: int, j_idx: int, rk: int) -> tuple[VGroup, VGroup, VGroup]:
            k_shift = 0.14 if rk == j_idx else 0.0
            return i_pointer_at(i_idx), j_pointer_at(j_idx), k_pointer_at(rk, x_shift=k_shift)

        prefix_box = None
        suffix_box = None
        prefix_check = None
        suffix_check = None

        def make_span_box(left_idx: int, right_idx: int, color) -> RoundedRectangle:
            pad_x, pad_y = 0.06, 0.08
            p0 = cells[left_idx].get_corner(UL) + LEFT * pad_x + UP * pad_y
            p1 = cells[right_idx].get_corner(DR) + RIGHT * pad_x + DOWN * pad_y
            w = p1[0] - p0[0]
            h = p0[1] - p1[1]
            rect = RoundedRectangle(
                width=w,
                height=h,
                corner_radius=0.08,
                color=color,
                stroke_width=2,
            )
            rect.move_to((p0 + p1) / 2)
            return rect

        def empty_placeholder():
            return VGroup()

        def update_prefix_box(j_idx: int):
            nonlocal prefix_box
            if j_idx <= 0:
                if prefix_box is not None:
                    self.remove(prefix_box)
                    prefix_box = None
                return
            new_b = make_span_box(0, j_idx - 1, GREEN)
            if prefix_box is None:
                prefix_box = new_b
                self.add(prefix_box)
                self.play(FadeIn(prefix_box, scale=0.96), run_time=0.38)
            else:
                self.play(Transform(prefix_box, new_b), run_time=0.42)

        def update_suffix_box(rk: int):
            nonlocal suffix_box
            if rk >= n - 1:
                if suffix_box is not None:
                    self.remove(suffix_box)
                    suffix_box = None
                return
            new_b = make_span_box(rk + 1, n - 1, RED)
            if suffix_box is None:
                suffix_box = new_b
                self.add(suffix_box)
                self.play(FadeIn(suffix_box, scale=0.96), run_time=0.38)
            else:
                self.play(Transform(suffix_box, new_b), run_time=0.42)

        # ---------- 开场 ----------
        self.play(FadeIn(array_g, shift=UP * 0.2))
        j_idx, rk = 0, n - 1
        i_idx = 0
        ptr_i, ptr_j, ptr_k = triple_at(i_idx, j_idx, rk)
        self.play(
            FadeIn(ptr_j, shift=DOWN * 0.12),
            FadeIn(ptr_k, shift=DOWN * 0.12),
            FadeIn(ptr_i, shift=UP * 0.12),
        )
        self.wait(0.25)

        # ---------- 一趟主循环 ----------
        while i_idx <= rk:
            ni, nj, nk = triple_at(i_idx, j_idx, rk)
            self.play(
                Transform(ptr_i, ni),
                Transform(ptr_j, nj),
                Transform(ptr_k, nk),
                run_time=0.45,
            )
            self.wait(0.08)

            if a[i_idx] == 0:
                if i_idx != j_idx:
                    y1, y2 = (
                        cells[i_idx].get_top()[1] + 0.35,
                        cells[j_idx].get_top()[1] + 0.35,
                    )
                    x1, x2 = col_x(i_idx), col_x(j_idx)
                    darrow = DoubleArrow(
                        np.array([x1, y1, 0.0]),
                        np.array([x2, y2, 0.0]),
                        color=GREEN,
                        stroke_width=4,
                        buff=0.0,
                        tip_length=0.18,
                    )
                    self.play(
                        cells[i_idx].animate.set_stroke(YELLOW, width=4),
                        cells[j_idx].animate.set_stroke(YELLOW, width=4),
                        FadeIn(darrow, scale=0.85),
                        run_time=0.28,
                    )
                    a[i_idx], a[j_idx] = a[j_idx], a[i_idx]
                    new_ti = Text(str(a[i_idx]), font_size=32).move_to(cells[i_idx].get_center())
                    new_tj = Text(str(a[j_idx]), font_size=32).move_to(cells[j_idx].get_center())
                    self.play(
                        Transform(texts[i_idx], new_ti),
                        Transform(texts[j_idx], new_tj),
                        run_time=0.5,
                    )
                    self.play(
                        FadeOut(darrow),
                        cells[i_idx].animate.set_stroke(GRAY_B, width=2),
                        cells[j_idx].animate.set_stroke(GRAY_B, width=2),
                        run_time=0.22,
                    )
                else:
                    self.play(
                        Indicate(cells[i_idx], color=YELLOW, scale_factor=1.08),
                        Flash(cells[i_idx], color=YELLOW, flash_radius=0.35),
                        run_time=0.5,
                    )
                j_idx += 1
                i_idx += 1
                update_prefix_box(j_idx)
            elif a[i_idx] == 2:
                if i_idx != rk:
                    y1, y2 = (
                        cells[i_idx].get_top()[1] + 0.35,
                        cells[rk].get_top()[1] + 0.35,
                    )
                    x1, x2 = col_x(i_idx), col_x(rk)
                    darrow = DoubleArrow(
                        np.array([x1, y1, 0.0]),
                        np.array([x2, y2, 0.0]),
                        color=RED,
                        stroke_width=4,
                        buff=0.0,
                        tip_length=0.18,
                    )
                    self.play(
                        cells[i_idx].animate.set_stroke(YELLOW, width=4),
                        cells[rk].animate.set_stroke(YELLOW, width=4),
                        FadeIn(darrow, scale=0.85),
                        run_time=0.28,
                    )
                    a[i_idx], a[rk] = a[rk], a[i_idx]
                    new_ti = Text(str(a[i_idx]), font_size=32).move_to(cells[i_idx].get_center())
                    new_tk = Text(str(a[rk]), font_size=32).move_to(cells[rk].get_center())
                    self.play(
                        Transform(texts[i_idx], new_ti),
                        Transform(texts[rk], new_tk),
                        run_time=0.5,
                    )
                    self.play(
                        FadeOut(darrow),
                        cells[i_idx].animate.set_stroke(GRAY_B, width=2),
                        cells[rk].animate.set_stroke(GRAY_B, width=2),
                        run_time=0.22,
                    )
                else:
                    self.play(
                        Indicate(cells[i_idx], color=YELLOW, scale_factor=1.08),
                        Flash(cells[i_idx], color=YELLOW, flash_radius=0.35),
                        run_time=0.5,
                    )
                rk -= 1
                update_suffix_box(rk)
            else:
                i_idx += 1

            if i_idx > rk:
                break

            ni2, nj2, nk2 = triple_at(i_idx, j_idx, rk)
            self.play(
                Transform(ptr_i, ni2),
                Transform(ptr_j, nj2),
                Transform(ptr_k, nk2),
                run_time=0.42,
            )
            self.wait(0.1)

        self.wait(0.35)

        # 前缀 / 后缀区域框下方的绿色 ✓（与两趟版本相同）
        if prefix_box is not None:
            prefix_check = _green_check_text()
            prefix_check.next_to(prefix_box, DOWN, buff=0.12)
            self.play(Write(prefix_check))
            self.wait(0.2)
        if suffix_box is not None:
            suffix_check = _green_check_text()
            suffix_check.next_to(suffix_box, DOWN, buff=0.12)
            self.play(Write(suffix_check))
            self.wait(0.2)

        # ---------- 收尾 ----------
        fade_targets = VGroup(ptr_i, ptr_j, ptr_k)
        if prefix_box is not None:
            fade_targets.add(prefix_box)
        if suffix_box is not None:
            fade_targets.add(suffix_box)
        if prefix_check is not None:
            fade_targets.add(prefix_check)
        if suffix_check is not None:
            fade_targets.add(suffix_check)
        self.play(FadeOut(fade_targets), run_time=1.0)

        self.play(
            array_g.animate.scale(1.06),
            rate_func=there_and_back,
            run_time=0.55,
        )
        self.play(
            array_g.animate.scale(1.04),
            rate_func=there_and_back,
            run_time=0.45,
        )
        self.play(
            array_g.animate.scale(1.03),
            rate_func=there_and_back,
            run_time=0.4,
        )
        self.wait(1.0)
