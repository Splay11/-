#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    long long countLiveWindows(vector<int>& loads, int cap) {
        int n = (int)loads.size();
        vector<long long> pref(n + 1, 0);
        for (int i = 0; i < n; ++i) pref[i + 1] = pref[i] + loads[i];
        vector<long long> dp(n + 2, 0);
        for (int i = n - 1; i >= 0; --i) {
            // 第一个使 pref[q] > pref[i] + cap 的位置
            int q = (int)(upper_bound(pref.begin(), pref.end(), pref[i] + cap) - pref.begin());
            dp[i] = dp[q] + (q - i - 1);
        }
        long long ans = 0;
        for (int i = 0; i <= n; ++i) ans += dp[i];
        return ans;
    }
};
