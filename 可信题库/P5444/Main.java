class Solution {
    public long bestCorrectedTotal(int[] scores) {
        long total = 0;
        // 数组非空，先把第一项当作最小值
        int mn = scores[0];
        // 一趟循环同时求出原总分与最小项
        for (int v : scores) {
            total += v;
            if (v < mn) mn = v;
        }
        // 订正最小项得到最大总分 total - 2 * mn；总和可能超 32 位，用 long
        return total - 2L * mn;
    }
}
