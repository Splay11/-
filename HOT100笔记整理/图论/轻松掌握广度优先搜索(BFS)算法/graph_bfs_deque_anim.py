# -*- coding: utf-8 -*-
"""
无向图单源最短路（BFS 按层扩展）— Manim 演示

中层队列与下层 vis 已移除；图置于画面中央。
节点圆内不显示编号，按层写入最短路距离（0,1,2,...）。
每一层：从当前前沿同时连向**所有**邻点。未访问：橙边橙点，写入距离+1；已访问：红边红点（如回到更浅层），**不**改该点已有数值。然后统一恢复白边白框。

画布 16:9；默认 480p。可用环境变量 `GRAPH_BFS_RES=1440p` 切 2560×1440。

渲染 480p:
  manim-env2\\Scripts\\python.exe -m manim graph_bfs_deque_anim.py GraphBfsDequeAnim -ql
"""

from __future__ import annotations

import os
from typing import Callable

import numpy as np
from manim import *
from manim.utils.rate_functions import smooth

_res = (os.environ.get("GRAPH_BFS_RES") or "480p").strip().lower()
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

ORANGE = "#ff8800"
RED_HL = "#ff3333"


def _trim_segment(p0: np.ndarray, p1: np.ndarray, r: float) -> tuple[np.ndarray, np.ndarray]:
    d = p1[:2] - p0[:2]
    L = float(np.linalg.norm(d))
    if L < 1e-6:
        return p0.copy(), p1.copy()
    u = np.array([d[0] / L, d[1] / L, 0.0], dtype=float)
    a = p0 + u * r
    b = p1 - u * r
    return a, b


class GraphBfsDequeAnim(Scene):
    def construct(self) -> None:
        self.camera.background_color = BLACK

        n = 10
        edges = [
            (0, 1),
            (0, 2),
            (1, 2),
            (1, 4),
            (1, 3),
            (3, 5),
            (5, 6),
            (5, 7),
            (5, 8),
            (7, 8),
            (8, 9),
        ]
        graph: list[list[int]] = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        for i in range(n):
            graph[i].sort()

        # ---------- 图布局：居中 ----------
        GRAPH_SCL = 0.85
        _raw = {
            0: (-6.0, 0.0),
            1: (-4.0, 1.5),
            2: (-4.0, -1.5),
            4: (-2.0, 1.5),
            3: (-2.0, 0.0),
            5: (0.5, 0.0),
            8: (2.5, 1.5),
            6: (-0.5, -1.5),
            7: (2.5, -1.5),
            9: (4.5, 1.5),
        }
        _rxs = [p[0] for p in _raw.values()]
        _rys = [p[1] for p in _raw.values()]
        _gcx = 0.5 * (min(_rxs) + max(_rxs))
        _gcy = 0.5 * (min(_rys) + max(_rys))
        pos = {
            i: np.array(
                [
                    _gcx + (_raw[i][0] - _gcx) * GRAPH_SCL,
                    _gcy + (_raw[i][1] - _gcy) * GRAPH_SCL,
                    0.0,
                ],
                dtype=float,
            )
            for i in range(n)
        }
        NODE_R = 0.24 * GRAPH_SCL

        z_graph = 2
        z_edge = 1
        z_node = 3

        edge_lines: dict[tuple[int, int], Line] = {}
        for u, v in edges:
            a, b = (min(u, v), max(u, v))
            p0, p1 = _trim_segment(pos[u], pos[v], NODE_R + 0.04)
            ln = Line(p0, p1, color=WHITE, stroke_width=2.6, z_index=z_edge)
            edge_lines[(a, b)] = ln

        FS_DIST = 30
        nodes: dict[int, VGroup] = {}
        dist_labels: dict[int, Text] = {}
        for i in range(n):
            c = Circle(
                radius=NODE_R,
                color=WHITE,
                stroke_width=2.6,
                fill_opacity=0,
                z_index=z_node,
            )
            lab = Text("", font_size=FS_DIST, color=WHITE, font="Arial", disable_ligatures=True)
            lab.move_to(c.get_center())
            g = VGroup(c, lab).move_to(pos[i])
            g.set_z_index(z_node)
            g.disc = c  # type: ignore[attr-defined]
            g.label = lab  # type: ignore[attr-defined]
            nodes[i] = g
            dist_labels[i] = lab

        upper = VGroup(*edge_lines.values(), *nodes.values())
        upper.set_z_index(z_graph)
        self.add(upper)

        slow = 1.45
        t_short = 0.28 * slow
        t_move = 0.85 * slow
        t_edge_grow = 0.78 * slow
        gap = max(0.9 / float(config.frame_rate), 0.05 * slow)

        def set_node_outline(node: int, color: str, w: float = 2.8) -> None:
            nodes[node].disc.set_stroke(color=color, width=w)  # type: ignore[union-attr]

        def set_edge_color(u: int, v: int, color: str, w: float = 2.6) -> None:
            a, b = (min(u, v), max(u, v))
            edge_lines[(a, b)].set_stroke(color=color, width=w)

        def _edge_endpoints_for_dir(cur: int, nxt: int) -> tuple[np.ndarray, np.ndarray]:
            a, b = (min(cur, nxt), max(cur, nxt))
            ps = np.array(edge_lines[(a, b)].get_start(), dtype=float)
            pe = np.array(edge_lines[(a, b)].get_end(), dtype=float)
            if float(np.linalg.norm(ps - pos[cur])) <= float(np.linalg.norm(pe - pos[cur])):
                return ps, pe
            return pe, ps

        def play_parallel_edge_grows_colored(pairs: list[tuple[int, int, str]]) -> None:
            """pairs: (u,v,color)，u 为当前前沿上的端点，用于决定生长方向。"""
            if not pairs:
                return
            grows: list[Line] = []
            updaters: list[Animation] = []
            edge_w = 3.45

            for cur, nxt, col in pairs:
                p_s, p_e = _edge_endpoints_for_dir(cur, nxt)
                grow = Line(
                    p_s,
                    p_s,
                    color=col,
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
            for cur, nxt, col in pairs:
                set_edge_color(cur, nxt, col, 3.35 if col == ORANGE else 3.4)

        def set_dist_text(i: int, val: int) -> None:
            nt = Text(str(val), font_size=FS_DIST, color=WHITE, font="Arial", disable_ligatures=True)
            nt.move_to(nodes[i].disc.get_center())  # type: ignore[union-attr]
            dist_labels[i].become(nt)

        def reset_wave_colors(
            orange_pairs: list[tuple[int, int]],
            red_pairs: list[tuple[int, int]],
            new_vertices: list[int],
            red_vertices: list[int],
        ) -> None:
            for u, v in orange_pairs:
                set_edge_color(u, v, WHITE, 2.6)
            for u, v in red_pairs:
                set_edge_color(u, v, WHITE, 2.6)
            for v in set(new_vertices) | set(red_vertices):
                set_node_outline(v, WHITE, 2.8)

        def collect_frontier_wave(
            frontier: list[int], dist_arr: list[int]
        ) -> tuple[list[tuple[int, int]], list[tuple[int, int]], list[int]]:
            """
            从当前前沿同时看向所有邻点。
            - 未访问 v：橙边方向 (u,v)，每条无向边本层只播一次；new_vs 为首次到达的顶点。
            - 已访问 v：红边「回指」已遍历过的点，每条无向边本层只播一次；不修改 dist。
            """
            seen_o: set[tuple[int, int]] = set()
            orange_dir: list[tuple[int, int]] = []
            new_vs: list[int] = []
            seen_v_new: set[int] = set()

            seen_r: set[tuple[int, int]] = set()
            red_dir: list[tuple[int, int]] = []

            for u in frontier:
                for v in graph[u]:
                    a, b = (min(u, v), max(u, v))
                    if dist_arr[v] == -1:
                        if (a, b) in seen_o:
                            continue
                        seen_o.add((a, b))
                        orange_dir.append((u, v))
                        if v not in seen_v_new:
                            seen_v_new.add(v)
                            new_vs.append(v)
                    else:
                        if (a, b) in seen_r:
                            continue
                        seen_r.add((a, b))
                        red_dir.append((u, v))
            return orange_dir, red_dir, new_vs

        # ---------- 单源最短路：从最左端点 0 开始，按层同步扩展 ----------
        start = 0
        dist_arr = [-1] * n
        dist_arr[start] = 0

        set_node_outline(start, ORANGE, 3.2)
        self.wait(t_short)
        set_dist_text(start, 0)
        self.wait(gap)
        set_node_outline(start, WHITE, 2.8)
        self.wait(t_short * 0.6)

        frontier = [start]
        while frontier:
            orange_pairs, red_pairs, new_vertices = collect_frontier_wave(frontier, dist_arr)
            if not orange_pairs and not red_pairs:
                break

            colored: list[tuple[int, int, str]] = [(u, v, ORANGE) for u, v in orange_pairs] + [
                (u, v, RED_HL) for u, v in red_pairs
            ]
            play_parallel_edge_grows_colored(colored)

            red_verts = list({v for _, v in red_pairs})
            anims_nodes: list = []
            for v in new_vertices:
                anims_nodes.append(nodes[v].disc.animate.set_stroke(color=ORANGE, width=3.2))
            for v in red_verts:
                anims_nodes.append(nodes[v].disc.animate.set_stroke(color=RED_HL, width=3.2))
            if anims_nodes:
                self.play(*anims_nodes, run_time=t_move * 0.55, rate_func=smooth)
            else:
                for v in new_vertices:
                    set_node_outline(v, ORANGE, 3.2)
                for v in red_verts:
                    set_node_outline(v, RED_HL, 3.2)
            self.wait(0.18 * slow)

            if new_vertices:
                d_next = dist_arr[frontier[0]] + 1
                for v in new_vertices:
                    dist_arr[v] = d_next
                    set_dist_text(v, d_next)
                self.wait(gap)

            reset_wave_colors(orange_pairs, red_pairs, new_vertices, red_verts)
            self.wait(0.14 * slow)

            frontier = new_vertices

        self.wait(0.55 * slow)
