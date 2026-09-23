#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        int64 d;
        cin >> n >> d;
        vector<int64> a(n);
        for (int i = 0; i < n; ++i) {
            cin >> a[i];
        }
        int ans = 1;
        int cur = 1;
        for (int i = 1; i < n; ++i) {
            int64 diff = a[i] - a[i - 1];
            if (diff < 0) {
                diff = -diff;
            }
            if (diff <= d) {
                ++cur;
            } else {
                cur = 1;
            }
            if (cur > ans) {
                ans = cur;
            }
        }
        cout << ans << '\n';
    }
    return 0;
}
