"""二分查找可视化（给定代码版本）：数组居中、左右分色、L / R / mid 指针、结束烟花或震动。

多组样例：若相邻两组数组相同，则组间只淡出 T、双指针、虚线，数组合并并重置数字颜色后继续下一组。

运行（480p）:
  .\\manim-env\\Scripts\\manim.exe -pql binary_search_manim.py BinarySearchAnimation
"""

from __future__ import annotations

from bisect import bisect_right

from manim import *


def collect_steps(A: list, x: int) -> list[tuple[int, int, int, bool]]:
    """每一步: (left, right, mid, a_mid_gt_x)。"""
    left = 0
    right = len(A) - 1
    steps: list[tuple[int, int, int, bool]] = []
    while left <= right:
        mid = (left + right) // 2
        gt = A[mid] > x
        steps.append((left, right, mid, gt))
        if gt:
            right = mid - 1
        else:
            left = mid + 1
    return steps


class BinarySearchAnimation(Scene):
    DEMO_CASES = [
        ([1, 2, 4, 5, 7, 10, 11, 13], 7),
        ([1, 2, 4, 5, 7, 10, 11, 13], 10),
        ([1, 2, 4, 5, 7, 10, 11, 13], 6),
    ]
    search_array = [1, 2, 4, 5, 7, 10, 11, 13]
    target = 7

    def construct(self):
        self._reuse_bundle = None
        for case_index, (arr, t) in enumerate(self.DEMO_CASES):
            self._play_one_demo(list(arr), int(t), case_index)

    def _transition_same_array_next(
        self,
        *,
        split_idx: int,
        split_dx: float,
        n: int,
        cells: VGroup,
        texts: VGroup,
        title: Mobject,
        ptr_l: Mobject,
        ptr_r: Mobject,
        dashed: Mobject | None,
    ) -> None:
        fade_mobs = [title, ptr_l, ptr_r]
        if dashed is not None:
            fade_mobs.append(dashed)
        self.play(FadeOut(VGroup(*fade_mobs)), run_time=0.55)
        if 0 < split_idx < n:
            merge_anims = []
            for i in range(split_idx):
                merge_anims.append(cells[i].animate.shift(RIGHT * split_dx))
                merge_anims.append(texts[i].animate.shift(RIGHT * split_dx))
            for i in range(split_idx, n):
                merge_anims.append(cells[i].animate.shift(LEFT * split_dx))
                merge_anims.append(texts[i].animate.shift(LEFT * split_dx))
            self.play(*merge_anims, run_time=0.5)
        self.play(*[texts[i].animate.set_color(WHITE) for i in range(n)], run_time=0.35)
        self.wait(0.12)

    def _play_one_demo(self, A: list, x: int, case_index: int) -> None:
        n = len(A)
        if n == 0:
            self.add(Text("search_array 为空", font_size=36))
            self.wait(1)
            return

        cell_w, cell_h = 0.72, 0.88
        gap = 0.06
        spacing = cell_w + gap
        start_x = -(n - 1) * spacing / 2

        fresh = self._reuse_bundle is None
        if fresh:
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
                tk = Text(str(A[k]), font_size=30, color=WHITE)
                box.move_to(RIGHT * (start_x + k * spacing))
                tk.move_to(box.get_center())
                cells.add(box)
                texts.add(tk)

            array_g = VGroup(cells, texts)
            array_g.move_to(ORIGIN)
        else:
            cells, texts, array_g, spacing, cell_w, gap, start_x = self._reuse_bundle
            self._reuse_bundle = None

        def col_x(k: int) -> float:
            return float(cells[k].get_center()[0])

        split_idx = bisect_right(A, x)
        left_color = "#2ecc71"
        right_color = "#e85d04"

        top_arr = float(array_g.get_top()[1])
        ptr_y_l = top_arr + 0.78
        ptr_y_r = top_arr + 0.58
        ptr_y_m = top_arr + 0.34

        title_bottom_clear = ptr_y_l + 0.45
        title_buff = max(1.35, (title_bottom_clear - top_arr) + 0.2)
        title = Text(f"T = {x}", font_size=40).next_to(array_g, UP, buff=title_buff)

        dashed = None
        if 0 < split_idx < n:
            x_line = (col_x(split_idx - 1) + col_x(split_idx)) / 2
            top_y = cells[0].get_top()[1] + 0.42
            bot_y = cells[0].get_bottom()[1] - 0.42
            dashed = DashedLine(
                [x_line, top_y, 0],
                [x_line, bot_y, 0],
                color=GRAY,
                stroke_width=2,
                dash_length=0.12,
                dashed_ratio=0.5,
            )

        split_dx = 0.14

        def tip_x_for_index(idx: int) -> float:
            if idx < 0:
                return col_x(0) - spacing * 0.55
            if idx >= n:
                return col_x(n - 1) + spacing * 0.55
            return col_x(idx)

        def cell_i(idx: int) -> int:
            return max(0, min(n - 1, idx))

        def pointer_l_at(idx: int) -> VGroup:
            tx = tip_x_for_index(idx) - 0.07
            tip_y = cells[cell_i(idx)].get_top()[1] + 0.06
            tip = np.array([tx, tip_y, 0.0])
            base = np.array([tx, ptr_y_l, 0.0])
            ar = Arrow(
                base,
                tip,
                buff=0.0,
                color=BLUE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.22,
            )
            lab = Text("L", font_size=34, color=BLUE).next_to(base, UP, buff=0.05)
            return VGroup(lab, ar)

        def pointer_r_at(idx: int) -> VGroup:
            tx = tip_x_for_index(idx) + 0.07
            tip_y = cells[cell_i(idx)].get_top()[1] + 0.06
            tip = np.array([tx, tip_y, 0.0])
            base = np.array([tx, ptr_y_r, 0.0])
            ar = Arrow(
                base,
                tip,
                buff=0.0,
                color=RED,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.22,
            )
            lab = Text("R", font_size=34, color=RED).next_to(base, UP, buff=0.05)
            return VGroup(lab, ar)

        def pointer_mid_at(idx: int) -> VGroup:
            tx = tip_x_for_index(idx)
            ci = cell_i(idx)
            tip_y = cells[ci].get_top()[1] + 0.06
            tip = np.array([tx, tip_y, 0.0])
            base = np.array([tx, ptr_y_m, 0.0])
            ar = Arrow(
                base,
                tip,
                buff=0.0,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
            )
            return VGroup(ar)

        if fresh:
            self.play(FadeIn(array_g, shift=UP * 0.15))
            self.wait(0.2)
        self.play(Write(title))
        self.wait(0.2)

        if dashed is not None:
            self.play(Create(dashed), run_time=0.6)
            self.wait(0.12)
            sep_anims = []
            for i in range(split_idx):
                sep_anims.append(cells[i].animate.shift(LEFT * split_dx))
                sep_anims.append(texts[i].animate.shift(LEFT * split_dx))
            for i in range(split_idx, n):
                sep_anims.append(cells[i].animate.shift(RIGHT * split_dx))
                sep_anims.append(texts[i].animate.shift(RIGHT * split_dx))
            self.play(*sep_anims, run_time=0.55)
            self.wait(0.12)

        left_anims = [texts[i].animate.set_color(left_color) for i in range(split_idx)]
        right_anims = [texts[i].animate.set_color(right_color) for i in range(split_idx, n)]
        if left_anims or right_anims:
            self.play(*left_anims, *right_anims, run_time=0.65)
        self.wait(0.25)

        steps = collect_steps(A, x)
        ptr_l = pointer_l_at(0)
        ptr_r = pointer_r_at(n - 1)
        ptr_m: VGroup | None = None

        self.play(FadeIn(ptr_l, shift=DOWN * 0.1), FadeIn(ptr_r, shift=DOWN * 0.1))
        self.wait(0.2)

        cur_l, cur_r = 0, n - 1

        for _, (entry_l, entry_r, mid, gt) in enumerate(steps):
            pl = pointer_l_at(entry_l)
            pr = pointer_r_at(entry_r)
            self.play(
                ReplacementTransform(ptr_l, pl),
                ReplacementTransform(ptr_r, pr),
                run_time=0.42,
            )
            ptr_l, ptr_r = pl, pr

            new_mid = pointer_mid_at(mid)
            if ptr_m is None:
                ptr_m = new_mid
                self.play(FadeIn(ptr_m, shift=DOWN * 0.06), run_time=0.28)
            else:
                self.play(ReplacementTransform(ptr_m, new_mid), run_time=0.3)
                ptr_m = new_mid

            self.play(
                Indicate(cells[mid], color=YELLOW, scale_factor=1.06),
                Flash(cells[mid], color=YELLOW, flash_radius=0.32),
                run_time=0.48,
            )

            if gt:
                cur_r = mid - 1
                pr2 = pointer_r_at(cur_r)
                self.play(ReplacementTransform(ptr_r, pr2), run_time=0.5)
                ptr_r = pr2
            else:
                cur_l = mid + 1
                pl2 = pointer_l_at(cur_l)
                self.play(ReplacementTransform(ptr_l, pl2), run_time=0.5)
                ptr_l = pl2

            self.play(FadeOut(ptr_m), run_time=0.14)
            ptr_m = None

        self.wait(1.25)

        right = cur_r
        r_idx = right
        success = r_idx >= 0 and r_idx < n and A[r_idx] == x

        if r_idx < 0 or r_idx >= n:
            self.play(Wiggle(title), run_time=0.85)
            self.wait(0.35)
        else:
            center = texts[r_idx].get_center()
            if success:
                parts = VGroup()
                n_part = 16
                for i in range(n_part):
                    ang = TAU * i / n_part
                    d = Dot(center, radius=0.055, color=interpolate_color(YELLOW, RED, i / n_part))
                    parts.add(d)
                self.add(parts)
                self.play(
                    LaggedStart(
                        *[
                            d.animate.shift(1.15 * np.array([np.cos(ang), np.sin(ang), 0])).set_opacity(0)
                            for d, ang in zip(parts, [TAU * i / n_part for i in range(n_part)])
                        ],
                        lag_ratio=0.04,
                    ),
                    Flash(cells[r_idx], color=YELLOW, line_length=0.2, num_lines=14),
                    run_time=1.1,
                )
                self.remove(parts)
            else:
                self.play(Wiggle(texts[r_idx]), run_time=0.9)
            self.wait(0.8)

        num_cases = len(self.DEMO_CASES)
        is_last = case_index >= num_cases - 1
        next_same = (
            not is_last and list(self.DEMO_CASES[case_index + 1][0]) == A
        )

        if next_same:
            self._transition_same_array_next(
                split_idx=split_idx,
                split_dx=split_dx,
                n=n,
                cells=cells,
                texts=texts,
                title=title,
                ptr_l=ptr_l,
                ptr_r=ptr_r,
                dashed=dashed,
            )
            self._reuse_bundle = (cells, texts, array_g, spacing, cell_w, gap, start_x)
        else:
            to_fade = [array_g, title, ptr_l, ptr_r]
            if dashed is not None:
                to_fade.append(dashed)
            self.play(FadeOut(VGroup(*to_fade)), run_time=0.75)
            self.wait(0.18)
