public class Solution {
    public int countIsolatedIntervals(int[][] intervals) {
        int n = intervals.length;
        int ans = 0;
        for (int i = 0; i < n; i++) {
            int s1 = intervals[i][0], e1 = intervals[i][1];
            boolean isolated = true;
            for (int j = 0; j < n; j++) {
                if (i == j) continue;
                int s2 = intervals[j][0], e2 = intervals[j][1];
                if (s1 <= e2 && s2 <= e1) {
                    isolated = false;
                    break;
                }
            }
            if (isolated) ans++;
        }
        return ans;
    }
}
