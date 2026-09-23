from __future__ import annotations

from manim import *


class MaxDepthBottomUpDemo(Scene):
    def construct(self) -> None:
        tree_offset = np.array([0.0, -0.25, 0.0])
        step_rt = 0.45
        focus_rt = 0.5

        # 样例树（叶子不在同一层）:
        #            1
        #         /     \
        #        2       3
        #      /  \    /   \
        #     4    5  6     7
        #    / \
        #   8   9
        # 最大深度 = 4
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
        edge_mobs: dict[tuple[int, int], VMobject] = {}
        edge_endpoints: dict[tuple[int, int], tuple[np.ndarray, np.ndarray]] = {}
        edge_group = VGroup()

        for parent, (left_child, right_child) in children.items():
            for child in (left_child, right_child):
                if child is None:
                    continue
                start = positions[parent] + tree_offset
                end = positions[child] + tree_offset
                line = DashedLine(
                    start,
                    end,
                    color=WHITE,
                    stroke_width=2.6,
                    dash_length=0.12,
                    dashed_ratio=0.52,
                )
                edge_mobs[(parent, child)] = line
                edge_endpoints[(parent, child)] = (start, end)
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

        def show_merge(node_id: int, left_val: int, right_val: int, res: int) -> None:
            anchor = node_mobs[node_id][0].get_center() + UP * 0.72

            lx = Text(str(left_val), font="Consolas", font_size=28, color=BLUE_B).move_to(anchor + LEFT * 0.33)
            rx = Text(str(right_val), font="Consolas", font_size=28, color=ORANGE).move_to(anchor + RIGHT * 0.33)
            vs = Text("vs", font="Consolas", font_size=22, color=GRAY_A).move_to(anchor)
            grp_lr = VGroup(lx, vs, rx)
            self.play(FadeIn(grp_lr, shift=UP * 0.03), run_time=0.3)

            if left_val >= right_val:
                self.play(lx.animate.set_color(GREEN), rx.animate.set_color(GRAY_D), run_time=0.28)
                self.play(FadeOut(rx), run_time=0.18)
                kept = lx
            else:
                self.play(rx.animate.set_color(GREEN), lx.animate.set_color(GRAY_D), run_time=0.28)
                self.play(FadeOut(lx), run_time=0.18)
                kept = rx
            self.play(FadeOut(vs), run_time=0.12)

            plus_one = Text("+1", font="Consolas", font_size=24, color=WHITE)
            plus_one.next_to(kept, RIGHT, buff=0.12)
            self.play(FadeIn(plus_one, shift=RIGHT * 0.05), run_time=0.25)

            eq = Text(f"={res}", font="Consolas", font_size=24, color=YELLOW)
            eq.next_to(plus_one, RIGHT, buff=0.12)
            self.play(FadeIn(eq, shift=RIGHT * 0.05), run_time=0.3)
            self.wait(0.12)

            self.play(FadeOut(VGroup(kept, plus_one, eq)), run_time=0.24)

        def mark_best_depth_edge(node_id: int, left_val: int, right_val: int) -> None:
            left_child, right_child = children[node_id]
            if left_child is None and right_child is None:
                return
            best_child = left_child if left_val >= right_val else right_child
            if best_child is None:
                return
            key = (node_id, best_child)
            start, end = edge_endpoints[key]
            solid = Line(start, end, color=RED, stroke_width=3.8)
            self.play(Transform(edge_mobs[key], solid), run_time=0.28)

        self.play(Create(edge_group), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(node_mobs[i], scale=0.86) for i in sorted(node_mobs)], lag_ratio=0.08),
            run_time=1.05,
        )

        answer_text = Text("maxDepth = ?", font="Consolas", font_size=34, color=WHITE)
        answer_text.move_to(np.array([0.0, -2.95, 0.0]))
        self.play(FadeIn(answer_text, shift=UP * 0.08), run_time=0.3)

        def dfs(node_id: int | None) -> tuple[int, list[int]]:
            if node_id is None:
                return 0, []

            focus_node(node_id)
            left_child, right_child = children[node_id]

            if left_child is None and right_child is None:
                set_return_status(node_id, "1", color=YELLOW)
                self.wait(0.15)
                return 1, [node_id]

            ensure_side_questions(node_id)
            self.wait(0.22)
            show_subtree_hint(left_child)
            left_val, left_path = dfs(left_child)
            show_backtrack(left_child, node_id)
            focus_node(node_id, rt=0.35)
            set_side_status(node_id, "left", str(left_val), color=BLUE_B)

            self.wait(0.2)
            show_subtree_hint(right_child)
            right_val, right_path = dfs(right_child)
            show_backtrack(right_child, node_id)
            focus_node(node_id, rt=0.35)
            set_side_status(node_id, "right", str(right_val), color=ORANGE)

            res = 1 + max(left_val, right_val)
            show_merge(node_id, left_val, right_val, res)
            finalize_internal_result(node_id, res)
            mark_best_depth_edge(node_id, left_val, right_val)
            self.wait(0.08)
            best_path = [node_id] + (left_path if left_val >= right_val else right_path)
            return res, best_path

        ans, max_depth_path = dfs(1)
        focus_node(None, rt=0.35)

        final_text = Text(f"maxDepth = {ans}", font="Consolas", font_size=34, color=YELLOW)
        final_text.move_to(answer_text.get_center())
        self.play(Transform(answer_text, final_text), run_time=0.45)

        # 递归结束后，让最大深度对应路径整体闪动 5 次
        path_edge_keys = [(a, b) for a, b in zip(max_depth_path, max_depth_path[1:])]
        for _ in range(5):
            self.play(
                *[node_mobs[n][0].animate.set_fill(YELLOW_E, opacity=1.0).set_stroke(YELLOW, width=4.2) for n in max_depth_path],
                *[edge_mobs[k].animate.set_color(YELLOW).set_stroke(width=4.2) for k in path_edge_keys],
                run_time=0.14,
            )
            self.play(
                *[node_mobs[n][0].animate.set_fill(RED_E, opacity=1.0).set_stroke(RED, width=4.0) for n in max_depth_path],
                *[edge_mobs[k].animate.set_color(RED).set_stroke(width=3.8) for k in path_edge_keys],
                run_time=0.14,
            )
        self.wait(0.8)

