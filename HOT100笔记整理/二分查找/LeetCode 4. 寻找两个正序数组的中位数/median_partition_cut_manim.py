"""LeetCode 4 切割线枚举：a 上枚举 i，j = half - i；max(左) vs min(右)；合法则出中位数。

每列为 VGroup(框, 文本)，分割/并拢时整列平移，框与数字不错位。

多组样例依次播放。运行:
  .\\manim-env\\Scripts\\manim.exe -ql median_partition_cut_manim.py MedianPartitionCut
  .\\manim-env\\Scripts\\manim.exe -qh median_partition_cut_manim.py MedianPartitionCut
"""

from __future__ import annotations

import math
from manim import *


CASES: list[tuple[list[int], list[int]]] = [
    ([1, 3, 5, 7, 11, 13, 15], [2, 3, 4, 5, 6, 7, 8]),
    ([1, 2, 3, 3, 4, 5], [5, 6, 7, 7, 8, 11, 13, 15]),
]


def median_on_valid_partition(A: list[int], B: list[int], i: int, j: int) -> float:
    m, n = len(A), len(B)
    max_l = max(A[i - 1] if i > 0 else -math.inf, B[j - 1] if j > 0 else -math.inf)
    min_r = min(A[i] if i < m else math.inf, B[j] if j < n else math.inf)
    if (m + n) % 2 == 1:
        return float(max_l)
    return (max_l + min_r) / 2.0


def _box_of(col: VGroup) -> RoundedRectangle:
    return col[0]


def _text_of(col: VGroup) -> Text:
    return col[1]


class MedianPartitionCut(Scene):
    def construct(self):
        for case_idx, (A, B) in enumerate(CASES):
            self._play_one_case(list(A), list(B), case_idx)
        self.wait(0.5)

    def _play_one_case(self, A: list[int], B: list[int], case_idx: int) -> None:
        m, n = len(A), len(B)
        half = (m + n + 1) // 2

        cell_w, cell_h = 0.52, 0.78
        gap_cells = 0.05
        sp = cell_w + gap_cells
        split_gap = 0.38

        def row_layout(length: int) -> tuple[float, float]:
            sx = -(length - 1) * sp / 2
            return sx, sp

        sx_a, sp_a = row_layout(m)
        sx_b, sp_b = row_layout(n)

        def build_row(vals: list[int], sx: float, sp: float) -> VGroup:
            """每列 VGroup(圆角框, 数字)，相对位置固定。"""
            cols = VGroup()
            for k, v in enumerate(vals):
                box = RoundedRectangle(
                    width=cell_w,
                    height=cell_h,
                    corner_radius=0.06,
                    color=GRAY_B,
                    stroke_width=2,
                    fill_opacity=0,
                )
                t = Text(str(v), font_size=28, color=WHITE)
                t.move_to(box.get_center())
                col = VGroup(box, t)
                col.move_to(np.array([sx + k * sp, 0.0, 0.0]))
                cols.add(col)
            return cols

        cols_a = build_row(A, sx_a, sp_a)
        cols_b = build_row(B, sx_b, sp_b)

        y_a, y_b = 0.95, -0.95
        row_a = cols_a
        row_b = cols_b
        row_a.move_to(np.array([0.0, y_a, 0.0]))
        row_b.move_to(np.array([0.0, y_b, 0.0]))

        lab_a = Text("a", font_size=32, color=WHITE).next_to(row_a, LEFT, buff=0.28)
        lab_b = Text("b", font_size=32, color=WHITE).next_to(row_b, LEFT, buff=0.28)

        y_mid = (y_a + y_b) / 2

        self.play(
            FadeIn(VGroup(lab_a, row_a, lab_b, row_b), scale=0.92),
            run_time=0.55,
        )
        self.wait(0.2)

        cut_lines_a: list[Line] = []
        cut_lines_b: list[Line] = []

        def shift_right_segment(cols: VGroup, cut: int, gap: float) -> list:
            return [cols[k].animate.shift(RIGHT * gap) for k in range(cut, len(cols))]

        def shift_back(cols: VGroup, cut: int, gap: float) -> list:
            return [cols[k].animate.shift(LEFT * gap) for k in range(cut, len(cols))]

        def cut_diagonal_in_gap(cols: VGroup, cut: int, gap: float) -> Line:
            """用列内框的世界坐标画 45° 红线（与 row 平移后一致）。"""
            if cut == 0:
                b0 = _box_of(cols[0])
                p0 = np.array([b0.get_left()[0] - gap * 0.35, b0.get_center()[1] - cell_h * 0.42, 0.0])
                p1 = np.array([b0.get_left()[0] + gap * 0.35, b0.get_center()[1] + cell_h * 0.42, 0.0])
            elif cut >= len(cols):
                bk = _box_of(cols[len(cols) - 1])
                p0 = np.array([bk.get_right()[0] - gap * 0.35, bk.get_center()[1] - cell_h * 0.42, 0.0])
                p1 = np.array([bk.get_right()[0] + gap * 0.35, bk.get_center()[1] + cell_h * 0.42, 0.0])
            else:
                bl = _box_of(cols[cut - 1])
                br = _box_of(cols[cut])
                xl, xr = bl.get_right()[0], br.get_left()[0]
                cy = (bl.get_center()[1] + br.get_center()[1]) / 2
                cx = (xl + xr) / 2
                p0 = np.array([cx - gap * 0.22, cy - cell_h * 0.44, 0.0])
                p1 = np.array([cx + gap * 0.22, cy + cell_h * 0.44, 0.0])
            return Line(p0, p1, color=RED, stroke_width=4)

        def reset_colors_anims():
            anims = []
            for k in range(m):
                anims.append(_text_of(cols_a[k]).animate.set_color(WHITE))
            for k in range(n):
                anims.append(_text_of(cols_b[k]).animate.set_color(WHITE))
            return anims

        def force_text_white():
            """与 animate 分离，保证蓝/黄在几何动画后必定恢复为白。"""
            for k in range(m):
                _text_of(cols_a[k]).set_color(WHITE)
            for k in range(n):
                _text_of(cols_b[k]).set_color(WHITE)

        found = False
        ever_shown_j_help = False
        j_hint_mob: Mobject | None = None

        for i in range(0, m + 1):
            if found:
                break
            j = half - i
            if j < 0 or j > n:
                continue

            cut_lines_a.clear()
            cut_lines_b.clear()

            an_a = shift_right_segment(cols_a, i, split_gap)
            if an_a:
                self.play(*an_a, run_time=0.45)
            else:
                self.wait(0.12)
            la = cut_diagonal_in_gap(cols_a, i, split_gap)
            cut_lines_a.append(la)
            self.play(Create(la), run_time=0.35)
            self.wait(0.12)

            show_j_help = False
            if not ever_shown_j_help:
                j_hint_mob = Text(f"j = {half} - {i} = {j}", font_size=26, color=WHITE).next_to(
                    row_b, DOWN, buff=0.35
                )
                self.play(FadeIn(j_hint_mob, shift=UP * 0.1), run_time=0.28)
                self.wait(0.1)
                ever_shown_j_help = True
                show_j_help = True

            an_b = shift_right_segment(cols_b, j, split_gap)
            if an_b:
                self.play(*an_b, run_time=0.45)
            else:
                self.wait(0.12)
            lb = cut_diagonal_in_gap(cols_b, j, split_gap)
            cut_lines_b.append(lb)
            self.play(Create(lb), run_time=0.35)
            if show_j_help and j_hint_mob is not None:
                self.play(FadeOut(j_hint_mob), run_time=0.2)
                j_hint_mob = None

            col_anims = []
            if i > 0:
                col_anims.append(_text_of(cols_a[i - 1]).animate.set_color(YELLOW))
            if i < m:
                col_anims.append(_text_of(cols_a[i]).animate.set_color(BLUE))
            if j > 0:
                col_anims.append(_text_of(cols_b[j - 1]).animate.set_color(YELLOW))
            if j < n:
                col_anims.append(_text_of(cols_b[j]).animate.set_color(BLUE))
            if col_anims:
                self.play(*col_anims, run_time=0.35)

            max_l = max(
                (A[i - 1] if i > 0 else -math.inf),
                (B[j - 1] if j > 0 else -math.inf),
            )
            min_r = min(
                (A[i] if i < m else math.inf),
                (B[j] if j < n else math.inf),
            )

            la_l = A[i - 1] if i > 0 else None
            la_r = A[i] if i < m else None
            lb_l = B[j - 1] if j > 0 else None
            lb_r = B[j] if j < n else None

            def fmt_num(x: float) -> str:
                if math.isinf(x):
                    return "-∞" if x < 0 else "+∞"
                return str(int(x)) if x == int(x) else str(x)

            if la_l is not None and lb_l is not None:
                max_str = f"max({la_l},{lb_l}) = {fmt_num(max_l)}"
            elif la_l is not None:
                max_str = f"max({la_l}) = {fmt_num(max_l)}"
            elif lb_l is not None:
                max_str = f"max({lb_l}) = {fmt_num(max_l)}"
            else:
                max_str = "max(-∞) = -∞"

            if la_r is not None and lb_r is not None:
                min_str = f"min({la_r},{lb_r}) = {fmt_num(min_r)}"
            elif la_r is not None:
                min_str = f"min({la_r}) = {fmt_num(min_r)}"
            elif lb_r is not None:
                min_str = f"min({lb_r}) = {fmt_num(min_r)}"
            else:
                min_str = "min(+∞) = +∞"

            x_max = -2.35
            x_min = 2.35
            t_max = Text(max_str, font_size=26, color=YELLOW).move_to(np.array([x_max, y_mid, 0.0]))
            t_min = Text(min_str, font_size=26, color=BLUE).move_to(np.array([x_min, y_mid, 0.0]))
            ok = max_l <= min_r
            sym_str = "<=" if ok else ">"
            t_sym = Text(sym_str, font_size=40, color=WHITE).move_to(np.array([0.0, y_mid, 0.0]))

            tgt_l = np.array([x_max + 0.15, y_mid, 0.0])
            tgt_r = np.array([x_min - 0.15, y_mid, 0.0])

            cps: list[Mobject] = []
            if i > 0:
                cps.append(_text_of(cols_a[i - 1]).copy())
            if j > 0:
                cps.append(_text_of(cols_b[j - 1]).copy())
            if cps:
                self.add(*cps)
                if len(cps) == 2:
                    self.play(
                        cps[0].animate.move_to(tgt_l + LEFT * 0.22),
                        cps[1].animate.move_to(tgt_l + RIGHT * 0.22),
                        run_time=0.4,
                    )
                    self.play(FadeOut(VGroup(*cps)), FadeIn(t_max), run_time=0.32)
                else:
                    self.play(cps[0].animate.move_to(tgt_l), run_time=0.4)
                    self.play(FadeOut(cps[0]), FadeIn(t_max), run_time=0.32)
                for c in cps:
                    if c in self.mobjects:
                        self.remove(c)
            else:
                self.play(FadeIn(t_max), run_time=0.22)

            cps2: list[Mobject] = []
            if i < m:
                cps2.append(_text_of(cols_a[i]).copy())
            if j < n:
                cps2.append(_text_of(cols_b[j]).copy())
            if cps2:
                self.add(*cps2)
                if len(cps2) == 2:
                    self.play(
                        cps2[0].animate.move_to(tgt_r + LEFT * 0.22),
                        cps2[1].animate.move_to(tgt_r + RIGHT * 0.22),
                        run_time=0.4,
                    )
                    self.play(FadeOut(VGroup(*cps2)), FadeIn(t_min), run_time=0.32)
                else:
                    self.play(cps2[0].animate.move_to(tgt_r), run_time=0.4)
                    self.play(FadeOut(cps2[0]), FadeIn(t_min), run_time=0.32)
                for c in cps2:
                    if c in self.mobjects:
                        self.remove(c)
            else:
                self.play(FadeIn(t_min), run_time=0.22)

            self.play(FadeIn(t_sym, scale=1.2), run_time=0.28)
            grp_cmp = VGroup(t_max, t_sym, t_min)
            self.wait(0.18)
            if ok:
                med = median_on_valid_partition(A, B, i, j)
                out_s = str(int(med)) if med == int(med) else str(med)
                self.play(FadeOut(grp_cmp), run_time=0.38)
                res = Text(f"中位数: {out_s}", font_size=32, color=GREEN).next_to(row_b, DOWN, buff=0.52)
                self.play(Write(res), run_time=0.5)
                self.wait(1.0)
                self.play(
                    FadeOut(VGroup(res, la, lb, lab_a, lab_b, row_a, row_b)),
                    run_time=0.65,
                )
                found = True
                break

            # 不合法：快速震动 max/min
            self.play(
                Succession(
                    grp_cmp.animate.shift(LEFT * 0.1),
                    grp_cmp.animate.shift(RIGHT * 0.2),
                    grp_cmp.animate.shift(LEFT * 0.1),
                    run_time=0.18,
                )
            )
            self.play(FadeOut(grp_cmp), run_time=0.2)

            back_a = shift_back(cols_a, i, split_gap)
            back_b = shift_back(cols_b, j, split_gap)
            fade_lines = [FadeOut(L) for L in cut_lines_a + cut_lines_b]
            self.play(
                *fade_lines,
                *back_a,
                *back_b,
                run_time=0.45,
            )
            self.remove(la, lb)
            # 与位移动画分开，再播一次颜色恢复，并强制 set_color 防止蓝字残留
            self.play(*reset_colors_anims(), run_time=0.28)
            force_text_white()
            self.wait(0.12)

        if not found:
            fail = Text("未找到合法划分（不应出现）", font_size=28, color=RED).move_to(ORIGIN)
            self.play(Write(fail), run_time=0.5)
            self.wait(0.8)
            self.play(FadeOut(fail), FadeOut(VGroup(lab_a, lab_b, row_a, row_b)), run_time=0.5)
