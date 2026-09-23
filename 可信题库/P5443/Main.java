class Solution {
    public int minAdjacentGap(int[] cookies) {
        // 先把第一对相邻烤盘的差当作当前最小答案
        int ans = Math.abs(cookies[1] - cookies[0]);
        for (int i = 1; i + 1 < cookies.length; i++) {
            // 算第 i 盘和第 i+1 盘的差，差值不分方向，取绝对值
            int gap = Math.abs(cookies[i + 1] - cookies[i]);
            // 出现更小的差就更新答案
            if (gap < ans) {
                ans = gap;
            }
        }
        return ans;
    }
}
