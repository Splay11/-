# -*- coding: utf-8 -*-
"""
MinStack 动画 — 1080p（1920×1080）成片入口。

在导入 `min_stack_anim` 之前设置环境变量；并在此模块内定义 `MinStackAnim` 子类，
以便 Manim CLI 能在本文件中解析到场景（仅 `from min_stack_anim import MinStackAnim` 会被判定为「无场景」）。

渲染（项目根目录）:
  python -m manim min_stack_anim_1080p.py MinStackAnim
"""

from __future__ import annotations

import os

os.environ["MIN_STACK_ANIM_RES"] = "1080p"

from min_stack_anim import MinStackAnim as _MinStackAnimBase


class MinStackAnim(_MinStackAnimBase):
    """与 `min_stack_anim.MinStackAnim` 相同，供本文件作为 1080p 渲染入口。"""


__all__ = ["MinStackAnim"]
