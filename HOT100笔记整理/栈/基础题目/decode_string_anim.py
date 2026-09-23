# -*- coding: utf-8 -*-
"""
Decode String（栈 + 重复展开）— 过程演示（Manim）

样例固定为 `3[a2[c]]`；黑底、无旁白字幕与题面大段说明。
左层为输入串逐字白框 + 黄色当前扫描框 + 红色指针箭头（无 `index` 文字）；右层仅上 `countStack`、中 `resStack`（左开口右封闭托盘）；当前串 `res` 在 **resStack 托盘正下方** 以与输入格同尺寸的字符框横向拼接（无托盘）。

画布比例 16:9（与 2560×1440 一致）；默认 480p 加快预览。更高清晰度可设置环境变量 `DECODE_STRING_ANIM_RES=1080p`。

渲染（项目根目录）:
  480p: manim-env2\\Scripts\\python.exe -m manim decode_string_anim.py DecodeStringAnim -ql
  1080p: DECODE_STRING_ANIM_RES=1080p manim-env2\\Scripts\\python.exe -m manim decode_string_anim.py DecodeStringAnim -qh
"""

from __future__ import annotations

import os

import numpy as np

from manim import *
from manim.utils.rate_functions import smooth

_res = (os.environ.get("DECODE_STRING_ANIM_RES") or "480p").strip().lower()
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


def _make_num_box(s: str, *, box_w: float, box_h: float, fs: int, stroke_w: float = 2.6) -> VGroup:
    return _make_char_box(s, box_w=box_w, box_h=box_h, fs=fs, stroke_w=stroke_w)


def _make_str_stack_box(text: str, *, box_w: float, box_h: float, fs: int, stroke_w: float = 2.2) -> VGroup:
    r = Rectangle(
        width=box_w,
        height=box_h,
        color=WHITE if text else GRAY_B,
        stroke_width=stroke_w,
        fill_opacity=0,
    )
    if text:
        t = Text(text, font_size=fs, color=WHITE, font="Arial", disable_ligatures=True)
        g = VGroup(r, t)
        g.val_text = t  # type: ignore[attr-defined]
    else:
        t = Text("", font_size=fs, color=WHITE, font="Arial", disable_ligatures=True)
        t.set_opacity(0)
        g = VGroup(r, t)
        g.val_text = t  # type: ignore[attr-defined]
    g.border = r  # type: ignore[attr-defined]
    g.raw = text  # type: ignore[attr-defined]
    return g


class DecodeStringAnim(Scene):
    def construct(self) -> None:
        self.camera.background_color = BLACK

        YELLOW_HL = "#ffcc00"
        RED_PT = "#ff3333"
        slow = 1.42

        s = "3[a2[c]]"
        BOX_W, BOX_H = 0.54, 0.48
        CHAR_FS = 28
        STR_FS = 22
        stroke_box = 2.4
        gap = 0.06

        # ---------- 左层：输入串 ----------
        n = len(s)
        left_y = 0.95
        left_x0 = -5.55
        char_cells: list[VGroup] = []
        for i, ch in enumerate(s):
            c = _make_char_box(ch, box_w=BOX_W, box_h=BOX_H, fs=CHAR_FS, stroke_w=stroke_box)
            cx = left_x0 + i * (BOX_W + gap)
            c.move_to([cx, left_y, 0])
            c.set_z_index(5)
            char_cells.append(c)

        yellow_frame = Rectangle(
            width=BOX_W * 1.06,
            height=BOX_H * 1.08,
            color=YELLOW_HL,
            stroke_width=3.4,
            fill_opacity=0,
        ).set_z_index(14)

        idx_arrow = Arrow(
            start=[0, left_y - 0.78, 0],
            end=[0, left_y - BOX_H * 0.52 - 0.06, 0],
            color=RED_PT,
            stroke_width=3.2,
            buff=0.02,
            max_tip_length_to_length_ratio=0.2,
        )
        idx_arrow.set_z_index(16)

        def char_center(i: int) -> np.ndarray:
            return char_cells[i].get_center()

        def span_yellow(i0: int, i1_exclusive: int) -> None:
            mid_x = (char_center(i0)[0] + char_center(i1_exclusive - 1)[0]) / 2
            w = (i1_exclusive - i0) * BOX_W + (i1_exclusive - i0 - 1) * gap + 0.08
            yellow_frame.set(width=w, height=BOX_H * 1.08)
            yellow_frame.move_to([mid_x, left_y, 0])

        def move_index_group(i: int) -> None:
            base = char_center(i)
            tip = base + DOWN * (BOX_H * 0.5 + 0.05)
            tail = base + DOWN * (BOX_H * 0.5 + 0.58)
            idx_arrow.put_start_and_end_on(tail, tip)

        # ---------- 右层：两个栈托盘 + res 拼接区 ----------
        inner_left = 0.45
        inner_right = 5.25
        tray_h = 0.74
        count_y = 2.05
        rs_y = 0.38

        def make_tray(y: float) -> VGroup:
            y_top = y + tray_h / 2
            y_bot = y - tray_h / 2
            top = Line(
                np.array([inner_left, y_top, 0]),
                np.array([inner_right, y_top, 0]),
                color=WHITE,
                stroke_width=3.0,
            )
            bot = Line(
                np.array([inner_left, y_bot, 0]),
                np.array([inner_right, y_bot, 0]),
                color=WHITE,
                stroke_width=3.0,
            )
            right = Line(
                np.array([inner_right, y_bot, 0]),
                np.array([inner_right, y_top, 0]),
                color=WHITE,
                stroke_width=3.0,
            )
            return VGroup(top, bot, right).set_z_index(1)

        tray_count = make_tray(count_y)
        tray_rs = make_tray(rs_y)

        lbl_count = Text(
            "countStack",
            font_size=21,
            color=WHITE,
            font="Arial",
            disable_ligatures=True,
        ).next_to(tray_count, UP, buff=0.12).set_z_index(6)
        lbl_rs = Text(
            "resStack",
            font_size=21,
            color=WHITE,
            font="Arial",
            disable_ligatures=True,
        ).next_to(tray_rs, UP, buff=0.12).set_z_index(6)

        def y_stack_row(y_tray: float) -> float:
            return float(y_tray - tray_h / 2 + BOX_H * 0.5 + 0.06)

        stack_gap = 0.1

        def centers_for_row_stack(stack: list[VGroup], y_tray: float) -> list[np.ndarray]:
            """栈顶在开口侧（索引 0 在最左），整体靠托盘右端对齐，格与格间距按实际宽度不重叠。"""
            ys = y_stack_row(y_tray)
            widths = [max(float(m.get_width()), BOX_W * 0.2) for m in stack]
            total_w = sum(widths) + stack_gap * max(0, len(stack) - 1)
            right_limit = inner_right - 0.1
            cur_left = right_limit - total_w
            out: list[np.ndarray] = []
            for w in widths:
                cx = cur_left + w * 0.5
                out.append(np.array([cx, ys, 0.0]))
                cur_left += w + stack_gap
            return out

        tray_rs_bottom = rs_y - tray_h / 2
        # 自上而下：托盘底边 → 较大空隙 → `res` 标题 → 字符行（相对标题水平居中）
        res_lbl_y = float(tray_rs_bottom - 0.62)
        res_row_y = float(res_lbl_y - 0.32 - BOX_H * 0.46)
        res_cx = float((inner_left + inner_right) / 2)
        # 合并演示区：在 res 字符行正下方、水平以 res_cx 为中心；k 在内层左侧，展开后再接前缀
        merge_stage_y = float(res_row_y - 0.58 - BOX_H * 0.42)
        lbl_res = Text(
            "res",
            font_size=21,
            color=WHITE,
            font="Arial",
            disable_ligatures=True,
        ).move_to([res_cx, res_lbl_y, 0]).set_z_index(6)

        merge_buff = 0.14

        def res_slot_x(j: int, total: int) -> float:
            """第 j 个字符中心 x；与左层同 BOX_W+gap，整行关于 res_cx 居中。"""
            if total <= 0:
                return res_cx
            step = BOX_W + gap
            total_w = (total - 1) * step + BOX_W
            x0 = res_cx - total_w / 2 + BOX_W / 2
            return x0 + j * step

        def build_char_row_chars(text: str) -> VGroup:
            """与输入串、res 主行完全同尺寸的字符格。"""
            if not text:
                return VGroup()
            parts = [
                _make_char_box(c, box_w=BOX_W, box_h=BOX_H, fs=CHAR_FS, stroke_w=stroke_box)
                for c in text
            ]
            return VGroup(*parts).arrange(RIGHT, buff=gap)

        def pack_res_stack_payload(text: str) -> VGroup:
            """压入 resStack 的载荷：等宽字格横向排开；空串为单个灰框。"""
            if not text:
                cell = _make_str_stack_box("", box_w=BOX_W, box_h=BOX_H, fs=STR_FS, stroke_w=stroke_box)
                return cell
            row = build_char_row_chars(text)
            row.raw = text  # type: ignore[attr-defined]
            return row

        def center_row_at(row: VGroup, cx: float, cy: float) -> None:
            row.move_to([cx, cy, 0])

        def mob_half_w(m: Mobject) -> float:
            return float(m.get_width() / 2)

        def place_left_of(target: Mobject, mob: Mobject, buff: float) -> np.ndarray:
            """mob 中心：紧挨 target 左侧。"""
            lx = float(target.get_left()[0])
            return np.array([lx - buff - mob_half_w(mob), float(target.get_center()[1]), 0.0])

        t_down = 0.62 * slow
        t_slot = 0.88 * slow
        t_merge = 1.05 * slow

        count_mobs: list[VGroup] = []
        rs_mobs: list[VGroup] = []
        res_mobs: list[VGroup] = []

        def str_from_res_mobs() -> str:
            return "".join(m.val_text.text for m in res_mobs)

        def anim_push_tray(fly: VGroup, stack: list[VGroup], y_tray: float) -> None:
            pending = [fly] + stack
            centers = centers_for_row_stack(pending, y_tray)
            if len(pending) == 1:
                self.play(
                    fly.animate.move_to(centers[0]),
                    run_time=t_down * 1.08,
                    rate_func=smooth,
                )
            else:
                self.play(
                    *[pending[k].animate.move_to(centers[k]) for k in range(len(pending))],
                    run_time=t_slot * 1.05,
                    rate_func=smooth,
                )
            stack.insert(0, fly)

        def anim_repack(stack: list[VGroup], y_tray: float) -> None:
            if not stack:
                return
            centers = centers_for_row_stack(stack, y_tray)
            self.play(
                *[stack[i].animate.move_to(centers[i]) for i in range(len(stack))],
                run_time=t_slot * 0.92,
                rate_func=smooth,
            )

        def layout_res_mobs() -> None:
            tot = len(res_mobs)
            for j, m in enumerate(res_mobs):
                m.move_to([res_slot_x(j, tot), res_row_y, 0])

        def clear_res_visual(self_ref: Scene) -> None:
            if not res_mobs:
                return
            grp = VGroup(*res_mobs)
            self_ref.play(FadeOut(grp, scale=0.92), run_time=0.45 * slow, rate_func=smooth)
            res_mobs.clear()

        def set_res_from_string(text: str) -> None:
            for m in list(res_mobs):
                self.remove(m)
            res_mobs.clear()
            for j, ch in enumerate(text):
                b = _make_char_box(ch, box_w=BOX_W, box_h=BOX_H, fs=CHAR_FS, stroke_w=stroke_box)
                b.move_to([res_slot_x(j, len(text)), res_row_y, 0])
                b.set_z_index(8)
                self.add(b)
                res_mobs.append(b)

        # ---------- 开场 ----------
        self.play(LaggedStart(*[FadeIn(c, scale=0.95) for c in char_cells], lag_ratio=0.06, run_time=1.02 * slow))
        self.play(
            FadeIn(tray_count, shift=RIGHT * 0.08),
            FadeIn(tray_rs, shift=RIGHT * 0.08),
            FadeIn(lbl_count, shift=UP * 0.06),
            FadeIn(lbl_rs, shift=UP * 0.06),
            FadeIn(lbl_res, shift=UP * 0.06),
            run_time=0.74 * slow,
            rate_func=smooth,
        )
        self.wait(0.32 * slow)

        def highlight_index(i0: int, i1_exclusive: int | None = None) -> None:
            if i1_exclusive is None:
                i1_exclusive = i0 + 1
            span_yellow(i0, i1_exclusive)
            move_index_group(i0)
            self.play(
                FadeIn(yellow_frame, scale=0.96),
                FadeIn(idx_arrow, shift=UP * 0.12),
                run_time=0.42 * slow,
                rate_func=smooth,
            )

        def unhighlight() -> None:
            self.play(
                FadeOut(yellow_frame, scale=0.96),
                FadeOut(idx_arrow, scale=0.96),
                run_time=0.34 * slow,
                rate_func=smooth,
            )

        # ---------- 主循环（与参考算法一致）----------
        index = 0
        while index < len(s):
            if s[index].isdigit():
                j = index
                while j < len(s) and s[j].isdigit():
                    j += 1
                highlight_index(index, j)
                num_s = s[index:j]
                fly_n = _make_num_box(num_s, box_w=BOX_W, box_h=BOX_H, fs=CHAR_FS)
                fly_n.move_to(char_center((index + j - 1) // 2))
                fly_n.set_z_index(22)
                self.add(fly_n)
                anim_push_tray(fly_n, count_mobs, count_y)
                index = j
                unhighlight()
                self.wait(0.16 * slow)
                continue

            if s[index] == "[":
                highlight_index(index)
                cur = str_from_res_mobs()
                payload = pack_res_stack_payload(cur)
                payload.move_to([res_cx, res_row_y, 0])
                payload.set_z_index(21)
                if cur:
                    grp = VGroup(*res_mobs)
                    self.play(ReplacementTransform(grp, payload), run_time=0.62 * slow, rate_func=smooth)
                    res_mobs.clear()
                else:
                    self.add(payload)
                    self.play(FadeIn(payload, scale=0.92), run_time=0.48 * slow, rate_func=smooth)
                anim_push_tray(payload, rs_mobs, rs_y)
                index += 1
                unhighlight()
                self.wait(0.16 * slow)
                continue

            if s[index] == "]":
                highlight_index(index)
                assert rs_mobs and count_mobs
                tmp_m = rs_mobs.pop(0)
                k_m = count_mobs.pop(0)
                inner_s = str_from_res_mobs()
                k_val = int(k_m.val_text.text)
                prefix = str(getattr(tmp_m, "raw", ""))
                new_s = prefix + inner_s * k_val

                anim_repack(rs_mobs, rs_y)
                anim_repack(count_mobs, count_y)

                if res_mobs:
                    self.play(
                        FadeOut(VGroup(*res_mobs), scale=0.9),
                        run_time=0.4 * slow,
                        rate_func=smooth,
                    )
                    for m in list(res_mobs):
                        self.remove(m)
                    res_mobs.clear()

                if not inner_s:
                    self.play(
                        FadeOut(tmp_m, scale=0.85),
                        FadeOut(k_m, scale=0.85),
                        run_time=0.42 * slow,
                        rate_func=smooth,
                    )
                    self.remove(tmp_m, k_m)
                    set_res_from_string(new_s)
                    self.play(
                        LaggedStart(*[FadeIn(m, scale=0.92) for m in res_mobs], lag_ratio=0.07, run_time=0.72 * slow)
                    )
                    index += 1
                    unhighlight()
                    self.wait(0.2 * slow)
                    continue

                if not prefix:
                    self.play(FadeOut(tmp_m, scale=0.85), run_time=0.32 * slow, rate_func=smooth)
                    self.remove(tmp_m)

                inner_row = build_char_row_chars(inner_s)
                center_row_at(inner_row, res_cx, merge_stage_y)
                inner_row.set_z_index(24)
                self.add(inner_row)
                self.play(FadeIn(inner_row, scale=0.92), run_time=0.5 * slow, rate_func=smooth)
                self.wait(0.14 * slow)

                k_m.set_z_index(26)
                k_tgt = place_left_of(inner_row, k_m, merge_buff)
                self.play(k_m.animate.move_to(k_tgt), run_time=t_merge * 0.88, rate_func=smooth)
                self.wait(0.16 * slow)

                rep_text = inner_s * k_val
                repeated_row = build_char_row_chars(rep_text)
                center_row_at(repeated_row, res_cx, merge_stage_y)
                repeated_row.set_z_index(24)
                self.play(
                    FadeOut(k_m, scale=0.85),
                    ReplacementTransform(inner_row, repeated_row),
                    run_time=0.78 * slow,
                    rate_func=smooth,
                )
                self.remove(k_m)

                if prefix:
                    self.wait(0.12 * slow)
                    tmp_m.set_z_index(25)
                    p_tgt = place_left_of(repeated_row, tmp_m, merge_buff)
                    self.play(tmp_m.animate.move_to(p_tgt), run_time=t_merge * 0.88, rate_func=smooth)
                    self.wait(0.16 * slow)

                    combined = build_char_row_chars(new_s)
                    center_row_at(combined, res_cx, merge_stage_y)
                    combined.set_z_index(24)
                    merge_grp = VGroup(tmp_m, repeated_row)
                    self.play(
                        ReplacementTransform(merge_grp, combined),
                        run_time=0.85 * slow,
                        rate_func=smooth,
                    )
                    self.remove(tmp_m, repeated_row)
                    merge_stage = combined
                else:
                    merge_stage = repeated_row

                self.play(FadeOut(merge_stage, scale=0.9), run_time=0.42 * slow, rate_func=smooth)
                self.remove(merge_stage)

                set_res_from_string(new_s)
                self.play(
                    LaggedStart(*[FadeIn(m, scale=0.92) for m in res_mobs], lag_ratio=0.07, run_time=0.78 * slow)
                )
                index += 1
                unhighlight()
                self.wait(0.22 * slow)
                continue

            # 普通字符
            highlight_index(index)
            ch = s[index]
            fly_c = _make_char_box(ch, box_w=BOX_W, box_h=BOX_H, fs=CHAR_FS, stroke_w=stroke_box)
            fly_c.move_to(char_center(index))
            fly_c.set_z_index(22)
            self.add(fly_c)
            jn = len(res_mobs)
            tgt = np.array([res_slot_x(jn, jn + 1), res_row_y, 0.0])
            self.play(
                fly_c.animate.move_to(tgt),
                run_time=t_down * 1.12,
                rate_func=smooth,
            )
            res_mobs.append(fly_c)
            layout_res_mobs()
            index += 1
            unhighlight()
            self.wait(0.16 * slow)

        # ---------- 最终结果（仍在右下角 res 区停留）----------
        self.wait(0.35 * slow)
        if res_mobs:
            self.play(
                *[m.border.animate.set_stroke(YELLOW_HL, width=3.2) for m in res_mobs],  # type: ignore[attr-defined]
                run_time=0.55 * slow,
                rate_func=smooth,
            )
        self.wait(1.45 * slow)
