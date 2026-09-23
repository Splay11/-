public class Solution {
    public int maximumProfit(int[] duration, int[] deadline, int[] profit) {
        int n = duration.length;
        int[] dpProfit = new int[1 << n];
        int[] dpTime = new int[1 << n];
        for (int mask = 1; mask < (1 << n); mask++) {
            int bestProfit = 0, bestTime = 0;
            for (int j = 0; j < n; j++) {
                if (((mask >> j) & 1) == 0) continue;
                int prevMask = mask ^ (1 << j);
                int finish = dpTime[prevMask] + duration[j];
                int gain = finish <= deadline[j] ? profit[j] : 0;
                int candProfit = dpProfit[prevMask] + gain;
                int candTime = finish;
                if (candProfit > bestProfit
                        || (candProfit == bestProfit && candTime < bestTime)) {
                    bestProfit = candProfit;
                    bestTime = candTime;
                }
            }
            dpProfit[mask] = bestProfit;
            dpTime[mask] = bestTime;
        }
        return dpProfit[(1 << n) - 1];
    }
}
