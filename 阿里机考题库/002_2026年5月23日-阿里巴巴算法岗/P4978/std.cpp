#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        long long s;
        cin >> m >> s;
        vector<long long> h(m);
        for (int i = 0; i < m; ++i) cin >> h[i];
        // 硬度从大到小：优先尝试更硬的工件
        sort(h.begin(), h.end(), greater<long long>());
        int cnt = 0;
        for (long long x : h) {
            // 已成功 cnt 次，当前耐久为 s - cnt
            if (s - cnt >= x) ++cnt;
        }
        cout << cnt << '\n';
    }
    return 0;
}
