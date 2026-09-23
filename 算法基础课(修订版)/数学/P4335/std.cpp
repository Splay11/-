#include <bits/stdc++.h>
using namespace std;

/*
 * 功能函数：给定 n, l, r
 * 若可满足，返回 {k_min, k_max}；否则返回空可选值
 */
optional<pair<int,int>> solve_case(int n, int l, int r) {
    // 计算向上/向下取整
    int k_min = (l + n - 1) / n; // ceil(l / n)
    int k_max = r / n;           // floor(r / n)
    if (k_min > k_max) return nullopt;
    return make_pair(k_min, k_max);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    for (int tc = 0; tc < T; ++tc) {
        int n, l, r;
        cin >> n >> l >> r;
        auto ans = solve_case(n, l, r);
        if (!ans.has_value()) {
            cout << -1;
        } else {
            cout << ans->first << " " << ans->second;
        }
        if (tc + 1 < T) cout << "\n";
    }
    return 0;
}
