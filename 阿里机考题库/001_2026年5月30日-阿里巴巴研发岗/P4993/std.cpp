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
        vector<long long> h(m);
        for (int i = 0; i < m; ++i) cin >> h[i];
        vector<int> L(m), R(m);
        long long mx = -1;
        int pos = -1;
        // 左扫：左侧最大值最近下标
        for (int i = 0; i < m; ++i) {
            L[i] = pos;
            if (h[i] > mx) { mx = h[i]; pos = i; }
            else if (h[i] == mx) pos = i;
        }
        mx = -1; pos = -1;
        // 右扫：右侧最大值最近下标
        for (int i = m - 1; i >= 0; --i) {
            R[i] = pos;
            if (h[i] > mx) { mx = h[i]; pos = i; }
            else if (h[i] == mx) pos = i;
        }
        int ans = 0;
        for (int p = 1; p + 1 < m; ++p)
            if (p - L[p] == R[p] - p) ++ans; // 等距峰点
        cout << ans << '\n';
    }
    return 0;
}
