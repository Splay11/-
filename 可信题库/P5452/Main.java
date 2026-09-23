import java.util.*;

class Solution {
    public long minCircleMerge(int[] weights) {
        int n = weights.length;
        if (n <= 1) return 0;
        if (n == 2) return (long) weights[0] + weights[1];

        int m = 2 * n;
        int[] a = new int[m];
        for (int i = 0; i < n; i++) {
            a[i] = weights[i];
            a[i + n] = weights[i];
        }
        long[] pref = new long[m + 1];
        for (int i = 0; i < m; i++) pref[i + 1] = pref[i] + a[i];

        final long INF = Long.MAX_VALUE / 4;
        long[][] dp = new long[m][m];
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < m; i++) {
                int j = i + len - 1;
                long best = INF;
                for (int k = i; k < j; k++) {
                    best = Math.min(best, dp[i][k] + dp[k + 1][j]);
                }
                dp[i][j] = best + (pref[j + 1] - pref[i]);
            }
        }
        long ans = INF;
        for (int i = 0; i < n; i++) ans = Math.min(ans, dp[i][i + n - 1]);
        return ans;
    }
}
