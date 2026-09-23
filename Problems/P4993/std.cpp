#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    if (!(cin >> q)) return 0;
    while (q--) {
        int m;
        cin >> m;
        vector<long long> h(m);
        for (int i = 0; i < m; ++i) cin >> h[i];
        vector<int> L(m), R(m);
        long long mx = -1;
        int pos = -1;
        for (int i = 0; i < m; ++i) {
            L[i] = pos;
            if (h[i] > mx) {
                mx = h[i];
                pos = i;
            } else if (h[i] == mx) {
                pos = i;
            }
        }
        mx = -1;
        pos = -1;
        for (int i = m - 1; i >= 0; --i) {
            R[i] = pos;
            if (h[i] > mx) {
                mx = h[i];
                pos = i;
            } else if (h[i] == mx) {
                pos = i;
            }
        }
        int ans = 0;
        for (int p = 1; p + 1 < m; ++p) {
            if (p - L[p] == R[p] - p) ++ans;
        }
        cout << ans << '\n';
    }
    return 0;
}
