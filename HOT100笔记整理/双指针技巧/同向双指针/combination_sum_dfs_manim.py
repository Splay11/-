"""组合求和 DFS：candidates=[2,4,6], target=8。左：数组 + target + 结果列表；中：虚线；右：递归树（节点为 curr）。

运行: python -m manim -ql 同向双指针\\combination_sum_dfs_manim.py CombinationSumDFS
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from manim import *


CANDIDATES = [2, 4, 6]
TARGET = 8
N = len(CANDIDATES)


@dataclass
class TreeNode:
    nid: int
    parent: int
    index: int
    total: int
    curr: tuple[int, ...]


def build_tree() -> tuple[list[TreeNode], dict[int, list[int]]]:
    nodes: list[TreeNode] = []
    ch: dict[int, list[int]] = defaultdict(list)

    def dfs(index: int, total: int, curr: list[int], pid: int) -> None:
        nid = len(nodes)
        nodes.append(TreeNode(nid, pid, index, total, tuple(curr)))
        if pid >= 0:
            ch[pid].append(nid)
        if index == N:
            return
        rest = TARGET - total
        up = rest // CANDIDATES[index]
        for i in range(up + 1):
            dfs(
                index + 1,
                total + i * CANDIDATES[index],
                curr + [CANDIDATES[index]] * i,
                nid,
            )

    dfs(0, 0, [], -1)
    return nodes, dict(ch)


NODES, CHILDREN = build_tree()


def compute_depths() -> dict[int, int]:
    d: dict[int, int] = {}
    for nd in NODES:
        if nd.parent < 0:
            d[nd.nid] = 0
        else:
            d[nd.nid] = d[nd.parent] + 1
    return d


DEPTHS = compute_depths()


def layout_tree_positions() -> dict[int, np.ndarray]:
    pos: dict[int, np.ndarray] = {}
    y_cursor = [0.0]
    spacing = 0.5

    def place(u: int) -> float:
        kids = CHILDREN.get(u, [])
        if not kids:
            y = y_cursor[0]
            y_cursor[0] += spacing
            d = DEPTHS[u]
            pos[u] = np.array([d * 0.95, y, 0.0])
            return y
        ys = [place(v) for v in kids]
        y_m = sum(ys) / len(ys)
        d = DEPTHS[u]
        pos[u] = np.array([d * 0.95, y_m, 0.0])
        return y_m

    place(0)
    if pos:
        ys = [p[1] for p in pos.values()]
        mid = (min(ys) + max(ys)) / 2.0
        for k in pos:
            pos[k] = pos[k] + np.array([0.0, -mid, 0.0])
    return pos


TREE_POS = layout_tree_positions()
TREE_ORIGIN = np.array([0.55, 0.0, 0.0])
SCALE_TREE = 0.58


def world_tree_pos(nid: int) -> np.ndarray:
    return TREE_ORIGIN + TREE_POS[nid] * SCALE_TREE


def curr_label_text(tup: tuple[int, ...]) -> str:
    if not tup:
        return "∅"
    return " ".join(str(x) for x in tup)


def make_tree_node_mob(nd: TreeNode, wpos: np.ndarray) -> VGroup:
    is_leaf = nd.index == N
    hit = is_leaf and nd.total == TARGET
    stroke_c = GREEN if hit else (RED_B if is_leaf else BLUE_B)
    label = curr_label_text(nd.curr)
    fs = 15 if len(label) > 10 else (17 if len(label) > 6 else 20)
    tx = Text(label, font_size=fs, color=WHITE)
    w = max(0.95, min(2.1, tx.width + 0.28))
    h = max(0.42, tx.height + 0.2)
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.08,
        color=stroke_c,
        stroke_width=2.5,
        fill_color=BLACK,
        fill_opacity=0.55,
    )
    box.move_to(wpos)
    tx.move_to(wpos)
    return VGroup(box, tx)


class CombinationSumDFS(Scene):
    def construct(self) -> None:
        split_x = -0.35
        left_center = np.array([-2.65, 0.55, 0.0])

        dash = DashedLine(
            np.array([split_x, -3.35, 0.0]),
            np.array([split_x, 3.35, 0.0]),
            color=GRAY_B,
            stroke_width=2.5,
            dash_length=0.14,
            dashed_ratio=0.45,
        )

        tgt_mob = Text(f"target = {TARGET}", font_size=30, color=YELLOW)
        tgt_mob.move_to(left_center + UP * 1.0)

        cell_w, cell_h = 0.58, 0.64
        gap = 0.05
        sp = cell_w + gap
        sx = -(N - 1) * sp / 2
        cells = VGroup()
        vals = VGroup()
        for i in range(N):
            r = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.08,
                color=GRAY_B,
                stroke_width=2,
            )
            t = Text(str(CANDIDATES[i]), font_size=30)
            r.move_to(np.array([sx + i * sp, 0.0, 0.0]))
            t.move_to(r.get_center())
            cells.add(r)
            vals.add(t)
        arr = VGroup(cells, vals)
        arr.move_to(left_center + DOWN * 0.02)

        idx_row = VGroup(
            *[
                Text(str(i), font_size=18, color=GRAY).next_to(cells[i], DOWN, buff=0.14)
                for i in range(N)
            ]
        )

        ans_title = Text("结果", font_size=22, color=GREEN)
        ans_title.move_to(left_center + DOWN * 1.02)
        ans_list = VGroup()

        left_panel = VGroup(tgt_mob, arr, idx_row, ans_title, ans_list)

        def prefix_rect_for(ix: int) -> SurroundingRectangle | None:
            if ix <= 0:
                return None
            sub = VGroup(*[cells[j] for j in range(ix)])
            return SurroundingRectangle(sub, buff=0.06, color=YELLOW, stroke_width=3)

        curr_row_anchor = left_center + DOWN * 0.72

        def curr_mob_from(tup: tuple[int, ...]) -> VGroup:
            if not tup:
                g = Text("curr: ∅", font_size=22, color=GRAY)
                return VGroup(g)
            chips = Text("curr: " + curr_label_text(tup), font_size=22, color=BLUE_B)
            return VGroup(chips)

        node_mobs: dict[int, VGroup] = {}
        edge_mobs: dict[tuple[int, int], Line] = {}

        for nd in NODES:
            wpos = world_tree_pos(nd.nid)
            g = make_tree_node_mob(nd, wpos)
            g.set_opacity(0)
            node_mobs[nd.nid] = g

        for p, kids in CHILDREN.items():
            for c in kids:
                p0 = world_tree_pos(p)
                c0 = world_tree_pos(c)
                dv = np.array([c0[0] - p0[0], c0[1] - p0[1], 0.0])
                nrm = float(np.linalg.norm(dv[:2]))
                if nrm < 1e-4:
                    ln = Line(p0, c0, color=GRAY_A, stroke_width=2.5)
                else:
                    u = dv / nrm
                    ln = Line(p0 + u * 0.12, c0 - u * 0.14, color=GRAY_A, stroke_width=2.5)
                ln.set_opacity(0)
                edge_mobs[(p, c)] = ln

        # 背景与左侧先加入，再把树与边置于上层，避免被挡
        self.add(dash, left_panel)
        for e in edge_mobs.values():
            self.add(e)
        for nd in NODES:
            self.add(node_mobs[nd.nid])
        for e in edge_mobs.values():
            self.bring_to_front(e)
        for nd in NODES:
            self.bring_to_front(node_mobs[nd.nid])

        def rt(t: float) -> float:
            return round(t * 1.0, 2)

        self.play(FadeIn(dash, shift=RIGHT * 0.08), FadeIn(left_panel, shift=RIGHT * 0.12), run_time=rt(0.5))
        self.wait(rt(0.18))

        curr_disp = curr_mob_from(())
        curr_disp.move_to(curr_row_anchor)
        self.play(FadeIn(curr_disp, shift=UP * 0.08), run_time=rt(0.32))

        active_box: Mobject | None = None

        for nd in NODES:
            ix = nd.index
            pr = prefix_rect_for(ix)
            if pr is None:
                if active_box is not None:
                    self.play(FadeOut(active_box), run_time=rt(0.18))
                    active_box = None
            else:
                if active_box is None:
                    active_box = pr
                    self.play(Create(active_box), run_time=rt(0.24))
                else:
                    self.play(Transform(active_box, pr), run_time=rt(0.22))

            new_curr = curr_mob_from(nd.curr)
            new_curr.move_to(curr_row_anchor)
            self.play(ReplacementTransform(curr_disp, new_curr), run_time=rt(0.22))
            curr_disp = new_curr

            nm = node_mobs[nd.nid]
            self.bring_to_front(nm)
            self.play(FadeIn(nm, scale=0.75), run_time=rt(0.26))
            if nd.parent >= 0:
                e = edge_mobs[(nd.parent, nd.nid)]
                self.bring_to_front(e)
                self.play(GrowFromCenter(e), run_time=rt(0.18))

            if nd.index == N and nd.total == TARGET:
                line = Text(curr_label_text(nd.curr), font_size=20, color=GREEN)
                if len(ans_list) == 0:
                    line.next_to(ans_title, DOWN, buff=0.16, aligned_edge=LEFT)
                else:
                    line.next_to(ans_list[-1], DOWN, buff=0.12, aligned_edge=LEFT)
                self.play(
                    Flash(nm, color=GREEN, flash_radius=0.5, line_length=0.12),
                    nm.animate.scale(1.06),
                    FadeIn(line, shift=LEFT * 0.12),
                    run_time=rt(0.42),
                )
                self.play(nm.animate.scale(1 / 1.06), run_time=rt(0.12))
                ans_list.add(line)
            elif nd.index == N:
                self.play(Indicate(nm, color=GRAY, scale_factor=1.04), run_time=rt(0.2))

            self.wait(rt(0.05))

        if active_box is not None:
            self.play(FadeOut(active_box), run_time=rt(0.18))
        self.play(
            LaggedStart(
                *[
                    Flash(node_mobs[nd.nid], color=GREEN, line_length=0.1)
                    for nd in NODES
                    if nd.index == N and nd.total == TARGET
                ],
                lag_ratio=0.12,
            ),
            run_time=rt(0.75),
        )
        self.wait(rt(0.45))
