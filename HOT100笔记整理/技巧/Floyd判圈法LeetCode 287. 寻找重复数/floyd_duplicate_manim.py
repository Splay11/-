"""LeetCode 287 Floyd 判圈动画（多组样例）。

运行：
  .\manim-env\Scripts\manim.exe -pql floyd_duplicate_manim.py FloydDuplicateCycleDemo
"""

from __future__ import annotations

from pathlib import Path

from manim import *

config.media_dir = str(Path(__file__).resolve().parent / "media")

FONT_CN = "Microsoft YaHei"

COL_CHAIN = "#5B83FF"
COL_CHAIN_STROKE = "#355ED9"
COL_ENTRY = "#FF6B6B"
COL_ENTRY_STROKE = "#D94848"
COL_CYCLE = "#22B8A3"
COL_CYCLE_STROKE = "#159885"
COL_EDGE_CHAIN = "#5D6AA7"
COL_EDGE_CYCLE = "#109D8B"
COL_EDGE_ENTRY = "#D94848"


def trace_from_zero(nums: list[int]) -> tuple[list[int], list[int], int, list[int]]:
    """返回链节点、环节点、环入口，以及 0 出发到首次重复前的轨迹。"""
    pos: dict[int, int] = {}
    order: list[int] = []
    cur = 0
    while cur not in pos:
        pos[cur] = len(order)
        order.append(cur)
        cur = nums[cur]
    cycle_start = pos[cur]
    chain_nodes = order[:cycle_start]
    cycle_nodes = order[cycle_start:]
    return chain_nodes, cycle_nodes, cur, order


def pointer_steps(nums: list[int]) -> tuple[list[tuple[int, int]], list[tuple[int, int]], int]:
    """返回两阶段指针位置序列与入口。"""
    slow = 0
    fast = 0
    phase1 = [(slow, fast)]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        phase1.append((slow, fast))
        if slow == fast:
            break
    meet = slow

    p1, p2 = 0, meet
    phase2 = [(p1, p2)]
    while p1 != p2:
        p1 = nums[p1]
        p2 = nums[p2]
        phase2.append((p1, p2))
    return phase1, phase2, p1


class FloydDuplicateCycleDemo(Scene):
    def node_style(self, node: int, entry: int, cycle_set: set[int]) -> tuple[str, str]:
        if node == entry:
            return COL_ENTRY, COL_ENTRY_STROKE
        if node in cycle_set:
            return COL_CYCLE, COL_CYCLE_STROKE
        return COL_CHAIN, COL_CHAIN_STROKE

    def build_layout(self, chain_nodes: list[int], cycle_nodes: list[int]) -> dict[int, np.ndarray]:
        pos: dict[int, np.ndarray] = {}
        y0 = -0.15
        x_start = -5.0
        chain_step = 1.65
        for i, node in enumerate(chain_nodes):
            pos[node] = np.array([x_start + i * chain_step, y0, 0.0])

        m = len(cycle_nodes)
        if m == 0:
            return pos

        if chain_nodes:
            anchor_x = pos[chain_nodes[-1]][0] + 2.0
        else:
            anchor_x = -1.0
        center = np.array([anchor_x + 1.6, y0, 0.0])
        radius = 1.18 if m >= 2 else 0.95

        if m == 1:
            pos[cycle_nodes[0]] = center + LEFT * radius
        else:
            for i, node in enumerate(cycle_nodes):
                angle = PI - i * TAU / m
                pos[node] = center + radius * np.array([np.cos(angle), np.sin(angle), 0.0])
        return pos

    def draw_graph(
        self,
        nums: list[int],
        chain_nodes: list[int],
        cycle_nodes: list[int],
        entry: int,
        show_labels: bool = True,
        y_shift: float = 0.0,
    ) -> tuple[dict[int, VGroup], VGroup]:
        pos = self.build_layout(chain_nodes, cycle_nodes)
        cycle_set = set(cycle_nodes)
        node_keys = chain_nodes + cycle_nodes

        def edge_color(u: int, v: int) -> str:
            if u in cycle_set and v in cycle_set:
                return COL_EDGE_CYCLE
            if v == entry and u not in cycle_set:
                return COL_EDGE_ENTRY
            return COL_EDGE_CHAIN

        edges = VGroup()
        radius = 0.35
        processed_reverse_pairs: set[tuple[int, int]] = set()
        for u in node_keys:
            v = nums[u]
            if v not in pos:
                continue
            p1, p2 = pos[u], pos[v]
            if u == v:
                loop = Arc(
                    radius=0.42,
                    start_angle=-PI / 5,
                    angle=TAU * 0.8,
                    arc_center=p1 + np.array([0.0, 0.52, 0.0]),
                    stroke_width=3.0,
                    color=COL_EDGE_CYCLE if u in cycle_set else COL_EDGE_CHAIN,
                )
                tip = Triangle(fill_opacity=1, stroke_width=0, color=loop.get_color()).scale(0.06)
                tip.move_to(p1 + np.array([0.2, 0.88, 0.0]))
                edges.add(loop, tip)
                continue

            has_reverse = 0 <= v < len(nums) and nums[v] == u
            if has_reverse:
                a, b = min(u, v), max(u, v)
                if (a, b) in processed_reverse_pairs:
                    continue
                processed_reverse_pairs.add((a, b))

                pa, pb = pos[a], pos[b]

                dab = pb - pa
                dab = dab / np.linalg.norm(dab)
                sab = pa + dab * radius
                tab = pb - dab * radius

                dba = pa - pb
                dba = dba / np.linalg.norm(dba)
                sba = pb + dba * radius
                tba = pa - dba * radius

                arc_ab = ArcBetweenPoints(sab, tab, angle=0.62, stroke_width=3.0, color=edge_color(a, b))
                arc_ab.add_tip(tip_length=0.16)
                arc_ba = ArcBetweenPoints(sba, tba, angle=-0.62, stroke_width=3.0, color=edge_color(b, a))
                arc_ba.add_tip(tip_length=0.16)
                edges.add(arc_ab, arc_ba)
                continue

            d = p2 - p1
            d = d / np.linalg.norm(d)
            s = p1 + d * radius
            t = p2 - d * radius
            edges.add(
                Arrow(
                    s,
                    t,
                    buff=0,
                    stroke_width=3.0,
                    color=edge_color(u, v),
                    max_tip_length_to_length_ratio=0.18,
                )
            )

        nodes: dict[int, VGroup] = {}
        node_group = VGroup()
        for node in node_keys:
            fill_col, stroke_col = self.node_style(node, entry, cycle_set)
            c = Circle(radius=radius, fill_color=fill_col, fill_opacity=1, stroke_color=stroke_col, stroke_width=3)
            c.move_to(pos[node])
            txt = Text(str(node), font=FONT_CN, font_size=30, color=WHITE).move_to(c.get_center())
            if show_labels:
                label = Text(f"a[{node}] = {nums[node]}", font=FONT_CN, font_size=22, color=GRAY_B)
                label.next_to(c, DOWN, buff=0.28)
                vg = VGroup(c, txt, label)
            else:
                vg = VGroup(c, txt)
            nodes[node] = vg
            node_group.add(vg)

        full = VGroup(edges, node_group).shift(UP * y_shift)
        return nodes, full

    def pointer(self, name: str, color: str, node_obj: VGroup, up: float) -> VGroup:
        dot = Dot(node_obj[0].get_center() + UP * up, radius=0.085, color=color)
        lab = Text(name, font=FONT_CN, font_size=24, color=color).next_to(dot, UP if up > 0 else DOWN, buff=0.06)
        return VGroup(dot, lab)

    def play_sample(self, nums: list[int], tag: str, show_labels: bool = True) -> None:
        chain_nodes, cycle_nodes, entry, _ = trace_from_zero(nums)
        phase1, phase2, found = pointer_steps(nums)

        title = Text(f"{tag}  {nums}", font=FONT_CN, font_size=30, color=GRAY_A)
        title.to_edge(UP, buff=0.25)

        nodes, graph = self.draw_graph(nums, chain_nodes, cycle_nodes, entry, show_labels=show_labels)
        stage = Text("阶段1：找相遇点", font=FONT_CN, font_size=26, color=YELLOW_D).next_to(title, DOWN, buff=0.2)

        self.play(FadeIn(title, shift=DOWN * 0.08), FadeIn(graph, shift=UP * 0.08))
        self.play(FadeIn(stage, shift=UP * 0.06))

        slow_ptr = self.pointer("slow", YELLOW, nodes[phase1[0][0]], up=0.58)
        fast_ptr = self.pointer("fast", ORANGE, nodes[phase1[0][1]], up=0.88)
        self.play(FadeIn(slow_ptr), FadeIn(fast_ptr))

        s_cur, f_cur = phase1[0]
        while True:
            s_next = nums[s_cur]
            f_mid = nums[f_cur]
            f_next = nums[f_mid]

            new_slow = self.pointer("slow", YELLOW, nodes[s_next], up=0.58)
            fast_path = VMobject(color=ORANGE)
            fast_path.set_points_as_corners(
                [
                    fast_ptr[0].get_center(),
                    nodes[f_mid][0].get_center() + UP * 0.88,
                    nodes[f_next][0].get_center() + UP * 0.88,
                ]
            )
            self.play(
                Transform(slow_ptr, new_slow),
                MoveAlongPath(fast_ptr, fast_path),
                run_time=1.0,
                rate_func=linear,
            )
            self.wait(0.22)
            s_cur, f_cur = s_next, f_next
            if s_cur == f_cur:
                break

        meet_node = phase1[-1][0]
        self.play(Flash(nodes[meet_node][0], color=YELLOW, line_length=0.2, flash_radius=0.55), run_time=0.4)

        stage2 = Text("阶段2：同步一步找入口", font=FONT_CN, font_size=26, color=GREEN_D).move_to(stage)
        self.play(Transform(stage, stage2), FadeOut(fast_ptr), run_time=0.35)

        ptr1 = self.pointer("ptr1", BLUE_B, nodes[phase2[0][0]], up=-0.58)
        ptr2 = self.pointer("ptr2", GOLD, nodes[phase2[0][1]], up=-0.88)
        self.play(FadeIn(ptr1), FadeIn(ptr2))

        for p1, p2 in phase2[1:]:
            new_p1 = self.pointer("ptr1", BLUE_B, nodes[p1], up=-0.58)
            new_p2 = self.pointer("ptr2", GOLD, nodes[p2], up=-0.88)
            self.play(
                Transform(ptr1, new_p1),
                Transform(ptr2, new_p2),
                run_time=0.86,
            )

        entry_node = nodes[found][0]
        final = Text("重复数字", font=FONT_CN, font_size=28, color=COL_ENTRY_STROKE)
        final.move_to(entry_node.get_center() + LEFT * 1.08 + UP * 1.05)
        self.play(
            nodes[found][0].animate.set_stroke(YELLOW, width=5),
            nodes[found][1].animate.set_color(YELLOW),
            FadeIn(final, shift=UP * 0.08),
            run_time=0.5,
        )
        self.wait(0.9)
        self.play(FadeOut(VGroup(title, stage, graph, slow_ptr, ptr1, ptr2, final)), run_time=0.65)

    def construct(self) -> None:
        watermark = Text("塔子哥学算法", font=FONT_CN, font_size=20, color=BLUE_D)
        watermark.to_corner(UR, buff=0.20)
        self.add(watermark)

        samples = [
            ("样例1", [1, 3, 4, 2, 2], True),
            ("样例2", [3, 1, 3, 4, 2], True),
            ("样例3", [2, 5, 9, 6, 9, 3, 8, 9, 7, 1], False),
        ]
        for i, (tag, nums, show_labels) in enumerate(samples):
            self.play_sample(nums, tag, show_labels=show_labels)
            if i < len(samples) - 1:
                self.wait(0.2)
