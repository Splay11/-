from __future__ import annotations

from collections import deque

from manim import *


def diameter_path(children: dict[int, tuple[int | None, int | None]], root: int) -> tuple[list[int], int]:
    adj: dict[int, list[int]] = {k: [] for k in children}
    for p, (lch, rch) in children.items():
        for ch in (lch, rch):
            if ch is None:
                continue
            adj[p].append(ch)
            adj[ch].append(p)

    def farthest(start: int) -> tuple[int, int, dict[int, int | None]]:
        q = deque([start])
        dist = {start: 0}
        parent: dict[int, int | None] = {start: None}
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v in dist:
                    continue
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
        node = max(dist, key=dist.get)
        return node, dist[node], parent

    a, _, _ = farthest(root)
    b, d, parent = farthest(a)
    path = []
    cur: int | None = b
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path, d


class DiameterBottomUpDemo(Scene):
    def construct(self) -> None:
        tree_offset = np.array([0.0, -0.25, 0.0])
        step_rt = 0.45
        focus_rt = 0.5

        # 调整后的样例树：
        # 1 的右子树移除，并挂到原 5 号节点位置（作为 2 的右子树）
        children = {
            1: (2, None),
            2: (4, 3),
            3: (6, 7),
            4: (8, 9),
            6: (None, None),
            7: (None, None),
            8: (None, None),
            9: (None, None),
        }
        positions = {
            # 水平居中展示，并将 2 的两个儿子分开一些
            1: np.array([0.0, 2.7, 0.0]),
            2: np.array([0.0, 1.7, 0.0]),
            4: np.array([-1.6, 0.7, 0.0]),
            3: np.array([1.6, 0.7, 0.0]),  # 原 1 的右子树挂到这里
            8: np.array([-2.2, -0.3, 0.0]),
            9: np.array([-1.0, -0.3, 0.0]),
            6: np.array([1.0, -0.3, 0.0]),
            7: np.array([2.2, -0.3, 0.0]),
        }

        dia_path_nodes, dia_len = diameter_path(children, 1)
        dia_edges = {(min(a, b), max(a, b)) for a, b in zip(dia_path_nodes, dia_path_nodes[1:])}

        node_mobs: dict[int, VGroup] = {}
        edge_mobs: dict[tuple[int, int], Line] = {}
        edge_group = VGroup()

        for parent, (left_child, right_child) in children.items():
            for child in (left_child, right_child):
                if child is None:
                    continue
                line = Line(
                    positions[parent] + tree_offset,
                    positions[child] + tree_offset,
                    color=GRAY,
                    stroke_width=2.6,
                )
                edge_mobs[(parent, child)] = line
                edge_group.add(line)

        for node_id, pos in positions.items():
            c = Circle(radius=0.24, color=WHITE, stroke_width=2.8)
            c.set_fill(BLUE_E, opacity=1.0)
            c.move_to(pos + tree_offset)
            t = Text(str(node_id), font_size=28, color=WHITE).move_to(c.get_center())
            node_mobs[node_id] = VGroup(c, t)

        side_status_mobs: dict[int, dict[str, Text]] = {}
        return_status_mobs: dict[int, Text] = {}
        current_node: int | None = None
        ans_val = 0

        def descendants(rt: int | None) -> list[int]:
            if rt is None:
                return []
            lch, rch = children[rt]
            return [rt] + descendants(lch) + descendants(rch)

        desc_map = {k: descendants(k) for k in children}

        def focus_node(node_id: int | None, rt: float = focus_rt) -> None:
            nonlocal current_node
            anims = []
            if current_node is not None:
                anims.append(
                    node_mobs[current_node][0].animate.set_stroke(WHITE, width=2.8).set_fill(BLUE_E, opacity=1.0)
                )
            if node_id is not None:
                anims.append(
                    node_mobs[node_id][0].animate.set_stroke(YELLOW, width=4.0).set_fill(YELLOW_E, opacity=1.0)
                )
            if anims:
                self.play(*anims, run_time=rt)
            current_node = node_id

        def ensure_side_questions(node_id: int) -> None:
            if node_id in side_status_mobs:
                return
            ql = Text("?", font="Consolas", font_size=30, color=YELLOW)
            qr = Text("?", font="Consolas", font_size=30, color=YELLOW)
            ql.next_to(node_mobs[node_id][0], LEFT, buff=0.18)
            qr.next_to(node_mobs[node_id][0], RIGHT, buff=0.18)
            side_status_mobs[node_id] = {"left": ql, "right": qr}
            self.play(FadeIn(ql, scale=0.88), FadeIn(qr, scale=0.88), run_time=0.25)

        def set_side_status(node_id: int, side: str, text: str, color=YELLOW) -> None:
            old = side_status_mobs[node_id][side]
            nxt = Text(text, font="Consolas", font_size=30, color=color)
            nxt.move_to(old.get_center())
            self.play(Transform(old, nxt), run_time=0.28)

        def set_return_status(node_id: int, text: str, color=YELLOW) -> None:
            if node_id not in return_status_mobs:
                t = Text(text, font="Consolas", font_size=30, color=color)
                t.next_to(node_mobs[node_id][0], RIGHT, buff=0.18)
                return_status_mobs[node_id] = t
                self.play(FadeIn(t, scale=0.88), run_time=0.25)
                return
            old = return_status_mobs[node_id]
            nxt = Text(text, font="Consolas", font_size=30, color=color).move_to(old.get_center())
            self.play(Transform(old, nxt), run_time=0.25)

        def finalize_internal_result(node_id: int, res: int) -> None:
            left_mob = side_status_mobs[node_id]["left"]
            right_mob = side_status_mobs[node_id]["right"]
            res_mob = Text(str(res), font="Consolas", font_size=30, color=YELLOW)
            res_mob.next_to(node_mobs[node_id][0], RIGHT, buff=0.18)
            self.play(FadeOut(left_mob), Transform(right_mob, res_mob), run_time=0.3)
            return_status_mobs[node_id] = right_mob

        def show_subtree_hint(sub_root: int) -> None:
            nodes = desc_map[sub_root]
            g = VGroup(*[node_mobs[n] for n in nodes])
            frame = SurroundingRectangle(
                g,
                buff=0.2,
                color=TEAL_A,
                stroke_width=3.0,
                corner_radius=0.12,
            )
            self.play(Create(frame), run_time=0.28)
            self.wait(0.18)
            self.play(FadeOut(frame), run_time=0.22)

        def show_backtrack(child_id: int, parent_id: int) -> None:
            child_center = node_mobs[child_id][0].get_center()
            parent_center = node_mobs[parent_id][0].get_center()
            start = child_center + UP * 0.12
            end = parent_center + DOWN * 0.14
            is_left = child_center[0] < parent_center[0]
            angle = PI / 3 if is_left else -PI / 3
            arrow = CurvedArrow(
                start,
                end,
                angle=angle,
                color=YELLOW_D,
                stroke_width=3.2,
                tip_length=0.17,
            )
            label = Text("回溯", font_size=23, color=YELLOW_D)
            mid = arrow.point_from_proportion(0.5)
            if is_left:
                label.move_to(mid + LEFT * 0.33 + UP * 0.18)
            else:
                label.move_to(mid + RIGHT * 0.33 + UP * 0.18)

            self.play(Create(arrow), FadeIn(label, shift=UP * 0.03), run_time=step_rt * 0.9)
            self.play(FadeOut(arrow), FadeOut(label), run_time=step_rt * 0.72)

        def show_merge_and_update_ans(node_id: int, left_val: int, right_val: int) -> None:
            nonlocal ans_val, ans_value
            candidate = left_val + right_val + 2
            anchor = node_mobs[node_id][0].get_center() + UP * 0.74

            expr = Text(
                f"{left_val}+{right_val}+2={candidate}",
                font="Consolas",
                font_size=24,
                color=WHITE,
            ).move_to(anchor)
            self.play(FadeIn(expr, shift=UP * 0.03), run_time=0.3)

            token = Text(str(candidate), font="Consolas", font_size=30, color=YELLOW).move_to(expr.get_center())
            self.play(Transform(expr, token), run_time=0.22)

            fly = expr.copy()
            self.add(fly)
            self.play(fly.animate.move_to(ans_value.get_center()), run_time=0.38)
            if candidate > ans_val:
                ans_val = candidate
                nv = Text(str(ans_val), font="Consolas", font_size=34, color=YELLOW).move_to(ans_value.get_center())
                self.play(Transform(ans_value, nv), run_time=0.24)
            else:
                self.play(Indicate(ans_value, color=GRAY_B), run_time=0.2)
            self.play(FadeOut(fly), FadeOut(expr), run_time=0.18)

        def flash_merge_path(path_nodes: list[int], root_node: int) -> None:
            if len(path_nodes) <= 1:
                return

            def edge_between(a: int, b: int) -> Line:
                if (a, b) in edge_mobs:
                    return edge_mobs[(a, b)]
                return edge_mobs[(b, a)]

            # 文字放在顶部空白区域，避免与树和状态文本重叠
            pivot_note = Text(
                f"以{root_node}为拐点的最长路径",
                font_size=26,
                color=YELLOW_D,
            )
            pivot_note.move_to(np.array([0.0, 3.35, 0.0]))
            pivot_arrow = Arrow(
                pivot_note.get_bottom() + DOWN * 0.03,
                node_mobs[root_node][0].get_top() + UP * 0.03,
                buff=0.03,
                color=YELLOW_D,
                stroke_width=3.0,
                max_tip_length_to_length_ratio=0.12,
            )
            self.play(FadeIn(pivot_note, shift=UP * 0.05), Create(pivot_arrow), run_time=0.35)

            for _ in range(3):
                edge_anims = []
                node_anims = []
                for a, b in zip(path_nodes, path_nodes[1:]):
                    edge_anims.append(edge_between(a, b).animate.set_color(RED).set_stroke(width=4.0))
                for nid in path_nodes:
                    node_anims.append(node_mobs[nid][0].animate.set_fill(RED_E, opacity=1.0).set_stroke(RED, width=4.2))
                self.play(*edge_anims, *node_anims, run_time=0.22)
                self.wait(0.08)

                recover_edge_anims = []
                recover_node_anims = []
                for a, b in zip(path_nodes, path_nodes[1:]):
                    recover_edge_anims.append(edge_between(a, b).animate.set_color(GRAY).set_stroke(width=2.6))
                for nid in path_nodes:
                    if nid == root_node:
                        recover_node_anims.append(
                            node_mobs[nid][0].animate.set_fill(YELLOW_E, opacity=1.0).set_stroke(YELLOW, width=4.0)
                        )
                    else:
                        recover_node_anims.append(
                            node_mobs[nid][0].animate.set_fill(BLUE_E, opacity=1.0).set_stroke(WHITE, width=2.8)
                        )
                self.play(*recover_edge_anims, *recover_node_anims, run_time=0.2)
                self.wait(0.05)

            self.play(FadeOut(pivot_note), FadeOut(pivot_arrow), run_time=0.2)

        self.play(Create(edge_group), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(node_mobs[i], scale=0.86) for i in sorted(node_mobs)], lag_ratio=0.08),
            run_time=1.05,
        )

        ans_label = Text("ans =", font="Consolas", font_size=34, color=WHITE)
        ans_value = Text("0", font="Consolas", font_size=34, color=YELLOW)
        ans_group = VGroup(ans_label, ans_value).arrange(RIGHT, buff=0.08).move_to(np.array([0.0, -2.65, 0.0]))
        depth_note = Text(
            "注意:每个节点旁边显示的数字为：从这个点出发往下走的最大深度(按边计数)",
            font="Microsoft YaHei",
            font_size=20,
            color=GRAY_B,
        ).move_to(np.array([0.0, -3.15, 0.0]))
        self.play(FadeIn(ans_group, shift=UP * 0.08), run_time=0.3)
        self.play(FadeIn(depth_note, shift=UP * 0.05), run_time=0.25)

        def dfs(node_id: int | None) -> tuple[int, list[int]]:
            if node_id is None:
                return -1, []

            focus_node(node_id)
            left_child, right_child = children[node_id]

            if left_child is None and right_child is None:
                set_return_status(node_id, "0", color=YELLOW)
                self.wait(0.12)
                return 0, [node_id]

            ensure_side_questions(node_id)
            self.wait(0.22)
            left_val = -1
            left_path: list[int] = []
            if left_child is not None:
                show_subtree_hint(left_child)
                left_val, left_path = dfs(left_child)
                show_backtrack(left_child, node_id)
                focus_node(node_id, rt=0.35)
            set_side_status(node_id, "left", str(left_val), color=BLUE_B)

            self.wait(0.2)
            right_val = -1
            right_path: list[int] = []
            if right_child is not None:
                show_subtree_hint(right_child)
                right_val, right_path = dfs(right_child)
                show_backtrack(right_child, node_id)
                focus_node(node_id, rt=0.35)
            set_side_status(node_id, "right", str(right_val), color=ORANGE)

            show_merge_and_update_ans(node_id, left_val, right_val)
            res = 1 + max(left_val, right_val)
            finalize_internal_result(node_id, res)
            # 闪红以当前节点为拐点的完整路径（对应 left_max + right_max + 2）
            left_down = [node_id] if left_val == -1 else [node_id] + left_path
            right_down = [node_id] if right_val == -1 else [node_id] + right_path
            merge_path = list(reversed(left_down)) + right_down[1:]
            flash_merge_path(merge_path, node_id)

            best_down_path = [node_id] + (left_path if left_val >= right_val else right_path)
            self.wait(0.08)
            return res, best_down_path

        dfs(1)
        focus_node(None, rt=0.35)

        # 递归结束后，标红整条直径路径
        node_anims = []
        edge_anims = []
        for node_id in dia_path_nodes:
            node_anims.append(node_mobs[node_id][0].animate.set_fill(RED_E, opacity=1.0).set_stroke(RED, width=4.2))
        for (u, v), line in edge_mobs.items():
            if (min(u, v), max(u, v)) in dia_edges:
                edge_anims.append(line.animate.set_color(RED).set_stroke(width=4.0))
        self.play(*edge_anims, *node_anims, run_time=0.7)

        note = Text("直径长度", font_size=28, color=YELLOW_D)
        note.next_to(ans_group, RIGHT, buff=0.9)
        arrow = Arrow(
            note.get_left() + LEFT * 0.04,
            ans_value.get_right() + RIGHT * 0.02,
            buff=0.02,
            color=YELLOW_D,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.12,
        )
        self.play(FadeIn(note, shift=UP * 0.05), Create(arrow), run_time=0.45)
        self.wait(0.9)

