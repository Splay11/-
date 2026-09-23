# -*- coding: utf-8 -*-
"""
最长回文子串 — DP 填表过程演示（Manim）

样例 s = "abcbca"；左侧 n×n 的 dp 表（0/1），右侧一维字符数组；黑底、无旁白字幕与题面大段说明。
遍历顺序与参考代码一致：i 从 n-1 到 0，j 从 i 到 n-1。

默认输出 1080p（1920×1080）@ 60fps。若需更快预览可临时改为 854×480 并用 -ql。

渲染示例（项目根目录）:
  manim -qh longest_palindrome_dp.py LongestPalindromeDP
"""

from __future__ import annotations

from manim import *
from manim.utils.rate_functions import smooth

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


def bracket_label(idx: int, fs: int = 22, color=WHITE) -> Text:
    return Text(f"[{idx}]", font_size=fs, color=color, font="Consolas", disable_ligatures=True)


def digit_txt(s: str, fs: int, color=WHITE) -> Text:
    return Text(s, font_size=fs, color=color, font="Arial", disable_ligatures=True)


def compute_dp_bool(s: str) -> list[list[bool]]:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if i == j:
                dp[i][j] = True
                continue
            if s[i] == s[j]:
                if i == j - 1:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i + 1][j - 1]
    return dp


class LongestPalindromeDP(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        s = "abcbca"
        n = len(s)
        dp_ref = compute_dp_bool(s)

        # 整体再放慢一档（含 Wiggle）：在 1/0.5 基础上再 ×1.15
        pace = 1.0 / 0.5
        slow = 0.82 * pace * 1.15
        t_intro = 0.45 * slow
        t_cell = 0.32 * slow
        t_arrow = 0.38 * slow
        t_val = 0.22 * slow
        t_out = 0.28 * slow

        RED_P = "#ff4444"
        BLUE_P = "#5599ff"
        YELLOW_HL = "#ffcc00"
        ORANGE_HL = "#ff9933"
        CYAN_HL = "#44ddcc"
        GREEN_P = "#33dd66"
        GREEN_ARROW = "#22cc55"
        ARROW_STROKE = 5.5
        ARROW_TIP_RATIO = 0.22
        # 右侧竖箭头较短，需放宽比例才能让线宽/箭头尖与左侧长箭头观感一致
        STR_ARROW_TIP_RATIO = 0.38
        STR_ARROW_STROKE_LEN_RATIO = 22.0

        cell_w, cell_h = 0.52, 0.5
        # i==j 时两箭同列：红略偏左、蓝略偏右，避免完全重合
        STR_ARROW_SAME_COL_X = cell_w * 0.18
        val_fs = 26
        idx_fs = 17
        stroke_solid = 2.4
        # 下标与格子间距（避免与边框/数字重合）
        idx_gap_row = cell_w * 1.08
        idx_gap_col = cell_h * 1.1
        idx_gap_str_down = cell_h * 1.22

        # ---------- 左侧 dp 网格：行 i 从上到下 0..n-1 ----------
        rows, cols = n, n
        total_w = cols * cell_w
        total_h = rows * cell_h
        dp_shift = LEFT * 2.85 + UP * 0.12
        left = -total_w / 2 + dp_shift[0]
        top = total_h / 2 + dp_shift[1]

        def dp_center(i: int, j: int) -> np.ndarray:
            return np.array(
                [left + j * cell_w + cell_w / 2, top - i * cell_h - cell_h / 2, 0.0],
                dtype=float,
            )

        dp_boxes: list[list[Rectangle]] = []
        for i in range(rows):
            row_b: list[Rectangle] = []
            for j in range(cols):
                r = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    color=WHITE,
                    stroke_width=stroke_solid,
                    fill_opacity=0,
                )
                r.move_to(dp_center(i, j))
                row_b.append(r)
            dp_boxes.append(row_b)

        dp_vals: list[list[Text]] = []
        for i in range(rows):
            row_v: list[Text] = []
            for j in range(cols):
                t = digit_txt("0", val_fs)
                t.move_to(dp_center(i, j))
                row_v.append(t)
            dp_vals.append(row_v)

        for row in dp_vals:
            for v in row:
                v.set_z_index(30)

        # 行标签 [i] 在第一列左侧
        row_labels = VGroup()
        for i in range(rows):
            lab = bracket_label(i, idx_fs)
            lab.move_to(dp_center(i, 0) + LEFT * idx_gap_row)
            row_labels.add(lab)

        # 列标签 [j] 在第一行上方
        col_labels = VGroup()
        for j in range(cols):
            lab = bracket_label(j, idx_fs)
            lab.move_to(dp_center(0, j) + UP * idx_gap_col)
            col_labels.add(lab)

        yellow_frame = Rectangle(
            width=cell_w * 0.98,
            height=cell_h * 0.98,
            color=YELLOW_HL,
            stroke_width=3.8,
            fill_opacity=0,
        )
        yellow_frame.set_z_index(11)

        # ---------- 右侧字符串 ----------
        str_shift = RIGHT * 3.05 + UP * 0.12
        s_left = -n * cell_w / 2 + str_shift[0]
        s_top = cell_h / 2 + str_shift[1]

        def str_center(k: int) -> np.ndarray:
            return np.array(
                [s_left + k * cell_w + cell_w / 2, s_top - cell_h / 2, 0.0],
                dtype=float,
            )

        str_boxes: list[Rectangle] = []
        str_chars: list[Text] = []
        str_idx_labs: list[Text] = []
        for k in range(n):
            r = Rectangle(
                width=cell_w,
                height=cell_h,
                color=WHITE,
                stroke_width=stroke_solid,
                fill_opacity=0,
            )
            r.move_to(str_center(k))
            str_boxes.append(r)
            ch = digit_txt(s[k], val_fs)
            ch.move_to(str_center(k))
            str_chars.append(ch)
            il = bracket_label(k, idx_fs)
            il.move_to(str_center(k) + DOWN * idx_gap_str_down)
            str_idx_labs.append(il)

        orange_frame = Rectangle(
            width=cell_w * 0.98,
            height=cell_h * 0.98,
            color=ORANGE_HL,
            stroke_width=3.6,
            fill_opacity=0,
        )
        orange_frame.set_z_index(12)

        cyan_frame = Rectangle(
            width=cell_w * 0.98,
            height=cell_h * 0.98,
            color=CYAN_HL,
            stroke_width=3.4,
            fill_opacity=0,
        )
        cyan_frame.set_z_index(13)

        # 矩阵外：红箭头指行 i，蓝箭头指列 j（继续外移，避免与 [i]/[j] 下标重合）
        buf = min(cell_w, cell_h) * 0.35
        left_arrow_x = left - cell_w * 2.72
        top_arrow_y = top + cell_h * 2.28
        y_row_arrow_off = -0.15 * cell_h
        x_col_arrow_off = 0.17 * cell_w

        def row_arrow_target(i: int) -> tuple[np.ndarray, np.ndarray]:
            c = dp_center(i, cols // 2)
            yy = c[1] + y_row_arrow_off
            start = np.array([left_arrow_x, yy, 0.0])
            end = np.array([left + buf * 0.28, yy, 0.0])
            return start, end

        def col_arrow_target(j: int) -> tuple[np.ndarray, np.ndarray]:
            c = dp_center(rows // 2, j)
            xx = c[0] + x_col_arrow_off
            start = np.array([xx, top_arrow_y, 0.0])
            end = np.array([xx, top - buf * 0.28, 0.0])
            return start, end

        rs, re = row_arrow_target(n - 1)
        arr_i = Arrow(
            rs,
            re,
            color=RED_P,
            stroke_width=ARROW_STROKE,
            buff=0.0,
            max_tip_length_to_length_ratio=ARROW_TIP_RATIO,
        )
        cs, ce = col_arrow_target(n - 1)
        arr_j = Arrow(
            cs,
            ce,
            color=BLUE_P,
            stroke_width=ARROW_STROKE,
            buff=0.0,
            max_tip_length_to_length_ratio=ARROW_TIP_RATIO,
        )
        arr_i.set_z_index(20)
        arr_j.set_z_index(19)

        # 右侧：从字符白格**上方**竖直向下指入格内（与左侧同步移动），线宽/箭头尖与左侧对齐
        def str_col_arrow_target(k: int, x_shift: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
            cx = str_center(k)[0] + x_shift
            cy = str_center(k)[1]
            y_top_edge = cy + cell_h * 0.5
            # 箭身尽量拉长，接近左侧水平箭头的长度量级，便于与左侧同粗细、同箭头尺寸
            span = 1.38
            y_start = y_top_edge + span
            y_end = y_top_edge - 0.16 * cell_h
            start = np.array([cx, y_start, 0.0])
            end = np.array([cx, y_end, 0.0])
            return start, end

        def make_str_arrow(start: np.ndarray, end: np.ndarray, *, color: str) -> Arrow:
            return Arrow(
                start,
                end,
                color=color,
                stroke_width=ARROW_STROKE,
                buff=0.0,
                max_tip_length_to_length_ratio=STR_ARROW_TIP_RATIO,
                max_stroke_width_to_length_ratio=STR_ARROW_STROKE_LEN_RATIO,
            )

        srs, sre = str_col_arrow_target(n - 1, -STR_ARROW_SAME_COL_X)
        srs_b, sre_b = str_col_arrow_target(n - 1, STR_ARROW_SAME_COL_X)
        sarr_i = make_str_arrow(srs, sre, color=RED_P)
        sarr_j = make_str_arrow(srs_b, sre_b, color=BLUE_P)
        sarr_i.set_z_index(20)
        sarr_j.set_z_index(19)

        def green_match_arc(ii: int, jj: int) -> VMobject:
            y_top = str_center(ii)[1] + cell_h * 0.52
            p0 = np.array([str_center(ii)[0], y_top, 0.0])
            p3 = np.array([str_center(jj)[0], str_center(jj)[1] + cell_h * 0.52, 0.0])
            ctrl_up = 0.44 * cell_h * (1.0 + 0.14 * abs(jj - ii))
            p1 = (2 * p0 + p3) / 3 + UP * ctrl_up
            p2 = (p0 + 2 * p3) / 3 + UP * ctrl_up
            arc = CubicBezier(p0, p1, p2, p3)
            arc.set_stroke(GREEN_ARROW, width=3.6)
            arc.set_fill(opacity=0)
            arc.set_z_index(25)
            return arc

        t_arc = 0.26 * slow
        t_shake = 0.78 * slow

        def orange_surround(ii: int, jj: int) -> None:
            w = (jj - ii + 1) * cell_w
            orange_frame.stretch_to_fit_width(w * 0.99)
            orange_frame.stretch_to_fit_height(cell_h * 0.98)
            mid = (str_center(ii) + str_center(jj)) / 2
            orange_frame.move_to(mid)

        def cyan_surround(ii: int, jj: int) -> None:
            w = (jj - ii + 1) * cell_w
            cyan_frame.stretch_to_fit_width(w * 0.99)
            cyan_frame.stretch_to_fit_height(cell_h * 0.98)
            mid = (str_center(ii) + str_center(jj)) / 2
            cyan_frame.move_to(mid)

        def small_firework_at(p: np.ndarray) -> None:
            rng = np.random.default_rng(0)
            dots = VGroup()
            for _ in range(14):
                ang = rng.random() * TAU
                rad = 0.08 + rng.random() * 0.12
                d = Dot(p + rad * np.array([np.cos(ang), np.sin(ang), 0]), radius=0.028, color=YELLOW)
                dots.add(d)
            dots.set_z_index(40)
            self.play(
                LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.04),
                run_time=0.14 * pace,
                rate_func=smooth,
            )
            self.play(FadeOut(dots, scale=1.2), run_time=0.12 * pace, rate_func=smooth)

        def feedback_above_orange_cyan(ok: bool, has_cyan: bool, *, fireworks: bool) -> None:
            o_mid = orange_frame.get_center()
            if has_cyan:
                c_mid = cyan_frame.get_center()
                p = (o_mid + c_mid) / 2 + UP * (cell_h * 0.62)
            else:
                p = o_mid + UP * (cell_h * 0.85)
            sym = Text("✓", font_size=36, color=GREEN_P) if ok else Text("✗", font_size=38, color=RED_P)
            sym.move_to(p)
            sym.set_z_index(45)
            if fireworks and ok:
                small_firework_at(p)
            self.play(FadeIn(sym, scale=0.85), run_time=0.12 * pace, rate_func=smooth)
            self.play(FadeOut(sym, scale=0.9), run_time=0.14 * pace, rate_func=smooth)

        # ---------- 开场：左右同步出现，dp 全 0 ----------
        dp_all = VGroup(*[b for row in dp_boxes for b in row], *row_labels, *col_labels)
        str_all = VGroup(*str_boxes, *str_chars, *str_idx_labs)

        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(dp_all, shift=DOWN * 0.06), FadeIn(str_all, shift=DOWN * 0.06)),
                lag_ratio=0.0,
            ),
            run_time=t_intro * 1.2,
            rate_func=smooth,
        )
        self.play(
            LaggedStart(*[FadeIn(dp_vals[i][j], scale=0.92) for i in range(n) for j in range(n)], lag_ratio=0.0),
            run_time=0.12 * slow,
        )

        orange_surround(0, n - 1)
        self.add(orange_frame)

        dp_track = [[False] * n for _ in range(n)]

        first_ij = True
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                yellow_frame.move_to(dp_center(i, j))
                self.play(FadeIn(yellow_frame, scale=0.95), run_time=t_cell * 0.75, rate_func=smooth)

                rs, re = row_arrow_target(i)
                cs, ce = col_arrow_target(j)
                if first_ij:
                    arr_i.put_start_and_end_on(rs, re)
                    arr_j.put_start_and_end_on(cs, ce)
                    x_red = -STR_ARROW_SAME_COL_X if i == j else 0.0
                    x_blue = STR_ARROW_SAME_COL_X if i == j else 0.0
                    srsi, srei = str_col_arrow_target(i, x_red)
                    srsj, srej = str_col_arrow_target(j, x_blue)
                    sarr_i.put_start_and_end_on(srsi, srei)
                    sarr_j.put_start_and_end_on(srsj, srej)
                    self.play(
                        FadeIn(arr_i, scale=0.9),
                        FadeIn(arr_j, scale=0.9),
                        FadeIn(sarr_i, scale=0.9),
                        FadeIn(sarr_j, scale=0.9),
                        run_time=t_arrow,
                        rate_func=smooth,
                    )
                    first_ij = False
                else:
                    narr_i = Arrow(
                        rs,
                        re,
                        color=RED_P,
                        stroke_width=ARROW_STROKE,
                        buff=0.0,
                        max_tip_length_to_length_ratio=ARROW_TIP_RATIO,
                    )
                    narr_j = Arrow(
                        cs,
                        ce,
                        color=BLUE_P,
                        stroke_width=ARROW_STROKE,
                        buff=0.0,
                        max_tip_length_to_length_ratio=ARROW_TIP_RATIO,
                    )
                    narr_i.set_z_index(20)
                    narr_j.set_z_index(19)
                    x_red = -STR_ARROW_SAME_COL_X if i == j else 0.0
                    x_blue = STR_ARROW_SAME_COL_X if i == j else 0.0
                    srsi, srei = str_col_arrow_target(i, x_red)
                    srsj, srej = str_col_arrow_target(j, x_blue)
                    nsarr_i = make_str_arrow(srsi, srei, color=RED_P)
                    nsarr_j = make_str_arrow(srsj, srej, color=BLUE_P)
                    nsarr_i.set_z_index(20)
                    nsarr_j.set_z_index(19)
                    self.play(
                        ReplacementTransform(arr_i, narr_i),
                        ReplacementTransform(arr_j, narr_j),
                        ReplacementTransform(sarr_i, nsarr_i),
                        ReplacementTransform(sarr_j, nsarr_j),
                        run_time=t_arrow,
                        rate_func=smooth,
                    )
                    arr_i, arr_j = narr_i, narr_j
                    sarr_i, sarr_j = nsarr_i, nsarr_j

                orange_surround(i, j)

                if i != j and s[i] == s[j]:
                    gam = green_match_arc(i, j)
                    self.play(Create(gam), run_time=0.56 * t_arc, rate_func=smooth)
                    self.play(FadeOut(gam), run_time=0.44 * t_arc, rate_func=smooth)
                elif i != j and s[i] != s[j]:
                    wob = VGroup(str_boxes[i], str_boxes[j], str_chars[i], str_chars[j])
                    self.play(
                        Wiggle(
                            wob,
                            scale_value=1.025,
                            rotation_angle=0.038 * TAU,
                            n_wiggles=4,
                            run_time=t_shake,
                        ),
                        rate_func=smooth,
                    )

                if i == j:
                    feedback_above_orange_cyan(True, has_cyan=False, fireworks=False)
                elif s[i] == s[j]:
                    if i == j - 1:
                        feedback_above_orange_cyan(True, has_cyan=False, fireworks=False)
                    else:
                        cyan_surround(i + 1, j - 1)
                        self.play(FadeIn(cyan_frame, scale=0.96), run_time=0.14 * slow, rate_func=smooth)

                        c_in = dp_center(i + 1, j - 1)
                        c_out = dp_center(i, j)
                        buf2 = min(cell_w, cell_h) * 0.18
                        green_arr = Arrow(
                            c_in,
                            c_out,
                            color=GREEN_ARROW,
                            stroke_width=5.0,
                            buff=buf2,
                            max_tip_length_to_length_ratio=0.2,
                        )
                        green_arr.set_z_index(16)
                        self.play(FadeIn(green_arr, scale=0.92), run_time=0.16 * slow, rate_func=smooth)

                        inner_ok = dp_track[i + 1][j - 1]
                        feedback_above_orange_cyan(inner_ok, has_cyan=True, fireworks=True)

                        self.play(
                            FadeOut(cyan_frame, scale=0.96),
                            FadeOut(green_arr, scale=0.92),
                            run_time=0.18 * slow,
                            rate_func=smooth,
                        )

                # 写回 dp_track 与格子显示
                if i == j:
                    dp_track[i][j] = True
                elif s[i] == s[j]:
                    if i == j - 1:
                        dp_track[i][j] = True
                    else:
                        dp_track[i][j] = dp_track[i + 1][j - 1]
                else:
                    dp_track[i][j] = False

                assert dp_track[i][j] == dp_ref[i][j]

                if dp_track[i][j]:
                    old = dp_vals[i][j]
                    nt = digit_txt("1", val_fs)
                    nt.move_to(dp_center(i, j))
                    self.play(ReplacementTransform(old, nt), run_time=t_val * 0.9, rate_func=smooth)
                    dp_vals[i][j] = nt
                else:
                    self.wait(0.04 * slow)

                self.play(
                    FadeOut(yellow_frame, scale=0.95),
                    run_time=t_out,
                    rate_func=smooth,
                )

        self.wait(0.45 * slow)
