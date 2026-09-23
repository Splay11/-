import java.util.*;

public class Main {
    public static void main(String[] args) {}
}

class Solution {
    public long minRotateCost(int[] sens, int baseCost, int maxBatches) {
        int n = sens.length;
        long[] pref = new long[n + 1];
        for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + sens[i];
        long inf = (1L << 62);
        long[][] dp = new long[n + 1][maxBatches + 1];
        for (int i = 0; i <= n; i++) Arrays.fill(dp[i], inf);
        dp[0][0] = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                long cost = baseCost + (pref[i] - pref[j]) * (i - j);
                for (int b = 1; b <= maxBatches; b++) {
                    if (dp[j][b - 1] != inf && dp[j][b - 1] + cost < dp[i][b])
                        dp[i][b] = dp[j][b - 1] + cost;
                }
            }
        }
        long ans = inf;
        for (int b = 1; b <= maxBatches; b++) ans = Math.min(ans, dp[n][b]);
        return ans;
    }
}
