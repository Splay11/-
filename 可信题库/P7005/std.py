from typing import List

MOD = 10**9 + 7


class Solution:
    def sumPeakRisk(self, loads: List[int]) -> int:
        n = len(loads)
        left = [0] * n
        right = [0] * n
        st: List[int] = []
        # 左侧：最近严格更大元素；left[i] 为可延伸跨度（含自身）
        for i in range(n):
            while st and loads[st[-1]] <= loads[i]:
                st.pop()
            left[i] = i - (st[-1] if st else -1)
            st.append(i)
        st.clear()
        # 右侧：最近大于等于；相等峰值只计一次（靠右侧 >= 切开）
        for i in range(n - 1, -1, -1):
            while st and loads[st[-1]] < loads[i]:
                st.pop()
            right[i] = (st[-1] if st else n) - i
            st.append(i)
        ans = 0
        for i in range(n):
            ans = (ans + loads[i] * left[i] * right[i]) % MOD
        return ans
