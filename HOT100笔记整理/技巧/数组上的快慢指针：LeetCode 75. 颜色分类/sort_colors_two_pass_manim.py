"""两遍扫描「颜色分类」算法可视化。

数组格子、指针与交换高亮与 move_nonzero_manim(1).py 一致（方格无填充，仅灰描边）；
前缀/后缀绿框下的对勾与参考里绿色「结果」行相同：Text、font_size=30、color=GREEN，用 Write 出现。

运行（480p，较快）：
  manim -ql sort_colors_two_pass_manim.py SortColorsTwoPass

高质量：
  manim -qh sort_colors_two_pass_manim.py SortColorsTwoPass

输出示例：
  media/videos/sort_colors_two_pass_manim/480p30/SortColorsTwoPass.mp4

说明：像素宽高须为偶数（如宽 852），否则部分环境下 PyAV 编码可能失败。
"""

from __future__ import annotations

import numpy as np

from manim import *

# 16:9（对齐 2560×1440）；480p；宽高偶数避免编码失败
config.pixel_height = 1080
config.pixel_width = 1920
config.background_color = BLACK
config.frame_rate = 60


def _green_check_text() -> Text:
    """与 move_nonzero_manim(1).py 中 result = Text(..., font_size=30, color=GREEN) 同字号同色。"""
    return Text("✓", font_size=30, color=GREEN)


class SortColorsTwoPass(Scene):
    def construct(self):
        nums = [2, 0, 2, 1, 1, 0, 0, 1, 2, 1, 0]
        n = len(nums)
        a = list(nums)

        # ---------- 数组居中（与 move_nonzero_manim 一致）----------
        cell_w, cell_h = 0.75, 0.9
        gap = 0.06
        spacing = cell_w + gap
        start_x = -(n - 1) * spacing / 2

        cells = VGroup()
        texts = VGroup()
        for k in range(n):
            box = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.08,
                color=GRAY_B,
                stroke_width=2,
            )
            t = Text(str(a[k]), font_size=32)
            box.move_to(RIGHT * (start_x + k * spacing))
            t.move_to(box.get_center())
            cells.add(box)
            texts.add(t)

        array_g = VGroup(cells, texts)
        array_g.move_to(ORIGIN)

        # 与 move_nonzero：j 在上、i 在下
        j_y = array_g.get_top()[1] + 0.75
        i_y = array_g.get_bottom()[1] - 0.75

        def col_x(k: int) -> float:
            return array_g.get_center()[0] + start_x + k * spacing

        # —— 双指针：与 move_nonzero_manim(1).py 中 j_pointer_at / i_pointer_at 完全一致 ——
        def j_pointer_at(k: int) -> VGroup:
            tip = np.array([col_x(k), cells[k].get_top()[1] + 0.1, 0.0])
            base = np.array([col_x(k), j_y, 0.0])
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

        def i_pointer_at(k: int) -> VGroup:
            tip = np.array([col_x(k), cells[k].get_bottom()[1] - 0.1, 0.0])
            base = np.array([col_x(k), i_y, 0.0])
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

        def pointer_pair_at(i_k: int, j_k: int) -> tuple[VGroup, VGroup]:
            return i_pointer_at(i_k), j_pointer_at(j_k)

        prefix_box = None
        suffix_box = None
        prefix_check = None
        suffix_check = None

        # 区域框：与格子同圆角、同线宽，描边为绿（无填充）
        def make_span_box(left_idx: int, right_idx: int, color=GREEN) -> RoundedRectangle:
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

        # ---------- 开场（同 move_nonzero：先数组，再双指针）----------
        self.play(FadeIn(array_g, shift=UP * 0.2))
        ptr_i, ptr_j = pointer_pair_at(0, 0)
        self.play(
            FadeIn(ptr_j, shift=DOWN * 0.12),
            FadeIn(ptr_i, shift=UP * 0.12),
        )
        self.wait(0.25)

        j = 0
        # ---------- 第一趟 ----------
        for i in range(n):
            ni, nj = pointer_pair_at(i, j)
            self.play(
                Transform(ptr_i, ni),
                Transform(ptr_j, nj),
                run_time=0.48,
            )
            self.wait(0.08)

            if a[i] == 0:
                if i != j:
                    y1, y2 = cells[i].get_top()[1] + 0.35, cells[j].get_top()[1] + 0.35
                    x1, x2 = col_x(i), col_x(j)
                    darrow = DoubleArrow(
                        np.array([x1, y1, 0.0]),
                        np.array([x2, y2, 0.0]),
                        color=GREEN,
                        stroke_width=4,
                        buff=0.0,
                        tip_length=0.18,
                    )
                    self.play(
                        cells[i].animate.set_stroke(YELLOW, width=4),
                        cells[j].animate.set_stroke(YELLOW, width=4),
                        FadeIn(darrow, scale=0.85),
                        run_time=0.28,
                    )
                    a[i], a[j] = a[j], a[i]
                    new_ti = Text(str(a[i]), font_size=32).move_to(cells[i].get_center())
                    new_tj = Text(str(a[j]), font_size=32).move_to(cells[j].get_center())
                    self.play(
                        Transform(texts[i], new_ti),
                        Transform(texts[j], new_tj),
                        run_time=0.5,
                    )
                    self.play(
                        FadeOut(darrow),
                        cells[i].animate.set_stroke(GRAY_B, width=2),
                        cells[j].animate.set_stroke(GRAY_B, width=2),
                        run_time=0.22,
                    )
                else:
                    self.play(
                        Indicate(cells[i], color=YELLOW, scale_factor=1.08),
                        Flash(cells[i], color=YELLOW, flash_radius=0.35),
                        run_time=0.5,
                    )

                j += 1
                new_pb = make_span_box(0, j - 1) if j > 0 else empty_placeholder()
                if prefix_box is None:
                    prefix_box = new_pb
                    if j > 0:
                        self.add(prefix_box)
                        self.play(FadeIn(prefix_box, scale=0.96), run_time=0.38)
                else:
                    if j > 0:
                        self.play(Transform(prefix_box, new_pb), run_time=0.42)
                    else:
                        self.remove(prefix_box)
                        prefix_box = None

                ni2, nj2 = pointer_pair_at(i, j)
                self.play(
                    Transform(ptr_i, ni2),
                    Transform(ptr_j, nj2),
                    run_time=0.45,
                )
                self.wait(0.12)
            else:
                self.wait(0.18)

        if prefix_box is not None:
            prefix_check = _green_check_text()
            prefix_check.next_to(prefix_box, DOWN, buff=0.12)
            self.play(Write(prefix_check))
            self.wait(0.2)

        self.wait(0.35)

        ni0, nj0 = pointer_pair_at(n - 1, n - 1)
        self.play(
            Transform(ptr_i, ni0),
            Transform(ptr_j, nj0),
            run_time=0.55,
        )
        self.wait(0.45)

        j = n - 1
        # ---------- 第二趟 ----------
        for i in range(n - 1, -1, -1):
            ni, nj = pointer_pair_at(i, j)
            self.play(
                Transform(ptr_i, ni),
                Transform(ptr_j, nj),
                run_time=0.48,
            )
            self.wait(0.08)

            if a[i] == 2:
                if i != j:
                    y1, y2 = cells[i].get_top()[1] + 0.35, cells[j].get_top()[1] + 0.35
                    x1, x2 = col_x(i), col_x(j)
                    darrow = DoubleArrow(
                        np.array([x1, y1, 0.0]),
                        np.array([x2, y2, 0.0]),
                        color=GREEN,
                        stroke_width=4,
                        buff=0.0,
                        tip_length=0.18,
                    )
                    self.play(
                        cells[i].animate.set_stroke(YELLOW, width=4),
                        cells[j].animate.set_stroke(YELLOW, width=4),
                        FadeIn(darrow, scale=0.85),
                        run_time=0.28,
                    )
                    a[i], a[j] = a[j], a[i]
                    new_ti = Text(str(a[i]), font_size=32).move_to(cells[i].get_center())
                    new_tj = Text(str(a[j]), font_size=32).move_to(cells[j].get_center())
                    self.play(
                        Transform(texts[i], new_ti),
                        Transform(texts[j], new_tj),
                        run_time=0.5,
                    )
                    self.play(
                        FadeOut(darrow),
                        cells[i].animate.set_stroke(GRAY_B, width=2),
                        cells[j].animate.set_stroke(GRAY_B, width=2),
                        run_time=0.22,
                    )
                else:
                    self.play(
                        Indicate(cells[i], color=YELLOW, scale_factor=1.08),
                        Flash(cells[i], color=YELLOW, flash_radius=0.35),
                        run_time=0.5,
                    )

                j -= 1
                new_sb = make_span_box(j + 1, n - 1) if j < n - 1 else empty_placeholder()
                if suffix_box is None:
                    suffix_box = new_sb
                    if j < n - 1:
                        self.add(suffix_box)
                        self.play(FadeIn(suffix_box, scale=0.96), run_time=0.38)
                else:
                    if j < n - 1:
                        self.play(Transform(suffix_box, new_sb), run_time=0.42)
                    else:
                        self.remove(suffix_box)
                        suffix_box = None

                ni2, nj2 = pointer_pair_at(i, j)
                self.play(
                    Transform(ptr_i, ni2),
                    Transform(ptr_j, nj2),
                    run_time=0.45,
                )
                self.wait(0.12)
            else:
                self.wait(0.18)

        if suffix_box is not None:
            suffix_check = _green_check_text()
            suffix_check.next_to(suffix_box, DOWN, buff=0.12)
            self.play(Write(suffix_check))
            self.wait(0.2)

        self.wait(0.45)

        # ---------- 收尾：淡出指针、绿框与绿勾 ----------
        fade_targets = VGroup(ptr_i, ptr_j)
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
        self.wait(1.2)
