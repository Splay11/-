#include <bits/stdc++.h>
using namespace std;

vector<int> primes_upto(int m) {
    vector<bool> isP(m + 1, true);
    isP[0] = isP[1] = false;
    for (int i = 2; i * i <= m; ++i) {
        if (isP[i]) {
            for (int j = i * i; j <= m; j += i) isP[j] = false;
        }
    }
    vector<int> ps;
    for (int i = 2; i <= m; ++i) if (isP[i]) ps.push_back(i);
    return ps;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; 
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    vector<int> ps = primes_upto(100);
    int ans = 0;
    for (int p : ps) {
        int pre2 = 0, pre1 = 0; // dp[i-2], dp[i-1]
        for (int x : a) {
            int b = (x % p == 0) ? 1 : 0;
            int cur = max(pre1, pre2 + b);
            pre2 = pre1; pre1 = cur;
        }
        ans = max(ans, pre1);
    }
    cout << ans << "\n";
    return 0;
}
