class Solution {
    public int maxLoadDrop(int[] loads) {
        int peak = loads[0], ans = 0;
        for (int x : loads) {
            if (peak - x > ans) ans = peak - x;
            if (x > peak) peak = x;
        }
        return ans;
    }
}
