# -*- coding: utf-8 -*-
"""
有效的括号 — 栈过程演示（Manim）

上下两行同时出现在画面中；先完整演示上层 {()}[]（下层保持静止），再演示下层 {}(][{ 至匹配失败处。
匹配成功时：右括号副本移到栈口右侧，栈顶左括号再弹出到其左侧成对，再淡出；收尾成功用绿色外框 + 几何对勾。
下层匹配失败时：同样把右括号拿到栈口右、左括号弹出比对，红叉表示不匹配，左括号回到栈内；最后用红色外框包住栈槽 + 整串，并加红色几何叉。
画布 1920×1080、黑底。

480p：
  manim -qh valid_parentheses_stack.py ValidParenthesesAnim
  ffmpeg -y -i media/videos/.../ValidParenthesesAnim.mp4 -vf scale=-2:480 -c:v libx264 -crf 18 -an valid_parentheses_480p.mp4
"""

from __future__ import annotations

from manim import *
from manim.utils.rate_functions import smooth

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

BOX_W = 0.64


# 栈口外沿到第一个「配对区」方框的间隙（与开口在同一水平线上）
OPEN_GAP = 0.1


def make_geom_cross(color: str, *, height: float = 0.38) -> VGroup:
    """几何叉号，不依赖字体。"""
    a = 0.14
    l1 = Line(np.array([-a, -a, 0.0]), np.array([a, a, 0.0]), color=color, stroke_width=5.0)
    l2 = Line(np.array([-a, a, 0.0]), np.array([a, -a, 0.0]), color=color, stroke_width=5.0)
    g = VGroup(l1, l2)
    g.scale_to_fit_height(height)
    return g


def make_geom_checkmark(color: str, *, height: float = 0.2) -> VGroup:
    """两段折线对勾，不依赖 Unicode 字形。"""
    p0 = np.array([-0.11, -0.02, 0.0])
    p1 = np.array([-0.03, -0.1, 0.0])
    p2 = np.array([0.12, 0.1, 0.0])
    l1 = Line(p0, p1, color=color, stroke_width=4.2)
    l2 = Line(p1, p2, color=color, stroke_width=4.2)
    g = VGroup(l1, l2)
    g.scale_to_fit_height(height)
    return g


def make_char_box(ch: str, *, stroke_color=WHITE, stroke_w: float = 2.8) -> VGroup:
    r = Rectangle(
        width=BOX_W,
        height=BOX_W,
        color=stroke_color,
        stroke_width=stroke_w,
        fill_opacity=0,
    )
    t = Text(ch, font_size=34, color=WHITE, font="Arial", disable_ligatures=True)
    g = VGroup(r, t)
    g.char = ch  # type: ignore[attr-defined]
    g.border = r  # type: ignore[attr-defined]
    return g


class BracketRow:
    """单行：左侧栈轮廓 + 右侧字符串方框；栈顶在容器内最右侧。"""

    def __init__(
        self,
        scene: Scene,
        y: float,
        s: str,
        *,
        inner_left: float = -6.15,
        inner_right: float = -2.75,
        tray_h: float = 0.88,
    ) -> None:
        self.scene = scene
        self.y = y
        self.s = s
        self.inner_left = inner_left
        self.inner_right = inner_right
        self.tray_h = tray_h
        self.stack: list[VGroup] = []
        self.success_band: SurroundingRectangle | None = None
        self.success_ok: VGroup | None = None
        self.failure_band: SurroundingRectangle | None = None
        self.failure_bad: VGroup | None = None

        y_top = y + tray_h / 2
        y_bot = y - tray_h / 2
        left = Line(
            np.array([inner_left, y_bot, 0]),
            np.array([inner_left, y_top, 0]),
            color=WHITE,
            stroke_width=3.2,
        )
        top = Line(
            np.array([inner_left, y_top, 0]),
            np.array([inner_right, y_top, 0]),
            color=WHITE,
            stroke_width=3.2,
        )
        bot = Line(
            np.array([inner_left, y_bot, 0]),
            np.array([inner_right, y_bot, 0]),
            color=WHITE,
            stroke_width=3.2,
        )
        self.tray = VGroup(left, top, bot)
        self.tray.set_z_index(1)

        row = VGroup()
        for ch in s:
            row.add(make_char_box(ch))
        row.arrange(RIGHT, buff=0.0)
        row.move_to(np.array([2.55, y, 0.0]))
        self.string_row = row
        for b in row:
            b.set_z_index(5)
        self.string_boxes = list(row)

        self.highlight = Rectangle(
            width=0.7,
            height=0.7,
            color="#ffcc00",
            stroke_width=4.2,
            fill_opacity=0,
        )
        self.highlight.set_z_index(4)

    def stack_slot_x(self, depth: int) -> float:
        return self.inner_left + (depth + 0.5) * BOX_W

    def add_to_scene(self) -> None:
        self.scene.add(self.tray, self.string_row)

    def refresh_highlight_pos(self, idx: int) -> None:
        self.highlight.move_to(self.string_boxes[idx].get_center())

    def anim_push(self, idx: int) -> Animation:
        src = self.string_boxes[idx]
        fly = make_char_box(src.char)  # type: ignore[attr-defined]
        fly.move_to(src.get_center())
        fly.set_z_index(20)
        depth = len(self.stack)
        target = np.array([self.stack_slot_x(depth), self.y, 0.0])
        self.stack.append(fly)
        self.scene.add(fly)
        return fly.animate.move_to(target).set_z_index(10)

    def _pair_right_center(self) -> np.ndarray:
        """紧贴栈口右侧外、右括号方框中心。"""
        x = self.inner_right + OPEN_GAP + BOX_W / 2
        return np.array([x, self.y, 0.0])

    def play_match_pair(self, idx: int, *, t_right: float, t_left: float, t_glow: float) -> None:
        """右括号移到开口旁 → 左括号从栈顶移到右括号左侧 → 高亮 → 成对淡出并从栈移除。"""
        src = self.string_boxes[idx]
        ch = str(src.char)  # type: ignore[attr-defined]
        right_box = make_char_box(ch)
        right_box.move_to(src.get_center())
        right_box.set_z_index(22)
        self.scene.add(right_box)

        pos_r = self._pair_right_center()
        pos_l = pos_r + LEFT * BOX_W

        left_top = self.stack[-1]

        self.scene.play(
            right_box.animate.move_to(pos_r).set_z_index(22),
            run_time=t_right,
            rate_func=smooth,
        )
        self.scene.play(
            left_top.animate.move_to(pos_l).set_z_index(25),
            run_time=t_left,
            rate_func=smooth,
        )
        self.scene.play(
            left_top.border.animate.set_stroke("#44aaff", width=4.2),  # type: ignore[attr-defined]
            right_box.border.animate.set_stroke("#44aaff", width=4.2),
            src.border.animate.set_stroke("#44aaff", width=4.2),  # type: ignore[attr-defined]
            run_time=t_glow * 0.48,
            rate_func=smooth,
        )
        self.scene.play(
            FadeOut(left_top, scale=0.92),
            FadeOut(right_box, scale=0.92),
            src.border.animate.set_stroke(WHITE, width=2.8),  # type: ignore[attr-defined]
            run_time=t_glow * 0.52,
            rate_func=smooth,
        )
        self.stack.pop()

    def play_match_fail_comparison(self, idx: int, *, t_right: float, t_left: float, t_bad: float) -> None:
        """与成功相同的「右外置 + 左弹出」比对，红叉表示不匹配，左括号回到栈顶原位。"""
        src = self.string_boxes[idx]
        ch = str(src.char)  # type: ignore[attr-defined]
        right_box = make_char_box(ch)
        right_box.move_to(src.get_center())
        right_box.set_z_index(22)
        self.scene.add(right_box)

        pos_r = self._pair_right_center()
        pos_l = pos_r + LEFT * BOX_W
        left_top = self.stack[-1]
        depth = len(self.stack) - 1
        back_pos = np.array([self.stack_slot_x(depth), self.y, 0.0])

        self.scene.play(
            right_box.animate.move_to(pos_r).set_z_index(22),
            run_time=t_right,
            rate_func=smooth,
        )
        self.scene.play(
            left_top.animate.move_to(pos_l).set_z_index(25),
            run_time=t_left,
            rate_func=smooth,
        )
        pair = VGroup(left_top, right_box)
        cx = Cross(pair, stroke_color="#ff3333", stroke_width=6.0, scale_factor=1.05)
        cx.set_z_index(35)
        self.scene.add(cx)
        self.scene.play(
            left_top.border.animate.set_stroke("#ff3333", width=5.0),  # type: ignore[attr-defined]
            right_box.border.animate.set_stroke("#ff3333", width=5.0),
            src.border.animate.set_stroke("#ff3333", width=5.0),  # type: ignore[attr-defined]
            FadeIn(cx, scale=0.9),
            run_time=t_bad * 0.55,
            rate_func=smooth,
        )
        self.scene.play(
            FadeOut(cx, scale=0.9),
            FadeOut(right_box, scale=0.9),
            left_top.animate.move_to(back_pos).set_z_index(10),
            run_time=t_bad * 0.48,
            rate_func=smooth,
        )
        self.scene.play(
            left_top.border.animate.set_stroke(WHITE, width=2.8),  # type: ignore[attr-defined]
            run_time=t_bad * 0.28,
            rate_func=smooth,
        )

    def failure_banner(self) -> AnimationGroup:
        band = SurroundingRectangle(
            VGroup(self.tray, self.string_row),
            color="#ff3333",
            buff=0.22,
            corner_radius=0.06,
            stroke_width=4.0,
        )
        band.set_z_index(3)
        bad = make_geom_cross("#ff3333", height=0.38)
        bad.next_to(self.string_row, UP, buff=0.28)
        bad.set_z_index(26)
        self.scene.add(band, bad)
        self.failure_band = band
        self.failure_bad = bad
        return AnimationGroup(
            FadeIn(band, scale=0.98),
            FadeIn(bad, shift=DOWN * 0.06),
            lag_ratio=0,
        )

    def success_banner(self) -> AnimationGroup:
        band = SurroundingRectangle(
            VGroup(self.tray, self.string_row),
            color="#33cc66",
            buff=0.22,
            corner_radius=0.06,
            stroke_width=4.0,
        )
        band.set_z_index(3)
        ok = make_geom_checkmark("#33cc66", height=0.38)
        ok.next_to(self.string_row, UP, buff=0.28)
        ok.set_z_index(26)
        self.scene.add(band, ok)
        self.success_band = band
        self.success_ok = ok
        return AnimationGroup(
            FadeIn(band, scale=0.98),
            FadeIn(ok, shift=DOWN * 0.06),
            lag_ratio=0,
        )


class ValidParenthesesAnim(Scene):
    def construct(self) -> None:
        self.camera.background_color = BLACK

        slow = 1.05
        t_hl = 0.52 * slow
        t_push = 0.92 * slow
        t_intro = 0.55 * slow
        t_end = 0.95 * slow
        t_pair_r = 0.58 * slow
        t_pair_l = 0.58 * slow
        t_pair_glow = 0.88 * slow

        y_u, y_l = 1.42, -1.42

        upper = BracketRow(self, y_u, "{()}[]")
        lower = BracketRow(self, y_l, "{}(][{")
        upper.add_to_scene()
        lower.add_to_scene()
        self.play(
            FadeIn(upper.tray, shift=RIGHT * 0.1),
            FadeIn(lower.tray, shift=RIGHT * 0.1),
            LaggedStart(
                *[FadeIn(b, scale=0.94) for b in upper.string_boxes],
                lag_ratio=0.05,
            ),
            LaggedStart(
                *[FadeIn(b, scale=0.94) for b in lower.string_boxes],
                lag_ratio=0.05,
            ),
            run_time=t_intro,
            rate_func=smooth,
        )
        self.wait(0.38 * slow)

        upper_steps = ["push", "push", "match", "match", "push", "match"]
        for i in range(6):
            upper.refresh_highlight_pos(i)
            self.play(FadeIn(upper.highlight, scale=0.96), run_time=t_hl, rate_func=smooth)
            u = upper_steps[i]
            if u == "push":
                self.play(upper.anim_push(i), run_time=t_push, rate_func=smooth)
            else:
                upper.play_match_pair(
                    i,
                    t_right=t_pair_r,
                    t_left=t_pair_l,
                    t_glow=t_pair_glow,
                )
            self.play(FadeOut(upper.highlight, scale=0.96), run_time=t_hl * 0.5, rate_func=smooth)

        self.wait(0.35 * slow)
        self.play(upper.success_banner(), run_time=t_end, rate_func=smooth)
        self.wait(0.45 * slow)

        lower_ops: list[tuple[str, int]] = [
            ("push", 0),
            ("match", 1),
            ("push", 2),
            ("fail", 3),
        ]

        for op, idx in lower_ops:
            lower.refresh_highlight_pos(idx)
            self.play(FadeIn(lower.highlight, scale=0.96), run_time=t_hl, rate_func=smooth)
            if op == "push":
                self.play(lower.anim_push(idx), run_time=t_push, rate_func=smooth)
                self.play(FadeOut(lower.highlight, scale=0.96), run_time=t_hl * 0.5, rate_func=smooth)
            elif op == "match":
                lower.play_match_pair(
                    idx,
                    t_right=t_pair_r,
                    t_left=t_pair_l,
                    t_glow=t_pair_glow,
                )
                self.play(FadeOut(lower.highlight, scale=0.96), run_time=t_hl * 0.5, rate_func=smooth)
            else:
                lower.play_match_fail_comparison(
                    idx,
                    t_right=t_pair_r,
                    t_left=t_pair_l,
                    t_bad=t_pair_glow,
                )
                self.play(FadeOut(lower.highlight, scale=0.96), run_time=t_hl * 0.45, rate_func=smooth)
                break

        self.wait(0.38 * slow)
        self.play(lower.failure_banner(), run_time=t_end, rate_func=smooth)
        self.wait(0.95 * slow)
