# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def longestValidSkillChain(self, type: List[int]) -> int:
        n = len(type)
        if n == 0:
            return 0

        dp0 = dp1 = dp2 = 0
        ans = 0

        for i in range(n):
            nd0 = nd1 = nd2 = 0
            if type[i] == 0:
                nd0 = 1
                if i > 0:
                    nd0 = max(nd0, dp0 + 1, dp1 + 1, dp2 + 1)
            elif type[i] == 1:
                if i > 0 and type[i - 1] == 0 and dp0 > 0:
                    nd1 = dp0 + 1
            elif type[i] == 2:
                if i >= 2 and type[i - 1] == 0 and type[i - 2] == 0 and dp0 > 0:
                    nd2 = dp0 + 1

            dp0, dp1, dp2 = nd0, nd1, nd2
            ans = max(ans, dp0, dp1, dp2)

        return ans
