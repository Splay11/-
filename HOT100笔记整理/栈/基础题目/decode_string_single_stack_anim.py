# -*- coding: utf-8 -*-
"""
Decode String（单栈写法）— 过程演示（Manim）

样例 `3[a]2[b2[cd]]` → `aaabcdcdbcdcd`；黑底、无旁白与大段题面说明。
**左侧**为 `stack` 托盘（**封闭端在左、开口朝右**，托盘宽比基础多一格；栈底在左，栈顶向右靠近开口）；**右侧**为输入串白框 + 黄扫描框 + 红箭头（串在**右下区域**；箭头在格子**下方**，尖端朝上）。右侧格与过程区格**经开口外点**再入栈，与出栈折线对称。
遍历串时：**当前格整体飞入栈**（不在右侧保留副本）；遇 `]` 时出栈：先收拢栈；若过程区已有字符则先归位；新块路径为 **出开口 → 沿开口外竖直下到过道（高于已放好的一行）→ 在过道水平对齐列 → 再落下到 proc_y**。子串在过程区先按 **弹出顺序** 从左排开（与 `now_str +=` 一致），再播一次 **重排** 对应 `now_str[::-1]`（含两个相同字符如 `cc` 时用弧线强调「翻转」）。展开时预览行 **从左到右** 各段 `now_str` **直接**刚性压入栈（不整行消失再新建）；仅 **两个相同字符** 时先淡出预览再按 **先右后左** 单字飞入。右侧字符入栈时黄框与箭头与飞入同一段淡出。`[` 仅在栈顶缩小消失。

画布 16:9；默认 480p。`DECODE_STRING_SS_RES=1080p` 可切高清。

渲染:
  480p: manim-env2\\Scripts\\python.exe -m manim decode_string_single_stack_anim.py DecodeStringSingleStackAnim -ql
"""

from __future__ import annotations

import os
import numpy as np

from manim import *
from manim.animation.movement import MoveAlongPath
from manim.utils.rate_functions import ease_out_sine, smooth

_res = (os.environ.get("DECODE_STRING_SS_RES") or "480p").strip().lower()
if _res in ("1080", "1080p", "fhd", "1920"):
    config.pixel_width = 1920
    config.pixel_height = 1080
else:
    config.pixel_width = 854
    config.pixel_height = 480
config.frame_rate = 30


def _make_char_box(ch: str, *, box_w: float, box_h: float, fs: int, stroke_w: float = 2.6) -> VGroup:
    r = Rectangle(
        width=box_w,
        height=box_h,
        color=WHITE,
        stroke_width=stroke_w,
        fill_opacity=0,
    )
    t = Text(str(ch), font_size=fs, color=WHITE, font="Arial", disable_ligatures=True)
    g = VGroup(r, t)
    g.border = r  # type: ignore[attr-defined]
    g.val_text = t  # type: ignore[attr-defined]
    return g


class DecodeStringSingleStackAnim(Scene):
    def construct(self) -> None:
        self.camera.background_color = BLACK

        YELLOW_HL = "#ffcc00"
        RED_ARROW = "#a81818"
        slow = 1.46
        # 所有「格子位移动画」相对原 run_time 再快 1.5 倍（run_time ÷ mv）
        mv = 1.5
        # 极短 wait 会低于 1 帧被 Manim 抬升，这里统一用下限避免无意义卡顿与告警
        gap_s = max(1.08 / float(config.frame_rate), 0.055 * slow / mv)

        s = "3[a]2[b2[cd]]"
        BOX_W, BOX_H = 0.54, 0.48
        CHAR_FS = 28
        stroke_box = 2.4
        gap = 0.06
        step = BOX_W + gap

        # ---------- 右侧：输入串（固定槽位，便于高亮与箭头） ----------
        # 右下角方向：更靠下、更靠右（仍 clamp 在画面内）
        right_y = -0.62
        _nch = max(len(s), 1)
        _span = (_nch - 1) * step
        _right_row_cx = 3.05
        right_x0 = _right_row_cx - _span / 2.0
        _half_fw = float(config.frame_width) / 2.0 - 0.32
        _right_edge = right_x0 + _span + BOX_W / 2.0
        if _right_edge > _half_fw:
            right_x0 -= _right_edge - _half_fw
        char_cells: list[VGroup] = []
        for i, ch in enumerate(s):
            c = _make_char_box(ch, box_w=BOX_W, box_h=BOX_H, fs=CHAR_FS, stroke_w=stroke_box)
            c.move_to([right_x0 + i * step, right_y, 0])
            c.set_z_index(6)
            char_cells.append(c)

        slot_centers: list[np.ndarray] = [np.array(c.get_center(), dtype=float) for c in char_cells]

        def char_center(i: int) -> np.ndarray:
            return slot_centers[i].copy()

        yellow_frame = Rectangle(
            width=BOX_W * 1.06,
            height=BOX_H * 1.08,
            color=YELLOW_HL,
            stroke_width=3.4,
            fill_opacity=0,
        ).set_z_index(14)

        # 箭头在格子**几何下方**：尾在下、尖在上贴近格子底边；显式 tip_length 避免尖端消失
        idx_arrow = Arrow(
            np.array([0.0, -1.0, 0.0]),
            np.array([0.0, -0.2, 0.0]),
            color=RED_ARROW,
            stroke_width=4.0,
            buff=0.0,
            tip_length=0.22,
            max_tip_length_to_length_ratio=0.35,
        ).set_z_index(15)

        def span_yellow(i0: int, i1_exclusive: int) -> None:
            mid_x = (char_center(i0)[0] + char_center(i1_exclusive - 1)[0]) / 2
            w = (i1_exclusive - i0) * BOX_W + (i1_exclusive - i0 - 1) * gap + 0.08
            yellow_frame.set(width=w, height=BOX_H * 1.08)
            yellow_frame.move_to([mid_x, right_y, 0])

        def move_index_arrow(i: int) -> None:
            base = char_center(i)
            tip = base + DOWN * (BOX_H * 0.5 + 0.06)
            tail = base + DOWN * (BOX_H * 0.5 + 0.72)
            idx_arrow.put_start_and_end_on(tail, tip)

        idx_group = idx_arrow

        # ---------- 左侧：stack 托盘（左封闭、右开口）+ 过程区 ----------
        # 略向左上挪，避免与右侧输入串拥挤、重叠
        _stack_dx = -0.55
        _stack_dy = 0.36
        tray_left = -6.15 + _stack_dx
        # 托盘向右再延长一格，容纳更长栈串
        tray_right = -0.72 + _stack_dx + step
        tray_h = 0.76
        stack_y = 1.35 + _stack_dy
        proc_y = -1.55 + _stack_dy

        def make_tray(y: float) -> VGroup:
            y_top = y + tray_h / 2
            y_bot = y - tray_h / 2
            top = Line(
                np.array([tray_left, y_top, 0]),
                np.array([tray_right, y_top, 0]),
                color=WHITE,
                stroke_width=3.0,
            )
            bot = Line(
                np.array([tray_left, y_bot, 0]),
                np.array([tray_right, y_bot, 0]),
                color=WHITE,
                stroke_width=3.0,
            )
            left_wall = Line(
                np.array([tray_left, y_bot, 0]),
                np.array([tray_left, y_top, 0]),
                color=WHITE,
                stroke_width=3.0,
            )
            return VGroup(top, bot, left_wall).set_z_index(1)

        tray_stack = make_tray(stack_y)
        lbl_stack = Text(
            "stack",
            font_size=22,
            color=WHITE,
            font="Arial",
            disable_ligatures=True,
        ).next_to(tray_stack, UP, buff=0.12).set_z_index(6)

        def y_stack_row(y_tray: float) -> float:
            return float(y_tray - tray_h / 2 + BOX_H * 0.5 + 0.06)

        stack_row_y = y_stack_row(stack_y)
        # 栈底在左（封闭端）；栈顶向右（开口侧）；索引增大 = 更靠右 = 栈顶
        stack_left_cx = float(tray_left + 0.14 + BOX_W * 0.5)

        def stack_slot_center(i: int, n: int) -> np.ndarray:
            x = stack_left_cx + i * step
            return np.array([x, stack_row_y, 0.0])

        proc_cx = float((tray_left + tray_right) / 2)

        t_slot = 1.0 * slow / mv
        t_expand_push = t_slot
        # 弹出：栈收拢与「出栈块」轨迹分离
        t_repack_after_pop = 0.62 * slow / mv
        # 出栈折线总时长；其中「过道水平段」在 play_pop_polyline_to_proc 内再 ÷1.5
        t_pop_polyline = 2.5 * slow / mv
        stack_exit_x = float(tray_right + 0.52 + BOX_W * 0.35)
        # 过程区字符行上方「过道」：先下到这里再水平对齐列，最后落下（不在栈行上往回折）
        proc_lane_y = float(proc_y + 0.76)
        proc_merge_y = proc_y - 0.55

        stack_mobs: list[VGroup] = []
        stack_chars: list[str] = []

        def anim_push_cell(fly: VGroup) -> None:
            """过程区生成的字符压栈（经开口入栈）。"""
            n = len(stack_mobs)
            fly.set_z_index(22)
            play_push_through_opening(fly, n)
            stack_mobs.append(fly)

        def anim_push_cell_expand(fly: VGroup) -> None:
            """拼接展开后压栈（经开口，时长档 t_expand_push）。"""
            n = len(stack_mobs)
            fly.set_z_index(22)
            play_push_through_opening(fly, n, t_move=t_expand_push)
            stack_mobs.append(fly)

        def anim_push_cell_sync_unhighlight(fly: VGroup) -> None:
            """右侧原串格经开口入栈，同时黄框与箭头淡出。"""
            n = len(stack_mobs)
            fly.set_z_index(22)
            fade = (
                FadeOut(yellow_frame, scale=0.96),
                FadeOut(idx_group, scale=0.96),
            )
            play_push_through_opening(fly, n, fade_anims=fade)
            stack_mobs.append(fly)

        def anim_repack_stack() -> None:
            n = len(stack_mobs)
            if n == 0:
                return
            self.play(
                *[stack_mobs[i].animate.move_to(stack_slot_center(i, n)) for i in range(n)],
                run_time=t_slot * 0.92,
                rate_func=smooth,
            )

        def repack_stack_only_after_pop() -> None:
            """仅收拢栈内剩余格（刚弹出的 mob 不在 stack_mobs 中，不参与本段）。"""
            n = len(stack_mobs)
            if n == 0:
                return
            self.play(
                *[stack_mobs[i].animate.move_to(stack_slot_center(i, n)) for i in range(n)],
                run_time=t_repack_after_pop,
                rate_func=smooth,
            )

        def _invisible_polyline(corners: list) -> VMobject:
            track = VMobject()
            track.set_points_as_corners([np.array(p, dtype=float) for p in corners])
            track.set_stroke(width=0, opacity=0)
            return track

        def play_push_through_opening(
            fly: Mobject,
            n_existing: int,
            *,
            fade_anims: tuple = (),
            t_move: float | None = None,
        ) -> None:
            """经栈外开口点 (stack_exit_x, stack_row_y) 再滑入槽位，与出栈折线对称的入栈路径。"""
            tbase = t_slot if t_move is None else t_move
            p0 = np.array(fly.get_center(), dtype=float)
            p_open = np.array([stack_exit_x, stack_row_y, 0.0], dtype=float)
            n_tot = n_existing + 1
            p_end = stack_slot_center(n_existing, n_tot)
            path = _invisible_polyline([p0, p_open, p_end])
            rt = tbase * (1.08 if n_existing == 0 else 1.05)
            if n_existing == 0:
                self.play(MoveAlongPath(fly, path), *fade_anims, run_time=rt, rate_func=smooth)
            else:
                anims = [
                    stack_mobs[i].animate.move_to(stack_slot_center(i, n_tot))
                    for i in range(n_existing)
                ]
                self.play(*anims, MoveAlongPath(fly, path), *fade_anims, run_time=rt, rate_func=smooth)

        def play_pop_polyline_to_proc(mob: Mobject, final_xyz: np.ndarray) -> None:
            """
            与「先出开口 → 再下落 → 再平移」一致：
            当前 → **开口外 (stack_exit_x, 栈行 y)** → **保持 x 竖直下到过道 proc_lane_y**
            → **在过道高度水平移到目标列 x**（向左或向右视目标而定）→ **竖直落到 proc_y**。
            水平段单独 1.5 倍速（用时为按弧长比例时间的 1/1.5），其余段时长不变。
            """
            p0 = np.array(mob.get_center(), dtype=float)
            fx, fy = float(final_xyz[0]), float(final_xyz[1])
            p1 = np.array([stack_exit_x, stack_row_y, 0.0], dtype=float)
            p2 = np.array([stack_exit_x, proc_lane_y, 0.0], dtype=float)
            p3 = np.array([fx, proc_lane_y, 0.0], dtype=float)
            p4 = np.array([fx, fy, 0.0], dtype=float)

            def _len(a: np.ndarray, b: np.ndarray) -> float:
                return float(np.linalg.norm(a - b))

            L1 = _len(p0, p1) + _len(p1, p2)
            Lh = _len(p2, p3)
            L3 = _len(p3, p4)
            Lsum = L1 + Lh + L3
            if Lsum < 1e-6:
                t1 = t_pop_polyline * 0.35
                th = t_pop_polyline * 0.3 / 1.5
                t3 = t_pop_polyline * 0.35
            else:
                r1, rh, r3 = L1 / Lsum, Lh / Lsum, L3 / Lsum
                t1 = t_pop_polyline * r1
                th = t_pop_polyline * rh / 1.5
                t3 = t_pop_polyline * r3

            mob.set_z_index(22)
            path1 = _invisible_polyline([p0, p1, p2])
            path_h = _invisible_polyline([p2, p3])
            path3 = _invisible_polyline([p3, p4])
            self.play(MoveAlongPath(mob, path1), run_time=t1, rate_func=smooth)
            self.play(MoveAlongPath(mob, path_h), run_time=th, rate_func=smooth)
            self.play(MoveAlongPath(mob, path3), run_time=t3, rate_func=smooth)

        def proc_row_target_centers(mobs: list[VGroup]) -> list[np.ndarray]:
            """用**副本**排过程区一行，只取目标中心，绝不移动真实 mob（避免 arrange 造成瞬移）。"""
            if not mobs:
                return []
            dummy = VGroup(*[m.copy() for m in mobs]).arrange(RIGHT, buff=gap).move_to([proc_cx, proc_y, 0])
            return [np.array(dummy[j].get_center(), dtype=float) for j in range(len(mobs))]

        def highlight(i0: int, i1_ex: int | None = None) -> None:
            if i1_ex is None:
                i1_ex = i0 + 1
            span_yellow(i0, i1_ex)
            move_index_arrow(i0)
            self.play(
                FadeIn(yellow_frame, scale=0.96),
                FadeIn(idx_group, shift=DOWN * 0.08),
                run_time=0.42 * slow / mv,
                rate_func=smooth,
            )

        def unhighlight() -> None:
            self.play(
                FadeOut(yellow_frame, scale=0.96),
                FadeOut(idx_group, scale=0.96),
                run_time=0.34 * slow / mv,
                rate_func=smooth,
            )

        # ---------- 开场 ----------
        self.play(
            LaggedStart(*[FadeIn(c, scale=0.95) for c in char_cells], lag_ratio=0.06, run_time=1.0 * slow / mv)
        )
        self.play(
            FadeIn(tray_stack, shift=LEFT * 0.08),
            FadeIn(lbl_stack, shift=UP * 0.06),
            run_time=0.7 * slow / mv,
            rate_func=smooth,
        )
        self.wait(max(0.08 * slow / mv, gap_s))

        # ---------- 主循环 ----------
        i = 0
        while i < len(s):
            ch = s[i]
            highlight(i)

            if ch != "]":
                fly = char_cells[i]
                anim_push_cell_sync_unhighlight(fly)
                stack_chars.append(ch)
                self.wait(gap_s)
                i += 1
                continue

            self.wait(gap_s)

            def layout_stage_at_proc(num_ms: list[VGroup], inner_ms: list[VGroup]) -> VGroup:
                inner_row = VGroup(*inner_ms).arrange(RIGHT, buff=gap)
                if not num_ms:
                    inner_row.move_to([proc_cx, proc_y, 0])
                    return inner_row
                num_row = VGroup(*num_ms).arrange(RIGHT, buff=gap)
                st = VGroup(num_row, inner_row).arrange(RIGHT, buff=gap * 1.2)
                st.move_to([proc_cx, proc_y, 0])
                return st

            pop_buf: list[VGroup] = []
            while stack_chars and stack_chars[-1] != "[":
                m = stack_mobs.pop()
                stack_chars.pop()
                pop_buf.append(m)
                repack_stack_only_after_pop()
                # 与 now_str += stack[-1] 一致：过程区从左到右为「先弹出的在左」→ 对 acc 为 c,c,a（即 "cca"）
                ltr_sub = list(pop_buf)
                centers = proc_row_target_centers(ltr_sub)
                idx_new = ltr_sub.index(m)
                # 先把已在过程区的块移到新行各槽位，再让新块沿「对齐 x 后下落」路径进入，避免同 y 横穿与已有块重合
                if len(ltr_sub) > 1:
                    self.play(
                        *[
                            ltr_sub[j].animate.move_to(centers[j]).set_z_index(22)
                            for j in range(len(ltr_sub))
                            if j != idx_new
                        ],
                        run_time=0.58 * slow / mv,
                        rate_func=smooth,
                    )
                play_pop_polyline_to_proc(m, centers[idx_new])
                self.wait(gap_s)

            inner_mobs = list(reversed(pop_buf))
            inner_str = "".join(m.val_text.text for m in inner_mobs)
            self.wait(gap_s)
            # now_str = now_str[::-1]：弹出序在过程区左→右，重排为 inner_str（含两个相同字符如 cc 也要明显「翻一下」）
            if len(inner_mobs) >= 2:
                centers_acc = proc_row_target_centers(inner_mobs)
                same_pair = len(inner_mobs) == 2 and inner_str[0] == inner_str[1]
                rt = ((0.95 * slow) if same_pair else (0.72 * slow)) / mv
                for m in inner_mobs:
                    m.set_z_index(22)
                anims = []
                for j in range(len(inner_mobs)):
                    m = inner_mobs[j]
                    if same_pair:
                        anims.append(m.animate(path_arc=-PI / 2.6).move_to(centers_acc[j]))
                    else:
                        anims.append(m.animate.move_to(centers_acc[j]))
                self.play(*anims, run_time=rt, rate_func=smooth)
                self.wait(gap_s)

            if stack_chars and stack_chars[-1] == "[":
                lb = stack_mobs.pop()
                stack_chars.pop()
                anim_repack_stack()
                lb.set_z_index(24)
                self.play(
                    lb.animate.scale(0.15).set_opacity(0),
                    run_time=0.52 * slow / mv,
                    rate_func=ease_out_sine,
                )
                self.remove(lb)

            num_pop_buf: list[VGroup] = []
            while stack_chars and stack_chars[-1].isdigit():
                nm = stack_mobs.pop()
                stack_chars.pop()
                num_pop_buf.append(nm)
                repack_stack_only_after_pop()
                partial_nums = list(reversed(num_pop_buf))
                if inner_mobs:
                    digit_mobs = list(partial_nums) + list(inner_mobs)
                    nc = [p.copy() for p in partial_nums]
                    ic = [im.copy() for im in inner_mobs]
                    inner_row_d = VGroup(*ic).arrange(RIGHT, buff=gap)
                    num_row_d = VGroup(*nc).arrange(RIGHT, buff=gap)
                    st_d = VGroup(num_row_d, inner_row_d).arrange(RIGHT, buff=gap * 1.2)
                    st_d.move_to([proc_cx, proc_y, 0])
                    digit_finals = [
                        np.array(num_row_d[j].get_center(), dtype=float)
                        for j in range(len(nc))
                    ] + [
                        np.array(inner_row_d[j].get_center(), dtype=float)
                        for j in range(len(ic))
                    ]
                else:
                    digit_mobs = list(partial_nums)
                    nc = [p.copy() for p in partial_nums]
                    num_row_d = VGroup(*nc).arrange(RIGHT, buff=gap)
                    num_row_d.move_to([proc_cx, proc_y, 0])
                    digit_finals = [
                        np.array(num_row_d[j].get_center(), dtype=float) for j in range(len(nc))
                    ]
                idx_nm = digit_mobs.index(nm)
                if len(digit_mobs) > 1:
                    self.play(
                        *[
                            digit_mobs[j].animate.move_to(digit_finals[j]).set_z_index(22)
                            for j in range(len(digit_mobs))
                            if j != idx_nm
                        ],
                        run_time=0.58 * slow / mv,
                        rate_func=smooth,
                    )
                play_pop_polyline_to_proc(nm, digit_finals[idx_nm])
                self.wait(gap_s)

            num_mobs_ltr = list(reversed(num_pop_buf))
            k_str = "".join(m.val_text.text for m in num_mobs_ltr)
            k_val = int(k_str) if k_str else 1

            self.wait(gap_s)

            wide: VGroup | None = None
            if inner_str:
                unit = VGroup(
                    *[
                        _make_char_box(
                            c,
                            box_w=BOX_W,
                            box_h=BOX_H,
                            fs=CHAR_FS,
                            stroke_w=stroke_box,
                        )
                        for c in inner_str
                    ]
                ).arrange(RIGHT, buff=gap)
                copies = [unit.copy() for _ in range(k_val)]
                wide = VGroup(*copies).arrange(RIGHT, buff=0.14)
                wide.move_to([proc_cx, proc_merge_y, 0])
                wide.set_z_index(23)
                stage_row = layout_stage_at_proc(num_mobs_ltr, inner_mobs)
                self.play(
                    ReplacementTransform(stage_row, wide),
                    run_time=0.95 * slow / mv,
                    rate_func=smooth,
                )
                self.wait(max(0.05 * slow / mv, gap_s))
            else:
                if num_mobs_ltr:
                    self.play(FadeOut(VGroup(*num_mobs_ltr), scale=0.9), run_time=0.35 * slow / mv)
                    for nm in num_mobs_ltr:
                        self.remove(nm)

            # 与代码语义一致：for _ in range(num): for c in now_str: stack.append(c)
            # 动画：预览行 wide 上从左到右依次为各轮 inner_str，依次整排刚性压栈（不先整行消失再新建）；
            # 仅「两个相同字符」时不用 wide 作起点，先淡出 wide 再按先右后左单字飞入。
            if inner_str and k_val > 0:

                def _play_rigid_cells_to_stack(chars: str, cells: list[VGroup]) -> None:
                    """整排先对齐到开口外一行，再与栈内格一起收拢入位。"""
                    L = len(cells)
                    for c in cells:
                        c.set_z_index(22)
                    n0 = len(stack_mobs)
                    targets = [stack_slot_center(n0 + j, n0 + L) for j in range(L)]
                    p_open = np.array([stack_exit_x, stack_row_y, 0.0], dtype=float)
                    open_targets = [p_open + LEFT * step * (L - 1 - j) for j in range(L)]
                    rt1 = t_expand_push * 0.58
                    rt2 = t_expand_push * 0.58
                    self.play(
                        *[cells[j].animate.move_to(open_targets[j]) for j in range(L)],
                        run_time=rt1,
                        rate_func=smooth,
                    )
                    if n0 == 0:
                        self.play(
                            *[cells[j].animate.move_to(targets[j]) for j in range(L)],
                            run_time=rt2,
                            rate_func=smooth,
                        )
                    else:
                        self.play(
                            *[
                                stack_mobs[i].animate.move_to(stack_slot_center(i, n0 + L))
                                for i in range(n0)
                            ],
                            *[cells[j].animate.move_to(targets[j]) for j in range(L)],
                            run_time=rt2,
                            rate_func=smooth,
                        )
                    stack_mobs.extend(cells)
                    stack_chars.extend(list(chars))

                dup_same_pair = (
                    len(inner_str) == 2
                    and inner_str[0] == inner_str[1]
                    and len(inner_mobs) >= 2
                )
                if dup_same_pair and wide is not None:
                    self.play(FadeOut(wide, scale=0.92), run_time=0.38 * slow / mv, rate_func=smooth)
                    self.remove(wide)
                    wide = None

                for rep in range(k_val):
                    if dup_same_pair:
                        # 栈序仍按 inner_str[0], inner_str[1]；视觉上先飞过程区右侧块、再飞左侧块
                        src_order = (1, 0)
                        for k_push, ch in enumerate(inner_str):
                            src_m = inner_mobs[src_order[k_push]]
                            cell = _make_char_box(
                                ch,
                                box_w=BOX_W,
                                box_h=BOX_H,
                                fs=CHAR_FS,
                                stroke_w=stroke_box,
                            )
                            cell.move_to(src_m.get_center())
                            cell.set_z_index(22)
                            self.add(cell)
                            anim_push_cell_expand(cell)
                            stack_chars.append(ch)
                            self.wait(gap_s)
                    else:
                        assert wide is not None
                        unit_group = wide[0]
                        cells = [unit_group[j] for j in range(len(unit_group))]
                        for c in cells:
                            unit_group.remove(c)
                        self.add(*cells)
                        wide.remove(unit_group)
                        self.remove(unit_group)
                        _play_rigid_cells_to_stack(inner_str, cells)
                        self.wait(max(0.05 * slow / mv, gap_s))
                    if rep < k_val - 1:
                        self.wait(max(0.06 * slow / mv, gap_s))

                if wide is not None and len(wide) == 0:
                    self.remove(wide)

            # `]` 处理完后右侧该格与扫描高亮同步消失（不再留在原位）
            br_cell = char_cells[i]
            self.play(
                FadeOut(yellow_frame, scale=0.96),
                FadeOut(idx_group, scale=0.96),
                FadeOut(br_cell, scale=0.92),
                run_time=0.34 * slow / mv,
                rate_func=smooth,
            )
            self.remove(br_cell)
            self.wait(max(0.06 * slow / mv, gap_s))
            i += 1

        # ---------- 结尾 ----------
        self.wait(max(0.1 * slow / mv, gap_s))
        out = "".join(stack_chars)
        result_y = proc_y - 0.95
        res_row = VGroup(
            *[
                _make_char_box(c, box_w=BOX_W, box_h=BOX_H, fs=CHAR_FS, stroke_w=stroke_box)
                for c in out
            ]
        ).arrange(RIGHT, buff=gap)

        def _result_row_fit_center(row: VGroup, pref_cx: float, y: float) -> np.ndarray:
            """水平平移使整行落在画面内（长串时优先保证左端可见）。"""
            half_fw = float(config.frame_width) / 2.0 - 0.34
            margin = 0.28
            w = float(row.get_width())
            if w < 1e-6:
                return np.array([pref_cx, y, 0.0], dtype=float)
            cx = float(pref_cx)
            left_edge = cx - 0.5 * w
            right_edge = cx + 0.5 * w
            if left_edge < -half_fw + margin:
                cx += (-half_fw + margin) - left_edge
            left_edge = cx - 0.5 * w
            right_edge = cx + 0.5 * w
            if right_edge > half_fw - margin:
                cx -= right_edge - (half_fw - margin)
            return np.array([cx, y, 0.0], dtype=float)

        if stack_mobs:
            src = VGroup(*stack_mobs)
            res_row.move_to(src.get_center())
            self.play(ReplacementTransform(src, res_row), run_time=1.12 * slow / mv, rate_func=smooth)
            for m in list(stack_mobs):
                self.remove(m)
            stack_mobs.clear()
            stack_chars.clear()
            self.add(res_row)
        else:
            res_row.move_to(_result_row_fit_center(res_row, proc_cx, result_y))
            self.add(res_row)

        _fit = _result_row_fit_center(res_row, proc_cx, result_y)
        self.play(
            res_row.animate.move_to(_fit),
            run_time=0.82 * slow / mv,
            rate_func=smooth,
        )
        res_frame = SurroundingRectangle(res_row, color=WHITE, buff=0.14, stroke_width=2.6)
        self.play(FadeIn(res_frame, scale=0.96), run_time=0.48 * slow / mv)
        self.wait(0.65 * slow / mv)
