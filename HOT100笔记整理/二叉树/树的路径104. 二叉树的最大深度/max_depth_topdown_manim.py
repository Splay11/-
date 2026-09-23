from __future__ import annotations

from manim import *


class MaxDepthTopDownDemo(Scene):
    def construct(self) -> None:
        tree_offset = np.array([0.0, -0.25, 0.0])
        step_rt = 0.45

        # 与解法1保持同样的样例树（叶子不在同一层）
        children = {
            1: (2, 3),
            2: (4, 5),
            3: (6, 7),
            4: (8, 9),
            5: (None, None),
            6: (None, None),
            7: (None, None),
            8: (None, None),
            9: (None, None),
        }
        positions = {
            1: np.array([0.0, 2.7, 0.0]),
            2: np.array([-2.2, 1.7, 0.0]),
            3: np.array([2.2, 1.7, 0.0]),
            4: np.array([-3.3, 0.7, 0.0]),
            5: np.array([-1.1, 0.7, 0.0]),
            6: np.array([1.1, 0.7, 0.0]),
            7: np.array([3.3, 0.7, 0.0]),
            8: np.array([-4.0, -0.4, 0.0]),
            9: np.array([-2.6, -0.4, 0.0]),
        }

        node_mobs: dict[int, VGroup] = {}
        edge_mobs: dict[tuple[int, int], Line] = {}
        edges = VGroup()

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
                edges.add(line)

        for node_id, pos in positions.items():
            c = Circle(radius=0.24, color=WHITE, stroke_width=2.8)
            c.set_fill(BLUE_E, opacity=1.0)
            c.move_to(pos + tree_offset)
            t = Text(str(node_id), font_size=28, color=WHITE).move_to(c.get_center())
            node_mobs[node_id] = VGroup(c, t)

        max_depth = 0
        depth_token: Text | None = None

        max_label = Text("maxDepth = ", font="Consolas", font_size=34, color=WHITE)
        max_value = Text("0", font="Consolas", font_size=34, color=YELLOW)
        max_box = VGroup(max_label, max_value).arrange(RIGHT, buff=0.08)
        max_box.move_to(np.array([0.0, -2.95, 0.0]))

        self.play(Create(edges), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(node_mobs[i], scale=0.86) for i in sorted(node_mobs)], lag_ratio=0.08),
            run_time=1.0,
        )
        self.play(FadeIn(max_box, shift=UP * 0.1), run_time=0.35)

        def make_depth_text(node_id: int, depth: int) -> Text:
            t = Text(str(depth), font="Consolas", font_size=30, color=YELLOW)
            t.next_to(node_mobs[node_id][0], RIGHT, buff=0.18)
            return t

        def init_root_token(node_id: int, depth: int) -> None:
            nonlocal depth_token
            depth_token = make_depth_text(node_id, depth)
            self.play(FadeIn(depth_token, scale=0.9), run_time=0.28)

        def descend(parent_id: int, child_id: int, child_depth: int) -> None:
            nonlocal depth_token
            if depth_token is None:
                return
            target_pos = node_mobs[child_id][0].get_right() + RIGHT * 0.28
            self.play(
                node_mobs[child_id][0].animate.set_stroke(YELLOW, width=4.0).set_fill(YELLOW_E, opacity=1.0),
                edge_mobs[(parent_id, child_id)].animate.set_color(YELLOW).set_stroke(width=3.3),
                depth_token.animate.move_to(target_pos),
                run_time=step_rt,
            )
            upgraded = Text(str(child_depth), font="Consolas", font_size=30, color=YELLOW).move_to(depth_token.get_center())
            self.play(Transform(depth_token, upgraded), run_time=0.24)

        def ascend(child_id: int, parent_id: int, parent_depth: int) -> None:
            nonlocal depth_token
            if depth_token is None:
                return
            target_pos = node_mobs[parent_id][0].get_right() + RIGHT * 0.28
            self.play(
                depth_token.animate.move_to(target_pos),
                run_time=0.28,
            )
            downgraded = Text(str(parent_depth), font="Consolas", font_size=30, color=YELLOW).move_to(depth_token.get_center())
            self.play(
                Transform(depth_token, downgraded),
                node_mobs[child_id][0].animate.set_stroke(WHITE, width=2.8).set_fill(BLUE_E, opacity=1.0),
                edge_mobs[(parent_id, child_id)].animate.set_color(GRAY).set_stroke(width=2.6),
                run_time=0.28,
            )

        def enter_root(node_id: int) -> None:
            anims = [
                node_mobs[node_id][0].animate.set_stroke(YELLOW, width=4.0).set_fill(YELLOW_E, opacity=1.0),
            ]
            self.play(*anims, run_time=step_rt)

        def leave_node(node_id: int, parent_id: int | None) -> None:
            anims = [
                node_mobs[node_id][0].animate.set_stroke(WHITE, width=2.8).set_fill(BLUE_E, opacity=1.0),
            ]
            self.play(*anims, run_time=0.26)

        def update_max_from_leaf(node_id: int, depth: int) -> None:
            nonlocal max_depth, max_value, depth_token
            if depth_token is None:
                return
            candidate = depth_token.copy()
            self.add(candidate)
            self.play(candidate.animate.move_to(max_value.get_center()), run_time=0.38)

            if depth > max_depth:
                max_depth = depth
                nv = Text(str(max_depth), font="Consolas", font_size=34, color=YELLOW).move_to(max_value.get_center())
                self.play(Transform(max_value, nv), run_time=0.25)
            else:
                self.play(Indicate(max_value, color=GRAY_B), run_time=0.22)
            self.play(FadeOut(candidate), run_time=0.15)

        def dfs(node_id: int | None, parent_id: int | None, depth: int) -> None:
            if node_id is None:
                return

            if parent_id is None:
                enter_root(node_id)
                init_root_token(node_id, depth)
            left_child, right_child = children[node_id]

            if left_child is None and right_child is None:
                update_max_from_leaf(node_id, depth)
                self.wait(0.08)
                return

            if left_child is not None:
                self.wait(0.15)
                descend(node_id, left_child, depth + 1)
                dfs(left_child, node_id, depth + 1)
                ascend(left_child, node_id, depth)
            if right_child is not None:
                self.wait(0.15)
                descend(node_id, right_child, depth + 1)
                dfs(right_child, node_id, depth + 1)
                ascend(right_child, node_id, depth)

        dfs(1, None, 1)
        leave_node(1, None)
        if depth_token is not None:
            self.play(FadeOut(depth_token), run_time=0.2)
        self.wait(0.8)

