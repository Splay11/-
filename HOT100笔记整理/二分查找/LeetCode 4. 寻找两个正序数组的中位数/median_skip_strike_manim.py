"""LeetCode 4「删去前一半再找中位数」：skip 阶段红斜线；中位数阶段金框；偶数末 (x+y)/2 展示。

运行 480p: `-ql`；1080p60: `-qh`。
  .\\manim-env\\Scripts\\manim.exe -ql median_skip_strike_manim.py MedianSkipStrike
  .\\manim-env\\Scripts\\manim.exe -qh median_skip_strike_manim.py MedianSkipStrike
"""

from __future__ import annotations

from manim import *


def build_events(A: list[int], B: list[int]):
    n, m = len(A), len(B)
    length = n + m
    i, j = 0, 0
    events: list[tuple] = []

    def take(phase: str):
        nonlocal i, j
        if i >= n:
            bi = j
            val = B[j]
            j += 1
            events.append((phase, "b", bi, val, i, j))
            return val
        if j >= m:
            ai = i
            val = A[i]
            i += 1
            events.append((phase, "a", ai, val, i, j))
            return val
        if A[i] < B[j]:
            ai = i
            val = A[i]
            i += 1
            events.append((phase, "a", ai, val, i, j))
            return val
        bi = j
        val = B[j]
        j += 1
        events.append((phase, "b", bi, val, i, j))
        return val

    for _ in range((length - 1) // 2):
        take("skip")

    median_cells: list[tuple[str, int]] = []
    if length % 2 == 1:
        take("median")
        e = events[-1]
        median_cells = [(e[1], e[2])]
    else:
        take("med_left")
        median_cells.append((events[-1][1], events[-1][2]))
        take("med_right")
        median_cells.append((events[-1][1], events[-1][2]))

    return events, median_cells, length


class MedianSkipStrike(Scene):
    def construct(self):
        A = [1, 3, 5, 7, 11, 13, 15]
        B = [2, 3, 4, 5, 6, 7, 8]
        events, median_cells, length = build_events(A, B)
        n_a, n_b = len(A), len(B)
        total_skip = (length - 1) // 2

        cell_w, cell_h = 0.58, 0.82
        gap = 0.05
        sp = cell_w + gap
        sx_a = -(n_a - 1) * sp / 2
        sx_b = -(n_b - 1) * sp / 2

        def row_boxes(n: int, sx: float) -> tuple[VGroup, VGroup]:
            cells = VGroup()
            texts = VGroup()
            for k in range(n):
                box = RoundedRectangle(
                    width=cell_w,
                    height=cell_h,
                    corner_radius=0.07,
                    color=GRAY_B,
                    stroke_width=2,
                    fill_opacity=0,
                )
                box.move_to(RIGHT * (sx + k * sp))
                t = Text("", font_size=30, color=WHITE).set_opacity(0)
                t.move_to(box.get_center())
                cells.add(box)
                texts.add(t)
            return cells, texts

        shift_left = LEFT * 1.05
        # 拉大 a、b 纵向间距；b 再略下移，避免挡住偶数末尾公式
        y_a = 1.38
        y_b = -1.72
        y_cmp = (y_a + y_b) / 2

        cells_a, texts_a = row_boxes(n_a, sx_a)
        cells_b, texts_b = row_boxes(n_b, sx_b)
        row_a = VGroup(cells_a, texts_a).move_to(np.array([0.0, y_a, 0.0]) + shift_left)
        row_b = VGroup(cells_b, texts_b).move_to(np.array([0.0, y_b, 0.0]) + shift_left)

        lab_a = Text("a", font_size=34, color=WHITE).next_to(row_a, LEFT, buff=0.32)
        lab_b = Text("b", font_size=34, color=WHITE).next_to(row_b, LEFT, buff=0.32)

        for k in range(n_a):
            texts_a[k].become(Text(str(A[k]), font_size=30, color=WHITE).move_to(cells_a[k].get_center()))
        for k in range(n_b):
            texts_b[k].become(Text(str(B[k]), font_size=30, color=WHITE).move_to(cells_b[k].get_center()))

        def col_center_x(cells: VGroup, sx: float, idx: int) -> float:
            return cells.get_center()[0] + sx + idx * sp

        ptr_y_a = row_a.get_bottom()[1] - 0.62
        ptr_y_b = row_b.get_bottom()[1] - 0.58

        def pointer_at(cells: VGroup, sx: float, idx: int, letter: str, base_y: float, color) -> VGroup:
            cx = col_center_x(cells, sx, idx)
            tip = np.array([cx, cells[idx].get_bottom()[1] - 0.08, 0.0])
            base = np.array([cx, base_y, 0.0])
            ar = Arrow(
                base,
                tip,
                buff=0.0,
                color=color,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.22,
            )
            lab = Text(letter, font_size=32, color=color).next_to(ar.get_start(), DOWN, buff=0.06)
            return VGroup(lab, ar)

        ptr_i = pointer_at(cells_a, sx_a, 0, "i", ptr_y_a, BLUE)
        ptr_j = pointer_at(cells_b, sx_b, 0, "j", ptr_y_b, RED)

        fs = 26
        line1 = Text(f"总长度:{length}", font_size=fs, color=WHITE)
        line2 = Text(f"总共需要删去 {total_skip} 个数字", font_size=fs, color=WHITE)
        y_rem_start = total_skip
        y_mob = Text(str(y_rem_start), font_size=fs, color=YELLOW)
        line3_left = Text("还需要删去 ", font_size=fs, color=WHITE)
        line3_right = Text(" 个 数字", font_size=fs, color=WHITE)
        line3 = VGroup(line3_left, y_mob, line3_right).arrange(RIGHT, buff=0.06)
        stats = VGroup(line1, line2, line3).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        stats.to_edge(RIGHT, buff=0.22)

        cmp_dx = 0.52
        ox, oy = float(shift_left[0]), float(shift_left[1])
        cmp_l = np.array([-cmp_dx / 2 + ox, y_cmp + oy, 0.0])
        cmp_r = np.array([cmp_dx / 2 + ox, y_cmp + oy, 0.0])

        def anim_ptr_i(ii: int):
            idx = min(max(ii, 0), n_a - 1)
            return Transform(ptr_i, pointer_at(cells_a, sx_a, idx, "i", ptr_y_a, BLUE))

        def anim_ptr_j(jj: int):
            idx = min(max(jj, 0), n_b - 1)
            return Transform(ptr_j, pointer_at(cells_b, sx_b, idx, "j", ptr_y_b, RED))

        def strike_line_for_cell(cell: RoundedRectangle) -> Line:
            inset = 0.1
            p0 = cell.get_corner(DL) + (DR + UP) * inset
            p1 = cell.get_corner(UR) + (UL + DOWN) * inset
            return Line(p0, p1, color=RED, stroke_width=4)

        def gold_frame_for_cell(cell: RoundedRectangle) -> SurroundingRectangle:
            return SurroundingRectangle(
                cell,
                color=GOLD,
                buff=0.06,
                corner_radius=0.06,
                stroke_width=3,
            )

        self.play(
            FadeIn(VGroup(lab_a, row_a, lab_b, row_b), shift=DOWN * 0.12),
            run_time=0.5,
        )
        self.play(FadeIn(stats, shift=LEFT * 0.15), run_time=0.48)
        self.wait(0.15)
        self.play(FadeIn(ptr_i, shift=UP * 0.1), FadeIn(ptr_j, shift=UP * 0.1), run_time=0.42)
        self.wait(0.15)

        skips_done = 0
        prev_i, prev_j = 0, 0
        med_left_val: int | None = None
        med_right_val: int | None = None

        for ev in events:
            phase, side, idx, val, i_after, j_after = ev
            ib, jb = prev_i, prev_j
            is_skip = phase == "skip"

            ptr_anims = [anim_ptr_i(i_after), anim_ptr_j(j_after)]
            y_anims: list = []
            if is_skip:
                skips_done += 1
                y_new = total_skip - skips_done
                new_y = Text(str(y_new), font_size=fs, color=YELLOW).move_to(y_mob.get_center())
                y_anims = [Transform(y_mob, new_y)]

            cell_take = cells_a[idx] if side == "a" else cells_b[idx]

            if ib < n_a and jb < n_b:
                ca = texts_a[ib].copy()
                cb = texts_b[jb].copy()
                self.add(ca, cb)
                self.play(
                    ca.animate.move_to(cmp_l),
                    cb.animate.move_to(cmp_r),
                    run_time=0.4,
                )
                self.wait(0.08)
                if side == "a":
                    winner, loser = ca, cb
                else:
                    winner, loser = cb, ca
                self.play(
                    loser.animate.set_opacity(0.28),
                    winner.animate.scale(1.1),
                    run_time=0.18,
                )
                self.play(
                    winner.animate.move_to(cell_take.get_center()).scale(1 / 1.1),
                    FadeOut(loser),
                    run_time=0.45,
                )
                self.remove(loser)
                self.play(FadeOut(winner, scale=0.85), run_time=0.22)
                self.remove(winner)
            elif ib >= n_a:
                cb = texts_b[idx].copy()
                self.add(cb)
                self.play(cb.animate.move_to((cmp_l + cmp_r) / 2), run_time=0.32)
                self.play(cb.animate.move_to(cell_take.get_center()), run_time=0.4)
                self.play(FadeOut(cb, scale=0.85), run_time=0.2)
                self.remove(cb)
            else:
                ca = texts_a[idx].copy()
                self.add(ca)
                self.play(ca.animate.move_to((cmp_l + cmp_r) / 2), run_time=0.32)
                self.play(ca.animate.move_to(cell_take.get_center()), run_time=0.4)
                self.play(FadeOut(ca, scale=0.85), run_time=0.2)
                self.remove(ca)

            if is_skip:
                strike = strike_line_for_cell(cell_take)
                if y_anims:
                    self.play(Create(strike), *ptr_anims, *y_anims, run_time=0.42)
                else:
                    self.play(Create(strike), *ptr_anims, run_time=0.42)
            else:
                frame = gold_frame_for_cell(cell_take)
                self.play(Create(frame), *ptr_anims, run_time=0.42)
                if phase == "med_left":
                    med_left_val = val
                elif phase == "med_right":
                    med_right_val = val

            prev_i, prev_j = i_after, j_after
            self.wait(0.08)

        # 奇数：中位数步已金框结束，不再叠框
        if length % 2 == 0 and med_left_val is not None and med_right_val is not None:
            self.wait(0.2)
            (s1, i1), (s2, i2) = median_cells
            c1 = texts_a[i1].copy() if s1 == "a" else texts_b[i1].copy()
            c2 = texts_a[i2].copy() if s2 == "a" else texts_b[i2].copy()
            self.add(c1, c2)
            mid_pt = np.array([ox, y_cmp + oy, 0.0])
            self.play(
                c1.animate.move_to(mid_pt + LEFT * 0.38),
                c2.animate.move_to(mid_pt + RIGHT * 0.38),
                run_time=0.65,
            )
            self.wait(0.15)
            x, y = med_left_val, med_right_val
            out = (x + y) / 2
            out_str = str(int(out)) if out == int(out) else str(out)
            # 按题意展示 (x+y)/2 = 结果；（x+y)/2 与「x + y/2」区分，此处为两数算术平均
            formula = Text(f"({x}+{y})/2 = {out_str}", font_size=32, color=WHITE).next_to(
                VGroup(c1, c2), DOWN, buff=0.32
            )
            formula.shift(UP * 0.22)
            self.play(Write(formula), run_time=0.65)
            self.wait(1.2)
