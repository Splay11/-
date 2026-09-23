"""下一个排列（LeetCode 31）可视化：黄指针 i、红指针 j、对调、翻转后缀。

步骤与「下一个排列.md」动画 prompt 一致：淡入数组；i 从后往前找第一个 nums[i]<nums[i+1] 并将该位数字标黄；
j 从后往前扫描，在 nums[k]>nums[i] 的候选中维护「当前最小值」下标并标红，若出现更小候选则旧红还原白；
指针淡出后对调 i、j；再翻转 i 之后区间；停留 1.5s 后淡出进入下一组样例。

样式参考「动态规划」目录下二分等脚本：RoundedRectangle 格子、顶置箭头指针。

运行（低清预览）:
  py -3.13 -m manim render -pql next_permutation_manim.py NextPermutationAnimation

运行（输出到 media/videos/...）:
  py -3.13 -m manim render -ql next_permutation_manim.py NextPermutationAnimation
"""

from __future__ import annotations

from manim import *


def swap_vgroup_children(g: VGroup, i: int, j: int) -> None:
    m = list(g.submobjects)
    m[i], m[j] = m[j], m[i]
    g.submobjects = m


class NextPermutationAnimation(Scene):
    DEMO_CASES = [
        [1, 2, 3, 4, 5],
        [3, 2, 1, 5, 4],
        [4, 6, 5, 3, 2, 1],
        [5, 4, 3, 2, 1],
    ]

    # 与 binary_search_manim 等保持接近的格子参数
    cell_w = 0.72
    cell_h = 0.88
    gap = 0.06

    yellow_i = YELLOW
    red_j = RED
    pivot_text = "#f1c40f"

    def construct(self) -> None:
        for case_index, raw in enumerate(self.DEMO_CASES):
            self._play_one_case(list(raw), case_index)

    def _pointer_at(
        self,
        cells: VGroup,
        n: int,
        spacing: float,
        start_x: float,
        idx: int,
        label: str,
        color,
        ptr_y: float,
    ) -> VGroup:
        def col_x(k: int) -> float:
            return float(cells[k].get_center()[0])

        def tip_x_for_index(k: int) -> float:
            if k < 0:
                return col_x(0) - spacing * 0.55
            if k >= n:
                return col_x(n - 1) + spacing * 0.55
            return col_x(k)

        def cell_i(k: int) -> int:
            return max(0, min(n - 1, k))

        tx = tip_x_for_index(idx)
        ci = cell_i(idx)
        tip_y = cells[ci].get_top()[1] + 0.06
        tip = np.array([tx, tip_y, 0.0])
        base = np.array([tx, ptr_y, 0.0])
        ar = Arrow(
            base,
            tip,
            buff=0.0,
            color=color,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )
        lab = Text(label, font_size=32, color=color).next_to(base, UP, buff=0.05)
        return VGroup(lab, ar)

    def _play_swap(
        self,
        i: int,
        j: int,
        cells: VGroup,
        texts: VGroup,
        nums: list[int],
    ) -> None:
        if i == j:
            return
        pos_i = cells[i].get_center()
        pos_j = cells[j].get_center()
        nums[i], nums[j] = nums[j], nums[i]
        self.play(
            cells[i].animate.move_to(pos_j),
            texts[i].animate.move_to(pos_j),
            cells[j].animate.move_to(pos_i),
            texts[j].animate.move_to(pos_i),
            run_time=0.55,
        )
        swap_vgroup_children(cells, i, j)
        swap_vgroup_children(texts, i, j)

    def _play_one_case(self, nums: list[int], case_index: int) -> None:
        n = len(nums)
        if n == 0:
            self.add(Text("数组为空", font_size=36))
            self.wait(1)
            return

        cell_w, cell_h = self.cell_w, self.cell_h
        gap = self.gap
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
            tk = Text(str(nums[k]), font_size=30, color=WHITE)
            pos = np.array([start_x + k * spacing, 0.0, 0.0])
            box.move_to(pos)
            tk.move_to(pos)
            cells.add(box)
            texts.add(tk)

        array_g = VGroup(cells, texts)

        top_arr = float(array_g.get_top()[1])
        ptr_y_i = top_arr + 0.72
        ptr_y_j = top_arr + 0.52

        # 标题底边需明显高于 i 指针与「i」标签，留出可视空隙
        title_bottom_clear = ptr_y_i + 0.78
        title_buff = max(1.95, (title_bottom_clear - top_arr) + 0.45)
        title = Text("下一个排列", font_size=38).next_to(array_g, UP, buff=title_buff)

        self.play(FadeIn(array_g, shift=UP * 0.14), run_time=0.55)
        self.wait(0.15)
        self.play(FadeIn(title, shift=DOWN * 0.08), run_time=0.35)
        self.wait(0.18)

        # ---------- 找 i：从 n-2 往前，第一个 nums[i] < nums[i+1] ----------
        i_idx = -1
        ptr_i: Mobject | None = None
        for k in range(n - 2, -1, -1):
            new_ptr = self._pointer_at(
                cells, n, spacing, start_x, k, "i", self.yellow_i, ptr_y_i
            )
            if ptr_i is None:
                ptr_i = new_ptr
                self.play(FadeIn(ptr_i, shift=DOWN * 0.08), run_time=0.28)
            else:
                self.play(ReplacementTransform(ptr_i, new_ptr), run_time=0.36)
                ptr_i = new_ptr
            self.wait(0.08)
            if nums[k] < nums[k + 1]:
                i_idx = k
                self.play(
                    texts[k].animate.set_color(self.pivot_text),
                    Indicate(cells[k], color=self.yellow_i, scale_factor=1.04),
                    run_time=0.42,
                )
                self.wait(0.2)
                break
            self.play(
                Flash(cells[k], color=GRAY, flash_radius=0.22, line_length=0.12),
                Flash(cells[k + 1], color=GRAY, flash_radius=0.22, line_length=0.12),
                run_time=0.28,
            )
            self.wait(0.06)

        if i_idx < 0:
            # 已是字典序最大：反转整个数组
            self.wait(0.15)
            if ptr_i is not None:
                self.play(FadeOut(ptr_i), run_time=0.3)
                ptr_i = None
            note = Text("已是最大排列 → 翻转为最小", font_size=32, color=GRAY_A)
            note.next_to(array_g, DOWN, buff=0.55)
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.35)
            self.wait(0.25)
            lo, hi = 0, n - 1
            while lo < hi:
                self._play_swap(lo, hi, cells, texts, nums)
                lo += 1
                hi -= 1
            self.play(FadeOut(note), run_time=0.25)
            self.wait(1.5)
            self.play(FadeOut(VGroup(array_g, title)), run_time=0.75)
            self.wait(0.15)
            return

        # ---------- 找 j：从后往前，在 > nums[i] 的候选里维护当前最小值 ----------
        ptr_j: Mobject | None = None
        best_j: int | None = None
        for k in range(n - 1, i_idx, -1):
            new_pj = self._pointer_at(
                cells, n, spacing, start_x, k, "j", self.red_j, ptr_y_j
            )
            if ptr_j is None:
                ptr_j = new_pj
                self.play(FadeIn(ptr_j, shift=DOWN * 0.08), run_time=0.28)
            else:
                self.play(ReplacementTransform(ptr_j, new_pj), run_time=0.32)
                ptr_j = new_pj
            self.wait(0.06)

            if nums[k] > nums[i_idx]:
                if best_j is None or nums[k] < nums[best_j]:
                    anims = []
                    if best_j is not None:
                        anims.append(texts[best_j].animate.set_color(WHITE))
                    best_j = k
                    anims.append(texts[k].animate.set_color(self.red_j))
                    self.play(*anims, run_time=0.28)
            self.wait(0.05)

        j_idx = best_j
        assert j_idx is not None

        # ---------- 指针淡出，对调 i、j ----------
        self.wait(0.12)
        fade_ptrs = [ptr_j]
        if ptr_i is not None:
            fade_ptrs.append(ptr_i)
        self.play(FadeOut(VGroup(*fade_ptrs)), run_time=0.35)
        ptr_i = ptr_j = None

        self.play(
            Circumscribe(VGroup(cells[i_idx], texts[i_idx]), color=self.yellow_i, run_time=0.45),
            Circumscribe(VGroup(cells[j_idx], texts[j_idx]), color=self.red_j, run_time=0.45),
        )
        self._play_swap(i_idx, j_idx, cells, texts, nums)

        # 对调后格子与下标已对齐；统一清掉黄/红高亮
        self.play(*[texts[k].animate.set_color(WHITE) for k in range(n)], run_time=0.25)

        # ---------- 翻转 [i_idx+1 .. n-1] ----------
        lo, hi = i_idx + 1, n - 1
        if lo < hi:
            brace = BraceBetweenPoints(
                cells[lo].get_bottom() + DOWN * 0.08,
                cells[hi].get_bottom() + DOWN * 0.08,
                direction=DOWN,
                color=BLUE_B,
            )
            cap = Text("翻转后缀", font_size=30, color=BLUE_B).next_to(brace, DOWN, buff=0.12)
            self.play(GrowFromCenter(brace), FadeIn(cap, shift=UP * 0.08), run_time=0.4)
            self.wait(0.15)
            while lo < hi:
                self._play_swap(lo, hi, cells, texts, nums)
                lo += 1
                hi -= 1
            self.play(FadeOut(brace), FadeOut(cap), run_time=0.3)

        self.wait(1.5)
        self.play(FadeOut(VGroup(array_g, title)), run_time=0.75)
        self.wait(0.15)
