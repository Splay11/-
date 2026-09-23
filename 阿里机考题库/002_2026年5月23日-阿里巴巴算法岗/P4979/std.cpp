#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<long long> x(m), y(m);
        vector<int> p(m);
        for (int i = 0; i < m; ++i) cin >> x[i];
        for (int i = 0; i < m; ++i) cin >> y[i];
        for (int i = 0; i < m; ++i) cin >> p[i];
        unordered_map<long long, int> freq;
        freq.reserve(m * 2);
        long long ans = 0;
        for (int v = 0; v < m; ++v) {
            ++freq[x[v]]; // 前缀纳入 x_v
            ans += freq[y[p[v] - 1]]; // 累加等于 y_{p_v} 的个数
        }
        cout << ans << '\n';
    }
    return 0;
}
