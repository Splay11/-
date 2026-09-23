#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int cycle_period(const string& s) {
    int m = (int)s.size();
    for (int d = 1; d <= m; ++d) {
        if (m % d != 0) continue;
        bool ok = true;
        for (int i = 0; i < m; ++i) {
            if (s[i] != s[i % d]) {
                ok = false;
                break;
            }
        }
        if (ok) return d;
    }
    return m;
}

void factor_max(int x, map<int, int>& mx) {
    for (int p = 2; 1LL * p * p <= x; ++p) {
        if (x % p == 0) {
            int e = 0;
            while (x % p == 0) {
                x /= p;
                ++e;
            }
            mx[p] = max(mx[p], e);
        }
    }
    if (x > 1) mx[x] = max(mx[x], 1);
}

long long mod_pow(long long a, int e) {
    long long r = 1;
    while (e > 0) {
        if (e & 1) r = r * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    string u;
    cin >> u;
    vector<int> p(n);
    for (int i = 0; i < n; ++i) {
        cin >> p[i];
        --p[i];
    }

    vector<char> vis(n, false);
    map<int, int> mx;
    for (int i = 0; i < n; ++i) {
        if (vis[i]) continue;
        string cyc;
        int x = i;
        while (!vis[x]) {
            vis[x] = true;
            cyc.push_back(u[x]);
            x = p[x];
        }
        factor_max(cycle_period(cyc), mx);
    }

    long long ans = 1;
    for (map<int, int>::iterator it = mx.begin(); it != mx.end(); ++it) {
        ans = ans * mod_pow(it->first, it->second) % MOD;
    }
    cout << ans << '\n';
    return 0;
}
