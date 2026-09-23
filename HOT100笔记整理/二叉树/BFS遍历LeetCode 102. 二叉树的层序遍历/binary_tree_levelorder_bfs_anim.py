# -*- coding: utf-8 -*-
"""
二叉树层序遍历（BFS）— Manim 教学动画

左侧层序表（一行一层，从左到右填入）；右侧横向大幅压缩的二叉树；黑底白线。
15 节点、14 边；黄：父 + 边 + 子；红框下移后整层清空。

默认 480p（854×480）；2560×1440：
  set BTREE_BFS_RES=1440p

渲染 480p:
  manim-env2\\Scripts\\python.exe -m manim binary_tree_levelorder_bfs_anim.py BinaryTreeLevelOrderBfsAnim -ql
"""

from __future__ import annotations

import os
from typing import Callable

import numpy as np
from manim import *
from manim.utils.rate_functions import smooth

_res = (os.environ.get("BTREE_BFS_RES") or "480p").strip().lower()
if _res in ("1440", "1440p", "2560", "q1440"):
    config.pixel_width = 2560
    config.pixel_height = 1440
elif _res in ("1080", "1080p", "fhd", "1920"):
    config.pixel_width = 1920
    config.pixel_height = 1080
else:
    config.pixel_width = 854
    config.pixel_height = 480
config.frame_rate = 30

YELLOW_HL = "#ffdd33"
RED_BOX = "#ff3333"


def _trim_segment(p0: np.ndarray, p1: np.ndarray, r: float) -> tuple[np.ndarray, np.ndarray]:
    d = p1[:2] - p0[:2]
    L = float(np.linalg.norm(d))
    if L < 1e-6:
        return p0.copy(), p1.copy()
    u = np.array([d[0] / L, d[1] / L, 0.0], dtype=float)
    a = p0 + u * r
    b = p1 - u * r
    return a, b


def _bbox_of_points(
    centers: list[np.ndarray], r: float, pad: float
) -> tuple[float, float, float, float]:
    xs = [float(p[0]) for p in centers]
    ys = [float(p[1]) for p in centers]
    return min(xs) - r - pad, max(xs) + r + pad, min(ys) - r - pad, max(ys) + r + pad


def _rect_from_bbox(x0: float, x1: float, y0: float, y1: float) -> Rectangle:
    w = max(x1 - x0, 0.15)
    h = max(y1 - y0, 0.15)
    cx = 0.5 * (x0 + x1)
    cy = 0.5 * (y0 + y1)
    r = Rectangle(width=w, height=h, color=RED_BOX, stroke_width=3.2, fill_opacity=0)
    r.move_to(np.array([cx, cy, 0.0]))
    return r


def _build_parent_and_side(
    directed_edges: list[tuple[int, int]],
    children: dict[int, list[int]],
) -> tuple[dict[int, int], dict[int, bool]]:
    """
    parent[v]=u；is_left_child[v]：v 相对父 u 的几何侧（双子取较小编号为左；
    单子：若父在整棵树里是「左链」则子也画在父左侧，否则画在右侧）。
    """
    parent: dict[int, int] = {}
    is_left_child: dict[int, bool] = {}
    for u, v in directed_edges:
        parent[v] = u

    is_left_child[2] = True
    is_left_child[3] = False

    for u in range(1, 16):
        ch = children.get(u, [])
        if not ch:
            continue
        if len(ch) == 2:
            a, b = ch[0], ch[1]
            is_left_child[a] = True
            is_left_child[b] = False
        else:
            v = ch[0]
            is_left_child[v] = is_left_child[u]
    return parent, is_left_child


def _binary_tree_x_layout(
    u: int,
    children: dict[int, list[int]],
    is_left_child: dict[int, bool],
    sibling_gap: float,
    sibling_gap_root: float,
    single_side_pad: float,
) -> tuple[float, float, dict[int, float]]:
    """
    左子整棵子树在父左侧、右子在右侧；单子按 is_left_child[父] 决定画在父左下或右下。
    返回 (min_x, max_x, {节点: x})，子树内坐标相对任意原点，最后整体平移到居中。
    """
    ch = children.get(u, [])

    def merge_shift(d: dict[int, float], dx: float) -> dict[int, float]:
        return {k: v + dx for k, v in d.items()}

    if not ch:
        return -0.5, 0.5, {u: 0.0}

    if len(ch) == 1:
        v = ch[0]
        L, R, sub = _binary_tree_x_layout(
            v, children, is_left_child, sibling_gap, sibling_gap_root, single_side_pad
        )
        dv = -sub[v]
        sub2 = merge_shift(sub, dv)
        L2, R2 = L + dv, R + dv
        if is_left_child[v]:
            # 左下：子 x < 父 x，父放在子树最右端外侧
            x_parent = R2 + single_side_pad
        else:
            # 右下：子 x > 父 x，父放在子树最左端外侧
            x_parent = L2 - single_side_pad
        sub2[u] = x_parent
        return min(L2, x_parent - 0.5), max(R2, x_parent + 0.5), sub2

    vL, vR = ch[0], ch[1]
    L0, R0, subL = _binary_tree_x_layout(
        vL, children, is_left_child, sibling_gap, sibling_gap_root, single_side_pad
    )
    L1, R1, subR = _binary_tree_x_layout(
        vR, children, is_left_child, sibling_gap, sibling_gap_root, single_side_pad
    )
    gap_here = sibling_gap_root if u == 1 else sibling_gap
    # 右子树整体右移，使与左子树间隔为 gap_here（根处更小 → 1→2 与 1→3 夹角更窄）
    shift_r = R0 + gap_here - L1
    subR2 = merge_shift(subR, shift_r)
    L1b, R1b = L1 + shift_r, R1 + shift_r
    merged = {**subL, **subR2}
    xu = 0.5 * (merged[vL] + merged[vR])
    merged[u] = xu
    return min(L0, L1b, xu - 0.5), max(R0, R1b, xu + 0.5), merged


class BinaryTreeLevelOrderBfsAnim(Scene):
    def construct(self) -> None:
        self.camera.background_color = BLACK

        # 有向树边（同时用于无向图绘制与 BFS）
        directed_edges = [
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 5),
            (3, 6),
            (3, 7),
            (4, 8),
            (5, 9),
            (5, 10),
            (6, 11),
            (7, 12),
            (8, 13),
            (10, 14),
            (12, 15),
        ]
        edges_uv = list(directed_edges)

        n = 16
        graph: list[list[int]] = [[] for _ in range(n)]
        for u, v in edges_uv:
            graph[u].append(v)
            graph[v].append(u)
        for i in range(n):
            graph[i].sort()

        children: dict[int, list[int]] = {i: [] for i in range(1, n)}
        for u, v in directed_edges:
            children[u].append(v)
        for k in list(children.keys()):
            children[k].sort()

        _parent, is_left_child = _build_parent_and_side(directed_edges, children)
        del _parent  # 布局仅用 is_left_child

        # 二叉树几何：双子女左右排布；单子随父在整棵树的左/右身份偏左下或右下
        # 大幅压缩水平方向，使左右连边夹角更小（为右侧栏腾空间）
        sibling_gap = 0.2
        sibling_gap_root = 0.055
        single_side_pad = 0.22
        _mn, _mx, x_rel = _binary_tree_x_layout(
            1, children, is_left_child, sibling_gap, sibling_gap_root, single_side_pad
        )
        all_ids = sorted(x_rel.keys())
        cx_tree = 0.5 * (min(x_rel.values()) + max(x_rel.values()))
        for i in all_ids:
            x_rel[i] -= cx_tree

        depth: dict[int, int] = {}
        dq = [1]
        depth[1] = 0
        while dq:
            u = dq.pop(0)
            for v in children.get(u, []):
                if v not in depth:
                    depth[v] = depth[u] + 1
                    dq.append(v)

        vert_step = 0.88
        y_top = 2.45
        pos: dict[int, np.ndarray] = {}
        for i in all_ids:
            y = y_top - depth[i] * vert_step
            pos[i] = np.array([x_rel[i], y, 0.0], dtype=float)

        # 整体缩放 + 仅横向再压缩（树更「窄」）
        GRAPH_SCL = 1.02
        X_COMPRESS = 0.52
        _xs = [pos[i][0] for i in all_ids]
        _ys = [pos[i][1] for i in all_ids]
        _cx = 0.5 * (min(_xs) + max(_xs))
        _cy = 0.5 * (min(_ys) + max(_ys))
        for i in all_ids:
            px = (pos[i][0] - _cx) * GRAPH_SCL * X_COMPRESS
            py = (pos[i][1] - _cy) * GRAPH_SCL
            pos[i] = np.array([px, py, 0.0], dtype=float)

        # 整棵树移到画面右侧
        TREE_X_SHIFT = 2.85
        for i in all_ids:
            pos[i] = pos[i] + np.array([TREE_X_SHIFT, 0.0, 0.0])

        NODE_R = 0.22
        z_edge = 1
        z_node = 3
        z_box = 4

        edge_lines: dict[tuple[int, int], Line] = {}
        for u, v in edges_uv:
            a, b = (min(u, v), max(u, v))
            p0, p1 = _trim_segment(pos[u], pos[v], NODE_R + 0.035)
            edge_lines[(a, b)] = Line(p0, p1, color=WHITE, stroke_width=2.85, z_index=z_edge)

        FS_NUM = 24
        nodes: dict[int, VGroup] = {}
        for i in range(1, n):
            if i not in pos:
                continue
            c = Circle(
                radius=NODE_R,
                color=WHITE,
                stroke_width=2.85,
                fill_opacity=0,
                z_index=z_node,
            )
            lab = Text(str(i), font_size=FS_NUM, color=WHITE, font="Arial", disable_ligatures=True)
            lab.move_to(c.get_center())
            g = VGroup(c, lab).move_to(pos[i])
            g.set_z_index(z_node)
            g.disc = c  # type: ignore[attr-defined]
            g.label = lab  # type: ignore[attr-defined]
            nodes[i] = g

        upper = VGroup(*edge_lines.values(), *nodes.values())
        self.add(upper)

        # BFS 层（本树共 5 层 → 左侧表 5 行）
        layers: list[list[int]] = []
        q = [1]
        seen = {1}
        while q:
            layers.append(list(q))
            nq: list[int] = []
            for u in q:
                for v in graph[u]:
                    if v not in seen:
                        seen.add(v)
                        nq.append(v)
            nq.sort()
            q = nq

        n_rows = len(layers)
        z_table = 0

        # ---------- 左侧层序表（行 = BFS 层，从左到右填格）----------
        row_anchor_left = -5.92
        row_width = 2.52
        TABLE_TOP_Y = 1.88
        ROW_STEP_Y = 0.86
        row_y = [TABLE_TOP_Y - ri * ROW_STEP_Y for ri in range(n_rows)]
        row_cell_count = [0] * n_rows

        CELL_W = 0.33
        CELL_H = 0.3
        CELL_GAP = 0.038
        FS_CELL = 19

        table_skeleton = VGroup()
        for ri in range(n_rows):
            guide = RoundedRectangle(
                width=row_width,
                height=CELL_H + 0.06,
                corner_radius=0.06,
                color=WHITE,
                stroke_width=1.35,
                stroke_opacity=0.32,
                fill_opacity=0,
            )
            guide.move_to(np.array([row_anchor_left + row_width * 0.5, row_y[ri], 0.0]))
            guide.set_z_index(z_table)
            table_skeleton.add(guide)
        self.add(table_skeleton)

        def make_table_cell(val: int) -> VGroup:
            box = RoundedRectangle(
                width=CELL_W,
                height=CELL_H,
                corner_radius=0.05,
                color=WHITE,
                stroke_width=1.85,
                fill_opacity=0,
            )
            t = Text(str(val), font_size=FS_CELL, color=WHITE, font="Arial", disable_ligatures=True)
            t.move_to(box.get_center())
            g = VGroup(box, t)
            g.set_z_index(z_table + 1)
            return g

        def add_table_cell(row_idx: int, val: int) -> VGroup:
            i = row_cell_count[row_idx]
            row_cell_count[row_idx] += 1
            cx = row_anchor_left + CELL_W * 0.5 + i * (CELL_W + CELL_GAP)
            cell = make_table_cell(val)
            cell.move_to(np.array([cx, row_y[row_idx], 0.0]))
            return cell

        slow = 1.32
        t_short = 0.3 * slow
        t_move = 0.92 * slow
        t_edge_grow = 1.42 * slow  # 黄线延伸更慢、更顺
        t_node = 0.62 * slow  # 节点变黄动画时长
        t_reset = 0.52 * slow  # 整层清空时略慢于瞬时
        gap = max(0.82 / float(config.frame_rate), 0.055 * slow)

        def set_node_outline(node: int, color: str, w: float = 2.82) -> None:
            nodes[node].disc.set_stroke(color=color, width=w)  # type: ignore[union-attr]

        def set_node_label_color(node: int, color: str) -> None:
            nodes[node].label.set_color(color)  # type: ignore[union-attr]

        def set_edge_color(u: int, v: int, color: str, w: float = 2.65) -> None:
            a, b = (min(u, v), max(u, v))
            edge_lines[(a, b)].set_stroke(color=color, width=w)

        def _edge_endpoints_for_dir(cur: int, nxt: int) -> tuple[np.ndarray, np.ndarray]:
            a, b = (min(cur, nxt), max(cur, nxt))
            ps = np.array(edge_lines[(a, b)].get_start(), dtype=float)
            pe = np.array(edge_lines[(a, b)].get_end(), dtype=float)
            if float(np.linalg.norm(ps - pos[cur])) <= float(np.linalg.norm(pe - pos[cur])):
                return ps, pe
            return pe, ps

        def play_parallel_edge_grows_yellow(pairs: list[tuple[int, int]]) -> None:
            if not pairs:
                return
            grows: list[Line] = []
            updaters: list[Animation] = []
            edge_w = 3.45

            for cur, nxt in pairs:
                p_s, p_e = _edge_endpoints_for_dir(cur, nxt)
                grow = Line(
                    p_s,
                    p_s,
                    color=YELLOW_HL,
                    stroke_width=edge_w,
                    z_index=z_edge + 3,
                )
                self.add(grow)
                grows.append(grow)

                def make_upd(ps: np.ndarray, pe: np.ndarray, m: Line) -> Callable[[Line, float], None]:
                    def _upd(__: Line, a: float) -> None:
                        aa = max(float(a), 1e-4)
                        m.put_start_and_end_on(ps, ps + (pe - ps) * aa)

                    return _upd

                updaters.append(UpdateFromAlphaFunc(grow, make_upd(p_s, p_e, grow)))

            self.play(*updaters, run_time=t_edge_grow, rate_func=smooth)
            for grow in grows:
                self.remove(grow)
            for cur, nxt in pairs:
                set_edge_color(cur, nxt, YELLOW_HL, 3.32)

        def layer_bbox_rect(nodes_in_layer: list[int], pad: float = 0.16) -> Rectangle:
            centers = [pos[i] for i in nodes_in_layer]
            x0, x1, y0, y1 = _bbox_of_points(centers, NODE_R, pad)
            return _rect_from_bbox(x0, x1, y0, y1)

        pad_box = 0.18
        layer_rects = [layer_bbox_rect(L, pad_box) for L in layers]

        self.wait(0.36 * slow)
        cur_box = layer_rects[0].copy().set_z_index(z_box)
        self.add(cur_box)

        def play_nodes_yellow(node_ids: list[int], *extra_anims: object) -> None:
            anims: list = []
            for nid in node_ids:
                anims.append(nodes[nid].disc.animate.set_stroke(color=YELLOW_HL, width=3.15))
                anims.append(nodes[nid].label.animate.set_color(YELLOW_HL))
            all_anims = [*anims, *extra_anims]
            if all_anims:
                self.play(*all_anims, run_time=t_node, rate_func=smooth)

        def sync_reset_all_yellow(
            node_set: set[int],
            edge_set: set[tuple[int, int]],
        ) -> None:
            anims: list = []
            for nn in node_set:
                anims.append(nodes[nn].disc.animate.set_stroke(color=WHITE, width=2.82))
                anims.append(nodes[nn].label.animate.set_color(WHITE))
            for a, b in edge_set:
                anims.append(edge_lines[(a, b)].animate.set_stroke(color=WHITE, width=2.65))
            if anims:
                self.play(*anims, run_time=t_reset, rate_func=smooth)

        # ---------- 按层 BFS：整层累积黄色，红框移到下一层后一次清空 ----------
        for li, layer in enumerate(layers):
            yellow_nodes: set[int] = set()
            yellow_edges: set[tuple[int, int]] = set()

            for u in sorted(layer):
                # 表格：仅根 1 在「第一次访问」时写入第 0 行；其余点在「从父边扩展发现」时写入 depth 行
                if li == 0 and u == 1:
                    tc0 = add_table_cell(0, 1)
                    self.add(tc0)
                    play_nodes_yellow([1], FadeIn(tc0, scale=0.88, shift=0.05 * UP))
                else:
                    play_nodes_yellow([u])
                yellow_nodes.add(u)
                self.wait(t_short * 0.38)

                ch = children.get(u, [])
                pairs = [(u, v) for v in ch]
                if pairs:
                    play_parallel_edge_grows_yellow(pairs)
                    child_ids = [v for _, v in pairs]
                    for v in child_ids:
                        yellow_nodes.add(v)
                        yellow_edges.add((min(u, v), max(u, v)))
                    tcs: list = []
                    for v in child_ids:
                        tc = add_table_cell(depth[v], v)
                        self.add(tc)
                        tcs.append(tc)
                    play_nodes_yellow(
                        child_ids,
                        *[FadeIn(t, scale=0.88, shift=0.05 * UP) for t in tcs],
                    )
                    self.wait(gap * 1.0)
                else:
                    self.wait(t_short * 0.38)

            if li + 1 < len(layers):
                self.play(
                    Transform(cur_box, layer_rects[li + 1]),
                    run_time=t_move,
                    rate_func=smooth,
                )
                self.wait(gap * 0.5)
                sync_reset_all_yellow(yellow_nodes, yellow_edges)
                self.wait(t_short * 0.38)
            else:
                self.wait(gap * 0.75)
                sync_reset_all_yellow(yellow_nodes, yellow_edges)

        self.wait(0.48 * slow)
