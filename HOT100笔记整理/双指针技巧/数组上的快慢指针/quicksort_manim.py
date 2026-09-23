"""快速排序（Lomuto 分区）+ 递归树可视化：左右分屏，中央虚线分隔。

运行（画质）：`-ql` 为 480p/15fps，全屏容易糊；需要清晰请用 `-qh` 或 `-qm`。

  全屏推荐（1080p / 60fps，较慢）:
    .\\manim-env\\Scripts\\manim.exe -pqh quicksort_manim.py QuickSortTree
  折中（720p / 30fps）:
    .\\manim-env\\Scripts\\manim.exe -pqm quicksort_manim.py QuickSortTree
  快速试渲（较糊）:
    .\\manim-env\\Scripts\\manim.exe -pql quicksort_manim.py QuickSortTree

初始数组 [3,1,7,2,4,5]，分区逻辑与题述代码一致。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from manim import *


DATA = [3, 1, 7, 2, 4, 5]


@dataclass
class TraceState:
    events: list[dict[str, Any]] = field(default_factory=list)

    def emit(self, **ev: Any) -> None:
        self.events.append(ev)


def quick_sort_record(st: TraceState, a: list[int], l: int, r: int, path: tuple[str, ...]) -> None:
    st.emit(
        type="enter",
        a=a.copy(),
        l=l,
        r=r,
        path=path,
    )
    if l >= r:
        st.emit(type="base", a=a.copy(), l=l, r=r, path=path)
        return

    st.emit(type="pivot_pick", a=a.copy(), l=l, r=r, piv=r, path=path)
    x = a[r]
    i = l
    for j in range(l, r):
        st.emit(
            type="j_scan",
            a=a.copy(),
            l=l,
            r=r,
            i=i,
            j=j,
            piv=r,
            x=x,
            path=path,
        )
        if a[j] <= x:
            st.emit(type="swap_ij", a=a.copy(), l=l, r=r, i=i, j=j, piv=r, path=path)
            a[i], a[j] = a[j], a[i]
            i += 1
            st.emit(type="after_swap", a=a.copy(), l=l, r=r, i=i, j=j, piv=r, path=path)

    st.emit(type="pivot_final", a=a.copy(), l=l, r=r, i=i, piv=r, path=path)
    a[i], a[r] = a[r], a[i]
    st.emit(type="partition_done", a=a.copy(), l=l, r=r, piv_idx=i, path=path)

    quick_sort_record(st, a, l, i - 1, path + ("L",))
    quick_sort_record(st, a, i + 1, r, path + ("R",))


def build_trace() -> list[dict[str, Any]]:
    st = TraceState()
    quick_sort_record(st, list(DATA), 0, len(DATA) - 1, ())
    return st.events


class QuickSortTree(Scene):
    def construct(self) -> None:
        events = build_trace()
        n = len(DATA)
        max_tree_depth = max(len(ev.get("path", ())) for ev in events)

        # 左右分屏：左侧递归树，右侧数组；x=0 为中央分隔虚线
        LEFT_CX = -2.95
        ARRAY_CX = 3.35
        tree_step = min(0.58, 2.25 / max(1, max_tree_depth))
        # 根到第一层子节点的水平步长按 2^(md-1) 最大，容易把整棵树拉爆宽；首层单独收拢
        first_hop_scale = 0.48

        def tree_pos(path: tuple[str, ...]) -> np.ndarray:
            depth = len(path)
            y = 2.12 - depth * 0.9
            md = max_tree_depth
            x = 0.0
            for idx, p in enumerate(path):
                power = max(0, md - 1 - idx)
                span = tree_step * (2**power)
                if idx == 0:
                    span *= first_hop_scale
                x += (-span if p == "L" else span)
            return np.array([LEFT_CX + x, y, 0.0])

        cell_w, cell_h = 0.72, 0.82
        gap = 0.05
        spacing = cell_w + gap
        start_x = -(n - 1) * spacing / 2

        array_center = DOWN * 0.35

        cells = VGroup()
        texts = VGroup()
        idx_labels = VGroup()
        for k in range(n):
            box = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.08,
                color=GRAY_B,
                stroke_width=2,
            )
            t = Text(str(DATA[k]), font_size=30)
            box.move_to(RIGHT * (start_x + k * spacing) + array_center)
            t.move_to(box.get_center())
            il = Text(str(k), font_size=20, color=GRAY).next_to(box, DOWN, buff=0.22)
            cells.add(box)
            texts.add(t)
            idx_labels.add(il)

        array_g = VGroup(cells, texts, idx_labels)
        array_g.move_to(np.array([ARRAY_CX, array_g.get_center()[1], 0.0]))

        yr = config.frame_y_radius
        screen_divider = DashedLine(
            np.array([0.0, yr - 0.15, 0.0]),
            np.array([0.0, -yr + 0.15, 0.0]),
            color=GRAY,
            stroke_width=2.8,
            dash_length=0.14,
            dashed_ratio=0.5,
        )
        screen_divider.set_z_index(-2)

        def col_x(k: int) -> float:
            return array_g.get_center()[0] + start_x + k * spacing

        lr_y = cells[0].get_bottom()[1] - 0.62
        j_y = cells[0].get_top()[1] + 0.62
        i_y = cells[0].get_bottom()[1] - 0.12

        def bracket_lr(l: int, r: int) -> VGroup:
            g = VGroup()
            lab_l = Text("l", color=GREEN, font_size=30)
            lab_r = Text("r", color=ORANGE, font_size=30)
            al = Arrow(
                np.array([col_x(l), lr_y, 0.0]),
                np.array([col_x(l), cells[l].get_bottom()[1] - 0.06, 0.0]),
                buff=0.0,
                color=GREEN,
                stroke_width=2.5,
            )
            ar = Arrow(
                np.array([col_x(r), lr_y, 0.0]),
                np.array([col_x(r), cells[r].get_bottom()[1] - 0.06, 0.0]),
                buff=0.0,
                color=ORANGE,
                stroke_width=2.5,
            )
            lab_l.next_to(al.get_start(), DOWN, buff=0.06)
            lab_r.next_to(ar.get_start(), DOWN, buff=0.06)
            g.add(lab_l, lab_r, al, ar)
            return g

        def j_ptr(j: int) -> VGroup:
            tip = np.array([col_x(j), cells[j].get_top()[1] + 0.08, 0.0])
            base = np.array([col_x(j), j_y, 0.0])
            ar = Arrow(base, tip, buff=0.0, color=RED, stroke_width=2.5)
            lab = Text("j", font_size=32, color=RED).next_to(ar.get_start(), UP, buff=0.06)
            return VGroup(lab, ar)

        def i_ptr(i: int) -> VGroup:
            tip = np.array([col_x(i), cells[i].get_bottom()[1] - 0.06, 0.0])
            base = np.array([col_x(i), i_y, 0.0])
            ar = Arrow(base, tip, buff=0.0, color=BLUE, stroke_width=2.5)
            lab = Text("i", font_size=32, color=BLUE).next_to(ar.get_start(), DOWN, buff=0.06)
            return VGroup(lab, ar)

        def range_shade(l: int, r: int) -> VGroup:
            left = cells[l].get_left()[0] - 0.04
            right = cells[r].get_right()[0] + 0.04
            top = cells[0].get_top()[1] + 0.12
            bot = cells[0].get_bottom()[1] - 0.12
            rect = Rectangle(
                width=right - left,
                height=top - bot,
                fill_color=YELLOW,
                fill_opacity=0.12,
                stroke_width=0,
            ).move_to(np.array([(left + right) / 2, (top + bot) / 2, 0.0]))
            return VGroup(rect)

        tree_root = VGroup()
        self.add(tree_root)
        node_mobs: dict[tuple[str, ...], VGroup] = {}
        edge_mobs: list[Line] = []

        def tree_node_mob(path: tuple[str, ...], l: int, r: int) -> VGroup:
            lab = Text(f"({l},{r})", font_size=26)
            box = SurroundingRectangle(lab, buff=0.18, corner_radius=0.1, color=WHITE, stroke_width=2)
            g = VGroup(box, lab)
            g.move_to(tree_pos(path))
            return g

        def connect_parent_child(p_child: tuple[str, ...]) -> Line | None:
            if not p_child:
                return None
            p_parent = p_child[:-1]
            if p_parent not in node_mobs or p_child not in node_mobs:
                return None
            a0 = node_mobs[p_parent][0].get_bottom()
            b0 = node_mobs[p_child][0].get_top()
            return Line(a0, b0, color=GRAY, stroke_width=2)

        shade_mob: VGroup | None = None
        lr_mob: VGroup | None = None
        j_mob: VGroup | None = None
        i_mob: VGroup | None = None
        pivot_hint_mob: VGroup | None = None

        def clear_partition_ui() -> None:
            nonlocal shade_mob, lr_mob, j_mob, i_mob, pivot_hint_mob
            to_fade = [m for m in (shade_mob, lr_mob, j_mob, i_mob, pivot_hint_mob) if m is not None]
            if to_fade:
                self.play(*[FadeOut(m) for m in to_fade], run_time=0.25)
            shade_mob = lr_mob = j_mob = i_mob = pivot_hint_mob = None

        def pivot_hint_at(piv: int) -> VGroup:
            tip = np.array([col_x(piv), cells[piv].get_top()[1] + 0.06, 0.0])
            base = np.array([col_x(piv), cells[piv].get_top()[1] + 1.05, 0.0])
            ar = Arrow(
                base,
                tip,
                buff=0.0,
                color=RED,
                stroke_width=3,
            )
            lab = Text("基准值", font_size=30, color=RED).next_to(ar.get_start(), UP, buff=0.08)
            return VGroup(lab, ar)

        def dashed_partition_line(piv_idx: int) -> DashedLine:
            y_top = cells[0].get_top()[1] + 0.28
            y_bot = idx_labels[0].get_bottom()[1] - 0.12
            if piv_idx < n - 1:
                x = 0.5 * (cells[piv_idx].get_right()[0] + cells[piv_idx + 1].get_left()[0])
            else:
                x = cells[piv_idx].get_right()[0] + 0.08
            return DashedLine(
                np.array([x, y_top, 0.0]),
                np.array([x, y_bot, 0.0]),
                color=WHITE,
                stroke_width=2.5,
                dash_length=0.1,
                dashed_ratio=0.55,
            )

        def stroke_all_gray_except_pivot(piv: int):
            anims = []
            for k in range(n):
                if k == piv:
                    anims.append(cells[k].animate.set_stroke(RED, width=5))
                else:
                    anims.append(cells[k].animate.set_stroke(GRAY_B, width=2))
            return anims

        def apply_array_values(vals: list[int]) -> Animation:
            anims = []
            for k in range(n):
                nt = Text(str(vals[k]), font_size=30).move_to(cells[k].get_center())
                anims.append(Transform(texts[k], nt))
            return AnimationGroup(*anims, lag_ratio=0.02)

        self.play(Create(screen_divider), FadeIn(array_g, shift=LEFT * 0.2), run_time=0.45)
        self.wait(0.12)

        seen_paths: set[tuple[str, ...]] = set()

        for ev in events:
            t = ev["type"]
            path = ev.get("path", ())

            if t == "enter":
                l, r = ev["l"], ev["r"]
                if path not in seen_paths:
                    seen_paths.add(path)
                    nm = tree_node_mob(path, l, r)
                    node_mobs[path] = nm
                    tree_root.add(nm)
                    ln = connect_parent_child(path)
                    if ln:
                        edge_mobs.append(ln)
                        tree_root.add(ln)
                        self.play(FadeIn(nm, shift=DOWN * 0.15), Create(ln), run_time=0.35)
                    else:
                        self.play(FadeIn(nm, shift=DOWN * 0.15), run_time=0.35)

                if shade_mob:
                    self.play(FadeOut(shade_mob), run_time=0.15)
                shade_mob = range_shade(l, r)
                if lr_mob:
                    self.play(FadeOut(lr_mob), run_time=0.12)
                lr_mob = bracket_lr(l, r)
                self.play(FadeIn(shade_mob), FadeIn(lr_mob), run_time=0.28)
                self.wait(0.08)

            elif t == "base":
                p = ev["path"]
                if p in node_mobs:
                    self.play(node_mobs[p][0].animate.set_stroke(GRAY, width=2), run_time=0.2)
                    self.wait(0.12)

            elif t == "pivot_pick":
                l, r, piv = ev["l"], ev["r"], ev["piv"]
                pivot_hint_mob = pivot_hint_at(piv)
                self.play(FadeIn(pivot_hint_mob, shift=DOWN * 0.12), run_time=0.38)
                self.wait(0.18)
                self.play(
                    apply_array_values(ev["a"]),
                    *stroke_all_gray_except_pivot(piv),
                    run_time=0.42,
                )
                self.wait(0.12)
                self.play(FadeOut(pivot_hint_mob), run_time=0.22)
                pivot_hint_mob = None
                if j_mob:
                    self.play(FadeOut(j_mob), run_time=0.12)
                if i_mob:
                    self.play(FadeOut(i_mob), run_time=0.12)
                j_mob = j_ptr(l)
                i_mob = i_ptr(l)
                self.play(FadeIn(j_mob), FadeIn(i_mob), run_time=0.25)

            elif t == "j_scan":
                new_j = j_ptr(ev["j"])
                if j_mob is None:
                    j_mob = new_j
                    self.play(FadeIn(j_mob), run_time=0.2)
                else:
                    self.play(Transform(j_mob, new_j), run_time=0.22)
                new_i = i_ptr(ev["i"])
                if i_mob is None:
                    i_mob = new_i
                    self.play(FadeIn(i_mob), run_time=0.18)
                else:
                    self.play(Transform(i_mob, new_i), run_time=0.18)
                self.wait(0.03)

            elif t == "swap_ij":
                piv = ev["piv"]
                self.play(
                    cells[ev["i"]].animate.set_stroke(YELLOW, width=3),
                    cells[ev["j"]].animate.set_stroke(YELLOW, width=3),
                    cells[piv].animate.set_stroke(RED, width=5),
                    run_time=0.15,
                )

            elif t == "after_swap":
                piv = ev["piv"]
                anims = [
                    apply_array_values(ev["a"]),
                    cells[ev["i"]].animate.set_stroke(GRAY_B, width=2),
                    cells[ev["j"]].animate.set_stroke(GRAY_B, width=2),
                    cells[piv].animate.set_stroke(RED, width=5),
                ]
                self.play(*anims, run_time=0.32)

            elif t == "pivot_final":
                piv = ev["piv"]
                self.play(
                    cells[ev["i"]].animate.set_stroke(YELLOW, width=3.5),
                    cells[piv].animate.set_stroke(YELLOW, width=3.5),
                    run_time=0.18,
                )

            elif t == "partition_done":
                piv_idx = ev["piv_idx"]
                div_line = dashed_partition_line(piv_idx)
                self.play(
                    apply_array_values(ev["a"]),
                    *[cells[k].animate.set_stroke(GRAY_B, width=2) for k in range(n)],
                    Create(div_line),
                    run_time=0.45,
                )
                self.wait(0.22)
                self.play(FadeOut(div_line), run_time=0.28)
                clear_partition_ui()

        self.wait(0.6)
