# -*- coding: utf-8 -*-
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    INT_MIN = -2147483648

    def analyzeSpiritPaths(self, root: Optional[TreeNode], threshold: int) -> List[int]:
        if root is None:
            return [self.INT_MIN, 0, 0]

        max_val = self.INT_MIN
        count = 0
        has_ge = 0

        def dfs(node: TreeNode, cur_sum: int, prev_neg: bool) -> None:
            nonlocal max_val, count, has_ge
            is_neg = node.val < 0
            if is_neg and prev_neg:
                return

            new_sum = cur_sum + node.val
            is_leaf = node.left is None and node.right is None
            if is_leaf:
                max_val = max(max_val, new_sum)
                count += 1
                if new_sum >= threshold:
                    has_ge = 1
                return

            if node.left is not None:
                dfs(node.left, new_sum, is_neg)
            if node.right is not None:
                dfs(node.right, new_sum, is_neg)

        dfs(root, 0, False)
        if count == 0:
            max_val = self.INT_MIN
        return [max_val, has_ge, count]
