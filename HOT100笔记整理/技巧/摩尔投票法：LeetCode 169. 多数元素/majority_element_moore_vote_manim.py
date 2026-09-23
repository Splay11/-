"""LeetCode 169 多数元素：摩尔投票「消消乐」可视化（题面见 技巧/摩尔投票法-超过一半的数字.md）。

视频输出目录：与本文件同级的 media/。

运行（在「动态规划」目录下）：
  .\\manim-env\\Scripts\\manim.exe -ql majority_element_moore_vote_manim.py MajorityMooreVote
  .\\manim-env\\Scripts\\manim.exe -qh majority_element_moore_vote_manim.py MajorityMooreVote
"""

from __future__ import annotations

import random
from pathlib import Path

from manim import *

config.media_dir = str(Path(__file__).resolve().parent / "media")

CELL_W = 0.52
CELL_BUFF = 0.07
CELL_STEP = CELL_W + CELL_BUFF
FONT_CN = "Microsoft YaHei"


def majority_element(nums: list[int]) -> int:
    cnt, cand = 0, 0
    for x in nums:
        if cnt == 0:
            cand = x
        cnt += 1 if x == cand else -1
    return cand


def all_unequal_pairs(values: list[int]) -> list[tuple[int, int]]:
    return [(i, j) for i in range(len(values)) for j in range(i + 1, len(values)) if values[i] != values[j]]


def nonmajority_unequal_pairs(values: list[int], maj: int) -> list[tuple[int, int]]:
    """两格值均非众数且互不相等时的下标对；用于在条件允许时至少演示一次「非众数互消」。"""
    return [
        (i, j)
        for i in range(len(values))
        for j in range(i + 1, len(values))
        if values[i] != values[j] and values[i] != maj and values[j] != maj
    ]


def pick_random_unequal_pair(values: list[int], rng: random.Random) -> tuple[int, int]:
    pairs = all_unequal_pairs(values)
    return rng.choice(pairs)


def pick_pair_for_step(
    values: list[int],
    rng: random.Random,
    maj: int,
    still_need_nonmajority_pair: bool,
) -> tuple[int, int, bool]:
    """返回 (i, j, 是否用掉了「尚须一次非众数互消」义务)。i < j。"""
    nm = nonmajority_unequal_pairs(values, maj)
    if still_need_nonmajority_pair and nm:
        i, j = rng.choice(nm)
        if i > j:
            i, j = j, i
        return i, j, False
    i, j = pick_random_unequal_pair(values, rng)
    if i > j:
        i, j = j, i
    return i, j, still_need_nonmajority_pair


def make_cell(val: int) -> VGroup:
    box = RoundedRectangle(
        width=CELL_W,
        height=0.72,
        corner_radius=0.06,
        color=GRAY_B,
        stroke_width=2,
        fill_color=BLACK,
        fill_opacity=0.35,
    )
    txt = Text(str(val), font_size=34, color=WHITE)
    return VGroup(box, txt)


def row_target_centers(n: int, y: float) -> list:
    if n == 0:
        return []
    return [np.array([-(n - 1) * CELL_STEP / 2 + i * CELL_STEP, y, 0.0]) for i in range(n)]


class MajorityMooreVote(Scene):
    def construct(self) -> None:
        samples = [
            [2, 2, 1, 1, 1, 2, 2],
            [1, 2, 1, 4, 1, 4, 1, 3, 1, 1, 2],
        ]
        for sample_idx, nums in enumerate(samples):
            self.play_one_sample(nums, sample_idx, y_row=-0.35)
            if sample_idx < len(samples) - 1:
                self.wait(0.35)

    def majority_highlight_show(self, cells: list[VGroup], values: list[int], maj: int) -> tuple[VGroup, list[int]]:
        idxs = [i for i, v in enumerate(values) if v == maj]
        row = VGroup(*cells)
        hub = row.get_center() + UP * (row.height / 2 + 0.95)
        hub_dot = Dot(hub, radius=0.06, color=YELLOW)
        label = Text("众数", font=FONT_CN, font_size=30, color=YELLOW)
        label.next_to(hub_dot, UP, buff=0.12)
        arrows = VGroup(
            *[
                Arrow(
                    hub,
                    cells[i].get_top() + UP * 0.02,
                    color=YELLOW,
                    stroke_width=2.5,
                    buff=0,
                    tip_length=0.16,
                    max_tip_length_to_length_ratio=0.22,
                )
                for i in idxs
            ]
        )
        overlay = VGroup(hub_dot, arrows, label)
        self.play(FadeIn(hub_dot, scale=0.5), Create(arrows), Write(label))
        self.play(*[cells[i][1].animate.set_color(YELLOW) for i in idxs], run_time=0.55)
        self.wait(0.3)
        return overlay, idxs

    def majority_highlight_dismiss(self, overlay: VGroup, cells: list[VGroup], idxs: list[int]) -> None:
        self.play(
            FadeOut(overlay),
            *[cells[i][1].animate.set_color(WHITE) for i in idxs],
            run_time=0.48,
        )

    def play_one_sample(self, nums: list[int], sample_idx: int, y_row: float) -> None:
        rng = random.Random(169000 + sample_idx)
        values = list(nums)
        maj = majority_element(nums)
        cells = [make_cell(v) for v in values]

        for i, c in enumerate(cells):
            c.move_to(row_target_centers(len(cells), y_row)[i])

        row_vis = VGroup(*cells)
        sample_tag = Text(f"样例 {sample_idx + 1}", font=FONT_CN, font_size=26, color=GRAY_A)
        sample_tag.next_to(row_vis, DOWN, buff=0.42)

        self.play(
            FadeIn(sample_tag, shift=UP * 0.12),
            LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cells], lag_ratio=0.05),
        )
        self.wait(0.3)

        ov, idxs = self.majority_highlight_show(cells, values, maj)
        self.majority_highlight_dismiss(ov, cells, idxs)
        self.wait(0.15)

        still_need_nm = True
        while len(values) > 1 and len(set(values)) > 1:
            i, j, still_need_nm = pick_pair_for_step(values, rng, maj, still_need_nm)
            a, b = cells[i], cells[j]
            self.play(a.animate.shift(UP * 1.05), b.animate.shift(UP * 1.05), run_time=0.42)
            mid = (a.get_center() + b.get_center()) / 2
            self.play(
                a.animate.move_to(mid + LEFT * 0.12),
                b.animate.move_to(mid + RIGHT * 0.12),
                run_time=0.32,
            )
            self.play(FadeOut(a), FadeOut(b), run_time=0.32)

            values.pop(j)
            values.pop(i)
            cells.pop(j)
            cells.pop(i)

            targets = row_target_centers(len(cells), y_row)
            self.play(*[c.animate.move_to(t) for c, t in zip(cells, targets)], run_time=0.52)
            self.wait(0.15)

        ov2, idxs2 = self.majority_highlight_show(cells, values, maj)
        self.wait(0.45)
        tail = VGroup(ov2, sample_tag, *cells)
        self.play(FadeOut(tail), run_time=0.75)
