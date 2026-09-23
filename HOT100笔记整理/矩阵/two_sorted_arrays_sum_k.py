"""
两个升序数组各取一个数使和为 k — 双指针过程演示（Manim）

「k = 5」与右侧比较式用 PIL 光栅成 ImageMobject（字号加大），绕过 Pango 伪影。
红/蓝长箭头表示 i、j。每一步：右侧算式先淡出 → 指针移动 → 再淡入下一条算式（不做整式变形）。

画布 1920x1080；480p 快速渲染；config.frame_rate=30（输出目录多为 1080p30），缓动 smooth + 少拼接更顺:
  .\\manim-env2\\Scripts\\manim.exe -pql two_sorted_arrays_sum_k.py TwoSortedArraysSumK
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from manim import *
from manim.utils.rate_functions import smooth

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30


def _load_pil_font(size_px: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    windir = Path(os.environ.get("WINDIR", r"C:\Windows"))
    for fn in ("arial.ttf", "segoeui.ttf", "calibri.ttf"):
        fp = windir / "Fonts" / fn
        if fp.is_file():
            try:
                return ImageFont.truetype(str(fp), size_px)
            except OSError:
                continue
    return ImageFont.load_default()


def pil_raster_line(
    text: str,
    *,
    font_size_px: int,
    height_manim: float,
    rgb: tuple[int, int, int] = (255, 255, 255),
) -> ImageMobject:
    """单行文字 → RGBA 位图 → ImageMobject，不经 Manim Text。"""
    font = _load_pil_font(font_size_px)
    probe = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    d0 = ImageDraw.Draw(probe)
    bb = d0.textbbox((0, 0), text, font=font)
    pad = 10
    w = max(16, bb[2] - bb[0] + pad * 2)
    h = max(16, bb[3] - bb[1] + pad * 2)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.text((pad - bb[0], pad - bb[1]), text, font=font, fill=(*rgb, 255))
    arr = np.asarray(im, dtype=np.uint8)
    mob = ImageMobject(arr)
    mob.height = height_manim
    return mob


def sans_txt(s: str, fs: int, color=WHITE) -> Text:
    return Text(s, font_size=fs, color=color, font="Arial", disable_ligatures=True)


def vector_check(color: str) -> VGroup:
    sw = 8.5
    l1 = Line(np.array([-0.26, -0.02, 0]), np.array([-0.08, -0.24, 0]), color=color, stroke_width=sw)
    l2 = Line(l1.get_end(), np.array([0.44, 0.28, 0]), color=color, stroke_width=sw)
    return VGroup(l1, l2)


class TwoSortedArraysSumK(Scene):
    def construct(self):
        slow = ((90 / 127.61) * 1.65 / 1.5) / 0.7
        slow *= 1.0 / 0.7
        slow *= 1.0 / 0.7
        self.camera.background_color = BLACK

        a = [1, 3, 4, 5]
        b = [1, 3, 5, 6]
        k = 5
        n = len(a)

        cell_w, cell_h = 0.72, 0.58
        buff_x = 0.0
        val_fs, lbl_fs = 34, 28
        y_a = 1.58
        y_b = -1.58
        center_x = -0.95

        unit_w = cell_w + buff_x
        total_w = n * cell_w + max(n - 1, 0) * buff_x
        left_x = center_x - total_w / 2

        def cell_left_x(idx: int) -> float:
            return left_x + idx * unit_w

        def cell_center(idx: int, y: float) -> np.ndarray:
            return np.array([cell_left_x(idx) + cell_w / 2, y, 0])

        t_intro = 0.55 * slow
        t_pause = 0.32 * slow
        t_expr = 0.38 * slow
        t_move = 0.48 * slow

        RED_P = "#ff5555"
        BLUE_P = "#5599ff"
        GREEN_OK = "#44dd66"

        lbl_a = sans_txt("a", lbl_fs)
        lbl_b = sans_txt("b", lbl_fs)

        a_boxes: list[Rectangle] = []
        a_vals: list[Text] = []
        a_cols: list[VGroup] = []
        b_boxes: list[Rectangle] = []
        b_vals: list[Text] = []
        b_cols: list[VGroup] = []

        for idx in range(n):
            cx_a = cell_center(idx, y_a)[0]
            ra = Rectangle(
                width=cell_w,
                height=cell_h,
                color=WHITE,
                stroke_width=2.6,
                fill_opacity=0,
            )
            ra.move_to(np.array([cx_a, y_a, 0]))
            va = sans_txt(str(a[idx]), val_fs)
            va.move_to(ra.get_center())
            a_boxes.append(ra)
            a_vals.append(va)
            a_cols.append(VGroup(ra, va))

            cx_b = cell_center(idx, y_b)[0]
            rb = Rectangle(
                width=cell_w,
                height=cell_h,
                color=WHITE,
                stroke_width=2.6,
                fill_opacity=0,
            )
            rb.move_to(np.array([cx_b, y_b, 0]))
            vb = sans_txt(str(b[idx]), val_fs)
            vb.move_to(rb.get_center())
            b_boxes.append(rb)
            b_vals.append(vb)
            b_cols.append(VGroup(rb, vb))

        lbl_a.next_to(a_cols[0], LEFT, buff=0.42)
        lbl_b.next_to(b_cols[0], LEFT, buff=0.42)

        row_a = VGroup(lbl_a, *a_cols)
        row_b = VGroup(lbl_b, *b_cols)

        k_mob = pil_raster_line(f"k = {k}", font_size_px=58, height_manim=0.48)
        k_mob.next_to(row_a, UP + LEFT, buff=0.04)
        k_mob.shift(LEFT * 0.38 + UP * 0.16)

        mid_y = (y_a + y_b) / 2
        expr_x = row_a.get_right()[0] + 1.82
        expr_anchor = np.array([expr_x, mid_y, 0.0])

        half_h = cell_h / 2
        arrow_shaft = 1.05

        def mk_arrow_i(at_idx: int) -> Arrow:
            c = cell_center(at_idx, y_a)
            cx = float(c[0])
            tip_y = y_a - half_h
            tip = np.array([cx, tip_y, 0.0])
            tail = np.array([cx, tip_y - arrow_shaft, 0.0])
            ar = Arrow(
                tail,
                tip,
                color=RED_P,
                stroke_width=7,
                buff=0,
                max_tip_length_to_length_ratio=0.18,
            )
            ar.set_z_index(9)
            return ar

        def mk_arrow_j(at_idx: int) -> Arrow:
            c = cell_center(at_idx, y_b)
            cx = float(c[0])
            tip_y = y_b + half_h
            tip = np.array([cx, tip_y, 0.0])
            tail = np.array([cx, tip_y + arrow_shaft, 0.0])
            ar = Arrow(
                tail,
                tip,
                color=BLUE_P,
                stroke_width=7,
                buff=0,
                max_tip_length_to_length_ratio=0.18,
            )
            ar.set_z_index(8)
            return ar

        def expr_raster(ai: int, bj: int, rel: str) -> ImageMobject:
            sym = ">" if rel == "gt" else ("<" if rel == "lt" else "=")
            s = f"{a[ai]} + {b[bj]} {sym} {k}"
            return pil_raster_line(s, font_size_px=64, height_manim=0.52)

        def play_fireworks(origin: np.ndarray) -> None:
            self.play(
                Flash(
                    origin,
                    color=GREEN_OK,
                    line_length=0.34,
                    num_lines=18,
                    flash_radius=0.52,
                    time_width=0.65,
                ),
                run_time=0.62 * slow,
                rate_func=smooth,
            )
            self.play(
                Flash(
                    origin,
                    color=WHITE,
                    line_length=0.22,
                    num_lines=12,
                    flash_radius=0.28,
                    time_width=0.5,
                ),
                run_time=0.42 * slow,
                rate_func=smooth,
            )

        self.play(
            FadeIn(k_mob, shift=DOWN * 0.06),
            FadeIn(row_a, shift=UP * 0.06),
            FadeIn(row_b, shift=DOWN * 0.06),
            run_time=t_intro,
            rate_func=smooth,
        )
        self.wait(0.28 * slow)

        expr_mob = expr_raster(0, n - 1, "gt")
        expr_mob.move_to(expr_anchor)
        expr_mob.set_z_index(10)

        arrow_i = mk_arrow_i(0)
        arrow_j = mk_arrow_j(n - 1)

        self.play(
            FadeIn(arrow_i, shift=UP * 0.12),
            FadeIn(arrow_j, shift=DOWN * 0.12),
            run_time=0.45 * slow,
            rate_func=smooth,
        )
        self.play(FadeIn(expr_mob, scale=0.92), run_time=t_expr * 0.85, rate_func=smooth)
        self.wait(t_pause * 0.55)

        states: list[tuple[int, int, str]] = [
            (0, 3, "gt"),
            (0, 2, "gt"),
            (0, 1, "lt"),
            (1, 1, "gt"),
            (1, 0, "lt"),
            (2, 0, "eq"),
        ]

        def rel_to_sym(r: str) -> str:
            return "gt" if r == "gt" else ("lt" if r == "lt" else "eq")

        cur_i, cur_j = states[0][0], states[0][1]

        t_expr_out = t_expr * 0.55
        t_expr_in = t_expr * 0.85

        for s in range(len(states) - 1):
            ni, nj, nrel = states[s + 1]

            new_ai = mk_arrow_i(ni)
            new_aj = mk_arrow_j(nj)
            arrow_parts = []
            if ni != cur_i:
                arrow_parts.append(ReplacementTransform(arrow_i, new_ai, rate_func=smooth))
                arrow_i = new_ai
            if nj != cur_j:
                arrow_parts.append(ReplacementTransform(arrow_j, new_aj, rate_func=smooth))
                arrow_j = new_aj
            arrow_block = AnimationGroup(*arrow_parts, run_time=t_move, rate_func=smooth)

            new_expr = expr_raster(ni, nj, rel_to_sym(nrel))
            new_expr.move_to(expr_anchor)
            new_expr.set_z_index(10)

            self.play(
                Succession(
                    FadeOut(
                        expr_mob,
                        shift=RIGHT * 0.06,
                        scale=0.92,
                        run_time=t_expr_out,
                        rate_func=smooth,
                    ),
                    arrow_block,
                    FadeIn(new_expr, scale=0.92, run_time=t_expr_in, rate_func=smooth),
                    lag_ratio=1.0,
                ),
            )
            expr_mob = new_expr
            cur_i, cur_j = ni, nj
            self.wait(t_pause * 0.45)

        check = vector_check(GREEN_OK)
        check.next_to(expr_mob, RIGHT, buff=0.28)
        check.set_z_index(11)

        self.play(FadeIn(check, scale=0.85), run_time=0.38 * slow, rate_func=smooth)
        self.wait(0.14 * slow)
        origin = (expr_mob.get_center() + check.get_center()) / 2
        play_fireworks(origin)
        self.wait(0.75 * slow)
