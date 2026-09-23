# -*- coding: utf-8 -*-
"""
二叉树层序遍历（BFS）— 距根距离标注版

在 binary_tree_levelorder_bfs_anim 基础上：去掉右侧红框；每次遍历到节点时，
在其左上（左子链）或右上（右子链）标注该点到 1 的最短距离（层数）；左侧表格与黄高亮逻辑不变。

左侧表格：按需逐行出现；每行左侧标注深度 0–4；子扩展先左后右串行。
默认 480p：
  manim-env2\\Scripts\\python.exe -m manim binary_tree_levelorder_bfs_dist_anim.py BinaryTreeLevelOrderBfsDistAnim -ql
1080p：
  set BTREE_BFS_RES=1080p 后 -qh
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


def _trim_segment(p0: np.ndarray, p1: np.ndarray, r: float) -> tuple[np.ndarray, np.ndarray]:
    d = p1[:2] - p0[:2]
    L = float(np.linalg.norm(d))
    if L < 1e-6:
        return p0.copy(), p1.copy()
    u = np.array([d[0] / L, d[1] / L, 0.0], dtype=float)
    a = p0 + u * r
    b = p1 - u * r
    return a, b


def _build_parent_and_side(
    directed_edges: list[tuple[int, int]],
    children: dict[int, list[int]],
) -> tuple[dict[int, int], dict[int, bool]]:
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
            x_parent = R2 + single_side_pad
        else:
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
    shift_r = R0 + gap_here - L1
    subR2 = merge_shift(subR, shift_r)
    L1b, R1b = L1 + shift_r, R1 + shift_r
    merged = {**subL, **subR2}
    xu = 0.5 * (merged[vL] + merged[vR])
    merged[u] = xu
    return min(L0, L1b, xu - 0.5), max(R0, R1b, xu + 0.5), merged


class BinaryTreeLevelOrderBfsDistAnim(Scene):
    def construct(self) -> None:
        self.camera.background_color = BLACK

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
        del _parent

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

        TREE_X_SHIFT = 2.85
        for i in all_ids:
            pos[i] = pos[i] + np.array([TREE_X_SHIFT, 0.0, 0.0])

        NODE_R = 0.22
        z_edge = 1
        z_node = 3
        z_dist = 5

        edge_lines: dict[tuple[int, int], Line] = {}
        for u, v in edges_uv:
            a, b = (min(u, v), max(u, v))
            p0, p1 = _trim_segment(pos[u], pos[v], NODE_R + 0.035)
            edge_lines[(a, b)] = Line(p0, p1, color=WHITE, stroke_width=2.85, z_index=z_edge)

        FS_NUM = 24
        FS_DIST = 17
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

        def make_dist_label(v: int) -> Text:
            dtxt = str(depth[v])
            t = Text(dtxt, font_size=FS_DIST, color=WHITE, font="Arial", disable_ligatures=True)
            t.set_z_index(z_dist)
            pc = pos[v]
            if v == 1:
                t.move_to(pc + np.array([0.0, NODE_R + 0.16, 0.0]))
            elif is_left_child[v]:
                t.move_to(pc + np.array([-NODE_R - 0.1, NODE_R + 0.12, 0.0]))
            else:
                t.move_to(pc + np.array([NODE_R + 0.1, NODE_R + 0.12, 0.0]))
            return t

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

        z_table = 0

        row_anchor_left = -5.92
        row_width = 2.52
        TABLE_TOP_Y = 1.88
        ROW_STEP_Y = 0.86

        CELL_W = 0.33
        CELL_H = 0.3
        CELL_GAP = 0.038
        FS_CELL = 19

        created_table_rows: set[int] = set()
        row_cell_count: dict[int, int] = {}

        def row_y_pos(row_idx: int) -> float:
            return TABLE_TOP_Y - row_idx * ROW_STEP_Y

        def ensure_table_row(row_idx: int) -> list:
            """首次使用该深度行时：左侧深度号 + 长条，与该行对齐。"""
            if row_idx in created_table_rows:
                return []
            created_table_rows.add(row_idx)
            y = row_y_pos(row_idx)
            strip_cx = row_anchor_left + row_width * 0.5
            guide = RoundedRectangle(
                width=row_width,
                height=CELL_H + 0.06,
                corner_radius=0.06,
                color=WHITE,
                stroke_width=1.35,
                stroke_opacity=0.32,
                fill_opacity=0,
            )
            guide.move_to(np.array([strip_cx, y, 0.0]))
            guide.set_z_index(z_table)
            depth_txt = Text(
                str(row_idx),
                font_size=FS_CELL + 2,
                color=WHITE,
                font="Arial",
                disable_ligatures=True,
            )
            depth_txt.move_to(np.array([row_anchor_left - 0.42, y, 0.0]))
            depth_txt.set_z_index(z_table + 1)
            self.add(guide, depth_txt)
            return [FadeIn(guide), FadeIn(depth_txt)]

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

        def add_table_cell(row_idx: int, val: int) -> tuple[VGroup, list]:
            row_anims = ensure_table_row(row_idx)
            i = row_cell_count.get(row_idx, 0)
            row_cell_count[row_idx] = i + 1
            cx = row_anchor_left + CELL_W * 0.5 + i * (CELL_W + CELL_GAP)
            cell = make_table_cell(val)
            cell.move_to(np.array([cx, row_y_pos(row_idx), 0.0]))
            return cell, row_anims

        slow = 1.32
        t_short = 0.3 * slow
        t_edge_grow = 1.42 * slow
        t_node = 0.62 * slow
        t_reset = 0.52 * slow
        gap = max(0.82 / float(config.frame_rate), 0.055 * slow)

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

        self.wait(0.36 * slow)

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

        for li, layer in enumerate(layers):
            yellow_nodes: set[int] = set()
            yellow_edges: set[tuple[int, int]] = set()

            for u in sorted(layer):
                if li == 0 and u == 1:
                    tc0, row0_anims = add_table_cell(0, 1)
                    dist1 = make_dist_label(1)
                    self.add(tc0)
                    self.add(dist1)
                    play_nodes_yellow(
                        [1],
                        *row0_anims,
                        FadeIn(tc0, scale=0.88, shift=0.05 * UP),
                        FadeIn(dist1, scale=0.88, shift=0.05 * UP),
                    )
                else:
                    du = make_dist_label(u)
                    self.add(du)
                    play_nodes_yellow([u], FadeIn(du, scale=0.88, shift=0.05 * UP))
                yellow_nodes.add(u)
                self.wait(t_short * 0.38)

                ch = children.get(u, [])
                if ch:
                    for v in ch:
                        play_parallel_edge_grows_yellow([(u, v)])
                        yellow_nodes.add(v)
                        yellow_edges.add((min(u, v), max(u, v)))
                        tc, row_anims = add_table_cell(depth[v], v)
                        self.add(tc)
                        dm = make_dist_label(v)
                        self.add(dm)
                        play_nodes_yellow(
                            [v],
                            *row_anims,
                            FadeIn(tc, scale=0.88, shift=0.05 * UP),
                            FadeIn(dm, scale=0.88, shift=0.05 * UP),
                        )
                        self.wait(gap * 0.55)
                    self.wait(gap * 0.45)
                else:
                    self.wait(t_short * 0.38)

            if li + 1 < len(layers):
                self.wait(gap * 0.5)
                sync_reset_all_yellow(yellow_nodes, yellow_edges)
                self.wait(t_short * 0.38)
            else:
                self.wait(gap * 0.75)
                sync_reset_all_yellow(yellow_nodes, yellow_edges)

        self.wait(0.48 * slow)
