import java.util.*;

public class Solution {
    public int maxSessionScore(int[][] sessions) {
        List<int[]> list = new ArrayList<>();
        for (int[] x : sessions) if (x[1] > x[0]) list.add(x);
        if (list.isEmpty()) return 0;
        list.sort(Comparator.comparingInt(a -> a[1]));
        int n = list.size();
        int[] ends = new int[n];
        for (int i = 0; i < n; i++) ends[i] = list.get(i)[1];
        int[] dp = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            int s = list.get(i - 1)[0], sc = list.get(i - 1)[2];
            // 最右 ends[j] <= s
            int lo = 0, hi = i - 2, p = -1;
            while (lo <= hi) {
                int mid = (lo + hi) >>> 1;
                if (ends[mid] <= s) { p = mid; lo = mid + 1; }
                else hi = mid - 1;
            }
            int take = sc + (p >= 0 ? dp[p + 1] : 0);
            dp[i] = Math.max(dp[i - 1], take);
        }
        return dp[n];
    }
}
