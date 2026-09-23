import java.util.*;

class Solution {
    public long countLiveWindows(int[] loads, int cap) {
        int n = loads.length;
        long[] pref = new long[n + 1];
        for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + loads[i];
        long[] dp = new long[n + 2];
        for (int i = n - 1; i >= 0; i--) {
            int q = upperBound(pref, pref[i] + cap);
            dp[i] = dp[q] + (q - i - 1);
        }
        long ans = 0;
        for (int i = 0; i <= n; i++) ans += dp[i];
        return ans;
    }

    // 第一个严格大于 target 的下标
    private int upperBound(long[] pref, long target) {
        int lo = 0, hi = pref.length;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (pref[mid] <= target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
}
