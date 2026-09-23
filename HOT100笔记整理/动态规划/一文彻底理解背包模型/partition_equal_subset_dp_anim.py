# -*- coding: utf-8 -*-
"""
分割等和子集 — 二维 DP 填表教学动画（Manim）

固定样例 nums = [1, 6, 2, 3]，total = 12，target = 6；矩阵 (n+1)×(target+1) = 5×7。
黑底、仅矩阵与符号、无旁白字幕。

成片 2560×1440（Manim -qp）:
  .\\manim-env2\\Scripts\\manim.exe -qp partition_equal_subset_dp_anim.py PartitionEqualSubsetDPDemo --disable_caching

480p（854×480，较快）:
  .\\manim-env2\\Scripts\\manim.exe -ql partition_equal_subset_dp_anim.py PartitionEqualSubsetDPDemo --disable_caching
"""

from __future__ import annotations

import numpy as np
from manim import *
from manim.utils.rate_functions import smooth

# 不在此写死分辨率，便于 CLI 控制：-ql 为 854×480（480p），-qp 为 2560×1440 等。


def compute_partition_dp(nums: list[int], target: int) -> list[list[bool]]:
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        for j in range(target + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= nums[i - 1]:
                dp[i][j] = dp[i][j] or dp[i - 1][j - nums[i - 1]]
    return dp


class PartitionEqualSubsetDPDemo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        nums = [1, 6, 2, 3]
        n = len(nums)
        target = 6
        total = sum(nums)
        assert total == 12 and target == total // 2

        dp_bool = compute_partition_dp(nums, target)

        # 节奏：略放慢便于看清箭头
        slow = 1.12
        t_cell_intro = 0.045 * slow
        t_sync_lbl = 0.55 * slow
        t_flash = 0.22 * slow
        t_row0_fast = 0.09 * slow
        t_hl = 0.38 * slow
        t_arrow = 0.52 * slow
        t_copy = 0.42 * slow
        t_orange = 0.55 * slow
        t_update = 0.4 * slow
        t_fade_arrow = 0.32 * slow
        t_unhl = 0.28 * slow
        t_between_cell = 0.12 * slow

        GREEN_P = "#55dd66"
        GREY_P = "#8899aa"
        BLUE_P = "#4da3ff"
        ORANGE_P = "#ff9933"
        RED_P = "#ff4444"
        YELLOW_HL = "#ffcc00"
        GOLD_P = "#e6c200"

        cell_w, cell_h = 0.62, 0.54
        gap = 0.06
        stroke_w = 2.6
        val_fs = 30
        idx_fs = 22
        dp_title_fs = 28
        row_lbl_fs = 19

        rows, cols = n + 1, target + 1
        row_labels = ["[]", "[1]", "[1, 6]", "[1, 6, 2]", "[1, 6, 2, 3]"]

        grid_w = cols * cell_w + max(cols - 1, 0) * gap
        grid_h = rows * cell_h + max(rows - 1, 0) * gap

        grid_left = -grid_w / 2 + 0.12
        # 行坐标：各标签右括号对齐到同一条竖线（略离网格左缘，避免贴太紧）
        row_label_right_x = grid_left - 0.22
        grid_top = grid_h / 2 - 0.05

        def cell_center(i: int, j: int) -> np.ndarray:
            x = grid_left + j * (cell_w + gap) + cell_w / 2
            y = grid_top - i * (cell_h + gap) - cell_h / 2
            return np.array([x, y, 0.0], dtype=float)

        # 列索引 0..6（在矩阵上方）
        idx_y = grid_top + cell_h * 0.5 + 0.36
        col_idx_mobs: list[Text] = []
        for j in range(cols):
            t = Text(str(j), font_size=idx_fs, color=GREY_P, font="Consolas")
            t.move_to(np.array([cell_center(0, j)[0], idx_y, 0]))
            col_idx_mobs.append(t)

        # 左上角 "dp"（相对网格顶角再往左上）
        dp_title = Text("dp", font_size=dp_title_fs, color=WHITE, font="Consolas")
        dp_corner = np.array(
            [grid_left - 0.58, grid_top + cell_h * 0.92, 0]
        )
        dp_title.move_to(dp_corner)

        boxes: list[list[Rectangle]] = []
        for i in range(rows):
            row_boxes: list[Rectangle] = []
            for j in range(cols):
                r = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    color=WHITE,
                    stroke_width=stroke_w,
                    fill_opacity=0,
                )
                r.move_to(cell_center(i, j))
                row_boxes.append(r)
            boxes.append(row_boxes)

        row_lbl_mobs: list[Text] = []
        for i in range(rows):
            lt = Text(row_labels[i], font_size=row_lbl_fs, color=GREY_P, font="Consolas")
            y_i = cell_center(i, 0)[1]
            lt.move_to(np.array([row_label_right_x - lt.width / 2, y_i, 0]))
            row_lbl_mobs.append(lt)

        # 开场：从左上到右下依次出现格子；首格同时出现列索引与行标签
        order: list[tuple[int, int]] = [(i, j) for i in range(rows) for j in range(cols)]
        for i, j in order:
            grp = [GrowFromCenter(boxes[i][j])]
            if i == 0 and j == 0:
                grp.append(FadeIn(dp_title, shift=DOWN * 0.06))
                grp.append(FadeIn(VGroup(*col_idx_mobs), shift=UP * 0.06))
            if j == 0:
                grp.append(FadeIn(row_lbl_mobs[i], shift=RIGHT * 0.08))
            self.play(*grp, run_time=t_cell_intro, rate_func=smooth)
        self.wait(0.25 * slow)

        # 数值层：初始为空（无 Text），用字典存
        vals: list[list[Text | None]] = [[None] * cols for _ in range(rows)]

        def val_color(v: int) -> ManimColor:
            return GREEN_P if v == 1 else GREY_P

        def place_val(i: int, j: int, v: int) -> Text:
            t = Text(str(v), font_size=val_fs, color=val_color(v), font="Consolas")
            t.move_to(cell_center(i, j))
            return t

        # dp[0][0] = 1 黄色闪烁
        hl0 = SurroundingRectangle(
            boxes[0][0], color=YELLOW_HL, buff=0.02, corner_radius=0.02, stroke_width=4
        )
        hl0.set_z_index(15)
        self.play(Create(hl0), run_time=t_hl * 0.5)
        self.play(
            boxes[0][0].animate.set_fill(YELLOW_HL, opacity=0.55),
            run_time=t_flash,
            rate_func=there_and_back,
        )
        vals[0][0] = place_val(0, 0, 1)
        self.play(FadeIn(vals[0][0], scale=0.85), run_time=t_copy * 0.8)
        self.play(
            FadeOut(hl0),
            boxes[0][0].animate.set_fill(BLACK, opacity=0),
            run_time=t_unhl,
        )

        # 第 0 行其余快速填 0
        for j in range(1, cols):
            vals[0][j] = place_val(0, j, 0)
            self.play(FadeIn(vals[0][j], scale=0.9), run_time=t_row0_fast, rate_func=smooth)

        self.wait(0.35 * slow)

        def arrow_between(
            i0: int, j0: int, i1: int, j1: int, color: str, z: int = 18
        ) -> Arrow:
            a, b = cell_center(i0, j0), cell_center(i1, j1)
            direction = b - a
            if np.linalg.norm(direction) < 1e-6:
                direction = DOWN
            direction = direction / np.linalg.norm(direction)
            arr = Arrow(
                a + direction * (cell_w * 0.22),
                b - direction * (cell_w * 0.22),
                buff=0,
                color=color,
                stroke_width=3.6,
                max_tip_length_to_length_ratio=0.22,
            )
            arr.set_z_index(z)
            return arr

        def row_pointer_for(i: int) -> Arrow:
            tip = np.array(
                [row_lbl_mobs[i].get_left()[0] - 0.06, row_lbl_mobs[i].get_center()[1], 0]
            )
            start = tip + LEFT * 0.55
            arr = Arrow(
                start,
                tip,
                buff=0,
                color=RED_P,
                stroke_width=3.8,
                max_tip_length_to_length_ratio=0.25,
            )
            arr.set_z_index(20)
            return arr

        ptr = row_pointer_for(1)
        self.play(FadeIn(ptr, shift=RIGHT * 0.12), run_time=0.45 * slow)

        for i in range(1, n + 1):
            w = nums[i - 1]
            if i > 1:
                self.play(Transform(ptr, row_pointer_for(i)), run_time=0.48 * slow, rate_func=smooth)

            for j in range(target + 1):
                hl = SurroundingRectangle(
                    boxes[i][j],
                    color=YELLOW_HL,
                    buff=0.02,
                    corner_radius=0.02,
                    stroke_width=4,
                )
                hl.set_z_index(14)
                self.play(Create(hl), run_time=t_hl * 0.55)

                # 不选：蓝箭头 + 复制 dp[i-1][j]
                src_skip = int(dp_bool[i - 1][j])
                blue = arrow_between(i - 1, j, i, j, BLUE_P)
                self.play(Create(blue), run_time=t_arrow, rate_func=smooth)
                cur = src_skip
                dest_mob = place_val(i, j, cur)
                vals[i][j] = dest_mob
                self.play(TransformFromCopy(vals[i - 1][j], dest_mob), run_time=t_copy, rate_func=smooth)

                orange: Arrow | None = None
                if j >= w:
                    src_take = int(dp_bool[i - 1][j - w])
                    orange = arrow_between(i - 1, j - w, i, j, ORANGE_P)
                    self.play(Create(orange), run_time=t_orange, rate_func=smooth)
                    new_val = 1 if (cur == 1 or src_take == 1) else 0
                    if new_val != cur:
                        new_t = place_val(i, j, new_val)
                        self.play(ReplacementTransform(vals[i][j], new_t), run_time=t_update, rate_func=smooth)
                        vals[i][j] = new_t
                        cur = new_val

                outs: list = [FadeOut(blue)]
                if orange is not None:
                    outs.append(FadeOut(orange))
                self.play(*outs, run_time=t_fade_arrow * 0.85)
                self.play(FadeOut(hl), run_time=t_unhl * 0.8)
                self.wait(t_between_cell)

        self.play(FadeOut(ptr), run_time=0.4 * slow)

        # 金色框 + dp[4][6] 放大闪烁 + true
        fi, fj = n, target
        gold_frame = SurroundingRectangle(
            boxes[fi][fj],
            color=GOLD_P,
            buff=0.04,
            corner_radius=0.03,
            stroke_width=5,
        )
        gold_frame.set_z_index(16)
        self.play(Create(gold_frame), run_time=0.55 * slow)
        v = vals[fi][fj]
        self.play(
            Indicate(v, scale_factor=1.75, color=GOLD_P),
            run_time=0.62 * slow,
            rate_func=smooth,
        )

        true_txt = Text("true", font_size=36, color=GREEN_P, font="Consolas")
        br = np.array(
            [
                grid_left + grid_w + 0.35,
                grid_top - grid_h - 0.42,
                0,
            ]
        )
        true_txt.move_to(br)
        self.play(FadeIn(true_txt, shift=LEFT * 0.12), run_time=0.55 * slow, rate_func=smooth)
        self.wait(1.0 * slow)


if __name__ == "__main__":
    pass
