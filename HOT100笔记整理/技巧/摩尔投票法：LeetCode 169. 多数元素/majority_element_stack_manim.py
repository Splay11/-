"""LeetCode 169：栈思路模拟（题面 技巧/摩尔投票法-超过一半的数字.md）。

栈区为右开口线框：竖直方向略大于一行格子；线框水平宽度略大于数组总宽的 1/4；格子仍按数组同间距横向排布。栈与数组之间留窄缝。

运行：
  .\\manim-env\\Scripts\\manim.exe -ql majority_element_stack_manim.py MajorityStackVote
  .\\manim-env\\Scripts\\manim.exe -qh majority_element_stack_manim.py MajorityStackVote
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

STACK_V_PAD = 0.1
STACK_H_MARGIN = 0.22
# 线框水平宽度：在「数组总宽的 1/4」基础上略加长（约 +20%）
STACK_OUTLINE_FRAC = 0.30
# 栈区（格子可排布）与数组之间的水平缝（略近）
STACK_ARRAY_GAP = 0.20


def majority_element(nums: list[int]) -> int:
    cnt, cand = 0, 0
    for x in nums:
        if cnt == 0:
            cand = x
        cnt += 1 if x == cand else -1
    return cand


def array_total_width(n: int) -> float:
    if n <= 1:
        return float(CELL_W)
    return float((n - 1) * CELL_STEP + CELL_W)


def horizontal_stack_centers(k: int, stack_left: float, inner_w: float, y_row: float) -> list:
    """k 个栈元横向左齐：索引 0 为栈底（最左），k-1 为栈顶（最右）。"""
    if k <= 0:
        return []
    margin_l = 0.09
    left0 = stack_left + margin_l + CELL_W / 2
    return [np.array([left0 + i * CELL_STEP, y_row, 0.0]) for i in range(k)]


def compute_stack_array_layout(n: int, y_row: float) -> dict:
    rx = float(config.frame_x_radius)
    mx = 0.42
    gap = STACK_ARRAY_GAP

    array_w = array_total_width(n)
    cell_layout_w = array_w + STACK_H_MARGIN
    outline_w = max(array_w * STACK_OUTLINE_FRAC, CELL_W * 0.65)
    inner_h = CELL_H + STACK_V_PAD

    amin = -rx + mx + array_w / 2 + gap + cell_layout_w
    amax = rx - mx - array_w / 2
    if amin <= amax:
        array_cx = (amin + amax) / 2
    else:
        array_cx = 0.0

    stack_left = array_cx - array_w / 2 - gap - cell_layout_w
    stack_left = max(stack_left, -rx + mx)

    box_bottom = y_row - inner_h / 2

    return {
        "array_cx": float(array_cx),
        "stack_left": float(stack_left),
        "cell_layout_w": float(cell_layout_w),
        "outline_w": float(outline_w),
        "inner_h": float(inner_h),
        "box_bottom": float(box_bottom),
    }


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


def stack_outline_open_right(
    x_left: float,
    y_bottom: float,
    width: float,
    height: float,
    color=GRAY_A,
    stroke_width: float = 3.0,
) -> VGroup:
    y_top = y_bottom + height
    x_right = x_left + width
    left_edge = Line(
        np.array([x_left, y_bottom, 0.0]),
        np.array([x_left, y_top, 0.0]),
        color=color,
        stroke_width=stroke_width,
    )
    top_edge = Line(
        np.array([x_left, y_top, 0.0]),
        np.array([x_right, y_top, 0.0]),
        color=color,
        stroke_width=stroke_width,
    )
    bottom_edge = Line(
        np.array([x_left, y_bottom, 0.0]),
        np.array([x_right, y_bottom, 0.0]),
        color=color,
        stroke_width=stroke_width,
    )
    return VGroup(left_edge, top_edge, bottom_edge)


class MajorityStackVote(Scene):
    def construct(self) -> None:
        samples = [
            [2, 2, 1, 1, 1, 2, 2],
            [1, 2, 1, 4, 1, 4, 1, 3, 1, 1, 2],
        ]
        for idx, nums in enumerate(samples):
            self.play_one_sample(nums, idx, y_row=-0.32)
            if idx < len(samples) - 1:
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
        self.wait(0.28)
        return overlay, idxs

    def majority_highlight_dismiss(self, overlay: VGroup, cells: list[VGroup], idxs: list[int]) -> None:
        self.play(
            FadeOut(overlay),
            *[cells[i][1].animate.set_color(WHITE) for i in idxs],
            run_time=0.45,
        )

    def layout_array_cells(self, cells: list[VGroup], y: float, array_cx: float) -> None:
        for c, p in zip(cells, row_centers(len(cells), y, array_cx)):
            c.move_to(p)

    def play_one_sample(self, nums: list[int], sample_idx: int, y_row: float) -> None:
        maj = majority_element(nums)
        values = list(nums)
        n = len(nums)
        lay = compute_stack_array_layout(n, y_row)
        array_cx = lay["array_cx"]
        stack_left = lay["stack_left"]
        inner_w = lay["cell_layout_w"]
        outline_w = lay["outline_w"]
        inner_h = lay["inner_h"]
        box_bottom = lay["box_bottom"]

        cells = [make_cell(v) for v in values]
        self.layout_array_cells(cells, y_row, array_cx)

        row_vis = VGroup(*cells)
        sample_tag = Text(f"样例 {sample_idx + 1}", font=FONT_CN, font_size=26, color=GRAY_A)
        sample_tag.next_to(row_vis, DOWN, buff=0.4)

        self.play(
            FadeIn(sample_tag, shift=UP * 0.1),
            LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.04),
        )
        self.wait(0.25)

        ov, idxs = self.majority_highlight_show(cells, values, maj)
        self.majority_highlight_dismiss(ov, cells, idxs)
        self.wait(0.12)

        stack_outline = stack_outline_open_right(stack_left, box_bottom, outline_w, inner_h)
        stack_tip = Text("栈", font=FONT_CN, font_size=22, color=GRAY_B)
        stack_tip.next_to(stack_outline, UP, buff=0.1)

        self.play(FadeIn(stack_outline, shift=RIGHT * 0.08), FadeIn(stack_tip, shift=DOWN * 0.05))
        self.wait(0.12)

        queue_vals = list(nums)
        queue_cells = list(cells)
        stack_vals: list[int] = []
        stack_cells: list[VGroup] = []

        while queue_vals:
            hv = queue_vals[0]
            head = queue_cells[0]
            top_val = stack_vals[-1] if stack_vals else None

            self.play(head[0].animate.set_stroke(YELLOW, width=3), head[1].animate.set_color(YELLOW_A), run_time=0.22)
            self.wait(0.08)

            if stack_vals and top_val != hv:
                top = stack_cells.pop()
                stack_vals.pop()
                queue_vals.pop(0)
                queue_cells.pop(0)
                mid = (head.get_center() + top.get_center()) / 2 + UP * 0.12
                self.play(
                    head.animate.move_to(mid + LEFT * 0.08),
                    top.animate.move_to(mid + RIGHT * 0.08),
                    run_time=0.36,
                )
                self.play(FadeOut(head), FadeOut(top), run_time=0.26)
                self.remove(head, top)
            else:
                queue_vals.pop(0)
                queue_cells.pop(0)
                stack_vals.append(hv)
                stack_cells.append(head)
                pos = horizontal_stack_centers(len(stack_cells), stack_left, inner_w, y_row)
                tgt = pos[-1]
                self.play(head.animate.move_to(tgt), run_time=0.42)
                head[0].set_stroke(GRAY_B, width=2)
                head[1].set_color(WHITE)

            if queue_cells:
                self.play(
                    *[
                        queue_cells[i].animate.move_to(
                            row_centers(len(queue_cells), y_row, array_cx)[i]
                        )
                        for i in range(len(queue_cells))
                    ],
                    run_time=0.34,
                )
            if queue_cells:
                sample_tag.next_to(VGroup(*queue_cells), DOWN, buff=0.4)
            elif stack_cells:
                sample_tag.next_to(VGroup(*stack_cells), DOWN, buff=0.38)
            for qc in queue_cells:
                qc[0].set_stroke(GRAY_B, width=2)
                qc[1].set_color(WHITE)
            self.wait(0.08)

        if not stack_cells:
            self.play(FadeOut(VGroup(stack_outline, stack_tip, sample_tag)), run_time=0.5)
            return

        stack_row = VGroup(*stack_cells)
        hub_s = stack_row.get_center() + UP * (stack_row.height / 2 + 0.72)
        hub_dot = Dot(hub_s, radius=0.06, color=YELLOW)
        maj_lbl = Text("众数", font=FONT_CN, font_size=30, color=YELLOW)
        maj_lbl.next_to(hub_dot, UP, buff=0.1)
        sarrows = VGroup(
            *[
                Arrow(
                    hub_s,
                    sc.get_top() + UP * 0.02,
                    color=YELLOW,
                    stroke_width=2.5,
                    buff=0,
                    tip_length=0.14,
                    max_tip_length_to_length_ratio=0.25,
                )
                for sc in stack_cells
            ]
        )
        end_grp = VGroup(hub_dot, sarrows, maj_lbl)
        self.play(FadeIn(hub_dot, scale=0.5), Create(sarrows), Write(maj_lbl))
        self.play(
            *[
                AnimationGroup(
                    sc[1].animate.set_color(YELLOW),
                    sc[0].animate.set_stroke(YELLOW, width=2.5),
                )
                for sc in stack_cells
            ],
            run_time=0.35,
        )
        self.wait(0.2)
        self.play(*[sc[1].animate.set_color(YELLOW_E) for sc in stack_cells], run_time=0.18)
        self.play(*[sc[1].animate.set_color(YELLOW) for sc in stack_cells], run_time=0.18)
        self.play(*[sc[1].animate.set_color(YELLOW_E) for sc in stack_cells], run_time=0.18)
        self.play(*[sc[1].animate.set_color(YELLOW) for sc in stack_cells], run_time=0.18)
        self.wait(0.25)

        tail = VGroup(stack_outline, stack_tip, sample_tag, end_grp, *stack_cells)
        self.play(FadeOut(tail), run_time=0.7)
