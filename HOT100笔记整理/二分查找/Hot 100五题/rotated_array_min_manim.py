"""旋转有序数组最小值：在「0/1」数组上二分（与题给 get_value / findMin 一致）。

- 无 T=x；两段递增着色并左右微分；无虚线；左侧标 a / b。
- b 在 a 之后出现：每位预先等于 get_value(i,nums)，但全为灰色（未「算出」）；二分每步在 mid 比较结束后，仅 b[mid] 从灰变白并强调，再移动 L/R。
- 比较区：只显示 **>** 或 **<=**。

运行:
  .\\manim-env\\Scripts\\manim.exe -pql rotated_array_min_manim.py RotatedArrayMinAnimation
  .\\manim-env\\Scripts\\manim.exe -qh rotated_array_min_manim.py RotatedArrayMinAnimation
"""

from __future__ import annotations

from manim import *


def get_value(index: int, nums: list) -> int:
    """与题给一致：a[i] > a[-1] 为 0，否则为 1（含等于）。"""
    return 0 if nums[index] > nums[-1] else 1


def collect_findmin_steps(nums: list) -> tuple[list[tuple[int, int, int, int]], int]:
    """每步 (left, right, mid, value)；循环结束后 left 为答案下标。"""
    left, right = 0, len(nums) - 1
    steps: list[tuple[int, int, int, int]] = []
    while left <= right:
        mid = (left + right) // 2
        v = get_value(mid, nums)
        steps.append((left, right, mid, v))
        if v == 0:
            left = mid + 1
        else:
            right = mid - 1
    return steps, left


def pivot_min_index(nums: list) -> int:
    """最小值下标，用于把 a 分成两段递增（着色与拉开）。"""
    return min(range(len(nums)), key=lambda i: nums[i])


class RotatedArrayMinAnimation(Scene):
    DEMO_CASES = [
        [4, 5, 6, 7, 0, 1, 2],
        [6, 7, 0, 1, 2, 4, 5],
        [0, 1, 2, 4, 5, 6, 7],
    ]

    def construct(self):
        for case_index, nums in enumerate(self.DEMO_CASES):
            self._play_one_demo(list(nums), case_index)

    def _play_one_demo(self, nums: list, case_index: int) -> None:
        n = len(nums)
        if n == 0:
            self.add(Text("数组为空", font_size=36))
            self.wait(1)
            return

        cell_w, cell_h = 0.68, 0.84
        gap = 0.06
        spacing = cell_w + gap
        start_x = -(n - 1) * spacing / 2

        # a / b 两行间距略加大，中间留给比较数字与符号
        row_a_y = 0.95
        row_b_y = -1.22

        a_cells = VGroup()
        a_texts = VGroup()
        b_cells = VGroup()
        b_texts = VGroup()
        b_hidden_color = GRAY_D

        for k in range(n):
            ac = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.08,
                color=GRAY_B,
                stroke_width=2,
            )
            at = Text(str(nums[k]), font_size=30, color=WHITE)
            pos_a = np.array([start_x + k * spacing, row_a_y, 0])
            ac.move_to(pos_a)
            at.move_to(pos_a)
            a_cells.add(ac)
            a_texts.add(at)

            bc = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.08,
                color=GRAY_B,
                stroke_width=2,
            )
            bv = get_value(k, nums)
            bt = Text(str(bv), font_size=30, color=b_hidden_color)
            pos_b = np.array([start_x + k * spacing, row_b_y, 0])
            bc.move_to(pos_b)
            bt.move_to(pos_b)
            b_cells.add(bc)
            b_texts.add(bt)

        label_a = Text("a", font_size=38, color=WHITE).next_to(a_cells[0], LEFT, buff=0.38)
        label_b = Text("b", font_size=38, color=WHITE).next_to(b_cells[0], LEFT, buff=0.38)
        row_a = VGroup(label_a, a_cells, a_texts)
        row_b = VGroup(label_b, b_cells, b_texts)
        scene_core = VGroup(row_a, row_b)
        scene_core.move_to(ORIGIN)

        def col_x(k: int) -> float:
            return float(a_cells[k].get_center()[0])

        def a_col_g(k: int) -> VGroup:
            return VGroup(a_cells[k], a_texts[k])

        def b_col_g(k: int) -> VGroup:
            return VGroup(b_cells[k], b_texts[k])

        pivot = pivot_min_index(nums)
        left_color = "#2ecc71"
        right_color = "#e85d04"
        split_dx = 0.12

        top_a = float(row_a.get_top()[1])
        ptr_y_l = top_a + 0.72
        ptr_y_r = top_a + 0.52
        ptr_y_m = top_a + 0.30

        def tip_x_for_index(idx: int) -> float:
            if idx < 0:
                return col_x(0) - spacing * 0.5
            if idx >= n:
                return col_x(n - 1) + spacing * 0.5
            return col_x(idx)

        def cell_i(idx: int) -> int:
            return max(0, min(n - 1, idx))

        def pointer_l_at(idx: int) -> VGroup:
            tx = tip_x_for_index(idx) - 0.06
            tip_y = a_cells[cell_i(idx)].get_top()[1] + 0.05
            tip = np.array([tx, tip_y, 0.0])
            base = np.array([tx, ptr_y_l, 0.0])
            ar = Arrow(
                base, tip, buff=0.0, color=BLUE, stroke_width=3,
                max_tip_length_to_length_ratio=0.22,
            )
            lab = Text("L", font_size=32, color=BLUE).next_to(base, UP, buff=0.05)
            return VGroup(lab, ar)

        def pointer_r_at(idx: int) -> VGroup:
            tx = tip_x_for_index(idx) + 0.06
            tip_y = a_cells[cell_i(idx)].get_top()[1] + 0.05
            tip = np.array([tx, tip_y, 0.0])
            base = np.array([tx, ptr_y_r, 0.0])
            ar = Arrow(
                base, tip, buff=0.0, color=RED, stroke_width=3,
                max_tip_length_to_length_ratio=0.22,
            )
            lab = Text("R", font_size=32, color=RED).next_to(base, UP, buff=0.05)
            return VGroup(lab, ar)

        def pointer_mid_at(idx: int) -> VGroup:
            tx = tip_x_for_index(idx)
            ci = cell_i(idx)
            tip_y = a_cells[ci].get_top()[1] + 0.05
            tip = np.array([tx, tip_y, 0.0])
            base = np.array([tx, ptr_y_m, 0.0])
            ar = Arrow(
                base, tip, buff=0.0, color=YELLOW, stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
            )
            return VGroup(ar)

        cmp_y = 0.5 * (row_a.get_bottom()[1] + row_b.get_top()[1])

        self.play(FadeIn(row_a, shift=UP * 0.12))
        self.wait(0.18)
        self.play(FadeIn(row_b, shift=DOWN * 0.1))
        self.wait(0.22)

        if 0 < pivot < n:
            for i in range(pivot):
                a_texts[i].set_color(left_color)
            for i in range(pivot, n):
                a_texts[i].set_color(right_color)
            anims = []
            for i in range(pivot):
                anims.append(a_cells[i].animate.shift(LEFT * split_dx))
                anims.append(a_texts[i].animate.shift(LEFT * split_dx))
                anims.append(b_cells[i].animate.shift(LEFT * split_dx))
                anims.append(b_texts[i].animate.shift(LEFT * split_dx))
            for i in range(pivot, n):
                anims.append(a_cells[i].animate.shift(RIGHT * split_dx))
                anims.append(a_texts[i].animate.shift(RIGHT * split_dx))
                anims.append(b_cells[i].animate.shift(RIGHT * split_dx))
                anims.append(b_texts[i].animate.shift(RIGHT * split_dx))
            self.play(*anims, run_time=0.55)
            self.wait(0.12)
        else:
            self.play(*[a_texts[i].animate.set_color(right_color) for i in range(n)], run_time=0.45)
            self.wait(0.1)

        steps, ans_idx = collect_findmin_steps(nums)
        ptr_l = pointer_l_at(0)
        ptr_r = pointer_r_at(n - 1)
        ptr_m: VGroup | None = None

        self.play(FadeIn(ptr_l, shift=DOWN * 0.08), FadeIn(ptr_r, shift=DOWN * 0.08))
        self.wait(0.18)

        for entry_l, entry_r, mid, val in steps:
            pl = pointer_l_at(entry_l)
            pr = pointer_r_at(entry_r)
            self.play(
                ReplacementTransform(ptr_l, pl),
                ReplacementTransform(ptr_r, pr),
                run_time=0.46,
            )
            ptr_l, ptr_r = pl, pr

            new_mid = pointer_mid_at(mid)
            if ptr_m is None:
                ptr_m = new_mid
                self.play(FadeIn(ptr_m, shift=DOWN * 0.06), run_time=0.26)
            else:
                self.play(ReplacementTransform(ptr_m, new_mid), run_time=0.28)
                ptr_m = new_mid

            self.play(
                Indicate(a_col_g(mid), color=YELLOW, scale_factor=1.05),
                Flash(a_cells[mid], color=YELLOW, flash_radius=0.28),
                run_time=0.45,
            )

            vm = nums[mid]
            vl = nums[-1]
            cx = col_x(mid)
            # 略宽，便于双字符 <= 与两侧数字不挤
            left_pos = np.array([cx - 1.18, cmp_y, 0.0])
            sym_pos = np.array([cx, cmp_y, 0.0])
            right_pos = np.array([cx + 1.18, cmp_y, 0.0])

            m_copy = Text(str(vm), font_size=36, color=WHITE)
            m_copy.move_to(a_texts[mid].get_center())
            last_copy = Text(str(vl), font_size=36, color=WHITE)
            last_copy.move_to(a_texts[-1].get_center())

            if vm > vl:
                sym = Text(">", font_size=46, color=YELLOW)
            else:
                sym = Text("<=", font_size=38, color=YELLOW)
            sym.move_to(sym_pos)

            self.add(m_copy, last_copy)
            self.play(
                m_copy.animate.move_to(left_pos),
                last_copy.animate.move_to(right_pos),
                run_time=0.55,
            )
            self.play(FadeIn(sym, scale=0.6), run_time=0.22)
            self.wait(0.28)

            self.play(
                FadeOut(m_copy),
                FadeOut(last_copy),
                FadeOut(sym),
                run_time=0.25,
            )

            # b[mid] 已由灰变白（显式 fill，避免与 Indicate 同帧被盖住）
            bt_mid = b_texts[mid]
            self.play(
                bt_mid.animate.set_color(WHITE).set_fill(WHITE, opacity=1),
                run_time=0.5,
            )
            self.play(
                Indicate(bt_mid, color=YELLOW, scale_factor=1.12),
                run_time=0.38,
            )

            self.play(FadeOut(ptr_m), run_time=0.12)
            ptr_m = None

            if val == 0:
                pl2 = pointer_l_at(mid + 1)
                self.play(ReplacementTransform(ptr_l, pl2), run_time=0.48)
                ptr_l = pl2
            else:
                pr2 = pointer_r_at(mid - 1)
                self.play(ReplacementTransform(ptr_r, pr2), run_time=0.48)
                ptr_r = pr2

        self.wait(0.55)
        self.play(
            Indicate(a_col_g(ans_idx), color=GREEN, scale_factor=1.12),
            Flash(a_cells[ans_idx], color=GREEN, flash_radius=0.35),
            run_time=0.85,
        )
        self.wait(0.45)

        fade_all = VGroup(scene_core, ptr_l, ptr_r)
        if ptr_m is not None:
            fade_all.add(ptr_m)
        self.play(FadeOut(fade_all), run_time=0.7)
        self.wait(0.12)
