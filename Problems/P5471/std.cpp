#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 状态压缩求最短巡回时长
int minTour(int m, const vector<int>& lo, const vector<int>& hi, const vector<vector<int>>& dur) {
    int k = m - 1;
    int full = (1 << k) - 1;
    const int INF = 1000000000;
    // dp[mask][u]：已送达集合为 mask、当前停在 u 时的最早到达时刻
    vector<vector<int>> dp(1 << k, vector<int>(m, INF));
    // 时刻 0 停在仓站，还没送过任何客户
    dp[0][0] = 0;
    for (int mask = 0; mask <= full; mask++) {
        for (int u = 0; u < m; u++) {
            int now = dp[mask][u];
            if (now >= INF) {
                continue;
            }
            // 枚举下一个尚未送达的客户
            for (int v = 1; v < m; v++) {
                int bit = 1 << (v - 1);
                if (mask & bit) {
                    continue;
                }
                int t = now + dur[u][v];
                // 早到必须等到可收货下界，等候计入总时长
                if (t < lo[v]) {
                    t = lo[v];
                }
                // 迟到则这条转移非法
                if (t > hi[v]) {
                    continue;
                }
                int nmask = mask | bit;
                if (t < dp[nmask][v]) {
                    dp[nmask][v] = t;
                }
            }
        }
    }
    int ans = INF;
    // 所有客户都送达后，从最后一站回到仓站
    for (int u = 1; u < m; u++) {
        if (dp[full][u] >= INF) {
            continue;
        }
        int t = dp[full][u] + dur[u][0];
        if (t < lo[0]) {
            t = lo[0];
        }
        if (t > hi[0]) {
            continue;
        }
        ans = min(ans, t);
    }
    return ans >= INF ? -1 : ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    cin >> m;
    vector<int> lo(m), hi(m);
    for (int p = 0; p < m; p++) {
        cin >> lo[p] >> hi[p];
    }
    vector<vector<int>> dur(m, vector<int>(m));
    for (int p = 0; p < m; p++) {
        for (int q = 0; q < m; q++) {
            cin >> dur[p][q];
        }
    }
    cout << minTour(m, lo, hi, dur) << "\n";
    return 0;
}
