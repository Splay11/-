"""LeetCode 15 三数之和：排序后固定 i，相向双指针 j、k，和与 0 比较。

数组 [-1,0,1,2,-1,-4] 排序后为 [-4,-1,-1,0,1,2]。
运行: python -m manim -ql 同向双指针\\three_sum_manim.py ThreeSumTwoPointers
"""

from __future__ import annotations

from manim import *


RAW = [-1, 0, 1, 2, -1, -4]
NUMS = sorted(RAW)
N = len(NUMS)

# 预计算与算法一致的每一步（便于逐帧动画）
STEPS: list[tuple] = []
for i in range(N):
    if i > 0 and NUMS[i] == NUMS[i - 1]:
        STEPS.append(("skip_i", i, None, None, None))
        continue
    j, k = i + 1, N - 1
    while j < k:
        s = NUMS[i] + NUMS[j] + NUMS[k]
        STEPS.append(("check", i, j, k, s))
        if s == 0:
            STEPS.append(("hit", i, j, k, 0))
            j += 1
            k -= 1
            STEPS.append(("shrink", i, j, k, None))
            while j < k and NUMS[j] == NUMS[j - 1]:
                STEPS.append(("skip_j", i, j, k, None))
                j += 1
            while j < k and NUMS[k] == NUMS[k + 1]:
                STEPS.append(("skip_k", i, j, k, None))
                k -= 1
        elif s < 0:
            STEPS.append(("jpp", i, j, k, s))
            j += 1
        else:
            STEPS.append(("kmm", i, j, k, s))
            k -= 1


def sum_line_tex(i: int, j: int, k: int, s: int) -> str:
    if s < 0:
        return f"nums[{i}] + nums[{j}] + nums[{k}] = {s} < 0"
    if s > 0:
        return f"nums[{i}] + nums[{j}] + nums[{k}] = {s} > 0"
    return f"nums[{i}] + nums[{j}] + nums[{k}] = 0"


class ThreeSumTwoPointers(Scene):
    def construct(self) -> None:
        # 总时长约 25s：rt(·) 内为「未拉伸」秒，整体乘 (_T_TARGET/_T_BASE)。偏快/偏慢可改 _T_BASE。
        _T_BASE = 21.0
        _T_TARGET = 25.0

        def rt(t: float) -> float:
            return round(t * (_T_TARGET / _T_BASE), 2)

        cell_w, cell_h = 0.62, 0.68
        gap = 0.06
        sp = cell_w + gap
        sx = -(N - 1) * sp / 2
        y_arr = 0.35

        cells = VGroup()
        vals = VGroup()
        for idx in range(N):
            r = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.08,
                color=GRAY_B,
                stroke_width=2,
            )
            t = Text(str(NUMS[idx]), font_size=30)
            r.move_to(np.array([sx + idx * sp, y_arr, 0.0]))
            t.move_to(r.get_center())
            cells.add(r)
            vals.add(t)

        arr_g = VGroup(cells, vals).move_to(ORIGIN + UP * 0.42)

        idx_row = VGroup(
            *[
                Text(str(idx), font_size=18, color=GRAY).next_to(cells[idx], DOWN, buff=0.16)
                for idx in range(N)
            ]
        )

        def col_x(p: int) -> float:
            return arr_g.get_center()[0] + sx + p * sp

        # 指针从上方指向格子（箭尾在上、箭头朝下）
        ptr_y_i = arr_g.get_top()[1] + 0.5
        ptr_y_j = arr_g.get_top()[1] + 0.72
        ptr_y_k = arr_g.get_top()[1] + 0.94

        def ptr_i_at(p: int) -> VGroup:
            tip = np.array([col_x(p), cells[p].get_top()[1] + 0.07, 0.0])
            base = np.array([col_x(p), ptr_y_i, 0.0])
            ar = Arrow(base, tip, buff=0.0, color=BLUE, stroke_width=3, max_tip_length_to_length_ratio=0.22)
            lb = Text("i", font_size=32, color=BLUE).next_to(ar.get_start(), UP, buff=0.05)
            return VGroup(lb, ar)

        def ptr_j_at(p: int) -> VGroup:
            tip = np.array([col_x(p), cells[p].get_top()[1] + 0.07, 0.0])
            base = np.array([col_x(p), ptr_y_j, 0.0])
            ar = Arrow(base, tip, buff=0.0, color=RED, stroke_width=3, max_tip_length_to_length_ratio=0.22)
            lb = Text("j", font_size=32, color=RED).next_to(ar.get_start(), UP, buff=0.02)
            return VGroup(lb, ar)

        def ptr_k_at(p: int) -> VGroup:
            tip = np.array([col_x(p), cells[p].get_top()[1] + 0.07, 0.0])
            base = np.array([col_x(p), ptr_y_k, 0.0])
            ar = Arrow(base, tip, buff=0.0, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.22)
            lb = Text("k", font_size=32, color=GREEN).next_to(ar.get_start(), UP, buff=0.02)
            return VGroup(lb, ar)

        sum_tex = Text(
            sum_line_tex(0, 1, N - 1, NUMS[0] + NUMS[1] + NUMS[N - 1]),
            font_size=26,
            color=WHITE,
        )
        sum_tex.next_to(idx_row, DOWN, buff=0.38)

        # 命中方案逐行排在 sum 式子下方（用列表记上一行位置）
        answer_lines: list = []

        self.play(FadeIn(arr_g, shift=DOWN * 0.12), FadeIn(idx_row, shift=DOWN * 0.08), run_time=rt(0.5))
        self.play(FadeIn(sum_tex, shift=UP * 0.1), run_time=rt(0.4))
        self.wait(rt(0.28))

        ptr_i = ptr_j = ptr_k = None

        for step in STEPS:
            kind = step[0]
            if kind == "skip_i":
                i = step[1]
                self.play(
                    Indicate(cells[i], color=YELLOW, scale_factor=1.08),
                    Indicate(cells[i - 1], color=YELLOW, scale_factor=1.05),
                    run_time=rt(0.45),
                )
                outs = []
                if ptr_i is not None:
                    outs.append(FadeOut(ptr_i))
                    ptr_i = None
                if ptr_j is not None:
                    outs.append(FadeOut(ptr_j))
                    ptr_j = None
                if ptr_k is not None:
                    outs.append(FadeOut(ptr_k))
                    ptr_k = None
                if outs:
                    self.play(*outs, run_time=rt(0.22))
                self.wait(rt(0.15))
                continue

            i, j, k = step[1], step[2], step[3]
            s = step[4]

            new_sum = Text(sum_line_tex(i, j, k, s if s is not None else NUMS[i] + NUMS[j] + NUMS[k]), font_size=26, color=WHITE)
            new_sum.move_to(sum_tex.get_center())

            if kind == "check" and s is not None:
                # 先动指针，再更新下方算式，再闪格子
                ni, nj, nk = ptr_i_at(i), ptr_j_at(j), ptr_k_at(k)
                anims = []
                if ptr_i is None:
                    ptr_i = ni
                    anims.append(FadeIn(ptr_i, shift=DOWN * 0.12))
                else:
                    anims.append(Transform(ptr_i, ni))
                if ptr_j is None:
                    ptr_j = nj
                    anims.append(FadeIn(ptr_j, shift=DOWN * 0.12))
                else:
                    anims.append(Transform(ptr_j, nj))
                if ptr_k is None:
                    ptr_k = nk
                    anims.append(FadeIn(ptr_k, shift=DOWN * 0.12))
                else:
                    anims.append(Transform(ptr_k, nk))
                self.play(*anims, run_time=rt(0.42))
                self.play(ReplacementTransform(sum_tex, new_sum), run_time=rt(0.36))
                sum_tex = new_sum
                self.play(
                    Flash(cells[i], color=BLUE, flash_radius=0.28, line_length=0.08),
                    Flash(cells[j], color=RED, flash_radius=0.28, line_length=0.08),
                    Flash(cells[k], color=GREEN, flash_radius=0.28, line_length=0.08),
                    run_time=rt(0.38),
                )
                self.wait(rt(0.18))

            elif kind in ("jpp", "kmm"):
                if kind == "jpp":
                    self.play(Transform(ptr_j, ptr_j_at(j)), run_time=rt(0.36))
                else:
                    self.play(Transform(ptr_k, ptr_k_at(k)), run_time=rt(0.36))
                self.play(ReplacementTransform(sum_tex, new_sum), run_time=rt(0.32))
                sum_tex = new_sum
                self.wait(rt(0.14))

            elif kind == "hit":
                self.play(
                    cells[i].animate.set_stroke(GREEN, width=4),
                    cells[j].animate.set_stroke(GREEN, width=4),
                    cells[k].animate.set_stroke(GREEN, width=4),
                    run_time=rt(0.38),
                )
                self.play(
                    Flash(cells[i], color=GREEN, flash_radius=0.4),
                    Flash(cells[j], color=GREEN, flash_radius=0.4),
                    Flash(cells[k], color=GREEN, flash_radius=0.4),
                    run_time=rt(0.48),
                )
                self.play(ReplacementTransform(sum_tex, new_sum), run_time=rt(0.34))
                sum_tex = new_sum
                # 三数复制一份飞到下方排成一行
                tri_vals = (NUMS[i], NUMS[j], NUMS[k])
                fly = VGroup(
                    *[
                        Text(str(tri_vals[t]), font_size=28, color=YELLOW).move_to(vals[p].get_center())
                        for t, p in enumerate((i, j, k))
                    ]
                )
                cent = (cells[i].get_center() + cells[j].get_center() + cells[k].get_center()) / 3.0
                fly.arrange(RIGHT, buff=0.12).move_to(cent + UP * 0.12)
                self.add(fly)

                row_final = VGroup(
                    *[Text(str(tri_vals[t]), font_size=26, color=GREEN) for t in range(3)]
                ).arrange(RIGHT, buff=0.28)
                if not answer_lines:
                    row_final.next_to(sum_tex, DOWN, buff=0.52)
                else:
                    row_final.next_to(answer_lines[-1], DOWN, buff=0.14)
                self.play(
                    ReplacementTransform(fly, row_final, path_arc=-TAU / 5),
                    run_time=rt(0.78),
                    rate_func=smooth,
                )
                answer_lines.append(row_final)

                self.play(
                    cells[i].animate.set_stroke(GRAY_B, width=2),
                    cells[j].animate.set_stroke(GRAY_B, width=2),
                    cells[k].animate.set_stroke(GRAY_B, width=2),
                    run_time=rt(0.28),
                )
                self.wait(rt(0.16))

            elif kind == "shrink":
                nj, nk = ptr_j_at(j), ptr_k_at(k)
                self.play(Transform(ptr_j, nj), Transform(ptr_k, nk), run_time=rt(0.38))
                self.wait(rt(0.12))

            elif kind == "skip_j":
                self.play(Transform(ptr_j, ptr_j_at(j)), run_time=rt(0.32))
                self.play(Indicate(cells[j], color=ORANGE, scale_factor=1.06), run_time=rt(0.3))
                self.wait(rt(0.12))

            elif kind == "skip_k":
                self.play(Transform(ptr_k, ptr_k_at(k)), run_time=rt(0.32))
                self.play(Indicate(cells[k], color=ORANGE, scale_factor=1.06), run_time=rt(0.3))
                self.wait(rt(0.12))

        self.wait(rt(0.65))
