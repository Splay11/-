# -*- coding: utf-8 -*-
"""
手写小根堆 + 堆排序（升序）教学动画（Manim）

堆顶为最小值；依次弹出根得到排序结果 1,2,3,…。
布局：上「小根堆」树形、中「原数组」、下「排序结果」；中下格子列严格对齐。
480p（勿在文件里写死宽高，否则会覆盖 -qp）:
  py -m manim render max_heap_sort_anim.py MinHeapSortDemo -ql --fps 48 --disable_caching

2560×1440 成片:
  py -m manim render max_heap_sort_anim.py MinHeapSortDemo -qp --fps 48 --disable_caching
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np
from manim import *

# 帧率默认 48；分辨率请用命令行 -ql(480p) / -qp(1440p)，避免写死 pixel 覆盖 CLI。
config.frame_rate = 48


class MinHeapSortDemo(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        WHITE_C = WHITE
        YELLOW_C = "#ffd84d"
        GREEN_C = "#55dd66"
        RED_C = "#ff4444"
        RED_POINTER = "#8b1515"  # 深红，原数组指针

        # 动画节奏（交换 / 删除放慢，便于观看）
        T_SWAP_ARROWS = 0.78
        T_SWAP_MOVE = 1.05
        T_SWAP_FADE_ARROWS = 0.48
        T_PUSH_FADEIN = 0.52
        T_DELETE_TO_RED = 0.42
        T_DELETE_FADEOUT = 0.72
        T_FLY_TO_RESULT = 0.72
        T_TAIL_TO_ROOT = 0.68
        T_LAST_ROOT_FADE = 0.48

        # --- 数据（题面示例）---
        n = 5
        original = [2, 4, 1, 5, 3]

        # --- 布局：中下同一 left_x / cell 尺寸，保证列对齐 ---
        cell_w, cell_h = 0.72, 0.58
        buff_x = 0.08
        unit_w = cell_w + buff_x
        total_w = n * cell_w + max(n - 1, 0) * buff_x
        left_x = -total_w / 2

        # 原数组、排序结果整体下移，与堆区拉开间距
        y_src = -1.12
        y_res = y_src - 1.15
        heap_center = np.array([0.0, 2.12, 0])

        val_fs = 30
        lbl_fs = 22

        def cell_center_row(y: float, k: int) -> np.ndarray:
            cx = left_x + k * unit_w + cell_w / 2
            return np.array([cx, y, 0])

        def cell_top_row(y: float, k: int) -> np.ndarray:
            return cell_center_row(y, k) + UP * (cell_h / 2)

        # --- 堆树位置（完全二叉树，1-based 层布局）---
        def node_pos_1based(i: int) -> np.ndarray:
            level = int(math.log2(i))
            level_start = 2**level
            idx_in_level = i - level_start
            nodes_in_level = 2**level
            span = 4.35 / (2 ** max(level - 1, 0))
            x = heap_center[0] + (idx_in_level - (nodes_in_level - 1) / 2) * span
            y = heap_center[1] - level * 0.92
            return np.array([x, y, 0])

        def pos_k(k: int) -> np.ndarray:
            return node_pos_1based(k + 1)

        # --- 标签 ---
        heap_lbl = Text("小根堆", font_size=24, color=WHITE_C, font="Microsoft YaHei")
        heap_lbl.move_to(np.array([left_x - 0.55, heap_center[1] + 0.95, 0]), aligned_edge=LEFT)
        src_lbl = Text("原数组", font_size=lbl_fs, color=WHITE_C, font="Microsoft YaHei")
        src_lbl.next_to(np.array([left_x, y_src, 0]), LEFT, buff=0.22).align_to(
            np.array([left_x, y_src, 0]), UP
        )
        res_lbl = Text("排序结果", font_size=lbl_fs, color=WHITE_C, font="Microsoft YaHei")
        res_lbl.next_to(np.array([left_x, y_res, 0]), LEFT, buff=0.22).align_to(
            np.array([left_x, y_res, 0]), UP
        )

        self.play(FadeIn(heap_lbl), FadeIn(src_lbl), FadeIn(res_lbl), run_time=0.4)

        # --- 原数组：一开始全部显示 ---
        src_cells: list[Rectangle] = []
        src_texts: list[Text] = []
        for k in range(n):
            r = Rectangle(
                width=cell_w,
                height=cell_h,
                color=WHITE_C,
                stroke_width=2.8,
                fill_opacity=0,
            ).move_to(cell_center_row(y_src, k))
            t = Text(str(original[k]), font_size=val_fs, color=WHITE_C, font="Consolas", disable_ligatures=True)
            t.move_to(r.get_center())
            src_cells.append(r)
            src_texts.append(t)
        self.play(
            *[FadeIn(VGroup(src_cells[k], src_texts[k]), scale=0.9) for k in range(n)],
            run_time=0.55,
        )

        # --- 排序结果：空白格 ---
        res_cells: list[Rectangle] = []
        res_texts: list[Optional[Text]] = [None] * n
        for k in range(n):
            r = Rectangle(
                width=cell_w,
                height=cell_h,
                color=WHITE_C,
                stroke_width=2.8,
                fill_opacity=0,
            ).move_to(cell_center_row(y_res, k))
            res_cells.append(r)
        self.play(*[FadeIn(res_cells[k], scale=0.9) for k in range(n)], run_time=0.45)

        # 堆状态（0-based 与算法一致）
        heap: list[int] = []
        node_circles: dict[int, Circle] = {}
        node_texts: dict[int, Text] = {}
        edge_lines: dict[int, Line] = {}  # key: 子下标 >=1，边 parent -> child

        def parent_idx(i: int) -> int:
            return (i - 1) // 2

        def make_pointer_above_src(k: int) -> Arrow:
            base = cell_top_row(y_src, k)
            # 更长箭头：箭身从上方向下指到格顶附近
            top = base + UP * 0.42
            tip = base + UP * 0.04
            return Arrow(
                start=top,
                end=tip,
                buff=0,
                color=RED_POINTER,
                stroke_width=6.2,
                max_tip_length_to_length_ratio=0.2,
            )

        pointer = make_pointer_above_src(0)
        self.play(FadeIn(pointer), run_time=0.28)

        def green_swap_arrows(ci: np.ndarray, cj: np.ndarray) -> tuple[CurvedArrow, CurvedArrow]:
            ar1 = CurvedArrow(
                ci, cj, angle=TAU / 7, color=GREEN_C, stroke_width=4.5, tip_length=0.2
            )
            ar2 = CurvedArrow(
                cj, ci, angle=TAU / 7, color=GREEN_C, stroke_width=4.5, tip_length=0.2
            )
            ar1.set_z_index(50)
            ar2.set_z_index(50)
            return ar1, ar2

        def apply_circle_highlight(follow: int | None):
            """黄框跟随「当前上浮/下沉」的值所在下标（小根堆）；其余白框。"""
            for k in node_circles:
                node_circles[k].set_stroke(YELLOW_C if follow is not None and k == follow else WHITE_C)

        def swap_node_values(i: int, j: int, follow_idx: int | None = None) -> int | None:
            """交换两结点数字；若 follow_idx 非空，黄边始终跟该下标上的值一起走。"""
            if i == j:
                return follow_idx
            if follow_idx is not None:
                apply_circle_highlight(follow_idx)

            ci, cj = node_circles[i].get_center(), node_circles[j].get_center()
            ar1, ar2 = green_swap_arrows(ci, cj)
            self.play(Create(ar1), Create(ar2), run_time=T_SWAP_ARROWS)

            heap[i], heap[j] = heap[j], heap[i]

            new_follow: int | None
            if follow_idx is None:
                new_follow = None
            elif follow_idx == i:
                new_follow = j
            elif follow_idx == j:
                new_follow = i
            else:
                new_follow = follow_idx

            t1 = node_texts[i].copy()
            t2 = node_texts[j].copy()

            self.add(t1, t2)
            self.remove(node_texts[i], node_texts[j])

            self.play(
                t1.animate.move_to(node_circles[j].get_center()),
                t2.animate.move_to(node_circles[i].get_center()),
                run_time=T_SWAP_MOVE,
            )

            tc_i = YELLOW_C if new_follow == i else WHITE_C
            tc_j = YELLOW_C if new_follow == j else WHITE_C
            node_texts[i] = Text(
                str(heap[i]), font_size=28, color=tc_i, font="Consolas", disable_ligatures=True
            ).move_to(node_circles[i])
            node_texts[j] = Text(
                str(heap[j]), font_size=28, color=tc_j, font="Consolas", disable_ligatures=True
            ).move_to(node_circles[j])
            self.remove(t1, t2)
            self.add(node_texts[i], node_texts[j])
            apply_circle_highlight(new_follow)
            self.play(FadeOut(ar1), FadeOut(ar2), run_time=T_SWAP_FADE_ARROWS)
            return new_follow

        def normalize_heap_white():
            anims = []
            for k in node_circles:
                anims.append(node_circles[k].animate.set_stroke(WHITE_C))
            for k in node_texts:
                anims.append(node_texts[k].animate.set_color(WHITE_C))
            for k in edge_lines:
                anims.append(edge_lines[k].animate.set_stroke(WHITE_C))
            if anims:
                self.play(*anims, run_time=0.34)

        def push_visual(v: int):
            heap.append(v)
            idx = len(heap) - 1
            c = Circle(radius=0.26, color=YELLOW_C, stroke_width=3.0)
            c.set_fill(opacity=0)
            c.move_to(pos_k(idx))
            txt = Text(str(v), font_size=28, color=YELLOW_C, font="Consolas", disable_ligatures=True)
            txt.move_to(c.get_center())
            node_circles[idx] = c
            node_texts[idx] = txt
            anims = [FadeIn(c, scale=0.85), FadeIn(txt, scale=0.85)]
            if idx > 0:
                p = parent_idx(idx)
                ln = Line(
                    node_circles[p].get_center(),
                    c.get_center(),
                    buff=0.26,
                    color=YELLOW_C,
                    stroke_width=2.6,
                )
                edge_lines[idx] = ln
                anims.append(Create(ln))
            self.play(*anims, run_time=T_PUSH_FADEIN)
            self.wait(0.1)

            # heapify_up（小根堆：若当前比父小则上浮）；黄框/黄字跟随当前插入值
            follow = idx
            apply_circle_highlight(follow)
            cur = idx
            while cur > 0:
                p = parent_idx(cur)
                if heap[p] <= heap[cur]:
                    break
                follow = swap_node_values(cur, p, follow_idx=follow)
                cur = p

            normalize_heap_white()

        # --- 建堆：红指针逐格 ---
        for k in range(n):
            if k > 0:
                self.play(Transform(pointer, make_pointer_above_src(k)), run_time=0.32)
            self.wait(0.06)
            push_visual(original[k])
            self.wait(0.12)

        self.play(FadeOut(pointer), run_time=0.24)

        # --- 排序阶段 ---
        result_fill = 0

        def fly_text_to_cell(mob: Mobject, target_center: np.ndarray, run_t: float = 0.52):
            self.play(mob.animate.move_to(target_center), run_time=run_t)

        def heapify_down_visual(start: int):
            follow = start
            apply_circle_highlight(follow)
            self.wait(0.1)
            i = start
            sz = len(heap)
            while True:
                l = 2 * i + 1
                r = 2 * i + 2
                smallest = i
                if l < sz and heap[l] < heap[smallest]:
                    smallest = l
                if r < sz and heap[r] < heap[smallest]:
                    smallest = r
                if smallest == i:
                    break
                follow = swap_node_values(i, smallest, follow_idx=follow)
                i = follow

        while len(heap) > 0:
            sz = len(heap)
            min_val = heap[0]

            # 堆顶（最小值）飞到排序结果下一格 → 升序
            fly_copy = node_texts[0].copy()
            fly_copy.set_z_index(60)
            self.add(fly_copy)
            tgt = cell_center_row(y_res, result_fill)
            fly_text_to_cell(fly_copy, tgt, run_t=T_FLY_TO_RESULT)
            nt = Text(
                str(min_val), font_size=val_fs, color=WHITE_C, font="Consolas", disable_ligatures=True
            )
            nt.move_to(tgt)
            res_texts[result_fill] = nt
            self.remove(fly_copy)
            self.play(FadeIn(nt, scale=0.92), run_time=0.12)
            result_fill += 1
            self.wait(0.08)

            if sz == 1:
                # 最后一个：整颗根变红消失
                self.play(
                    node_circles[0].animate.set_stroke(RED_C),
                    node_texts[0].animate.set_color(RED_C),
                    run_time=T_DELETE_TO_RED,
                )
                self.play(
                    FadeOut(node_circles[0]),
                    FadeOut(node_texts[0]),
                    run_time=T_LAST_ROOT_FADE,
                )
                heap.clear()
                node_circles.clear()
                node_texts.clear()
                edge_lines.clear()
                break

            tail_idx = sz - 1
            tail_val = heap[tail_idx]

            # 堆尾数字飞到根（位置不动只换数字的视觉效果：尾字飞到根中心）
            tail_mob = node_texts[tail_idx].copy()
            tail_mob.set_z_index(55)
            self.add(tail_mob)
            root_c = node_circles[0].get_center()
            self.play(tail_mob.animate.move_to(root_c), run_time=T_TAIL_TO_ROOT)
            self.remove(tail_mob)
            heap[0] = tail_val
            self.remove(node_texts[0])
            node_texts[0] = Text(
                str(tail_val), font_size=28, color=WHITE_C, font="Consolas", disable_ligatures=True
            ).move_to(root_c)
            self.add(node_texts[0])

            # 删堆尾：节点与连边变红淡出
            self.play(
                node_circles[tail_idx].animate.set_stroke(RED_C),
                node_texts[tail_idx].animate.set_color(RED_C),
                edge_lines[tail_idx].animate.set_color(RED_C),
                run_time=T_DELETE_TO_RED,
            )
            self.play(
                FadeOut(node_circles[tail_idx]),
                FadeOut(node_texts[tail_idx]),
                FadeOut(edge_lines[tail_idx]),
                run_time=T_DELETE_FADEOUT,
            )

            # 逻辑删除尾结点：把 tail 的图挪走/字典更新
            node_circles.pop(tail_idx, None)
            node_texts.pop(tail_idx, None)
            edge_lines.pop(tail_idx, None)
            heap.pop()  # 去掉旧尾（值已在根）

            heapify_down_visual(0)
            normalize_heap_white()
            self.wait(0.1)

        self.wait(0.9)
