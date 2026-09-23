# -*- coding: utf-8 -*-
"""
LeetCode 121 买卖股票的最佳时机 — 一次遍历维护前缀最小与最大利润（Manim）

黑底；中间一行 prices（白格）；黄框当前格 + 红箭从上指向下边中点；
绿框仅框住当前黄格左侧前缀（不含当前格）；右缘与「黄格左边那一格」的白框右缘对齐，不向右超出以免压到黄格；左缘可略外扩；框体比单行略高；蓝框标出该左侧区间最小值所在格；
当前价与蓝框最小值飞到数组上方做差；下方 ans，更大则飞入更新并在 ans 处小烟花。

逻辑画幅 16:9。1080p（1920×1080）:
  .\\manim-env2\\Scripts\\manim.exe -pqh best_time_buy_sell_stock_anim.py MaxProfitStockDemo --disable_caching

快速 480p 预览:
  .\\manim-env2\\Scripts\\manim.exe -pql best_time_buy_sell_stock_anim.py MaxProfitStockDemo
"""

from __future__ import annotations

import numpy as np

from manim import *
from manim.utils.rate_functions import smooth


class Solution:
    def maxProfit(self, prices: list) -> int:
        minPrice = float("inf")
        maxProfit = 0
        for price in prices:
            minPrice = min(minPrice, price)
            maxProfit = max(maxProfit, price - minPrice)
        return maxProfit


# 1080p 成片默认
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


class MaxProfitStockDemo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        prices = [5, 4, 3, 9, 2, 5, 7, 5, 10]
        n = len(prices)
        assert n > 0

        slow = 1.05
        cell_w, cell_h = 0.52, 0.46
        buff_x = 0.03
        val_fs = 24
        lbl_fs = 21
        prices_y = 0.22
        eq_y = 1.22
        ans_y = -1.12

        green_pad_x = 0.14
        green_pad_y = 0.12
        green_extra_h = 0.1
        stroke_white = 2.4
        stroke_yellow = 3.6
        stroke_green = 2.8
        stroke_blue = 3.4

        RED_P = "#ff3333"
        GREEN_P = "#33cc55"
        BLUE_P = "#4499ff"
        YELLOW_P = "#ffcc00"
        GOLD = "#ffdd66"

        unit_w = cell_w + buff_x
        total_w = n * cell_w + max(n - 1, 0) * buff_x
        left_x = -total_w / 2

        def cell_left_x(k: int) -> float:
            return left_x + k * unit_w

        def cell_center(k: int, y: float) -> np.ndarray:
            return np.array([cell_left_x(k) + cell_w / 2, y, 0])

        def green_prefix_rect(right_k: int, y: float, h: float, color, sw: float) -> Rectangle:
            """覆盖 prices[0..right_k]；右边界与第 right_k 格白框右缘对齐，仅向左扩 green_pad_x。"""
            le = cell_left_x(0) - green_pad_x
            re = cell_left_x(right_k) + cell_w
            rw = re - le
            r = Rectangle(width=rw, height=h, color=color, stroke_width=sw, fill_opacity=0)
            r.move_to(np.array([(le + re) / 2, y, 0]))
            return r

        t_step = 0.52 * slow
        t_move = 0.55 * slow
        t_green = 0.62 * slow
        t_eq = 0.75 * slow
        t_fly_ans = 0.72 * slow
        t_pause = 0.32 * slow
        boxes: list[Rectangle] = []
        vals: list[Text] = []
        cols: list[VGroup] = []
        for k in range(n):
            r = Rectangle(
                width=cell_w,
                height=cell_h,
                color=WHITE,
                stroke_width=stroke_white,
                fill_opacity=0,
            )
            r.move_to(cell_center(k, prices_y))
            r.set_z_index(2)
            t = Text(str(prices[k]), font_size=val_fs, color=WHITE, font="Consolas", disable_ligatures=True)
            t.move_to(r.get_center())
            t.set_z_index(3)
            boxes.append(r)
            vals.append(t)
            cols.append(VGroup(r, t))

        prices_lbl = Text("prices", font_size=lbl_fs, color=WHITE, font="Consolas", disable_ligatures=True)
        prices_lbl.next_to(boxes[0], LEFT, buff=0.28)
        prices_lbl.set_z_index(3)

        ans_box_w, ans_box_h = 0.72, 0.5
        ans_box = Rectangle(
            width=ans_box_w,
            height=ans_box_h,
            color=WHITE,
            stroke_width=stroke_white,
            fill_opacity=0,
        )
        ans_lbl = Text("ans", font_size=lbl_fs, color=WHITE, font="Consolas", disable_ligatures=True)
        ans_val = Text("0", font_size=val_fs, color=WHITE, font="Consolas", disable_ligatures=True)
        ans_grp = VGroup(ans_lbl, ans_box, ans_val)
        ans_lbl.next_to(ans_box, LEFT, buff=0.22)
        ans_val.move_to(ans_box.get_center())
        ans_grp.move_to(np.array([0.0, ans_y, 0.0]))
        ans_box.set_z_index(2)
        ans_val.set_z_index(4)
        ans_lbl.set_z_index(4)

        yellow_rect = Rectangle(width=cell_w, height=cell_h, color=YELLOW_P, stroke_width=stroke_yellow, fill_opacity=0)
        yellow_rect.move_to(cell_center(0, prices_y))
        yellow_rect.set_z_index(12)

        top_mid_0 = np.array([cell_center(0, prices_y)[0], prices_y + cell_h / 2, 0])
        arrow_len = 0.38
        ptr_arrow = Arrow(
            top_mid_0 + UP * arrow_len,
            top_mid_0,
            color=RED_P,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.22,
            buff=0,
        )
        ptr_arrow.set_z_index(14)

        gh = cell_h + 2 * green_pad_y + green_extra_h
        green_rect: Rectangle | None = None
        blue_rect: Rectangle | None = None

        minus_sym = Text("−", font_size=36, color=WHITE, font="Consolas")
        eq_sym = Text("=", font_size=36, color=WHITE, font="Consolas")
        minus_sym.set_z_index(20)
        eq_sym.set_z_index(20)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.08) for c in cols],
                lag_ratio=0.06,
            ),
            FadeIn(prices_lbl, shift=RIGHT * 0.1),
            run_time=0.55 * slow,
            rate_func=smooth,
        )
        self.play(FadeIn(ans_grp, shift=DOWN * 0.08), run_time=0.45 * slow, rate_func=smooth)
        self.wait(0.35 * slow)

        min_price = float("inf")
        max_profit = 0

        def argmin_prefix(upto: int) -> int:
            """prices[0..upto]  inclusive 的最小值下标。"""
            j = 0
            for k in range(1, upto + 1):
                if prices[k] < prices[j]:
                    j = k
            return j

        def top_mid(k: int) -> np.ndarray:
            return np.array([cell_center(k, prices_y)[0], prices_y + cell_h / 2, 0])

        def new_arrow_for_cell(k: int) -> Arrow:
            tm = top_mid(k)
            return Arrow(
                tm + UP * arrow_len,
                tm,
                color=RED_P,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.22,
                buff=0,
            ).set_z_index(14)

        def small_firework_at(p: np.ndarray) -> None:
            rng = np.random.default_rng(42)
            dots = VGroup()
            for _ in range(16):
                ang = rng.random() * TAU
                rad = 0.07 + rng.random() * 0.11
                d = Dot(p + rad * np.array([np.cos(ang), np.sin(ang), 0]), radius=0.022, color=GOLD)
                dots.add(d)
            dots.set_z_index(40)
            self.play(
                LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.035),
                run_time=0.12 * slow,
                rate_func=smooth,
            )
            self.play(FadeOut(dots, scale=1.25), run_time=0.1 * slow, rate_func=smooth)

        for i in range(n):
            price = prices[i]
            min_price = min(min_price, price)
            profit = price - min_price
            min_j_left = argmin_prefix(i - 1) if i >= 1 else 0
            old_ans = max_profit
            max_profit = max(max_profit, profit)

            new_yellow = Rectangle(
                width=cell_w,
                height=cell_h,
                color=YELLOW_P,
                stroke_width=stroke_yellow,
                fill_opacity=0,
            ).move_to(cell_center(i, prices_y))
            new_yellow.set_z_index(12)

            new_arrow = new_arrow_for_cell(i)

            if i == 0:
                self.play(
                    Create(yellow_rect),
                    GrowArrow(ptr_arrow),
                    run_time=t_step,
                    rate_func=smooth,
                )
            else:
                self.play(
                    ReplacementTransform(yellow_rect, new_yellow),
                    ReplacementTransform(ptr_arrow, new_arrow),
                    run_time=t_move,
                    rate_func=smooth,
                )
                yellow_rect, ptr_arrow = new_yellow, new_arrow

                new_green = green_prefix_rect(i - 1, prices_y, gh, GREEN_P, stroke_green)
                new_green.set_z_index(4)
                new_blue = Rectangle(
                    width=cell_w * 0.92,
                    height=cell_h * 0.88,
                    color=BLUE_P,
                    stroke_width=stroke_blue,
                    fill_opacity=0,
                ).move_to(cell_center(min_j_left, prices_y))
                new_blue.set_z_index(10)

                if green_rect is None:
                    green_rect = new_green
                    blue_rect = new_blue
                    self.play(Create(green_rect), Create(blue_rect), run_time=t_green, rate_func=smooth)
                else:
                    assert green_rect is not None and blue_rect is not None
                    self.play(
                        Transform(green_rect, new_green),
                        Transform(blue_rect, new_blue),
                        run_time=t_green,
                        rate_func=smooth,
                    )

            self.wait(t_pause * 0.45)

            if i == 0:
                self.wait(0.35 * slow)
            else:
                assert green_rect is not None
                a = vals[i].copy()
                b = vals[min_j_left].copy()
                a.set_z_index(25)
                b.set_z_index(25)
                self.add(a, b)

                cx = (cell_center(i, prices_y)[0] + cell_center(min_j_left, prices_y)[0]) / 2
                minus_sym.move_to(np.array([cx - 0.42, eq_y, 0]))
                eq_sym.move_to(np.array([cx + 0.42, eq_y, 0]))
                raw_diff = prices[i] - prices[min_j_left]
                res_txt = Text(str(raw_diff), font_size=val_fs, color=YELLOW_P, font="Consolas", disable_ligatures=True)
                res_txt.move_to(np.array([cx + 0.92, eq_y, 0]))
                res_txt.set_z_index(25)

                self.play(
                    a.animate.move_to(np.array([cx - 0.92, eq_y, 0])),
                    b.animate.move_to(np.array([cx, eq_y, 0])),
                    FadeIn(minus_sym, scale=0.85),
                    run_time=t_eq,
                    rate_func=smooth,
                )
                self.play(FadeIn(eq_sym, scale=0.85), FadeIn(res_txt, shift=UP * 0.12), run_time=t_eq * 0.55, rate_func=smooth)

                if profit > old_ans:
                    fly = res_txt.copy()
                    self.add(fly)
                    self.play(
                        fly.animate.move_to(ans_val.get_center()),
                        FadeOut(res_txt),
                        FadeOut(a),
                        FadeOut(b),
                        FadeOut(minus_sym),
                        FadeOut(eq_sym),
                        run_time=t_fly_ans,
                        rate_func=smooth,
                    )
                    new_ans_t = Text(str(max_profit), font_size=val_fs, color=WHITE, font="Consolas", disable_ligatures=True)
                    new_ans_t.move_to(ans_box.get_center())
                    new_ans_t.set_z_index(4)
                    self.play(Transform(ans_val, new_ans_t), run_time=0.28 * slow, rate_func=smooth)
                    small_firework_at(ans_box.get_center() + UP * 0.06)
                    self.remove(fly)
                else:
                    self.play(
                        FadeOut(res_txt),
                        FadeOut(a),
                        FadeOut(b),
                        FadeOut(minus_sym),
                        FadeOut(eq_sym),
                        run_time=0.42 * slow,
                        rate_func=smooth,
                    )

            self.wait(t_pause * 0.55)

        self.wait(0.85 * slow)


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read().strip()
    if raw:
        prices_main = list(map(int, raw.split()))
        sol = Solution()
        print(sol.maxProfit(prices_main))
