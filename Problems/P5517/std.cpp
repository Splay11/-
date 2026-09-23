#include <bits/stdc++.h>
using namespace std;

long long kadane(const vector<long long>& a) {
    long long best = a[0], cur = a[0];
    for (size_t i = 1; i < a.size(); i++) {
        cur = max(a[i], cur + a[i]);
        best = max(best, cur);
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    long long one = kadane(a);
    if (k == 1) {
        cout << one << "\n";
        return 0;
    }
    long long total = 0;
    for (long long x : a) total += x;
    // 最大前缀和
    long long s = 0, max_pref = a[0];
    for (long long x : a) {
        s += x;
        max_pref = max(max_pref, s);
    }
    // 最大后缀和
    s = 0;
    long long max_suf = a[n - 1];
    for (int i = n - 1; i >= 0; i--) {
        s += a[i];
        max_suf = max(max_suf, s);
    }
    long long ans = max(one, max_suf + max_pref);
    if (k > 2 && total > 0) {
        ans = max(ans, max_suf + (k - 2) * total + max_pref);
    }
    cout << ans << "\n";
    return 0;
}
