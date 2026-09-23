"""LeetCode 169：摩尔投票「左侧候选 + 计数」可视化（题面 技巧/摩尔投票法-超过一半的数字.md 102–115）。

无栈：画面分左右两区；数组在右侧区居中，左侧为当前候选格与上方计数。队首每次飞入左侧执行相等则 ++、不等则烟花并 --，计数为 0 时左侧清空。

运行：
  .\\manim-env\\Scripts\\manim.exe -ql majority_element_counter_manim.py MajorityCounterMoore
  .\\manim-env\\Scripts\\manim.exe -qh majority_element_counter_manim.py MajorityCounterMoore
"""

from __future__ import annotations

from pathlib import Path

from manim import *

config.media_dir = str(Path(__file__).resolve().parent / "media")

CELL_W = 0.52
CELL_BUFF = 0.07
CELL_STEP = CELL_W + CELL_BUFF
CELL_H = 0.72
FONT_CN = "Microsoft YaHei"


def majority_element(nums: list[int]) -> int:
    cnt, cand = 0, 0
    for x in nums:
        if cnt == 0:
            cand = x
        cnt += 1 if x == cand else -1
    return cand


def make_cell(val: int) -> VGroup:
    box = RoundedRectangle(
        width=CELL_W,
        height=CELL_H,
        corner_radius=0.06,
        color=GRAY_B,
        stroke_width=2,
        fill_color=BLACK,
        fill_opacity=0.35,
    )
    txt = Text(str(val), font_size=34, color=WHITE)
    return VGroup(box, txt)


def row_centers(n: int, y: float, cx: float) -> list:
    if n == 0:
        return []
    return [np.array([cx - (n - 1) * CELL_STEP / 2 + i * CELL_STEP, y, 0.0]) for i in range(n)]


def panel_centers(y_row: float) -> tuple[float, float]:
    """左半区、右半区陈列中心 x（各自区域内近似居中）。"""
    rx = float(config.frame_x_radius)
    left_cx = -rx * 0.40
    right_cx = rx * 0.40
    return left_cx, right_cx


class MajorityCounterMoore(Scene):
    def play_fireworks_on(self, mob: Mobject, run_time: float = 0.48) -> None:
        c = mob.get_center()
        n = 14
        cols = [YELLOW, RED, ORANGE, GOLD, PINK]
        dots = VGroup(
            *[
                Dot(
                    c,
                    radius=0.042,
                    color=cols[i % len(cols)],
                )
                for i in range(n)
            ]
        )
        self.add(dots)
        anims = []
        for i, d in enumerate(dots):
            ang = TAU * i / n + 0.15
            anims.append(
                d.animate.shift(0.55 * np.array([np.cos(ang), np.sin(ang), 0.0])).set_opacity(0)
            )
        self.play(
            LaggedStart(*anims, lag_ratio=0.06),
            Flash(mob, color=YELLOW, flash_radius=0.5, line_length=0.22, time_width=0.35),
            run_time=run_time,
        )
        self.remove(dots)

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
        self.wait(0.22)
        return overlay, idxs

    def majority_highlight_dismiss(self, overlay: VGroup, cells: list[VGroup], idxs: list[int]) -> None:
        self.play(
            FadeOut(overlay),
            *[cells[i][1].animate.set_color(WHITE) for i in idxs],
            run_time=0.45,
        )

    def construct(self) -> None:
        samples = [
            [2, 2, 1, 1, 1, 2, 2],
            [1, 2, 1, 4, 1, 4, 1, 3, 1, 1, 2],
        ]
        for idx, nums in enumerate(samples):
            self.play_one_sample(nums, idx, y_row=-0.28)
            if idx < len(samples) - 1:
                self.wait(0.35)

    def play_one_sample(self, nums: list[int], sample_idx: int, y_row: float) -> None:
        maj = majority_element(nums)
        left_cx, right_cx = panel_centers(y_row)

        values = list(nums)
        cells = [make_cell(v) for v in values]
        for c, p in zip(cells, row_centers(len(cells), y_row, right_cx)):
            c.move_to(p)

        sample_tag = Text(f"样例 {sample_idx + 1}", font=FONT_CN, font_size=26, color=GRAY_A)
        sample_tag.next_to(VGroup(*cells), DOWN, buff=0.42)

        self.play(
            FadeIn(sample_tag, shift=UP * 0.08),
            LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.04),
        )
        self.wait(0.22)

        ov, idxs = self.majority_highlight_show(cells, values, maj)
        self.majority_highlight_dismiss(ov, cells, idxs)
        self.wait(0.1)

        queue_cells = list(cells)
        queue_vals = list(nums)

        cnt = 0
        left_val: int | None = None
        left_cell: VGroup | None = None
        cnt_text: Text | None = None

        left_anchor = np.array([left_cx, y_row, 0.0])

        while queue_vals:
            hv = queue_vals[0]
            head = queue_cells[0]
            self.play(head[0].animate.set_stroke(YELLOW, width=3), head[1].animate.set_color(YELLOW_A), run_time=0.2)
            self.wait(0.06)

            if cnt == 0:
                self.play(head.animate.move_to(left_anchor), run_time=0.48)
                queue_vals.pop(0)
                queue_cells.pop(0)
                left_cell = head
                left_val = hv
                cnt = 1
                cnt_text = Text("1", font=FONT_CN, font_size=38, color=YELLOW)
                cnt_text.next_to(left_cell, UP, buff=0.22)
                self.play(FadeIn(cnt_text, shift=UP * 0.04), run_time=0.12)
                head[0].set_stroke(GRAY_B, width=2)
                head[1].set_color(WHITE)
            elif hv == left_val:
                self.play(head.animate.move_to(left_cell.get_center()), run_time=0.4)
                queue_vals.pop(0)
                queue_cells.pop(0)
                cnt += 1
                new_t = Text(str(cnt), font=FONT_CN, font_size=38, color=YELLOW)
                new_t.move_to(cnt_text.get_center())
                self.play(FadeOut(head), ReplacementTransform(cnt_text, new_t), run_time=0.16)
                cnt_text = new_t
            else:
                mid = (head.get_center() + left_cell.get_center()) / 2 + UP * 0.08
                self.play(head.animate.move_to(mid + LEFT * 0.06), run_time=0.34)
                self.play_fireworks_on(left_cell)
                cnt -= 1
                queue_vals.pop(0)
                queue_cells.pop(0)
                self.play(FadeOut(head), run_time=0.2)
                if cnt == 0:
                    self.play(FadeOut(left_cell), FadeOut(cnt_text), run_time=0.4)
                    left_cell = None
                    cnt_text = None
                    left_val = None
                else:
                    new_t = Text(str(cnt), font=FONT_CN, font_size=38, color=YELLOW)
                    new_t.move_to(cnt_text.get_center())
                    self.play(ReplacementTransform(cnt_text, new_t), run_time=0.14)
                    cnt_text = new_t

            if queue_cells:
                self.play(
                    *[
                        queue_cells[i].animate.move_to(
                            row_centers(len(queue_cells), y_row, right_cx)[i]
                        )
                        for i in range(len(queue_cells))
                    ],
                    run_time=0.34,
                )
                sample_tag.next_to(VGroup(*queue_cells), DOWN, buff=0.42)
            for qc in queue_cells:
                qc[0].set_stroke(GRAY_B, width=2)
                qc[1].set_color(WHITE)
            self.wait(0.08)

        if left_cell is not None and cnt_text is not None:
            hub = left_cell.get_center() + UP * (left_cell.height / 2 + 0.72)
            hub_dot = Dot(hub, radius=0.06, color=YELLOW)
            maj_lbl = Text("众数", font=FONT_CN, font_size=30, color=YELLOW)
            maj_lbl.next_to(hub_dot, UP, buff=0.1)
            arr = Arrow(
                hub,
                left_cell.get_top() + UP * 0.02,
                color=YELLOW,
                stroke_width=2.5,
                buff=0,
                tip_length=0.14,
                max_tip_length_to_length_ratio=0.25,
            )
            end_grp = VGroup(hub_dot, arr, maj_lbl)
            self.play(FadeIn(hub_dot, scale=0.5), Create(arr), Write(maj_lbl))
            self.play(
                AnimationGroup(
                    left_cell[1].animate.set_color(YELLOW),
                    left_cell[0].animate.set_stroke(YELLOW, width=2.5),
                ),
                run_time=0.28,
            )
            self.wait(0.18)
            self.play(left_cell[1].animate.set_color(YELLOW_E), run_time=0.16)
            self.play(left_cell[1].animate.set_color(YELLOW), run_time=0.16)
            self.play(left_cell[1].animate.set_color(YELLOW_E), run_time=0.16)
            self.play(left_cell[1].animate.set_color(YELLOW), run_time=0.16)
            self.wait(0.2)
            tail = VGroup(sample_tag, left_cell, cnt_text, end_grp)
        else:
            tail = VGroup(sample_tag)

        self.play(FadeOut(tail), run_time=0.65)
