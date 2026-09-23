# -*- coding: utf-8 -*-
"""
第 k 大元素（小根堆）教学动画（Manim）

快速预览（480p）:
  py -m manim kth_largest_heap_acm_anim.py KthLargestHeapACMDemo -ql --disable_caching

按要求画布尺寸导出（2560x1440）:
  py -m manim kth_largest_heap_acm_anim.py KthLargestHeapACMDemo --resolution 2560,1440 --disable_caching
"""

from __future__ import annotations

import math
from manim import *

config.pixel_width = 854
config.pixel_height = 480
config.frame_rate = 30


class KthLargestHeapACMDemo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        WHITE_C = WHITE
        YELLOW_C = "#ffd84d"
        GREEN_C = "#55dd66"
        RED_C = "#ff4444"

        nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]
        k = 4
        sorted_desc = sorted(nums, reverse=True)

        # ---- 四象限布局锚点 ----
        heap_title_pos = np.array([-6.1, 2.9, 0])
        heap_center = np.array([-3.9, 1.45, 0])

        heap_arr_origin = np.array([-5.0, -2.1, 0])

        origin_title_pos = np.array([-0.9, 2.9, 0])
        origin_arr_origin = np.array([0.6, 1.5, 0])

        sorted_title_pos = np.array([-0.9, -1.35, 0])
        sorted_arr_origin = np.array([0.6, -2.1, 0])

        cell_w = 0.60
        cell_h = 0.60
        cell_gap = 0.06

        # ---- 标题 ----
        heap_title = Text("堆", font="Microsoft YaHei", font_size=28, color=WHITE_C).move_to(heap_title_pos, aligned_edge=LEFT)
        origin_title = Text("原数组(K=4)", font="Microsoft YaHei", font_size=28, color=WHITE_C).move_to(origin_title_pos, aligned_edge=LEFT)
        sorted_title = Text("降序排序", font="Microsoft YaHei", font_size=28, color=WHITE_C).move_to(sorted_title_pos, aligned_edge=LEFT)
        mid_dash = DashedLine(
            start=np.array([origin_title_pos[0] - 0.45, origin_title_pos[1] + 0.35, 0]),
            end=np.array([origin_title_pos[0] - 0.45, sorted_title_pos[1] - 0.35, 0]),
            dash_length=0.16,
            color=WHITE_C,
            stroke_width=2.2,
        )

        self.play(FadeIn(heap_title), FadeIn(origin_title), FadeIn(sorted_title), Create(mid_dash), run_time=0.6)

        # ---- 数组工具 ----
        def make_array(values: list[int], start: np.ndarray):
            cells = []
            texts = []
            for i, v in enumerate(values):
                x = start[0] + i * (cell_w + cell_gap)
                y = start[1]
                sq = Rectangle(width=cell_w, height=cell_h, color=WHITE_C, stroke_width=2.2).move_to([x, y, 0])
                tx = Text(str(v), font="Consolas", font_size=26, color=WHITE_C).move_to(sq.get_center())
                cells.append(sq)
                texts.append(tx)
            return cells, texts

        origin_cells, origin_texts = make_array(nums, origin_arr_origin)
        sorted_cells, sorted_texts = make_array(sorted_desc, sorted_arr_origin)

        # ---- 预备阶段：先展示原数组 ----
        for sq, tx in zip(origin_cells, origin_texts):
            self.play(FadeIn(sq, scale=0.95), FadeIn(tx, scale=0.95), run_time=0.16)
        self.wait(0.25)

        # 向下箭头 + 降序数组出现
        arr_mid = (origin_cells[0].get_center() + origin_cells[-1].get_center()) / 2
        sorted_mid = (sorted_cells[0].get_center() + sorted_cells[-1].get_center()) / 2
        down_arrow = Arrow(
            start=arr_mid + DOWN * 0.62,
            end=sorted_mid + UP * 0.62,
            color=WHITE_C,
            buff=0.05,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )
        self.play(Create(down_arrow), run_time=0.42)
        for sq, tx in zip(sorted_cells, sorted_texts):
            self.play(FadeIn(sq, scale=0.95), FadeIn(tx, scale=0.95), run_time=0.16)
        self.wait(0.15)
        self.play(FadeOut(down_arrow), run_time=0.2)

        # 前 k 个黄框 + 第 k 个绿色加粗
        k_group_box = SurroundingRectangle(
            VGroup(*sorted_cells[:k]),
            color=YELLOW_C,
            buff=0.08,
            stroke_width=3.5,
        )
        self.play(Create(k_group_box), run_time=0.45)
        sorted_texts[k - 1].set_weight(BOLD)
        self.play(sorted_texts[k - 1].animate.set_color(GREEN_C).scale(1.12), run_time=0.35)
        self.wait(0.2)

        # ---- 堆结构数据 ----
        heap_vals = [None]  # 1-index
        node_circles: dict[int, Circle] = {}
        node_texts: dict[int, Text] = {}
        edge_lines: dict[int, Line] = {}

        heap_arr_cells: list[Rectangle] = []
        heap_arr_texts: list[Text] = []

        def heap_node_pos(i: int):
            level = int(math.log2(i))
            first = 2**level
            idx = i - first
            cnt = 2**level
            span = 3.8 / (2 ** max(level - 1, 0))
            x = heap_center[0] + (idx - (cnt - 1) / 2) * span
            y = heap_center[1] - level * 1.05
            return np.array([x, y, 0])

        def create_heap_node(i: int, v: int, yellow=False):
            c = Circle(radius=0.25, color=YELLOW_C if yellow else WHITE_C, stroke_width=2.6).set_fill(opacity=0)
            c.move_to(heap_node_pos(i))
            t = Text(str(v), font="Consolas", font_size=28, color=YELLOW_C if yellow else WHITE_C).move_to(c.get_center())

            node_circles[i] = c
            node_texts[i] = t
            anims = [FadeIn(c, scale=0.88), FadeIn(t, scale=0.88)]
            if i > 1:
                p = i // 2
                ln = Line(node_circles[p].get_center(), c.get_center(), buff=0.25, color=YELLOW_C if yellow else WHITE_C, stroke_width=2.2)
                edge_lines[i] = ln
                anims.append(Create(ln))
            self.play(*anims, run_time=0.35)

        def recolor_heap_white():
            anims = []
            for i in range(1, len(heap_vals)):
                if i in node_circles:
                    anims.append(node_circles[i].animate.set_stroke(WHITE_C))
                if i in node_texts:
                    anims.append(node_texts[i].animate.set_color(WHITE_C))
                if i in edge_lines:
                    anims.append(edge_lines[i].animate.set_stroke(WHITE_C))
            if anims:
                self.play(*anims, run_time=0.2)

        def apply_active_highlight(active_idx: int | None):
            for t in range(1, len(heap_vals)):
                if t not in node_circles or t not in node_texts:
                    continue
                if active_idx is not None and t == active_idx:
                    node_circles[t].set_stroke(YELLOW_C)
                    node_texts[t].set_color(YELLOW_C)
                    if t in edge_lines:
                        edge_lines[t].set_stroke(YELLOW_C)
                else:
                    node_circles[t].set_stroke(WHITE_C)
                    node_texts[t].set_color(WHITE_C)
                    if t in edge_lines:
                        edge_lines[t].set_stroke(WHITE_C)

        def swap_value_anim(i: int, j: int, active_idx: int | None = None):
            a, b = node_circles[i].get_center(), node_circles[j].get_center()
            left_to_right = CurvedDoubleArrow(a, b, color=GREEN_C, stroke_width=3.8, tip_length=0.14)
            right_to_left = CurvedDoubleArrow(b, a, color=GREEN_C, stroke_width=3.8, tip_length=0.14)
            self.play(Create(left_to_right), Create(right_to_left), run_time=0.48)

            ti = node_texts[i].copy()
            tj = node_texts[j].copy()
            self.add(ti, tj)
            self.remove(node_texts[i], node_texts[j])
            self.play(ti.animate.move_to(node_circles[j]), tj.animate.move_to(node_circles[i]), run_time=0.52)

            heap_vals[i], heap_vals[j] = heap_vals[j], heap_vals[i]
            new_active = active_idx
            if active_idx == i:
                new_active = j
            elif active_idx == j:
                new_active = i

            node_texts[i] = Text(str(heap_vals[i]), font="Consolas", font_size=28, color=WHITE_C).move_to(node_circles[i])
            node_texts[j] = Text(str(heap_vals[j]), font="Consolas", font_size=28, color=WHITE_C).move_to(node_circles[j])
            self.remove(ti, tj)
            self.add(node_texts[i], node_texts[j])
            apply_active_highlight(new_active)
            self.play(FadeOut(left_to_right), FadeOut(right_to_left), run_time=0.26)
            return new_active

        def sift_up(i: int):
            active = i
            apply_active_highlight(active)
            while i > 1:
                p = i // 2
                if heap_vals[i] >= heap_vals[p]:
                    break
                active = swap_value_anim(i, p, active_idx=active)
                i = p
            apply_active_highlight(active)

        def sift_down(i: int):
            n = len(heap_vals) - 1
            active = i
            apply_active_highlight(active)
            while True:
                l, r = i * 2, i * 2 + 1
                smallest = i
                if l <= n and heap_vals[l] < heap_vals[smallest]:
                    smallest = l
                if r <= n and heap_vals[r] < heap_vals[smallest]:
                    smallest = r
                if smallest == i:
                    break
                active = swap_value_anim(i, smallest, active_idx=active)
                i = smallest
            apply_active_highlight(active)

        def add_to_heap_array(v: int):
            x = heap_arr_origin[0] + len(heap_arr_cells) * (cell_w + cell_gap)
            y = heap_arr_origin[1]
            sq = Rectangle(width=cell_w, height=cell_h, color=WHITE_C, stroke_width=2.2).move_to([x, y, 0])
            tx = Text(str(v), font="Consolas", font_size=26, color=WHITE_C).move_to(sq.get_center())
            heap_arr_cells.append(sq)
            heap_arr_texts.append(tx)
            self.play(FadeIn(sq, scale=0.9), FadeIn(tx, scale=0.9), run_time=0.22)

        def pop_min_from_heap(to_array: bool):
            n = len(heap_vals) - 1
            if n <= 0:
                return None
            root_val = heap_vals[1]
            old_root_circle = node_circles[1]
            old_root_text = node_texts[1]

            if to_array:
                root_copy = node_texts[1].copy().set_color(WHITE_C)
                target = np.array(
                    [
                        heap_arr_origin[0] + len(heap_arr_cells) * (cell_w + cell_gap),
                        heap_arr_origin[1],
                        0,
                    ]
                )
                self.add(root_copy)
                self.play(root_copy.animate.move_to(target), run_time=0.35)
                self.remove(root_copy)
                add_to_heap_array(root_val)

            if n == 1:
                self.play(FadeOut(old_root_circle), FadeOut(old_root_text), run_time=0.25)
                self.remove(old_root_circle, old_root_text)
                heap_vals.pop()
                node_circles.pop(1)
                node_texts.pop(1)
                return root_val

            last_idx = n
            last_val = heap_vals[last_idx]
            root_pos = node_circles[1].get_center()
            node_circles[last_idx].set_stroke(YELLOW_C)
            node_texts[last_idx].set_color(YELLOW_C)
            move_anims = [
                node_circles[last_idx].animate.move_to(root_pos),
                node_texts[last_idx].animate.move_to(root_pos),
            ]
            if last_idx in edge_lines:
                move_anims.append(FadeOut(edge_lines[last_idx]))
            self.play(*move_anims, FadeOut(old_root_circle), FadeOut(old_root_text), run_time=0.35)

            heap_vals[1] = last_val
            heap_vals.pop()
            node_circles[1] = node_circles[last_idx]
            node_texts[1] = node_texts[last_idx]
            node_circles.pop(last_idx)
            node_texts.pop(last_idx)
            if last_idx in edge_lines:
                edge_lines.pop(last_idx)

            # 删除搬上来过程中的旧数字对象，避免和新根数字重叠残留
            self.remove(node_texts[1])
            node_texts[1] = Text(str(last_val), font="Consolas", font_size=28, color=YELLOW_C).move_to(node_circles[1])
            self.add(node_texts[1])
            sift_down(1)
            recolor_heap_white()
            return root_val

        # ---- 红色指针 ----
        pointer = Arrow(
            start=origin_cells[0].get_top() + UP * 0.50,
            end=origin_cells[0].get_top() + UP * 0.06,
            color=RED_C,
            stroke_width=4.8,
            buff=0,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(FadeIn(pointer), run_time=0.25)

        # ---- 建堆 / 枚举 ----
        for idx, x in enumerate(nums):
            if idx > 0:
                new_pointer = Arrow(
                    start=origin_cells[idx].get_top() + UP * 0.50,
                    end=origin_cells[idx].get_top() + UP * 0.06,
                    color=RED_C,
                    stroke_width=4.8,
                    buff=0,
                    max_tip_length_to_length_ratio=0.2,
                )
                self.play(Transform(pointer, new_pointer), run_time=0.25)

            # A: size < k, push + sift_up
            if len(heap_vals) - 1 < k:
                heap_vals.append(x)
                i = len(heap_vals) - 1
                create_heap_node(i, x, yellow=True)
                self.wait(0.1)
                sift_up(i)
                recolor_heap_white()
                self.wait(0.08)
                continue

            # B: size == k, compare with top
            fly = Text(str(x), font="Consolas", font_size=26, color=WHITE_C).move_to(origin_cells[idx].get_center())
            root_right = node_circles[1].get_center() + RIGHT * 0.82
            self.add(fly)
            self.play(fly.animate.move_to(root_right), run_time=0.35)

            if x <= heap_vals[1]:
                # 画面中左侧是堆顶、右侧是当前 x，因此应展示为 heap_top >= x
                sign = Text("≥", font="Consolas", font_size=34, color=WHITE_C).move_to((root_right + node_circles[1].get_center()) / 2 + UP * 0.05)
                self.play(FadeIn(sign, scale=0.9), run_time=0.15)

                # 不进入结果区，直接消失
                self.play(FadeOut(fly), run_time=0.2)
                self.play(FadeOut(sign), run_time=0.1)
            else:
                # 画面中左侧是堆顶、右侧是当前 x，因此应展示为 heap_top < x
                sign = Text("<", font="Consolas", font_size=34, color=WHITE_C).move_to((root_right + node_circles[1].get_center()) / 2 + UP * 0.05)
                self.play(FadeIn(sign, scale=0.9), run_time=0.15)
                self.wait(0.15)

                # replace_top：原堆顶直接消失，x 飞进根并下沉
                self.play(fly.animate.move_to(node_circles[1].get_center()), run_time=0.3)
                self.remove(fly, node_texts[1])
                heap_vals[1] = x
                node_circles[1].set_stroke(YELLOW_C)
                node_texts[1] = Text(str(x), font="Consolas", font_size=28, color=YELLOW_C).move_to(node_circles[1])
                self.add(node_texts[1])
                self.play(FadeOut(sign), run_time=0.1)
                self.wait(0.08)
                sift_down(1)
                recolor_heap_white()

            self.wait(0.06)

        # ---- 收尾：遍历结束后再连续 pop k 次到堆下数组 ----
        self.play(FadeOut(pointer), run_time=0.22)
        popped_vals: list[int] = []
        while len(heap_vals) > 1:
            popped_vals.append(pop_min_from_heap(to_array=True))
            self.wait(0.08)

        # 小根堆 pop 出来是升序，反转得到降序
        left, right = 0, len(heap_arr_texts) - 1
        while left < right:
            a = heap_arr_texts[left].copy()
            b = heap_arr_texts[right].copy()
            self.add(a, b)
            self.remove(heap_arr_texts[left], heap_arr_texts[right])
            self.play(
                a.animate.move_to(heap_arr_cells[right].get_center()),
                b.animate.move_to(heap_arr_cells[left].get_center()),
                run_time=0.42,
            )
            popped_vals[left], popped_vals[right] = popped_vals[right], popped_vals[left]
            heap_arr_texts[left] = Text(str(popped_vals[left]), font="Consolas", font_size=28, color=WHITE_C).move_to(heap_arr_cells[left])
            heap_arr_texts[right] = Text(str(popped_vals[right]), font="Consolas", font_size=28, color=WHITE_C).move_to(heap_arr_cells[right])
            self.remove(a, b)
            self.add(heap_arr_texts[left], heap_arr_texts[right])
            left += 1
            right -= 1

        # 堆下数组第 k 个值对齐右下排序数组第 k 个值
        heap_arr_texts[k - 1].set_weight(BOLD)
        self.play(heap_arr_texts[k - 1].animate.set_color(GREEN_C).scale(1.1), run_time=0.28)
        final_arrow = CurvedArrow(
            start_point=heap_arr_cells[k - 1].get_center() + RIGHT * 0.1,
            end_point=sorted_cells[k - 1].get_center() + LEFT * 0.1,
            angle=-1.05,
            color=GREEN_C,
            stroke_width=5,
            tip_length=0.2,
        )
        self.play(Create(final_arrow), run_time=0.42)
        self.wait(1.2)
