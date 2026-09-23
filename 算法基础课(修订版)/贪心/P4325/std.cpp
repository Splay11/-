#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        int g = 0, len = 0, ans = 0;
        for (int x : a) {
            g = std::gcd(g, x);
            ++len;
            if (g <= len) {   // 能切就切
                ++ans;
                g = 0;
                len = 0;
            }
        }
        cout << (ans == 0 ? -1 : ans) << "\n";
    }
    return 0;
}
