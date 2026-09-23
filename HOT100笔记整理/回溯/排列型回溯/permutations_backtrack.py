# -*- coding: utf-8 -*-
"""
全排列 — 回溯 DFS：排版对齐参考草图 — 根下一点三分叉；第二层三列宽间距；
第三层倒 V；叶层竖线。白线 + 蓝/红 Arrow GrowArrow。

标准 DFS 的 down/up/result 顺序不变；每次 down 前在子结点位置从 1 起枚举当前位，
重复则震动后擦掉，非本次选中则短暂显示后擦掉，选中数保留后再画白线 + 蓝箭头。

480p: ffmpeg 缩放 → PermutationBacktrackDemo_480p.mp4
"""

from __future__ import annotations

from manim import *
from manim.animation.indication import Wiggle

config.pixel_width = 1920
config.pixel_height = 1080

N_SLOT = 3
WHITE_ = "#ffffff"

# 箭头后在子结点 nxt 上做枚举时整体放慢；与用户描述的「层 / 第几个」一一对应：
# - 第二层第2、3个：1__→2__、→3__ 即 (2,) (3,)
# - 第三层第1、2个（左支倒 V）：1 1 _↔1 2 _、(1,2) 与 1 2 _↔1 3 _、(1,3)
# - 第三层第3、4个（中支）：2__→2 1 _、(2,1) 与 2 1 _↔2 2 _、(2,3)
# - 第三层第6个（右支）：3 1 _↔3 2 _、(3,2)
SLOWER_ENUM_AT_NXT: frozenset[tuple[int, ...]] = frozenset(
    {
        (2,),
        (3,),
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 3),
        (3, 2),
    }
)

ALL_STATES: set[tuple[int, ...]] = {
    (),
    (1,),
    (2,),
    (3,),
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 3),
    (3, 1),
    (3, 2),
    (1, 2, 3),
    (1, 3, 2),
    (2, 1, 3),
    (2, 3, 1),
    (3, 1, 2),
    (3, 2, 1),
}


def diagram_layout_positions() -> dict[tuple[int, ...], np.ndarray]:
    """
    与参考图一致：
    - 根在正中；第二层 1__/2__/3__ 分列左 / 中 / 右；
    - 每层下两支为倒 V（±dx）；叶与对应第三层节点同 x，竖直连上。
    """
    W = 4.42
    dx = 1.24
    y0, y1, y2, y3 = 1.82, 0.46, -0.7, -1.94
    return {
        (): np.array([0.0, y0, 0.0]),
        (1,): np.array([-W, y1, 0.0]),
        (2,): np.array([0.0, y1, 0.0]),
        (3,): np.array([W, y1, 0.0]),
        (1, 2): np.array([-W - dx, y2, 0.0]),
        (1, 3): np.array([-W + dx, y2, 0.0]),
        (2, 1): np.array([-dx, y2, 0.0]),
        (2, 3): np.array([dx, y2, 0.0]),
        (3, 1): np.array([W - dx, y2, 0.0]),
        (3, 2): np.array([W + dx, y2, 0.0]),
        (1, 2, 3): np.array([-W - dx, y3, 0.0]),
        (1, 3, 2): np.array([-W + dx, y3, 0.0]),
        (2, 1, 3): np.array([-dx, y3, 0.0]),
        (2, 3, 1): np.array([dx, y3, 0.0]),
        (3, 1, 2): np.array([W - dx, y3, 0.0]),
        (3, 2, 1): np.array([W + dx, y3, 0.0]),
    }


def make_underline_cell(
    i: int,
    st: tuple[int, ...],
    *,
    font_size: float,
    line_half_width: float,
    font: str = "Consolas",
) -> VGroup:
    line = Line(LEFT * line_half_width, RIGHT * line_half_width, stroke_width=2.0, color=WHITE_)
    if i < len(st):
        lab = Text(str(st[i]), font_size=font_size, font=font, color=WHITE_)
        lab.next_to(line, UP, buff=0.06)
        return VGroup(lab, line)
    ghost = Text("8", font_size=font_size, font=font).set_opacity(0)
    ghost.next_to(line, UP, buff=0.06)
    return VGroup(ghost, line)


def make_underline_row(
    st: tuple[int, ...],
    *,
    font_size: float,
    line_half_width: float,
    cell_buff: float,
    font: str = "Consolas",
) -> VGroup:
    row = VGroup()
    for i in range(N_SLOT):
        row.add(make_underline_cell(i, st, font_size=font_size, line_half_width=line_half_width, font=font))
    row.arrange(RIGHT, buff=cell_buff)
    return row


def middle_underline_center(row: VGroup) -> np.ndarray:
    mid_cell = row[1]
    line = mid_cell[1]
    return np.array(line.get_center())


def shorten_segment(
    a: np.ndarray,
    b: np.ndarray,
    shrink_start: float,
    shrink_end: float,
) -> tuple[np.ndarray, np.ndarray]:
    d = b - a
    L = float(np.linalg.norm(d))
    if L < 1e-5:
        return a, b
    u = d / L
    return a + u * shrink_start, b - u * shrink_end


def straight_edge_endpoints(
    parent_row: VGroup,
    child_row: VGroup,
    parent_st: tuple[int, ...],
) -> tuple[np.ndarray, np.ndarray]:
    cx, _, _ = middle_underline_center(child_row)
    end_y = float(child_row.get_top()[1]) + 0.26

    if not parent_st:
        start = np.array(parent_row.get_center()) + DOWN * 0.24
        end = np.array([float(cx), end_y, 0.0])
    elif len(parent_st) == 1:
        start = middle_underline_center(parent_row) + DOWN * 0.07
        end = np.array([float(cx), end_y, 0.0])
    else:
        start = middle_underline_center(parent_row) + DOWN * 0.07
        px = float(start[0])
        end = np.array([px, end_y, 0.0])

    return shorten_segment(start, end, 0.09, 0.15)


def make_dir_arrow(p0: np.ndarray, p1: np.ndarray, *, color: str) -> Arrow:
    arr = Arrow(
        p0,
        p1,
        buff=0,
        stroke_width=2.0,
        color=color,
        max_tip_length_to_length_ratio=0.11,
    )
    arr.set_stroke(color, width=2.0)
    arr.set_fill(color, opacity=1)
    arr.set_z_index(4)
    return arr


def paint_row_leaf_green(row: VGroup, green: str) -> None:
    for cell in row:
        for sub in cell:
            if isinstance(sub, Line):
                sub.set_stroke(green, width=2.0)
            elif isinstance(sub, Text) and sub.get_fill_opacity() > 1e-3:
                sub.set_color(green)


def row_leaf_green_anims(row: VGroup, green: str) -> list:
    anims = []
    for cell in row:
        for sub in cell:
            if isinstance(sub, Line):
                anims.append(sub.animate.set_stroke(green, width=2.0))
            elif isinstance(sub, Text) and sub.get_fill_opacity() > 1e-3:
                anims.append(sub.animate.set_color(green))
    return anims


def replace_cell_digit(
    cell: VGroup,
    value: int | None,
    *,
    font_size: float,
    color: str,
    font: str = "Consolas",
) -> Text:
    """只改某一格的数字；None 恢复为透明占位（下划线不动）。"""
    line: Line | None = None
    for m in cell:
        if isinstance(m, Line):
            line = m
            break
    assert line is not None
    for m in list(cell.submobjects):
        cell.remove(m)
    if value is None:
        lab = Text("8", font_size=font_size, font=font).set_opacity(0)
    else:
        lab = Text(str(value), font_size=font_size, font=font, color=color)
    lab.next_to(line, UP, buff=0.06)
    cell.add(lab, line)
    return lab


def gen_dfs_events(nums: list[int]) -> list[tuple]:
    n = len(nums)
    out: list[tuple] = []

    def walk(path: list[int]) -> None:
        if len(path) == n:
            out.append(("result", tuple(path)))
            return
        for x in nums:
            if x in path:
                continue
            out.append(("down", tuple(path), x))
            path.append(x)
            walk(path)
            path.pop()
            out.append(("up", tuple(path), x))

    out.append(("phase_root",))
    walk([])
    out.append(("phase_finale",))
    return out


class PermutationBacktrackDemo(Scene):
    def construct(self) -> None:
        slow = 0.7
        self.camera.background_color = BLACK

        nums = [1, 2, 3]
        events = gen_dfs_events(nums)

        C_DOWN = "#1e6fd9"
        C_UP = "#d92c2c"
        C_LEAF = "#12a34a"

        fs_title = 32
        fs_node = 22
        line_hw = 0.14
        cell_buff = 0.3

        pos_vec = diagram_layout_positions()

        t_white = 0.5 * slow
        t_arrow = 1.12 * slow
        t_node_in = 0.45 * slow
        t_leaf = 0.52 * slow
        t_pause = 0.24 * slow
        t_enum_in = 0.16 * slow
        # 重复数字：整段震动时长 + 摆动次数全局一致，避免后面视觉上比「第三层左支 1 1 _」那一下更密、更闪
        t_dup_wiggle = 1.02 * slow
        n_dup_wiggles = 3
        dup_rotation = 0.03 * TAU
        dup_scale = 1.04
        t_dup_fade_out = t_enum_in * 1.05
        t_dup_after = 0.12 * slow
        t_enum_skip = 0.11 * slow
        enum_stretch_slow = 1.68

        title = Text("nums = [1, 2, 3]", font_size=fs_title, color=WHITE_, font="Consolas")
        title.to_edge(UP, buff=0.52)

        self.play(FadeIn(title, shift=DOWN * 0.06), run_time=0.45 * slow)
        self.wait(0.2 * slow)

        def make_row_at(st: tuple[int, ...]) -> VGroup:
            row = make_underline_row(
                st,
                font_size=fs_node,
                line_half_width=line_hw,
                cell_buff=cell_buff,
            )
            row.move_to(pos_vec[st])
            row.set_z_index(2)
            return row

        node_rows: dict[tuple[int, ...], VGroup] = {}
        edge_pts: dict[tuple[tuple[int, ...], tuple[int, ...]], tuple[np.ndarray, np.ndarray]] = {}
        completed_leaves: set[tuple[int, ...]] = set()

        def child_state(parent: tuple[int, ...], num: int) -> tuple[int, ...]:
            return parent + (num,)

        def paint_all_white_except_leaves() -> None:
            for k, row in node_rows.items():
                if k in completed_leaves:
                    paint_row_leaf_green(row, C_LEAF)
                else:
                    for cell in row:
                        for sub in cell:
                            if isinstance(sub, Line):
                                sub.set_stroke(WHITE_, width=2.0)
                            elif isinstance(sub, Text) and sub.get_fill_opacity() > 1e-3:
                                sub.set_color(WHITE_)

        active_path: list[tuple[int, ...]] = []
        active_path_set: set[tuple[int, ...]] = set()

        def refresh_path_set() -> None:
            active_path_set.clear()
            active_path_set.update(active_path)

        finale_done = False

        def play_slot_enumeration_after_arrow(
            parent_tp: tuple[int, ...],
            nxt_tp: tuple[int, ...],
            chosen: int,
        ) -> VGroup:
            """白线+蓝箭头已画完：在 nxt 处 FadeIn 前缀行，再原地从 1 枚举当前位（重复震动擦掉等）。"""
            es = enum_stretch_slow if nxt_tp in SLOWER_ENUM_AT_NXT else 1.0
            te = t_enum_in * es
            tw = t_dup_wiggle * es
            tfo = te * 1.05
            ta = t_dup_after * es
            tsk = t_enum_skip * es
            twait_skip = 0.05 * slow * es
            t_row_in = t_node_in * 0.75 * (1.0 + 0.35 * (es - 1.0))

            slot_idx = len(parent_tp)
            staging = make_underline_row(
                parent_tp,
                font_size=fs_node,
                line_half_width=line_hw,
                cell_buff=cell_buff,
            )
            staging.move_to(pos_vec[nxt_tp])
            staging.set_z_index(9)
            self.add(staging)
            self.play(FadeIn(staging, shift=DOWN * 0.08), run_time=t_row_in)
            try_cell = staging[slot_idx]

            for v in nums:
                if v in parent_tp:
                    lab = replace_cell_digit(try_cell, v, font_size=fs_node, color=WHITE_)
                    self.play(FadeIn(lab, scale=0.92), run_time=te)
                    self.play(
                        Wiggle(
                            try_cell,
                            n_wiggles=n_dup_wiggles,
                            rotation_angle=dup_rotation,
                            scale_value=dup_scale,
                            run_time=tw,
                        )
                    )
                    # 与「非选中」分支一致：先淡出再从格里摘掉，避免 FadeIn(lab) 留在场景顶层与下一数字叠影
                    self.play(FadeOut(lab, scale=0.92), run_time=tfo)
                    replace_cell_digit(try_cell, None, font_size=fs_node, color=WHITE_)
                    self.remove(lab)
                    self.wait(ta)
                elif v != chosen:
                    lab = replace_cell_digit(try_cell, v, font_size=fs_node, color=WHITE_)
                    self.play(FadeIn(lab, scale=0.92), run_time=te)
                    self.wait(tsk)
                    self.play(FadeOut(lab, scale=0.95), run_time=te * 0.85)
                    replace_cell_digit(try_cell, None, font_size=fs_node, color=WHITE_)
                    self.remove(lab)
                    self.wait(twait_skip)
                else:
                    lab = replace_cell_digit(try_cell, v, font_size=fs_node, color=WHITE_)
                    self.play(FadeIn(lab, shift=DOWN * 0.05), run_time=te * 1.05)
                    break

            staging.set_z_index(2)
            return staging

        for ev in events:
            kind = ev[0]
            if kind == "phase_root":
                st_root: tuple[int, ...] = ()
                g0 = make_row_at(st_root)
                node_rows[st_root] = g0
                active_path.append(st_root)
                refresh_path_set()
                paint_all_white_except_leaves()
                self.play(FadeIn(g0, scale=0.96), run_time=0.48 * slow)
                self.wait(t_pause * 0.6)
                continue

            if kind == "down":
                _, parent, num = ev
                nxt = child_state(parent, num)

                # 仅用不可见占位算端点：先直线 + 蓝箭头，再出现排列与枚举（枚举过程不再动这条边）
                geo = make_row_at(nxt)
                geo.set_opacity(0)
                self.add(geo)

                sa, sb = straight_edge_endpoints(node_rows[parent], geo, parent)
                white = Line(sa, sb, stroke_color=WHITE_, stroke_width=2.3)
                white.set_z_index(1)
                key = (parent, nxt)
                edge_pts[key] = (sa, sb)

                active_path.append(nxt)
                refresh_path_set()
                paint_all_white_except_leaves()

                self.play(Create(white), run_time=t_white)
                arr_d = make_dir_arrow(sa, sb, color=C_DOWN)
                self.play(GrowArrow(arr_d), run_time=t_arrow * 0.58)
                self.play(FadeOut(arr_d), run_time=t_arrow * 0.42)
                self.remove(arr_d)
                self.remove(geo)

                sl = play_slot_enumeration_after_arrow(parent, nxt, num)
                node_rows[nxt] = sl
                paint_all_white_except_leaves()

                self.wait(t_pause * 0.5)
                continue

            if kind == "result":
                st_res: tuple[int, ...] = ev[1]
                completed_leaves.add(st_res)
                paint_all_white_except_leaves()
                self.play(*row_leaf_green_anims(node_rows[st_res], C_LEAF), run_time=t_leaf)
                paint_row_leaf_green(node_rows[st_res], C_LEAF)
                self.play(
                    Indicate(node_rows[st_res], scale_factor=1.05, color=C_LEAF),
                    run_time=0.72 * slow,
                )
                self.wait(t_pause * 0.65)
                paint_all_white_except_leaves()
                continue

            if kind == "up":
                _, parent_up, num_up = ev
                child_st = child_state(parent_up, num_up)
                key_u = (parent_up, child_st)
                pts = edge_pts.get(key_u)
                if pts is None:
                    continue
                sa, sb = pts

                if active_path and active_path[-1] == child_st:
                    active_path.pop()
                refresh_path_set()
                paint_all_white_except_leaves()

                arr_u = make_dir_arrow(sb, sa, color=C_UP)
                self.play(GrowArrow(arr_u), run_time=t_arrow * 0.58)
                self.play(FadeOut(arr_u), run_time=t_arrow * 0.42)
                self.remove(arr_u)

                paint_all_white_except_leaves()
                self.wait(t_pause * 0.45)
                continue

            if kind == "phase_finale" and not finale_done:
                finale_done = True
                self.wait(0.85 * slow)
                break

        self.wait(0.35 * slow)
