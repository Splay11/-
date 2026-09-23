# -*- coding: utf-8 -*-
"""
矩阵 → 网格图（四邻且均为 1 才有边）→ 逐行扫描 + 未访问 1 上 BFS 染色连通块；
遇 0 或已访问 1：边框红光闪烁 + 上方红叉。右侧每个格子都有顶点圆（与 1 同大），0 格圆心黑点区分。
矩阵淡出后，从扫描第一格那一帧起上方显示计数（从 0 起）；每遍历完一个连通块即更新计数。
末尾三个连通块依次整体闪烁（计数已在扫描阶段更新完毕）。

渲染 480p（默认 854×480）:
  set MATRIX_GRID_BFS_RES=480p
  manim-env2\\Scripts\\python.exe -m manim matrix_grid_bfs_islands_anim.py MatrixGridBfsIslandsAnim -ql
"""

from __future__ import annotations

import os
from collections import deque

import numpy as np
from manim import *
from manim.utils.rate_functions import smooth

_res = (os.environ.get("MATRIX_GRID_BFS_RES") or "480p").strip().lower()
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

GREEN_HL = "#22dd55"
RED_HL = "#ff3333"
EDGE_COL = "#aaaaaa"
NODE_IDLE = "#666666"


def _cell_pos(r: int, c: int, rows: int, cols: int, cell: float) -> np.ndarray:
    """矩阵 (r,c) 中心；r 向下为正，画面 y 向上为正。"""
    x = (c - (cols - 1) / 2.0) * cell
    y = -((r - (rows - 1) / 2.0)) * cell
    return np.array([x, y, 0.0], dtype=float)


class MatrixGridBfsIslandsAnim(Scene):
    def construct(self) -> None:
        self.camera.background_color = BLACK

        rows, cols = 4, 5
        grid = [
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 1],
        ]

        CELL = 0.62
        NODE_R = 0.22
        ZERO_DOT_R = 0.055
        STROKE = 2.6
        slow = 1.35
        t_smooth = 1.05 * slow
        t_short = 0.22 * slow
        gap = max(0.08, 0.05 * slow)

        def pos(r: int, c: int) -> np.ndarray:
            return _cell_pos(r, c, rows, cols, CELL)

        # ---------- 邻接（四邻且均为 1） ----------
        ones: set[tuple[int, int]] = {(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1}
        nbr4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adj: dict[tuple[int, int], list[tuple[int, int]]] = {p: [] for p in ones}
        edges_list: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for r, c in ones:
            for dr, dc in nbr4:
                nr, nc = r + dr, c + dc
                if (nr, nc) in ones:
                    adj[(r, c)].append((nr, nc))
                    if (r, c) < (nr, nc):
                        edges_list.append(((r, c), (nr, nc)))
        for p in ones:
            adj[p].sort(key=lambda x: (x[0], x[1]))

        # ---------- 矩阵展示（数字 + 细边框） ----------
        matrix_cells: dict[tuple[int, int], VGroup] = {}
        matrix_group = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(
                    side_length=CELL * 0.92,
                    color=WHITE,
                    stroke_width=STROKE * 0.85,
                    fill_opacity=0,
                )
                v = grid[r][c]
                t = Text(str(v), font_size=34, color=WHITE, font="Arial", disable_ligatures=True)
                g = VGroup(sq, t).move_to(pos(r, c))
                g.sq = sq  # type: ignore[attr-defined]
                g.txt = t  # type: ignore[attr-defined]
                matrix_cells[(r, c)] = g
                matrix_group.add(g)
        matrix_group.move_to(ORIGIN)

        # ---------- 图：底格（扫描用）+ 边 + 顶点 ----------
        cell_under: dict[tuple[int, int], Square] = {}
        under = VGroup()
        for r in range(rows):
            for c in range(cols):
                s = Square(
                    side_length=CELL * 0.95,
                    color=NODE_IDLE,
                    stroke_width=1.2,
                    stroke_opacity=0.35,
                    fill_opacity=0,
                )
                s.move_to(pos(r, c))
                cell_under[(r, c)] = s
                under.add(s)

        edge_mobs: dict[tuple[tuple[int, int], tuple[int, int]], Line] = {}
        lines_g = VGroup()
        for a, b in edges_list:
            p0, p1 = pos(*a), pos(*b)
            d = p1 - p0
            L = float(np.linalg.norm(d[:2]))
            if L < 1e-6:
                continue
            u = d / L
            q0 = p0 + u * NODE_R
            q1 = p1 - u * NODE_R
            ln = Line(q0, q1, color=EDGE_COL, stroke_width=2.4, stroke_opacity=0)
            key = (a, b)
            edge_mobs[key] = ln
            lines_g.add(ln)

        nodes: dict[tuple[int, int], VGroup] = {}
        nodes_g = VGroup()
        for r in range(rows):
            for c in range(cols):
                disc = Circle(
                    radius=NODE_R,
                    color=WHITE,
                    stroke_width=STROKE,
                    fill_opacity=0,
                )
                if grid[r][c] == 0:
                    # 纯黑点在黑底上不可见，细白描边保证黑点可辨
                    dot = Dot(
                        radius=ZERO_DOT_R,
                        fill_color=BLACK,
                        stroke_color=WHITE,
                        stroke_width=1.0,
                    )
                    g = VGroup(disc, dot).move_to(pos(r, c))
                    g.dot = dot  # type: ignore[attr-defined]
                else:
                    lbl = Text(
                        "1",
                        font_size=30,
                        color=WHITE,
                        font="Arial",
                        disable_ligatures=True,
                    )
                    g = VGroup(disc, lbl).move_to(pos(r, c))
                    g.lbl = lbl  # type: ignore[attr-defined]
                g.disc = disc  # type: ignore[attr-defined]
                nodes[(r, c)] = g
                nodes_g.add(g)

        graph_group = VGroup(under, lines_g, nodes_g)
        # 初始：图在右侧；边不可见、顶点描边不可见
        graph_group.move_to(RIGHT * 4.05)
        for r in range(rows):
            for c in range(cols):
                nodes[(r, c)].disc.set_stroke(opacity=0)  # type: ignore[union-attr]
                nodes[(r, c)].disc.set_fill(opacity=0)
                if grid[r][c] == 1:
                    nodes[(r, c)].lbl.set_opacity(0)  # type: ignore[union-attr]

        self.add(matrix_group)

        # 1) 先展示矩阵
        self.wait(0.45 * slow)

        # 2) 矩阵左移 + 同步「生成」网格图（边显现、顶点描边显现）
        def reveal_graph(_alpha: float) -> None:
            a = float(np.clip(_alpha, 0.0, 1.0))
            for ln in lines_g:
                ln.set_stroke(opacity=a * 0.9)
            for r in range(rows):
                for c in range(cols):
                    nodes[(r, c)].disc.set_stroke(opacity=a)  # type: ignore[union-attr]
                    if grid[r][c] == 1:
                        nodes[(r, c)].lbl.set_opacity(a)  # type: ignore[union-attr]

        alpha_driver = Mobject()
        self.add(alpha_driver)

        def _reveal_upd(m: Mobject, a: float) -> None:
            reveal_graph(a)

        self.add(graph_group)

        self.play(
            matrix_group.animate.shift(LEFT * 2.95),
            graph_group.animate.shift(LEFT * 0.85),
            UpdateFromAlphaFunc(alpha_driver, _reveal_upd),
            run_time=t_smooth,
            rate_func=smooth,
        )
        self.remove(alpha_driver)
        reveal_graph(1.0)

        # 3) 箭头：矩阵 → 图
        m_right = matrix_group.get_right() + RIGHT * 0.05
        g_left = graph_group.get_left() + LEFT * 0.12
        arr = Arrow(
            m_right,
            g_left,
            buff=0.12,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )
        arr.set_z_index(20)
        self.play(GrowFromCenter(arr), run_time=0.42 * slow, rate_func=smooth)
        self.wait(0.18 * slow)
        self.play(FadeOut(arr, scale=0.85), run_time=0.35 * slow, rate_func=smooth)

        # 4) 矩阵淡出；图移到画面中央
        self.play(
            FadeOut(matrix_group, shift=LEFT * 0.2),
            graph_group.animate.move_to(ORIGIN).set_rate_func(smooth),
            run_time=t_smooth,
            rate_func=smooth,
        )
        self.remove(matrix_group)

        # ---------- 扫描高亮框 ----------
        scan = Square(
            side_length=CELL * 1.02,
            color=YELLOW,
            stroke_width=3.2,
            fill_opacity=0,
            z_index=15,
        )
        scan.move_to(pos(0, 0))
        self.add(scan)

        visited: set[tuple[int, int]] = set()

        def _ctr_txt(n: int) -> Text:
            return Text(str(n), font_size=56, color=WHITE, font="Arial", disable_ligatures=True)

        ctr = _ctr_txt(0)
        ctr.next_to(graph_group, UP, buff=0.55)
        ctr.set_z_index(25)

        def make_red_x_at(r: int, c: int) -> VGroup:
            base = pos(r, c) + UP * (CELL * 0.62)
            h = 0.16
            l1 = Line(base + LEFT * h + DOWN * h, base + RIGHT * h + UP * h, color=RED_HL, stroke_width=3.8, z_index=18)
            l2 = Line(base + LEFT * h + UP * h, base + RIGHT * h + DOWN * h, color=RED_HL, stroke_width=3.8, z_index=18)
            return VGroup(l1, l2)

        def flash_reject(r: int, c: int) -> None:
            s = cell_under[(r, c)]
            xg = make_red_x_at(r, c)
            self.add(xg)
            anims_in = [s.animate.set_stroke(color=RED_HL, width=4.2, opacity=1), FadeIn(xg, scale=0.85)]
            anims_in.append(nodes[(r, c)].disc.animate.set_stroke(color=RED_HL, width=4.0))  # type: ignore[union-attr]
            self.play(*anims_in, run_time=0.22 * slow, rate_func=smooth)
            anims_out: list = [FadeOut(xg, scale=0.9)]
            if (r, c) in visited:
                anims_out.append(s.animate.set_stroke(color=GREEN_HL, width=2.8, opacity=1))
            else:
                anims_out.append(s.animate.set_stroke(color=NODE_IDLE, width=1.2, opacity=0.35))
            # 已 BFS 访问过的 1：圆描边恢复绿色；否则恢复白描边（0 格同理按是否访问，0 永不在 visited）
            col = GREEN_HL if (r, c) in visited else WHITE
            w = 3.2 if (r, c) in visited else STROKE
            anims_out.append(nodes[(r, c)].disc.animate.set_stroke(color=col, width=w))  # type: ignore[union-attr]
            self.play(*anims_out, run_time=0.28 * slow, rate_func=smooth)
            self.remove(xg)

        def move_scan(r: int, c: int) -> None:
            self.play(scan.animate.move_to(pos(r, c)), run_time=0.16 * slow, rate_func=smooth)

        def run_bfs(start: tuple[int, int]) -> None:
            q: deque[tuple[int, int]] = deque([start])
            seen: set[tuple[int, int]] = {start}

            disc0 = nodes[start].disc  # type: ignore[union-attr]
            sq0 = cell_under[start]
            self.play(
                disc0.animate.set_stroke(color=GREEN_HL, width=4.0),
                sq0.animate.set_stroke(color=GREEN_HL, width=3.0, opacity=1),
                run_time=0.2 * slow,
                rate_func=smooth,
            )

            while q:
                u = q.popleft()
                for v in adj[u]:
                    if v in seen:
                        continue
                    seen.add(v)
                    q.append(v)
                    dv = nodes[v].disc  # type: ignore[union-attr]
                    sv = cell_under[v]
                    self.play(
                        dv.animate.set_stroke(color=GREEN_HL, width=3.6),
                        sv.animate.set_stroke(color=GREEN_HL, width=2.8, opacity=1),
                        run_time=0.14 * slow,
                        rate_func=smooth,
                    )
                    self.wait(gap * 0.5)

            visited.update(seen)

            # BFS 结束后该连通块的边染绿
            edge_anims = []
            for a, b in edges_list:
                if a in seen and b in seen:
                    ln = edge_mobs[(a, b)]
                    edge_anims.append(ln.animate.set_color(GREEN_HL).set_stroke(width=2.9))
            if edge_anims:
                self.play(*edge_anims, run_time=0.22 * slow, rate_func=smooth)
            self.wait(t_short)

        # ---------- 逐行扫描 ----------
        completed_islands = 0
        scan_started = False
        for r in range(rows):
            for c in range(cols):
                if not scan_started:
                    scan_started = True
                    self.play(
                        FadeIn(ctr, shift=DOWN * 0.12),
                        run_time=0.35 * slow,
                        rate_func=smooth,
                    )
                else:
                    move_scan(r, c)
                v = grid[r][c]
                if v == 0:
                    flash_reject(r, c)
                elif (r, c) in visited:
                    flash_reject(r, c)
                else:
                    run_bfs((r, c))
                    completed_islands += 1
                    new_t = _ctr_txt(completed_islands).move_to(ctr.get_center())
                    self.play(Transform(ctr, new_t), run_time=0.28 * slow, rate_func=smooth)

        self.play(FadeOut(scan), run_time=0.25 * slow)

        # ---------- 三个连通分量（用于最后闪烁） ----------
        comps: list[set[tuple[int, int]]] = []
        seen_comp: set[tuple[int, int]] = set()
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 1 or (r, c) in seen_comp:
                    continue
                q = deque([(r, c)])
                comp: set[tuple[int, int]] = set()
                while q:
                    u = q.popleft()
                    if u in comp:
                        continue
                    comp.add(u)
                    seen_comp.add(u)
                    for w in adj[u]:
                        if w not in comp:
                            q.append(w)
                comps.append(comp)

        for comp in comps:
            self.play(
                LaggedStart(
                    *[
                        nodes[p].disc.animate.set_stroke(color=YELLOW, width=6.0)  # type: ignore[union-attr]
                        for p in comp
                    ],
                    lag_ratio=0.08,
                ),
                run_time=0.32 * slow,
                rate_func=smooth,
            )
            self.play(
                LaggedStart(
                    *[
                        nodes[p].disc.animate.set_stroke(color=GREEN_HL, width=3.2)  # type: ignore[union-attr]
                        for p in comp
                    ],
                    lag_ratio=0.06,
                ),
                run_time=0.36 * slow,
                rate_func=smooth,
            )
            self.wait(0.12 * slow)

        self.wait(0.55 * slow)
