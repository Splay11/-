from __future__ import annotations

from collections import defaultdict

from manim import *


class PathSum3PrefixSumDemo(Scene):
    def construct(self) -> None:
        target = 8
        ans = 0

        # 与 path_sum3_topdown_manim.py 使用同一组样例树
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

        # 左树稍微缩紧，给右侧 cnt 面板留空间
        pos = {
            1: np.array([-3.8, 2.0, 0.0]),
            2: np.array([-5.1, 1.1, 0.0]),
            3: np.array([-2.5, 1.1, 0.0]),
            4: np.array([-5.9, 0.2, 0.0]),
            5: np.array([-4.3, 0.2, 0.0]),
            6: np.array([-2.0, 0.2, 0.0]),
            7: np.array([-6.3, -0.7, 0.0]),
            8: np.array([-5.5, -0.7, 0.0]),
            9: np.array([-3.9, -0.7, 0.0]),
        }

        node_mobs: dict[int, VGroup] = {}
        edge_mobs: dict[tuple[int, int], Line] = {}
        edges_group = VGroup()

        for nid, (_, lch, rch) in tree.items():
            for ch in (lch, rch):
                if ch is None:
                    continue
                ln = Line(pos[nid], pos[ch], color=GRAY, stroke_width=2.6)
                edge_mobs[(nid, ch)] = ln
                edges_group.add(ln)

        for nid, (val, _, _) in tree.items():
            c = Circle(radius=0.22, color=WHITE, stroke_width=2.8)
            c.set_fill(BLUE_E, opacity=1.0).move_to(pos[nid])
            t = Text(str(val), font_size=23, color=WHITE).move_to(c.get_center())
            node_mobs[nid] = VGroup(c, t)

        ans_text = Text("ans = 0", font="Consolas", font_size=34, color=YELLOW)
        target_label = Text("target =", font="Consolas", font_size=34, color=WHITE)
        target_value = Text(str(target), font="Consolas", font_size=34, color=WHITE)
        target_group = VGroup(target_label, target_value).arrange(RIGHT, buff=0.12)
        top_text = VGroup(ans_text, target_group).arrange(RIGHT, buff=0.8).to_edge(UP).shift(DOWN * 0.15)

        # 右侧 cnt 面板
        cnt_rect = RoundedRectangle(
            corner_radius=0.12,
            width=4.7,
            height=4.0,
            stroke_color=TEAL_A,
            stroke_width=2.8,
        ).set_fill(BLACK, opacity=0.06)
        cnt_rect.move_to(np.array([3.6, 0.35, 0.0]))
        cnt_title = Text("cnt（路径前缀和 : 出现次数）", font="Microsoft YaHei", font_size=20, color=TEAL_A)
        cnt_title.next_to(cnt_rect, UP, buff=0.12)

        self.play(FadeIn(top_text, shift=UP * 0.08), run_time=0.4)
        self.play(Create(edges_group), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(node_mobs[i], scale=0.9) for i in sorted(node_mobs)], lag_ratio=0.07),
            run_time=0.95,
        )
        self.play(Create(cnt_rect), FadeIn(cnt_title, shift=UP * 0.03), run_time=0.45)

        cnt = defaultdict(int)
        cnt[0] = 1
        prefix_paths: dict[int, list[str]] = defaultdict(list)
        prefix_paths[0].append("()")
        cnt_order: list[int] = [0]  # 按“首次加入”顺序展示，不按 key 排序
        cnt_rows_group: VGroup | None = None
        cnt_row_map: dict[int, Mobject] = {}

        def refresh_ans() -> None:
            nonlocal ans_text
            nxt = Text(f"ans = {ans}", font="Consolas", font_size=34, color=YELLOW).move_to(ans_text.get_center())
            self.play(Transform(ans_text, nxt), run_time=0.22)

        def build_cnt_rows() -> tuple[VGroup, dict[int, Mobject]]:
            keys = [k for k in cnt_order if cnt.get(k, 0) > 0][:12]
            rows = VGroup()
            row_map: dict[int, Mobject] = {}
            start_y = cnt_rect.get_top()[1] - 0.7
            x = cnt_rect.get_left()[0] + 0.25
            for i, k in enumerate(keys):
                y = start_y - i * 0.42
                path_str = prefix_paths[k][-1] if prefix_paths[k] else "()"
                row = Text(f"{k:>4} : {cnt[k]}  ({path_str})", font="Consolas", font_size=18, color=WHITE)
                row.move_to(np.array([x, y, 0.0]), aligned_edge=LEFT)
                rows.add(row)
                row_map[k] = row
            return rows, row_map

        def refresh_cnt(rt: float = 0.22) -> None:
            nonlocal cnt_rows_group, cnt_row_map
            new_group, new_map = build_cnt_rows()
            if cnt_rows_group is None:
                self.play(FadeIn(new_group, shift=UP * 0.03), run_time=rt)
            else:
                self.play(FadeOut(cnt_rows_group), FadeIn(new_group), run_time=rt)
            cnt_rows_group = new_group
            cnt_row_map = new_map

        refresh_cnt(rt=0.25)

        s_token = Text("0", font="Consolas", font_size=30, color=YELLOW)
        s_token.move_to(node_mobs[1][0].get_right() + RIGHT * 0.72)
        self.play(FadeIn(s_token, scale=0.9), run_time=0.3)

        path_nodes: list[int] = []
        prefix_sums: list[int] = [0]  # prefix_sums[i] 是 path_nodes 前 i 个节点的和

        def update_s_token(node_id: int, cur_sum: int) -> None:
            target_pos = node_mobs[node_id][0].get_right() + RIGHT * 0.72
            self.play(s_token.animate.move_to(target_pos), run_time=0.32)
            nxt = Text(str(cur_sum), font="Consolas", font_size=30, color=YELLOW).move_to(s_token.get_center())
            self.play(Transform(s_token, nxt), run_time=0.22)

        def blink_path_three_times(need: int) -> None:
            # 找到所有满足 prefix == need 的起点，合并需要闪烁的节点和边
            highlight_nodes: set[int] = set()
            highlight_edges: set[tuple[int, int]] = set()
            k = len(path_nodes)
            for i in range(k):
                if prefix_sums[i] != need:
                    continue
                seg = path_nodes[i:]
                for nid in seg:
                    highlight_nodes.add(nid)
                for a, b in zip(seg, seg[1:]):
                    if (a, b) in edge_mobs:
                        highlight_edges.add((a, b))
                    elif (b, a) in edge_mobs:
                        highlight_edges.add((b, a))

            if not highlight_nodes:
                return

            # 当前 DFS 路径边集合：闪烁结束后应恢复为黄色而不是灰色
            path_edge_set: set[tuple[int, int]] = set()
            for a, b in zip(path_nodes, path_nodes[1:]):
                if (a, b) in edge_mobs:
                    path_edge_set.add((a, b))
                elif (b, a) in edge_mobs:
                    path_edge_set.add((b, a))

            for _ in range(3):
                self.play(
                    *[node_mobs[nid][0].animate.set_stroke(RED_D, width=4.2).set_fill(RED_E, opacity=1.0) for nid in highlight_nodes],
                    *[edge_mobs[e].animate.set_color(RED_D).set_stroke(width=4.0) for e in highlight_edges],
                    run_time=0.18,
                )
                self.play(
                    *[node_mobs[nid][0].animate.set_stroke(YELLOW_D, width=4.0).set_fill(BLUE_E, opacity=1.0) for nid in highlight_nodes if nid in path_nodes],
                    *[node_mobs[nid][0].animate.set_stroke(WHITE, width=2.8).set_fill(BLUE_E, opacity=1.0) for nid in highlight_nodes if nid not in path_nodes],
                    *[
                        edge_mobs[e].animate.set_color(YELLOW_D).set_stroke(width=3.3)
                        if e in path_edge_set
                        else edge_mobs[e].animate.set_color(GRAY).set_stroke(width=2.6)
                        for e in highlight_edges
                    ],
                    run_time=0.18,
                )

        def show_need_and_check(cur_sum: int, need: int) -> None:
            formula_anchor = np.array([-0.5, -2.75, 0.0])
            lead = Text("s-target =", font="Consolas", font_size=30, color=WHITE).move_to(formula_anchor)
            self.play(FadeIn(lead, shift=UP * 0.03), run_time=0.16)

            s_num = Text(str(cur_sum), font="Consolas", font_size=30, color=YELLOW)
            s_num.move_to(s_token.get_center())
            s_slot = lead.get_right() + RIGHT * 0.35
            self.add(s_num)
            self.play(s_num.animate.move_to(s_slot), run_time=0.28)

            minus = Text("-", font="Consolas", font_size=30, color=WHITE).move_to(s_slot + RIGHT * 0.42)
            self.play(FadeIn(minus), run_time=0.12)

            t_num = Text(str(target), font="Consolas", font_size=30, color=WHITE).move_to(target_value.get_center())
            t_slot = minus.get_right() + RIGHT * 0.35
            self.add(t_num)
            self.play(t_num.animate.move_to(t_slot), run_time=0.28)

            eq = Text("=", font="Consolas", font_size=30, color=WHITE).move_to(t_slot + RIGHT * 0.42)
            self.play(FadeIn(eq), run_time=0.12)

            result = Text(str(need), font="Consolas", font_size=30, color=ORANGE).move_to(eq.get_right() + RIGHT * 0.38)
            self.play(FadeIn(result, shift=UP * 0.02), run_time=0.15)

            self.play(FadeOut(VGroup(lead, s_num, minus, t_num, eq)), run_time=0.14)

            if cnt.get(need, 0) > 0 and need in cnt_row_map:
                self.play(result.animate.move_to(cnt_row_map[need].get_left() + RIGHT * 0.18), run_time=0.32)
                hit_box = SurroundingRectangle(
                    cnt_row_map[need],
                    buff=0.06,
                    color=YELLOW,
                    stroke_width=3.0,
                    corner_radius=0.06,
                )
                self.play(Create(hit_box), run_time=0.22)
                blink_path_three_times(need)
                self.play(FadeOut(hit_box), run_time=0.15)
            self.play(FadeOut(result), run_time=0.12)

        def fly_current_path_to_cnt_box(target_idx: int) -> None:
            # 把当前递归路径复制一份飞到“将新增的那一行”位置
            if not path_nodes:
                return
            g = VGroup()
            for a, b in zip(path_nodes, path_nodes[1:]):
                if (a, b) in edge_mobs:
                    g.add(edge_mobs[(a, b)].copy())
                elif (b, a) in edge_mobs:
                    g.add(edge_mobs[(b, a)].copy())
            for nid in path_nodes:
                g.add(node_mobs[nid].copy())

            start_y = cnt_rect.get_top()[1] - 0.7
            row_y = start_y - target_idx * 0.42
            row_x = cnt_rect.get_left()[0] + 1.15
            target = np.array([row_x, row_y, 0.0])
            self.add(g)
            self.play(g.animate.scale(0.32).move_to(target), run_time=0.45)
            self.play(FadeOut(g), run_time=0.14)

        def dfs(node_id: int | None, cur_sum: int) -> None:
            nonlocal ans
            if node_id is None:
                return

            val, lch, rch = tree[node_id]
            path_nodes.append(node_id)
            cur_sum += val
            prefix_sums.append(cur_sum)
            path_str = "->".join(str(tree[nid][0]) for nid in path_nodes)

            # 进入节点动画
            enter_anims = [node_mobs[node_id][0].animate.set_stroke(YELLOW_D, width=4.0)]
            if len(path_nodes) >= 2:
                p = path_nodes[-2]
                if (p, node_id) in edge_mobs:
                    enter_anims.append(edge_mobs[(p, node_id)].animate.set_color(YELLOW_D).set_stroke(width=3.3))
            self.play(*enter_anims, run_time=0.34)
            update_s_token(node_id, cur_sum)

            need = cur_sum - target
            show_need_and_check(cur_sum, need)

            ans += cnt[need]
            if cnt[need] > 0:
                refresh_ans()

            is_new_prefix = cnt[cur_sum] == 0
            if is_new_prefix:
                active_keys = [k for k in cnt_order if cnt.get(k, 0) > 0]
                fly_current_path_to_cnt_box(target_idx=len(active_keys))

            cnt[cur_sum] += 1
            prefix_paths[cur_sum].append(path_str)
            if cnt[cur_sum] == 1:
                cnt_order.append(cur_sum)
            refresh_cnt(rt=0.2)

            if lch is None and rch is None:
                # 叶子节点计算完成后，停留 0.5s 再回溯
                self.wait(0.5)

            dfs(lch, cur_sum)
            if lch is not None:
                update_s_token(node_id, cur_sum)
            dfs(rch, cur_sum)
            if rch is not None:
                update_s_token(node_id, cur_sum)

            # 回溯：撤销当前前缀和
            deleting_row = cnt.get(cur_sum, 0) == 1 and cur_sum in cnt_row_map
            if deleting_row:
                # 先在将被删除的项上打红色 ×，再删掉该项
                row_to_delete = cnt_row_map[cur_sum]
                cross = Text("×", font="Microsoft YaHei", font_size=34, color=RED_D)
                cross.move_to(row_to_delete.get_right() + LEFT * 0.12)
                self.play(FadeIn(cross, scale=0.8), run_time=0.2)
                self.wait(0.3)

            cnt[cur_sum] -= 1
            if prefix_paths[cur_sum]:
                prefix_paths[cur_sum].pop()
            if not prefix_paths[cur_sum]:
                del prefix_paths[cur_sum]
            if cnt[cur_sum] == 0:
                del cnt[cur_sum]
                if cur_sum in cnt_order:
                    cnt_order.remove(cur_sum)
            # 删除动画放慢一点，再进行向上回溯
            refresh_cnt(rt=0.38)
            if deleting_row:
                self.play(FadeOut(cross), run_time=0.14)

            leave_anims = [node_mobs[node_id][0].animate.set_stroke(WHITE, width=2.8).set_fill(BLUE_E, opacity=1.0)]
            if len(path_nodes) >= 2:
                p = path_nodes[-2]
                if (p, node_id) in edge_mobs:
                    leave_anims.append(edge_mobs[(p, node_id)].animate.set_color(GRAY).set_stroke(width=2.6))
            self.play(*leave_anims, run_time=0.24)

            path_nodes.pop()
            prefix_sums.pop()

        dfs(1, 0)
        self.play(FadeOut(s_token), run_time=0.2)
        self.wait(0.9)
