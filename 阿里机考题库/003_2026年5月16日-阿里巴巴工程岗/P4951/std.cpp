#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    const long long MOD = 1000000007;
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<long long> h(m);
        for (int i = 0; i < m; ++i) cin >> h[i];
        vector<pair<long long, long long>> st; // (最小值, 段数)
        long long cur = 0, ans = 0;
        for (int k = 1; k <= m; ++k) {
            long long x = h[k - 1];
            long long cnt = 1;
            while (!st.empty() && st.back().first >= x) {
                cur -= st.back().first * st.back().second;
                cnt += st.back().second;
                st.pop_back();
            }
            st.push_back({x, cnt});
            cur += x * cnt;
            cur %= MOD;
            if (cur < 0) cur += MOD;
            ans = (ans + cur * (m - k + 1)) % MOD;
        }
        cout << ans << '\n';
    }
    return 0;
}
