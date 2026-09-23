#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int h, w;
        cin >> h >> w;
        vector<vector<long long>> G(h, vector<long long>(w));
        vector<long long> rs(h, 0), cs(w, 0); // 行和、列和
        for (int i = 0; i < h; ++i)
            for (int j = 0; j < w; ++j) {
                cin >> G[i][j];
                rs[i] += G[i][j];
                cs[j] += G[i][j];
            }
        long long ans = LLONG_MIN;
        for (long long v : rs) ans = max(ans, v); // 同线摘两次
        for (long long v : cs) ans = max(ans, v);
        if (h >= 2) {
            long long a = LLONG_MIN, b = LLONG_MIN;
            for (long long v : rs) {
                if (v >= a) { b = a; a = v; }
                else if (v > b) b = v;
            }
            ans = max(ans, a + b);
        }
        if (w >= 2) {
            long long a = LLONG_MIN, b = LLONG_MIN;
            for (long long v : cs) {
                if (v >= a) { b = a; a = v; }
                else if (v > b) b = v;
            }
            ans = max(ans, a + b);
        }
        for (int i = 0; i < h; ++i)
            for (int j = 0; j < w; ++j)
                ans = max(ans, rs[i] + cs[j] - G[i][j]); // 一行一列扣交点
        cout << ans << '\n';
    }
    return 0;
}
