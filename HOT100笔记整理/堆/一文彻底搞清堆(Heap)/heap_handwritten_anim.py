# -*- coding: utf-8 -*-
"""
手写堆（小根堆）教学动画（Manim）

480p 预览:
  py -m manim heap_handwritten_anim.py HandwrittenHeapDemo -ql --disable_caching

1440p 成片:
  py -m manim heap_handwritten_anim.py HandwrittenHeapDemo --resolution 2560,1440 --disable_caching
"""

from __future__ import annotations

import math
from manim import *

config.pixel_width = 2560
config.pixel_height = 1440
config.frame_rate = 60


class HandwrittenHeapDemo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        WHITE_C = WHITE
        YELLOW_C = "#ffd84d"
        GREEN_C = "#55dd66"
        RED_C = "#ff4444"

        # --- 布局 ---
        left_x = -5.85
        ops_top_y = 2.7
        line_gap = 0.5
        op_fs = 25

        heap_center = np.array([2.95, 1.65, 0])
        # 数组移动到二叉堆正下方附近并稍微左上
        array_start_center_x = 1.85
        array_origin = np.array([array_start_center_x, -2.05, 0])
        array_cell_w = 0.78
        array_cell_h = 0.62

        heap_label = Text("堆", font_size=24, color=WHITE_C, font="Microsoft YaHei")
        heap_label.move_to(np.array([1.1, 3.2, 0]))
        arr_label = Text("数组形式", font_size=22, color=WHITE_C, font="Microsoft YaHei")
        _first_array_left = np.array([array_start_center_x - array_cell_w / 2, -2.05, 0])
        arr_label.next_to(_first_array_left, LEFT, buff=0.25)
        self.play(FadeIn(heap_label), FadeIn(arr_label), run_time=0.5)

        # 第 1 行：用「1. 插入元素序列」右侧的 [3,2,5,6,4] 本行数字做红指针，不另复制一列
        seq_values = [3, 2, 5, 6, 4]
        line0_pre = Text("1. 插入元素序列", font_size=op_fs, color=WHITE_C, font="Microsoft YaHei")
        lbr0 = Text(" [", font_size=op_fs, color=WHITE_C, font="Microsoft YaHei")
        line0_parts: list[Mobject] = [line0_pre, lbr0]
        seq_digit_mobs: list[Text] = []
        for k, v in enumerate(seq_values):
            num_t = Text(str(v), font_size=op_fs, color=WHITE_C, font="Consolas")
            seq_digit_mobs.append(num_t)
            line0_parts.append(num_t)
            if k < len(seq_values) - 1:
                line0_parts.append(Text(", ", font_size=op_fs, color=WHITE_C, font="Consolas"))
        line0_parts.append(Text("]", font_size=op_fs, color=WHITE_C, font="Consolas"))
        line0 = VGroup(*line0_parts)
        line0.arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
        line0.shift(
            np.array(
                [
                    left_x - line0.get_left()[0],
                    ops_top_y - line0.get_center()[1],
                    0,
                ]
            )
        )
        # 12 条左侧操作：第 1 条为 VGroup，其余 11 条为整行 Text
        op_mobs: list[Mobject] = [line0]
        rest_op_lines = [
            "2. 取最小值",
            "3. 插入元素 1",
            "4. 取最小值",
            "5. 删除最小值",
            "6. 取最小值",
            "7. 插入元素 8",
            "8. 取最小值",
            "9. 删除最小值",
            "10. 删除最小值",
            "11. 插入元素 2",
            "12. 取最小值",
        ]
        for i, s in enumerate(rest_op_lines, start=1):
            t = Text(s, font_size=op_fs, color=WHITE_C, font="Microsoft YaHei")
            t.move_to(np.array([left_x, ops_top_y - i * line_gap, 0]), aligned_edge=LEFT)
            op_mobs.append(t)

        # 堆状态
        heap_vals = [None]  # 1-index
        node_circles: dict[int, Circle] = {}
        node_texts: dict[int, Text] = {}
        edge_lines: dict[int, Line] = {}

        arr_cells: list[Square] = []
        arr_texts: list[Text] = []

        def node_pos(i: int) -> np.ndarray:
            level = int(math.log2(i))
            level_start = 2**level
            idx_in_level = i - level_start
            nodes_in_level = 2**level
            span = 4.4 / (2 ** max(level - 1, 0))
            x = heap_center[0] + (idx_in_level - (nodes_in_level - 1) / 2) * span
            y = heap_center[1] - level * 0.95
            return np.array([x, y, 0])

        def create_node(i: int, v: int, highlight: bool = False):
            c = Circle(radius=0.26, color=YELLOW_C if highlight else WHITE_C, stroke_width=3)
            c.set_fill(opacity=0)
            c.move_to(node_pos(i))
            txt = Text(str(v), font_size=28, color=YELLOW_C if highlight else WHITE_C, font="Consolas")
            txt.move_to(c.get_center())
            node_circles[i] = c
            node_texts[i] = txt

            anims = [FadeIn(c, scale=0.85), FadeIn(txt, scale=0.85)]
            if i > 1:
                p = i // 2
                line = Line(
                    node_circles[p].get_center(),
                    c.get_center(),
                    buff=0.26,
                    color=YELLOW_C if highlight else WHITE_C,
                    stroke_width=2.6,
                )
                edge_lines[i] = line
                anims.append(Create(line))
            self.play(*anims, run_time=0.42)

        def create_array_cell(v: int, highlight: bool = False):
            x = array_origin[0] + len(arr_cells) * (array_cell_w + 0.06)
            y = array_origin[1]
            sq = Square(side_length=array_cell_w, color=YELLOW_C if highlight else WHITE_C, stroke_width=2.6)
            sq.set_fill(opacity=0)
            sq.move_to(np.array([x, y, 0]))
            txt = Text(str(v), font_size=30, color=YELLOW_C if highlight else WHITE_C, font="Consolas")
            txt.move_to(sq.get_center())
            arr_cells.append(sq)
            arr_texts.append(txt)
            self.play(FadeIn(sq, scale=0.85), FadeIn(txt, scale=0.85), run_time=0.35)

        def normalize_colors():
            anims = []
            for i in range(1, len(heap_vals)):
                if i in node_circles:
                    anims.append(node_circles[i].animate.set_stroke(WHITE_C))
                if i in node_texts:
                    anims.append(node_texts[i].animate.set_color(WHITE_C))
                if i in edge_lines:
                    anims.append(edge_lines[i].animate.set_stroke(WHITE_C))
            for i in range(len(arr_cells)):
                anims.append(arr_cells[i].animate.set_stroke(WHITE_C))
                anims.append(arr_texts[i].animate.set_color(WHITE_C))
            if anims:
                self.play(*anims, run_time=0.2)

        def activate_step(idx: int):
            self.play(
                op_mobs[idx].animate.set_color(YELLOW_C).set_stroke(color=YELLOW_C, width=1.6),
                run_time=0.18,
            )

        def deactivate_step(idx: int):
            self.play(
                op_mobs[idx].animate.set_color(WHITE_C).set_stroke(color=WHITE_C, width=0),
                run_time=0.18,
            )

        def swap_anim(i: int, j: int, active_idx: int | None = None) -> int | None:
            if i == j:
                return active_idx

            a, b = node_circles[i].get_center(), node_circles[j].get_center()
            ar1 = CurvedArrow(
                a,
                b,
                angle=TAU / 7,
                color=GREEN_C,
                stroke_width=4.5,
                tip_length=0.2,
            )
            ar2 = CurvedArrow(
                b,
                a,
                angle=TAU / 7,
                color=GREEN_C,
                stroke_width=4.5,
                tip_length=0.2,
            )
            ar1.set_z_index(20)
            ar2.set_z_index(20)

            aa, bb = arr_cells[i - 1].get_center(), arr_cells[j - 1].get_center()
            ar3 = CurvedArrow(
                aa,
                bb,
                angle=TAU / 8,
                color=GREEN_C,
                stroke_width=4.0,
                tip_length=0.17,
            )
            ar4 = CurvedArrow(
                bb,
                aa,
                angle=TAU / 8,
                color=GREEN_C,
                stroke_width=4.0,
                tip_length=0.17,
            )
            ar3.set_z_index(20)
            ar4.set_z_index(20)

            self.play(Create(ar1), Create(ar2), Create(ar3), Create(ar4), run_time=0.5)

            i_is_active = active_idx == i
            j_is_active = active_idx == j

            t1 = node_texts[i].copy().set_color(YELLOW_C if i_is_active else WHITE_C)
            t2 = node_texts[j].copy().set_color(YELLOW_C if j_is_active else WHITE_C)
            a1 = arr_texts[i - 1].copy().set_color(YELLOW_C if i_is_active else WHITE_C)
            a2 = arr_texts[j - 1].copy().set_color(YELLOW_C if j_is_active else WHITE_C)
            s1 = arr_cells[i - 1].copy().set_stroke(YELLOW_C if i_is_active else WHITE_C)
            s2 = arr_cells[j - 1].copy().set_stroke(YELLOW_C if j_is_active else WHITE_C)
            self.add(t1, t2, a1, a2, s1, s2)
            self.remove(node_texts[i], node_texts[j], arr_texts[i - 1], arr_texts[j - 1])
            self.play(
                t1.animate.move_to(node_circles[j].get_center()),
                t2.animate.move_to(node_circles[i].get_center()),
                a1.animate.move_to(arr_cells[j - 1].get_center()),
                a2.animate.move_to(arr_cells[i - 1].get_center()),
                s1.animate.move_to(arr_cells[j - 1].get_center()),
                s2.animate.move_to(arr_cells[i - 1].get_center()),
                run_time=0.65,
            )

            heap_vals[i], heap_vals[j] = heap_vals[j], heap_vals[i]
            c_i = YELLOW_C if j_is_active else WHITE_C
            c_j = YELLOW_C if i_is_active else WHITE_C
            self.play(
                node_circles[i].animate.set_stroke(c_i),
                node_circles[j].animate.set_stroke(c_j),
                run_time=0.22,
            )
            node_texts[i] = Text(str(heap_vals[i]), font_size=28, color=c_i, font="Consolas").move_to(node_circles[i])
            node_texts[j] = Text(str(heap_vals[j]), font_size=28, color=c_j, font="Consolas").move_to(node_circles[j])
            arr_texts[i - 1] = Text(str(heap_vals[i]), font_size=30, color=c_i, font="Consolas").move_to(arr_cells[i - 1])
            arr_texts[j - 1] = Text(str(heap_vals[j]), font_size=30, color=c_j, font="Consolas").move_to(arr_cells[j - 1])
            arr_cells[i - 1].set_stroke(c_i)
            arr_cells[j - 1].set_stroke(c_j)
            self.remove(t1, t2, a1, a2, s1, s2)
            self.add(node_texts[i], node_texts[j], arr_texts[i - 1], arr_texts[j - 1])

            self.play(FadeOut(ar1), FadeOut(ar2), FadeOut(ar3), FadeOut(ar4), run_time=0.35)
            if i_is_active:
                return j
            if j_is_active:
                return i
            return active_idx

        def up(i: int):
            active = i
            while i > 1:
                p = i // 2
                if heap_vals[p] <= heap_vals[i]:
                    break
                active = swap_anim(p, i, active_idx=active)
                i = p

        def down(i: int):
            n = len(heap_vals) - 1
            active = i
            while i * 2 <= n:
                t = i
                l = i * 2
                r = i * 2 + 1
                if l <= n and heap_vals[l] < heap_vals[t]:
                    t = l
                if r <= n and heap_vals[r] < heap_vals[t]:
                    t = r
                if t == i:
                    break
                active = swap_anim(i, t, active_idx=active)
                i = t

        def insert_value(v: int):
            heap_vals.append(v)
            i = len(heap_vals) - 1
            create_node(i, v, highlight=True)
            create_array_cell(v, highlight=True)
            self.wait(0.08)
            up(i)
            normalize_colors()

        def get_min_to_line(op_idx: int):
            if len(heap_vals) <= 1:
                return
            value = heap_vals[1]
            root_copy = node_texts[1].copy()
            target = Text(str(value), font_size=30, color=WHITE_C, font="Consolas")
            target.next_to(op_mobs[op_idx], RIGHT, buff=0.26)
            self.add(root_copy)
            self.play(root_copy.animate.move_to(target.get_center()), run_time=0.45)
            self.remove(root_copy)
            self.play(FadeIn(target), run_time=0.1)

        def delete_min():
            n = len(heap_vals) - 1
            if n <= 0:
                return
            if n == 1:
                self.play(
                    FadeOut(node_circles[1]),
                    FadeOut(node_texts[1]),
                    FadeOut(arr_cells[0]),
                    FadeOut(arr_texts[0]),
                    run_time=0.36,
                )
                heap_vals.pop()
                node_circles.pop(1)
                node_texts.pop(1)
                arr_cells.pop()
                arr_texts.pop()
                return

            tail_val = heap_vals[n]
            root_pos = node_circles[1].get_center()

            # 根节点先消失
            self.play(FadeOut(node_circles[1]), FadeOut(node_texts[1]), run_time=0.25)

            # 尾节点飞到根位置，同时尾边消失；数组末尾删除并把尾值写到首格
            node_circles[n].set_stroke(YELLOW_C)
            node_texts[n].set_color(YELLOW_C)
            new_arr_root = Text(str(tail_val), font_size=30, color=YELLOW_C, font="Consolas").move_to(arr_cells[0])
            self.play(
                node_circles[n].animate.move_to(root_pos),
                node_texts[n].animate.move_to(root_pos),
                FadeOut(edge_lines[n]),
                Transform(arr_texts[0], new_arr_root),
                FadeOut(arr_cells[-1]),
                FadeOut(arr_texts[-1]),
                run_time=0.28,
            )

            # 重建索引：飞上来的尾节点成为新根
            heap_vals[1] = tail_val
            node_circles[1] = node_circles[n]
            node_texts[1] = node_texts[n]
            node_circles.pop(n)
            node_texts.pop(n)
            edge_lines.pop(n)
            arr_cells.pop()
            arr_texts.pop()
            heap_vals.pop()

            down(1)
            normalize_colors()

        # --- 逐行出现并执行 ---
        self.play(FadeIn(op_mobs[0], shift=RIGHT * 0.1), run_time=0.35)
        activate_step(0)

        # 第一行：红指针在「1. 插入元素序列」右侧的序列数字上逐格移动（不另复制一列）
        d0 = seq_digit_mobs[0]
        pointer = Arrow(
            start=d0.get_top() + UP * 0.42,
            end=d0.get_top() + UP * 0.02,
            buff=0,
            color=RED_C,
            stroke_width=5.0,
            max_tip_length_to_length_ratio=0.22,
        )
        self.play(FadeIn(pointer), run_time=0.22)
        for k, v in enumerate(seq_values):
            if k > 0:
                dk = seq_digit_mobs[k]
                new_p = Arrow(
                    start=dk.get_top() + UP * 0.42,
                    end=dk.get_top() + UP * 0.02,
                    buff=0,
                    color=RED_C,
                    stroke_width=5.0,
                    max_tip_length_to_length_ratio=0.22,
                )
                self.play(Transform(pointer, new_p), run_time=0.28)
            insert_value(v)
            self.wait(0.15)
        self.play(FadeOut(pointer), run_time=0.24)
        deactivate_step(0)

        # 2
        self.play(FadeIn(op_mobs[1], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(1)
        get_min_to_line(1)
        self.wait(0.16)
        deactivate_step(1)

        # 3
        self.play(FadeIn(op_mobs[2], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(2)
        insert_value(1)
        self.wait(0.16)
        deactivate_step(2)

        # 4
        self.play(FadeIn(op_mobs[3], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(3)
        get_min_to_line(3)
        self.wait(0.16)
        deactivate_step(3)

        # 5
        self.play(FadeIn(op_mobs[4], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(4)
        delete_min()
        self.wait(0.16)
        deactivate_step(4)

        # 6
        self.play(FadeIn(op_mobs[5], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(5)
        get_min_to_line(5)
        self.wait(0.16)
        deactivate_step(5)

        # 7
        self.play(FadeIn(op_mobs[6], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(6)
        insert_value(8)
        self.wait(0.16)
        deactivate_step(6)

        # 8
        self.play(FadeIn(op_mobs[7], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(7)
        get_min_to_line(7)
        self.wait(0.16)
        deactivate_step(7)

        # 9
        self.play(FadeIn(op_mobs[8], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(8)
        delete_min()
        self.wait(0.16)
        deactivate_step(8)

        # 10
        self.play(FadeIn(op_mobs[9], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(9)
        delete_min()
        self.wait(0.12)
        deactivate_step(9)

        # 11
        self.play(FadeIn(op_mobs[10], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(10)
        insert_value(2)
        self.wait(0.12)
        deactivate_step(10)

        # 12
        self.play(FadeIn(op_mobs[11], shift=RIGHT * 0.1), run_time=0.28)
        activate_step(11)
        get_min_to_line(11)
        deactivate_step(11)

        self.wait(1.0)
