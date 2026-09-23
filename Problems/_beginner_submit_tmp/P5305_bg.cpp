#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxMaintenanceScore(vector<vector<int>>& windows) {
        vector<vector<int>> a;
        for (auto& x : windows) if (x[1] > x[0]) a.push_back(x);
        if (a.empty()) return 0;
        sort(a.begin(), a.end(), [](auto& p, auto& q) { return p[1] < q[1]; });
        int n = (int)a.size();
        vector<int> ends(n), dp(n + 1, 0);
        for (int i = 0; i < n; i++) ends[i] = a[i][1];
        for (int i = 1; i <= n; i++) {
            int s = a[i - 1][0], sc = a[i - 1][2];
            int lo = 0, hi = i - 2, p = -1;
            while (lo <= hi) {
                int mid = (lo + hi) / 2;
                if (ends[mid] <= s) { p = mid; lo = mid + 1; }
                else hi = mid - 1;
            }
            int take = sc + (p >= 0 ? dp[p + 1] : 0);
            dp[i] = max(dp[i - 1], take);
        }
        return dp[n];
    }
};
