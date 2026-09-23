"""LeetCode 4 归并求中位数：a / b / res 自上而下；a、b 已取出格变黄，res 内数字保持白色。

偶数长度结尾：框住两个中位格，框上方直接给出平均值；奇数则框单格。

运行 480p: 加 `-ql`；1080p60: 加 `-qh`。
  .\\manim-env\\Scripts\\manim.exe -ql median_two_sorted_merge_manim.py MedianTwoSortedMerge
  .\\manim-env\\Scripts\\manim.exe -qh median_two_sorted_merge_manim.py MedianTwoSortedMerge
"""

from __future__ import annotations

from manim import *


def merge_events(nums1: list[int], nums2: list[int]) -> list[tuple]:
    """事件: ('both', i, j, take_from) take_from 'a'|'b' | ('tail_a', i) | ('tail_b', j)"""
    i, j = 0, 0
    out: list[tuple] = []
    while i < len(nums1) and j < len(nums2):
        if nums1[i] < nums2[j]:
            out.append(("both", i, j, "a"))
            i += 1
        else:
            out.append(("both", i, j, "b"))
            j += 1
    while i < len(nums1):
        out.append(("tail_a", i))
        i += 1
    while j < len(nums2):
        out.append(("tail_b", j))
        j += 1
    return out


class MedianTwoSortedMerge(Scene):
    def construct(self):
        a = [1, 3, 5, 7, 11, 13, 15]
        b = [2, 3, 4, 5, 6, 7, 8]
        events = merge_events(a, b)
        n_a, n_b = len(a), len(b)
        n_res = n_a + n_b
        merged: list[int] = []

        cell_w_a, cell_h = 0.58, 0.82
        cell_w_b = 0.58
        cell_w_r, cell_h_r = 0.4, 0.78
        gap_a, gap_b, gap_r = 0.05, 0.05, 0.03
        sp_a = cell_w_a + gap_a
        sp_b = cell_w_b + gap_b
        sp_r = cell_w_r + gap_r

        sx_a = -(n_a - 1) * sp_a / 2
        sx_b = -(n_b - 1) * sp_b / 2
        sx_r = -(n_res - 1) * sp_r / 2

        def row_boxes(
            n: int,
            sx: float,
            sp: float,
            cw: float,
            ch: float,
            *,
            font: int,
        ) -> tuple[VGroup, VGroup]:
            cells = VGroup()
            texts = VGroup()
            for k in range(n):
                box = RoundedRectangle(
                    width=cw,
                    height=ch,
                    corner_radius=0.07,
                    color=GRAY_B,
                    stroke_width=2,
                    fill_opacity=0,
                )
                box.move_to(RIGHT * (sx + k * sp))
                t = Text("", font_size=font, color=WHITE).set_opacity(0)
                t.move_to(box.get_center())
                cells.add(box)
                texts.add(t)
            return cells, texts

        # a 上移避免 i 与 b 重叠；b 再上移一点，避免 j 与 res 重叠
        y_a = 2.58
        y_b = 0.38
        y_res = -1.78
        y_cmp = (y_a + y_b) / 2 + 0.08

        cells_a, texts_a = row_boxes(n_a, sx_a, sp_a, cell_w_a, cell_h, font=30)
        cells_b, texts_b = row_boxes(n_b, sx_b, sp_b, cell_w_b, cell_h, font=30)
        cells_r, texts_r = row_boxes(n_res, sx_r, sp_r, cell_w_r, cell_h_r, font=22)

        row_a = VGroup(cells_a, texts_a).move_to(np.array([0.0, y_a, 0.0]))
        row_b = VGroup(cells_b, texts_b).move_to(np.array([0.0, y_b, 0.0]))
        row_r = VGroup(cells_r, texts_r).move_to(np.array([0.0, y_res, 0.0]))

        lab_a = Text("a", font_size=34, color=WHITE).next_to(row_a, LEFT, buff=0.35)
        lab_b = Text("b", font_size=34, color=WHITE).next_to(row_b, LEFT, buff=0.35)
        lab_r = Text("res", font_size=30, color=WHITE).next_to(row_r, LEFT, buff=0.28)

        for k in range(n_a):
            texts_a[k].become(Text(str(a[k]), font_size=30, color=WHITE).move_to(cells_a[k].get_center()))
        for k in range(n_b):
            texts_b[k].become(Text(str(b[k]), font_size=30, color=WHITE).move_to(cells_b[k].get_center()))

        def col_center_x(cells: VGroup, sx: float, sp: float, idx: int) -> float:
            return cells.get_center()[0] + sx + idx * sp

        ptr_y_a = row_a.get_bottom()[1] - 0.62
        ptr_y_b = row_b.get_bottom()[1] - 0.58

        def pointer_at(
            cells: VGroup,
            sx: float,
            sp: float,
            idx: int,
            letter: str,
            base_y: float,
            color,
        ) -> VGroup:
            cx = col_center_x(cells, sx, sp, idx)
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
            lab = Text(letter, font_size=34, color=color).next_to(ar.get_start(), DOWN, buff=0.06)
            return VGroup(lab, ar)

        ptr_i = pointer_at(cells_a, sx_a, sp_a, 0, "i", ptr_y_a, BLUE)
        ptr_j = pointer_at(cells_b, sx_b, sp_b, 0, "j", ptr_y_b, RED)

        self.play(
            FadeIn(VGroup(lab_a, row_a, lab_b, row_b, lab_r, row_r), shift=DOWN * 0.15),
            run_time=0.55,
        )
        self.play(FadeIn(ptr_i, shift=UP * 0.1), FadeIn(ptr_j, shift=UP * 0.1), run_time=0.45)
        self.wait(0.2)

        k_res = 0
        i_cur, j_cur = 0, 0

        def anim_ptr_i(ii: int):
            idx = min(max(ii, 0), n_a - 1)
            return Transform(ptr_i, pointer_at(cells_a, sx_a, sp_a, idx, "i", ptr_y_a, BLUE))

        def anim_ptr_j(jj: int):
            idx = min(max(jj, 0), n_b - 1)
            return Transform(ptr_j, pointer_at(cells_b, sx_b, sp_b, idx, "j", ptr_y_b, RED))

        cmp_dx = 0.55
        cmp_l = np.array([-cmp_dx / 2, y_cmp, 0.0])
        cmp_r = np.array([cmp_dx / 2, y_cmp, 0.0])

        for ev in events:
            if ev[0] == "both":
                _, ii, jj, side = ev
                ca = texts_a[ii].copy()
                cb = texts_b[jj].copy()
                self.add(ca, cb)
                self.play(
                    ca.animate.move_to(cmp_l),
                    cb.animate.move_to(cmp_r),
                    run_time=0.45,
                )
                self.wait(0.12)
                if side == "a":
                    winner, loser = ca, cb
                    val = a[ii]
                    merged.append(val)
                    i_cur = ii + 1
                    j_cur = jj
                    after_ptr = [anim_ptr_i(i_cur), anim_ptr_j(j_cur)]
                    src_yellow = texts_a[ii].animate.set_color(YELLOW)
                else:
                    winner, loser = cb, ca
                    val = b[jj]
                    merged.append(val)
                    i_cur = ii
                    j_cur = jj + 1
                    after_ptr = [anim_ptr_i(i_cur), anim_ptr_j(j_cur)]
                    src_yellow = texts_b[jj].animate.set_color(YELLOW)

                self.play(
                    loser.animate.set_opacity(0.25),
                    winner.animate.scale(1.12),
                    run_time=0.22,
                )
                tgt = cells_r[k_res].get_center()
                self.play(
                    winner.animate.move_to(tgt).scale(1 / 1.12),
                    FadeOut(loser),
                    run_time=0.55,
                )
                self.remove(loser)
                new_t = Text(str(val), font_size=22, color=WHITE).move_to(tgt)
                old_slot = texts_r[k_res]
                self.play(
                    ReplacementTransform(winner, new_t),
                    src_yellow,
                    *after_ptr,
                    run_time=0.42,
                )
                self.remove(old_slot)
                subs = list(texts_r.submobjects)
                subs[k_res] = new_t
                texts_r.submobjects = subs
                k_res += 1
                self.wait(0.1)

            elif ev[0] == "tail_a":
                ii = ev[1]
                val = a[ii]
                merged.append(val)
                ca = texts_a[ii].copy()
                self.add(ca)
                self.play(ca.animate.move_to(np.array([0.0, y_cmp, 0.0])), run_time=0.38)
                tgt = cells_r[k_res].get_center()
                self.play(ca.animate.move_to(tgt), run_time=0.5)
                i_cur = ii + 1
                new_t = Text(str(val), font_size=22, color=WHITE).move_to(tgt)
                old_slot = texts_r[k_res]
                self.play(
                    ReplacementTransform(ca, new_t),
                    texts_a[ii].animate.set_color(YELLOW),
                    anim_ptr_i(i_cur),
                    run_time=0.42,
                )
                self.remove(old_slot)
                subs = list(texts_r.submobjects)
                subs[k_res] = new_t
                texts_r.submobjects = subs
                k_res += 1
                self.wait(0.08)

            else:  # tail_b
                jj = ev[1]
                val = b[jj]
                merged.append(val)
                cb = texts_b[jj].copy()
                self.add(cb)
                self.play(cb.animate.move_to(np.array([0.0, y_cmp, 0.0])), run_time=0.38)
                tgt = cells_r[k_res].get_center()
                self.play(cb.animate.move_to(tgt), run_time=0.5)
                j_cur = jj + 1
                new_t = Text(str(val), font_size=22, color=WHITE).move_to(tgt)
                old_slot = texts_r[k_res]
                self.play(
                    ReplacementTransform(cb, new_t),
                    texts_b[jj].animate.set_color(YELLOW),
                    anim_ptr_j(j_cur),
                    run_time=0.42,
                )
                self.remove(old_slot)
                subs = list(texts_r.submobjects)
                subs[k_res] = new_t
                texts_r.submobjects = subs
                k_res += 1
                self.wait(0.08)

        self.wait(0.35)

        # —— 中位数：框选 + 框上方直接给出数值 ——
        if n_res % 2 == 1:
            mid = n_res // 2
            ring = SurroundingRectangle(
                cells_r[mid],
                color=GOLD,
                buff=0.06,
                corner_radius=0.06,
                stroke_width=3,
            )
            out_val = merged[mid]
            out_str = str(int(out_val)) if out_val == int(out_val) else str(out_val)
            ans = Text(out_str, font_size=40, color=WHITE).next_to(ring, UP, buff=0.22)
            self.play(Create(ring), run_time=0.55)
            self.play(FadeIn(ans, shift=DOWN * 0.15), run_time=0.45)
            self.wait(1.0)
        else:
            lo, hi = n_res // 2 - 1, n_res // 2
            ring = SurroundingRectangle(
                VGroup(cells_r[lo], cells_r[hi]),
                color=GOLD,
                buff=0.05,
                corner_radius=0.06,
                stroke_width=3,
            )
            out_val = (merged[lo] + merged[hi]) / 2
            out_str = str(int(out_val)) if out_val == int(out_val) else str(out_val)
            ans = Text(out_str, font_size=40, color=WHITE).next_to(ring, UP, buff=0.22)
            self.play(Create(ring), run_time=0.55)
            self.play(FadeIn(ans, shift=DOWN * 0.15), run_time=0.45)
            self.wait(1.0)
