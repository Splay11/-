// 标准 DP：dp[j][k] 表示当前占用体积为 j、是否已触发优惠 k 时的最大货值
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

long long maxValue(int n, int W, int T, const vector<int>& v, const vector<int>& w) {
    const long long NEG = -1;
    // dp[vol][trig]：占用 vol、触发标记 trig 的最大货值；-1 表示不可达
    vector<vector<long long>> dp(W + 1, vector<long long>(2, NEG));
    dp[0][0] = 0;
    for (int i = 0; i < n; i++) {
        // 先复制上一轮，对应不装第 i 件
        vector<vector<long long>> newDp = dp;
        for (int vol = 0; vol <= W; vol++) {
            for (int trig = 0; trig <= 1; trig++) {
                if (dp[vol][trig] < 0) {
                    continue;
                }
                // 装第 i 件：未触发用原体积，已触发用折半
                int cost = trig ? (v[i] / 2) : v[i];
                int nvol = vol + cost;
                if (nvol > W) {
                    continue;
                }
                // 装上后体积首次达到 T，之后才算触发
                int ntrig = (trig || nvol >= T) ? 1 : 0;
                long long val = dp[vol][trig] + w[i];
                if (val > newDp[nvol][ntrig]) {
                    newDp[nvol][ntrig] = val;
                }
            }
        }
        dp.swap(newDp);
    }
    // 所有可达状态里取最大货值
    long long ans = 0;
    for (int vol = 0; vol <= W; vol++) {
        for (int trig = 0; trig <= 1; trig++) {
            ans = max(ans, dp[vol][trig]);
        }
    }
    return ans;
}

int main() {
    int n, W, T;
    // 第一行：货物件数、载重上限、优惠阈值
    cin >> n >> W >> T;
    vector<int> v(n), w(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i] >> w[i];
    }
    cout << maxValue(n, W, T, v, w) << "\n";
    return 0;
}
