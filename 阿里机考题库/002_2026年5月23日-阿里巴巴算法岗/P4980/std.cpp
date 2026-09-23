#include <bits/stdc++.h>
using namespace std;

vector<int> primes;
void init_primes() {
    const int N = 32000;
    vector<char> vis(N + 1, 1);
    for (int i = 2; i <= N; ++i) {
        if (!vis[i]) continue;
        primes.push_back(i);
        if (1LL * i * i > N) continue;
        for (int j = i * i; j <= N; j += i) vis[j] = 0;
    }
}
vector<int> factorize(long long x) {
    vector<int> fac;
    for (int p : primes) {
        if (1LL * p * p > x) break;
        if (x % p == 0) {
            fac.push_back(p);
            while (x % p == 0) x /= p;
        }
    }
    if (x > 1) fac.push_back((int)x);
    return fac;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    init_primes();
    int m, t;
    cin >> m >> t;
    vector<long long> v(m);
    for (int i = 0; i < m; ++i) cin >> v[i];
    unordered_map<int, int> pid;
    pid.reserve(m * 4);
    int pc = 0;
    vector<vector<int>> fac_ids(m);
    for (int i = 0; i < m; ++i) {
        if (v[i] == 1) continue; // 1 无法参与长度>=2 的公约链
        for (int p : factorize(v[i])) {
            if (!pid.count(p)) pid[p] = pc++;
            fac_ids[i].push_back(pid[p]);
        }
    }
    auto check = [&](long long M) -> bool {
        if (t == 1) {
            for (long long x : v) if (x <= M) return true;
            return false;
        }
        vector<int> best(pc, 0);
        int mx = 0;
        for (int i = 0; i < m; ++i) {
            if (v[i] > M || v[i] == 1) continue;
            int dp = 1;
            for (int id : fac_ids[i]) dp = max(dp, best[id] + 1);
            mx = max(mx, dp);
            if (mx >= t) return true;
            for (int id : fac_ids[i]) if (best[id] < dp) best[id] = dp;
        }
        return false;
    };
    vector<long long> vals = v;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    long long res = -1;
    int lo = 0, hi = (int)vals.size() - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (check(vals[mid])) { res = vals[mid]; hi = mid - 1; }
        else lo = mid + 1;
    }
    cout << res << '\n';
    return 0;
}
