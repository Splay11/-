"""朴素二分查找（有序数组中查找是否存在 x）：双指针 + mid，命中烟花；否则淘汰半区变灰后继续。

无左右分色、无竖虚线、无数组分离。三组样例与 binary_search_manim 相同；相邻组若数组相同则只淡出 T 与指针并重置格子样式。

运行:
  .\\manim-env\\Scripts\\manim.exe -pql binary_search_classic_manim.py ClassicBinarySearchAnimation
  .\\manim-env\\Scripts\\manim.exe -qh binary_search_classic_manim.py ClassicBinarySearchAnimation
"""

from __future__ import annotations

from manim import *

# 格子「已淘汰」灰化样式
_CELL_GRAY = dict(fill_color=GRAY_D, fill_opacity=0.42, stroke_color=GRAY, stroke_width=2)
_TEXT_GRAY = GRAY_C


def collect_classic_events(A: list, x: int) -> list[tuple]:
    """事件序列（依次播放）:
    ('probe', L, R, mid)
    ('discard_right', lo_gray, hi_gray, new_L, new_R) —— 淘汰 [lo_gray,hi_gray]，指针收到 new_L,new_R
    ('discard_left', lo_gray, hi_gray, new_L, new_R)
    ('found', mid)
    ('exhausted',)
    """
    left, right = 0, len(A) - 1
    out: list[tuple] = []
    while left <= right:
        mid = (left + right) // 2
        out.append(("probe", left, right, mid))
        if A[mid] == x:
            out.append(("found", mid))
            return out
        if A[mid] > x:
            out.append(("discard_right", mid, right, left, mid - 1))
            right = mid - 1
        else:
            out.append(("discard_left", left, mid, mid + 1, right))
            left = mid + 1
    out.append(("exhausted",))
    return out


class ClassicBinarySearchAnimation(Scene):
    DEMO_CASES = [
        ([1, 2, 4, 5, 7, 10, 11, 13], 7),
        ([1, 2, 4, 5, 7, 10, 11, 13], 10),
        ([1, 2, 4, 5, 7, 10, 11, 13], 6),
    ]

    def construct(self):
        self._reuse_bundle = None
        for case_index, (arr, t) in enumerate(self.DEMO_CASES):
            self._play_one_demo(list(arr), int(t), case_index)

    def _reset_cells_visual(self, cells: VGroup, texts: VGroup, n: int) -> None:
        """恢复未淘汰外观（无填充、灰边框数字白）。"""
        anims = []
        for i in range(n):
            anims.append(
                cells[i].animate.set_style(
                    fill_opacity=0,
                    stroke_color=GRAY_B,
                    stroke_width=2,
                )
            )
            anims.append(texts[i].animate.set_color(WHITE))
        self.play(*anims, run_time=0.45)

    def _transition_same_array_next(
        self,
        *,
        n: int,
        cells: VGroup,
        texts: VGroup,
        title: Mobject,
        ptr_l: Mobject,
        ptr_r: Mobject,
    ) -> None:
        self.play(FadeOut(VGroup(title, ptr_l, ptr_r)), run_time=0.55)
        self._reset_cells_visual(cells, texts, n)
        self.wait(0.12)

    def _play_one_demo(self, A: list, x: int, case_index: int) -> None:
        n = len(A)
        if n == 0:
            self.add(Text("数组为空", font_size=36))
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

        top_arr = float(array_g.get_top()[1])
        ptr_y_l = top_arr + 0.78
        ptr_y_r = top_arr + 0.58
        ptr_y_m = top_arr + 0.34

        title_bottom_clear = ptr_y_l + 0.45
        title_buff = max(1.35, (title_bottom_clear - top_arr) + 0.2)
        title = Text(f"T = {x}", font_size=40).next_to(array_g, UP, buff=title_buff)

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
                base, tip, buff=0.0, color=BLUE, stroke_width=3,
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
                base, tip, buff=0.0, color=RED, stroke_width=3,
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
                base, tip, buff=0.0, color=YELLOW, stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
            )
            return VGroup(ar)

        if fresh:
            self.play(FadeIn(array_g, shift=UP * 0.15))
            self.wait(0.2)
        self.play(Write(title))
        self.wait(0.2)

        events = collect_classic_events(A, x)
        ptr_l = pointer_l_at(0)
        ptr_r = pointer_r_at(n - 1)
        ptr_m: VGroup | None = None

        self.play(FadeIn(ptr_l, shift=DOWN * 0.1), FadeIn(ptr_r, shift=DOWN * 0.1))
        self.wait(0.18)

        found_mid: int | None = None
        i = 0
        while i < len(events):
            ev = events[i]
            tag = ev[0]

            if tag == "probe":
                _, entry_l, entry_r, mid = ev
                pl = pointer_l_at(entry_l)
                pr = pointer_r_at(entry_r)
                self.play(
                    ReplacementTransform(ptr_l, pl),
                    ReplacementTransform(ptr_r, pr),
                    run_time=0.48,
                )
                ptr_l, ptr_r = pl, pr

                new_mid = pointer_mid_at(mid)
                if ptr_m is None:
                    ptr_m = new_mid
                    self.play(FadeIn(ptr_m, shift=DOWN * 0.06), run_time=0.28)
                else:
                    self.play(ReplacementTransform(ptr_m, new_mid), run_time=0.32)
                    ptr_m = new_mid

                self.play(
                    Indicate(cells[mid], color=YELLOW, scale_factor=1.06),
                    Flash(cells[mid], color=YELLOW, flash_radius=0.32),
                    run_time=0.5,
                )
                i += 1

                if i < len(events) and events[i][0] == "found":
                    found_mid = events[i][1]
                    center = texts[found_mid].get_center()
                    parts = VGroup()
                    n_part = 16
                    for j in range(n_part):
                        ang = TAU * j / n_part
                        d = Dot(center, radius=0.055, color=interpolate_color(YELLOW, RED, j / n_part))
                        parts.add(d)
                    self.add(parts)
                    self.play(
                        LaggedStart(
                            *[
                                d.animate.shift(1.15 * np.array([np.cos(ang), np.sin(ang), 0])).set_opacity(0)
                                for d, ang in zip(parts, [TAU * j / n_part for j in range(n_part)])
                            ],
                            lag_ratio=0.04,
                        ),
                        Flash(cells[found_mid], color=YELLOW, line_length=0.2, num_lines=14),
                        run_time=1.1,
                    )
                    self.remove(parts)
                    self.play(FadeOut(ptr_m), run_time=0.15)
                    ptr_m = None
                    self.wait(0.65)
                    i += 1
                    break

                if i >= len(events):
                    break

                nxt = events[i]
                if nxt[0] == "discard_right":
                    _, g0, g1, _nl, nr = nxt
                    gray_anims = []
                    for k in range(g0, g1 + 1):
                        gray_anims.append(cells[k].animate.set_style(**_CELL_GRAY))
                        gray_anims.append(texts[k].animate.set_color(_TEXT_GRAY))
                    self.play(*gray_anims, run_time=0.52)
                    self.play(FadeOut(ptr_m), run_time=0.14)
                    ptr_m = None
                    pr2 = pointer_r_at(nr)
                    self.play(ReplacementTransform(ptr_r, pr2), run_time=0.52)
                    ptr_r = pr2
                    i += 1
                elif nxt[0] == "discard_left":
                    _, g0, g1, nl, _nr = nxt
                    gray_anims = []
                    for k in range(g0, g1 + 1):
                        gray_anims.append(cells[k].animate.set_style(**_CELL_GRAY))
                        gray_anims.append(texts[k].animate.set_color(_TEXT_GRAY))
                    self.play(*gray_anims, run_time=0.52)
                    self.play(FadeOut(ptr_m), run_time=0.14)
                    ptr_m = None
                    pl2 = pointer_l_at(nl)
                    self.play(ReplacementTransform(ptr_l, pl2), run_time=0.52)
                    ptr_l = pl2
                    i += 1
                continue

            if tag == "exhausted":
                self.wait(0.55)
                self.play(Wiggle(title), run_time=0.85)
                self.wait(0.35)
                i += 1
                break

            i += 1

        if found_mid is None and events and events[-1][0] != "exhausted":
            self.wait(1.05)
        elif found_mid is not None:
            self.wait(0.45)

        num_cases = len(self.DEMO_CASES)
        is_last = case_index >= num_cases - 1
        next_same = not is_last and list(self.DEMO_CASES[case_index + 1][0]) == A

        ptr_m_final = ptr_m
        if next_same:
            fade_extra = [ptr_m_final] if ptr_m_final is not None else []
            self.play(
                FadeOut(VGroup(title, ptr_l, ptr_r, *fade_extra)),
                run_time=0.55,
            )
            self._reset_cells_visual(cells, texts, n)
            self.wait(0.12)
            self._reuse_bundle = (cells, texts, array_g, spacing, cell_w, gap, start_x)
        else:
            to_fade = [array_g, title, ptr_l, ptr_r]
            if ptr_m_final is not None:
                to_fade.append(ptr_m_final)
            self.play(FadeOut(VGroup(*to_fade)), run_time=0.75)
            self.wait(0.18)
