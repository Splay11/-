#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    long long minCircleMerge(vector<int>& weights) {
        int n = (int)weights.size();
        if (n <= 1) return 0;
        if (n == 2) return (long long)weights[0] + weights[1];

        int m = 2 * n;
        vector<int> a = weights;
        a.insert(a.end(), weights.begin(), weights.end());
        vector<long long> pref(m + 1, 0);
        for (int i = 0; i < m; i++) pref[i + 1] = pref[i] + a[i];

        const long long INF = (1LL << 62);
        vector<vector<long long>> dp(m, vector<long long>(m, 0));
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < m; i++) {
                int j = i + len - 1;
                long long best = INF;
                for (int k = i; k < j; k++) {
                    best = min(best, dp[i][k] + dp[k + 1][j]);
                }
                dp[i][j] = best + (pref[j + 1] - pref[i]);
            }
        }
        long long ans = INF;
        for (int i = 0; i < n; i++) ans = min(ans, dp[i][i + n - 1]);
        return ans;
    }
};
