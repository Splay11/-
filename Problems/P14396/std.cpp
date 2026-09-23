#include <algorithm>
#include <utility>
#include <vector>

using namespace std;

class Solution {
 public:
  int maximumProfit(vector<int>& duration, vector<int>& deadline,
                    vector<int>& profit) {
    int n = duration.size();
    vector<pair<int, int>> dp(1 << n, {0, 0});
    for (int mask = 1; mask < (1 << n); mask++) {
      int bestProfit = 0, bestTime = 0;
      for (int j = 0; j < n; j++) {
        if (((mask >> j) & 1) == 0) continue;
        int prevMask = mask ^ (1 << j);
        auto [prevProfit, prevTime] = dp[prevMask];
        int finish = prevTime + duration[j];
        int gain = (finish <= deadline[j]) ? profit[j] : 0;
        int candProfit = prevProfit + gain;
        int candTime = finish;
        if (candProfit > bestProfit ||
            (candProfit == bestProfit && candTime < bestTime)) {
          bestProfit = candProfit;
          bestTime = candTime;
        }
      }
      dp[mask] = {bestProfit, bestTime};
    }
    return dp[(1 << n) - 1].first;
  }
};
