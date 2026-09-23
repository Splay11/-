from __future__ import annotations

from manim import *


class PathSum3TopDownDemo(Scene):
    def construct(self) -> None:
        target_sum = 8
        dfs_focus_rt = 0.28

        # 节点编号 -> (值, 左儿子, 右儿子)
        tree = {
            1: (10, 2, 3),
            2: (5, 4, 5),
            3: (-3, None, 6),
            4: (3, 7, 8),
            5: (2, None, 9),
            6: (11, None, None),
            7: (3, None, None),
            8: (-2, None, None),
            9: (1, None, None),
        }

        # 单树居中并整体下移：叶子接近下边界
        pos = {
            1: np.array([0.0, 1.70, 0.0]),
            2: np.array([-2.45, 0.30, 0.0]),
            3: np.array([2.45, 0.30, 0.0]),
            4: np.array([-3.65, -1.10, 0.0]),
            5: np.array([-1.25, -1.10, 0.0]),
            6: np.array([3.65, -1.10, 0.0]),
            7: np.array([-4.35, -2.70, 0.0]),
            8: np.array([-2.95, -2.70, 0.0]),
            9: np.array([-0.75, -2.70, 0.0]),
        }

        node_mobs: dict[int, VGroup] = {}
        edge_mobs: dict[tuple[int, int], Line] = {}
        edges_group = VGroup()
        computed_nodes: set[int] = set()
        find_call_cnt = 0

        for nid, (_, lch, rch) in tree.items():
            for ch in (lch, rch):
                if ch is None:
                    continue
                line = Line(pos[nid], pos[ch], color=GRAY, stroke_width=2.6)
                edge_mobs[(nid, ch)] = line
                edges_group.add(line)

        for nid, (val, _, _) in tree.items():
            c = Circle(radius=0.25, color=GRAY_B, stroke_width=2.8)
            c.set_fill(GRAY_E, opacity=1.0).move_to(pos[nid])
            t = Text(str(val), font_size=25, color=WHITE).move_to(c.get_center())
            node_mobs[nid] = VGroup(c, t)

        ans_value_num = 0
        ans_text = Text("ans = 0", font="Consolas", font_size=34, color=YELLOW)
        target_text = Text("target = 8", font="Consolas", font_size=34, color=WHITE)
        status_box = VGroup(ans_text, target_text).arrange(RIGHT, buff=0.9).to_edge(UP).shift(DOWN * 0.10)

        tree_group = VGroup(edges_group, *node_mobs.values())
        dfs_frame = SurroundingRectangle(tree_group, buff=0.62, color=TEAL_A, stroke_width=2.8, corner_radius=0.14)
        dfs_title = Text("dfs", font="Consolas", font_size=28, color=TEAL_A).next_to(dfs_frame, UP, buff=0.10)

        self.play(FadeIn(status_box, shift=UP * 0.08), run_time=0.45)
        self.play(Create(edges_group), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(node_mobs[i], scale=0.86) for i in sorted(node_mobs)], lag_ratio=0.08),
            run_time=1.0,
        )
        self.play(Create(dfs_frame), FadeIn(dfs_title, shift=UP * 0.05), run_time=0.38)

        def descendants(rt: int | None) -> list[int]:
            if rt is None:
                return []
            _, lch, rch = tree[rt]
            return [rt] + descendants(lch) + descendants(rch)

        def refresh_ans() -> None:
            nonlocal ans_text
            nxt = Text(f"ans = {ans_value_num}", font="Consolas", font_size=34, color=YELLOW).move_to(ans_text.get_center())
            self.play(Transform(ans_text, nxt), run_time=0.24)

        def restore_node_style(node_id: int, rt: float = 0.22) -> None:
            circle = node_mobs[node_id][0]
            if node_id in computed_nodes:
                self.play(
                    circle.animate.set_stroke(WHITE, width=2.8).set_fill(BLUE_E, opacity=1.0),
                    run_time=rt,
                )
            else:
                self.play(
                    circle.animate.set_stroke(GRAY_B, width=2.8).set_fill(GRAY_E, opacity=1.0),
                    run_time=rt,
                )

        def subtree_groups(start: int) -> tuple[VGroup, VGroup]:
            nodes = descendants(start)
            nodes_group = VGroup(*[node_mobs[nid] for nid in nodes])
            local_edges = VGroup()
            for nid in nodes:
                _, lch, rch = tree[nid]
                for ch in (lch, rch):
                    if ch is not None and ch in nodes:
                        local_edges.add(edge_mobs[(nid, ch)])
            return nodes_group, local_edges

        def run_find_target(start: int, speed_scale: float) -> None:
            nonlocal ans_value_num

            def rt(base: float) -> float:
                return base * speed_scale

            subtree_nodes = descendants(start)
            nodes_group, local_edges = subtree_groups(start)
            if len(subtree_nodes) == 1:
                frame_target = node_mobs[start][0]
                frame_buff = 0.02
            else:
                frame_target = VGroup(nodes_group, local_edges)
                frame_buff = 0.34
            find_frame = SurroundingRectangle(
                frame_target,
                buff=frame_buff,
                color=PURPLE_B,
                stroke_width=3.0,
                corner_radius=0.12,
            )
            find_title = Text("findTarget", font="Consolas", font_size=28, color=PURPLE_B).next_to(find_frame, UP, buff=0.10)
            self.play(Create(find_frame), FadeIn(find_title, shift=UP * 0.05), run_time=rt(0.45))

            # 只显示数字，不显示 "cur_sum ="
            sum_token = Text("0", font="Consolas", font_size=34, color=YELLOW)
            sum_token.move_to(node_mobs[start][0].get_right() + RIGHT * 0.64)
            self.play(FadeIn(sum_token, scale=0.92), run_time=rt(0.35))

            def token_anchor(node_id: int) -> np.ndarray:
                return node_mobs[node_id][0].get_right() + RIGHT * 0.64

            def update_sum_token(new_sum: int) -> None:
                nonlocal sum_token
                nxt = Text(str(new_sum), font="Consolas", font_size=34, color=YELLOW).move_to(sum_token.get_center())
                self.play(Transform(sum_token, nxt), run_time=rt(0.35))

            def show_hit(path_nodes: list[int]) -> None:
                nonlocal ans_value_num
                path_group = VGroup()
                for a, b in zip(path_nodes, path_nodes[1:]):
                    if (a, b) in edge_mobs:
                        path_group.add(edge_mobs[(a, b)].copy())
                    elif (b, a) in edge_mobs:
                        path_group.add(edge_mobs[(b, a)].copy())
                for nid in path_nodes:
                    path_group.add(node_mobs[nid].copy())

                fly_anchor = target_text.get_right() + RIGHT * 0.7
                self.add(path_group)
                self.play(path_group.animate.scale(0.45).move_to(fly_anchor), run_time=rt(0.58))
                self.play(
                    Flash(
                        fly_anchor,
                        color=YELLOW,
                        line_length=0.22,
                        flash_radius=0.35,
                        num_lines=14,
                    ),
                    run_time=rt(0.55),
                )
                self.play(FadeOut(path_group), run_time=rt(0.22))
                ans_value_num += 1
                refresh_ans()

            def dfs_find(node_id: int | None, parent_id: int | None, cur_sum: int, path_nodes: list[int]) -> None:
                if node_id is None:
                    return

                val, lch, rch = tree[node_id]
                new_sum = cur_sum + val
                path2 = path_nodes + [node_id]

                enter_anims = [
                    node_mobs[node_id][0].animate.set_stroke(YELLOW, width=4.0).set_fill(YELLOW_E, opacity=1.0),
                    sum_token.animate.move_to(token_anchor(node_id)),
                ]
                if parent_id is not None and (parent_id, node_id) in edge_mobs:
                    enter_anims.append(edge_mobs[(parent_id, node_id)].animate.set_color(YELLOW).set_stroke(width=3.4))
                self.play(*enter_anims, run_time=rt(0.72))
                update_sum_token(new_sum)

                if new_sum == target_sum:
                    show_hit(path2)
                    self.wait(rt(0.10))

                if lch is not None:
                    dfs_find(lch, node_id, new_sum, path2)
                    self.play(sum_token.animate.move_to(token_anchor(node_id)), run_time=rt(0.50))
                    update_sum_token(new_sum)
                if rch is not None:
                    dfs_find(rch, node_id, new_sum, path2)
                    self.play(sum_token.animate.move_to(token_anchor(node_id)), run_time=rt(0.50))
                    update_sum_token(new_sum)

                back_anims = []
                # 回溯后恢复到进入 findTarget 前的原色（灰或蓝）
                if node_id in computed_nodes:
                    back_anims.append(node_mobs[node_id][0].animate.set_stroke(WHITE, width=2.8).set_fill(BLUE_E, opacity=1.0))
                else:
                    back_anims.append(node_mobs[node_id][0].animate.set_stroke(GRAY_B, width=2.8).set_fill(GRAY_E, opacity=1.0))
                if parent_id is not None and (parent_id, node_id) in edge_mobs:
                    back_anims.append(edge_mobs[(parent_id, node_id)].animate.set_color(GRAY).set_stroke(width=2.6))
                if back_anims:
                    self.play(*back_anims, run_time=rt(0.34))

            dfs_find(start, None, 0, [])
            # findTarget 完整结束后，仅调用根节点变蓝
            if start not in computed_nodes:
                self.play(
                    node_mobs[start][0].animate.set_stroke(WHITE, width=2.8).set_fill(BLUE_E, opacity=1.0),
                    run_time=rt(0.36),
                )
            computed_nodes.add(start)
            self.play(FadeOut(sum_token), FadeOut(find_title), FadeOut(find_frame), run_time=rt(0.45))

        def mark_dfs_node(node_id: int, on: bool) -> None:
            circle = node_mobs[node_id][0]
            if on:
                self.play(
                    circle.animate.set_stroke(YELLOW_D, width=4.0),
                    run_time=dfs_focus_rt,
                )
            else:
                restore_node_style(node_id, rt=0.2)

        def show_backtrack(child_id: int, parent_id: int) -> None:
            child_center = node_mobs[child_id][0].get_center()
            parent_center = node_mobs[parent_id][0].get_center()
            start = child_center + UP * 0.10
            end = parent_center + DOWN * 0.12
            is_left = child_center[0] < parent_center[0]
            angle = PI / 3 if is_left else -PI / 3
            arrow = CurvedArrow(
                start,
                end,
                angle=angle,
                color=YELLOW_D,
                stroke_width=3.0,
                tip_length=0.17,
            )
            self.play(Create(arrow), run_time=0.35)
            self.play(FadeOut(arrow), run_time=0.2)

        def dfs_enum(node_id: int | None, parent_id: int | None) -> None:
            nonlocal find_call_cnt
            if node_id is None:
                return
            _, lch, rch = tree[node_id]

            if parent_id is not None and (parent_id, node_id) in edge_mobs:
                self.play(edge_mobs[(parent_id, node_id)].animate.set_color(YELLOW).set_stroke(width=3.3), run_time=0.28)

            mark_dfs_node(node_id, True)
            # 所有 findTarget 都使用统一加速速度
            speed_scale = 0.62
            run_find_target(node_id, speed_scale=speed_scale)
            find_call_cnt += 1
            mark_dfs_node(node_id, True)

            if lch is not None:
                dfs_enum(lch, node_id)
                show_backtrack(lch, node_id)
                mark_dfs_node(node_id, True)
            if rch is not None:
                dfs_enum(rch, node_id)
                show_backtrack(rch, node_id)
                mark_dfs_node(node_id, True)

            mark_dfs_node(node_id, False)
            if parent_id is not None and (parent_id, node_id) in edge_mobs:
                self.play(edge_mobs[(parent_id, node_id)].animate.set_color(GRAY).set_stroke(width=2.6), run_time=0.24)

        dfs_enum(1, None)
        self.wait(0.9)
