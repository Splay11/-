public class Solution {
    public int maxOnline(int[] changes) {
        // cur 当前在线，ans 历史峰值
        int cur = 0;
        int ans = 0;
        for (int x : changes) {
            // 模拟每一时刻的增减
            cur += x;
            if (cur > ans) {
                ans = cur;
            }
        }
        return ans;
    }
}
