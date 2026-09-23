#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

// 把业务条目映射成二进制，每台机器变成覆盖掩码，再做 0-1 最短覆盖 DP
int minDevices(const vector<vector<int>>& specs, const vector<int>& need) {
    unordered_map<int, int> bit;
    int t = (int)need.size();
    // 只关心业务点名的条目，给它们编号 0..t-1
    for (int i = 0; i < t; i++) {
        bit[need[i]] = i;
    }
    vector<int> covers;
    for (const auto& row : specs) {
        int mask = 0;
        for (int x : row) {
            auto it = bit.find(x);
            if (it != bit.end()) {
                mask |= 1 << it->second;
            }
        }
        covers.push_back(mask);
    }
    int full = (1 << t) - 1;
    int inf = t + 5;
    // dp[s]：覆盖集合恰好为 s 时的最少台数
    vector<int> dp(1 << t, inf);
    dp[0] = 0;
    for (int c : covers) {
        if (c == 0) {
            continue;
        }
        // 倒序枚举，保证每台机器最多用一次
        for (int s = full; s >= 0; s--) {
            if (dp[s] >= inf) {
                continue;
            }
            int ns = s | c;
            int v = dp[s] + 1;
            if (v < dp[ns]) {
                dp[ns] = v;
            }
        }
    }
    return dp[full] >= inf ? 0 : dp[full];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int d, w, t;
    cin >> d >> w >> t;
    vector<vector<int>> specs(d, vector<int>(w));
    for (int i = 0; i < d; i++) {
        for (int j = 0; j < w; j++) {
            cin >> specs[i][j];
        }
    }
    vector<int> need(t);
    for (int i = 0; i < t; i++) {
        cin >> need[i];
    }
    cout << minDevices(specs, need) << '\n';
    return 0;
}
