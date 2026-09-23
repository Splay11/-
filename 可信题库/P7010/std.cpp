#include <vector>
using namespace std;

class Solution {
 public:
  long long minRotateCost(vector<int>& sens, int baseCost, int maxBatches) {
    int n = (int)sens.size();
    vector<long long> pref(n + 1, 0);
    for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + sens[i];
    const long long INF = (1LL << 62);
    vector<vector<long long>> dp(n + 1, vector<long long>(maxBatches + 1, INF));
    dp[0][0] = 0;
    for (int i = 1; i <= n; i++) {
      for (int j = 0; j < i; j++) {
        long long cost = baseCost + (pref[i] - pref[j]) * (i - j);
        for (int b = 1; b <= maxBatches; b++) {
          if (dp[j][b - 1] != INF && dp[j][b - 1] + cost < dp[i][b])
            dp[i][b] = dp[j][b - 1] + cost;
        }
      }
    }
    long long ans = INF;
    for (int b = 1; b <= maxBatches; b++) ans = min(ans, dp[n][b]);
    return ans;
  }
};
