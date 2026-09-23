# -*- coding: utf-8 -*-
from typing import List, Tuple


class Solution:
    def maximumProfit(
        self, duration: List[int], deadline: List[int], profit: List[int]
    ) -> int:
        n = len(duration)
        # dp[mask] = (最大收益, 达成该收益的最小完成时刻)
        dp: List[Tuple[int, int]] = [(0, 0)] * (1 << n)
        for mask in range(1, 1 << n):
            best_profit, best_time = 0, 0
            for j in range(n):
                if (mask >> j) & 1 == 0:
                    continue
                # 假设任务 j 为当前子集中最后一个执行
                prev_mask = mask ^ (1 << j)
                prev_profit, prev_time = dp[prev_mask]
                finish = prev_time + duration[j]
                gain = profit[j] if finish <= deadline[j] else 0
                cand_profit = prev_profit + gain
                cand_time = finish
                if cand_profit > best_profit or (
                    cand_profit == best_profit and cand_time < best_time
                ):
                    best_profit, best_time = cand_profit, cand_time
            dp[mask] = (best_profit, best_time)
        return dp[(1 << n) - 1][0]
