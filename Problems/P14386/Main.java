public class Solution {
    public int longestValidSkillChain(int[] type) {
        int n = type.length;
        if (n == 0) return 0;

        int dp0 = 0, dp1 = 0, dp2 = 0, ans = 0;
        for (int i = 0; i < n; i++) {
            int nd0 = 0, nd1 = 0, nd2 = 0;
            if (type[i] == 0) {
                nd0 = 1;
                if (i > 0) nd0 = Math.max(nd0, Math.max(dp0 + 1, Math.max(dp1 + 1, dp2 + 1)));
            } else if (type[i] == 1) {
                if (i > 0 && type[i - 1] == 0 && dp0 > 0) nd1 = dp0 + 1;
            } else if (type[i] == 2) {
                if (i >= 2 && type[i - 1] == 0 && type[i - 2] == 0 && dp0 > 0) nd2 = dp0 + 1;
            }
            dp0 = nd0;
            dp1 = nd1;
            dp2 = nd2;
            ans = Math.max(ans, Math.max(dp0, Math.max(dp1, dp2)));
        }
        return ans;
    }
}
