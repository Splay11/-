#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        long long d;
        cin >> m >> d;
        vector<long long> h(m);
        for (int i = 0; i < m; ++i) cin >> h[i];
        // dp0 = 前 i-1 人方案数，dp1 = 前 i 人方案数；空方案记为 1
        long long dp0 = 1, dp1 = 1;
        for (int i = 1; i < m; ++i) {
            long long nd = dp1; // 第 i 人单人组
            if (h[i] - h[i - 1] <= d) {
                // 与前一人配对
                nd = (nd + dp0) % MOD;
            }
            dp0 = dp1;
            dp1 = nd;
        }
        cout << (m == 0 ? 1 : dp1) << '\n';
    }
    return 0;
}
