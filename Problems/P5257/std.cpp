#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

struct FenwickMax {
    int n;
    vector<int> a;
    FenwickMax() : n(0) {}
    explicit FenwickMax(int n_) : n(n_), a(n_ + 1, 0) {}
    void upd(int i, int v) {
        while (i <= n) {
            a[i] = max(a[i], v);
            i += i & -i;
        }
    }
    int qry(int i) const {
        int r = 0;
        while (i > 0) {
            r = max(r, a[i]);
            i -= i & -i;
        }
        return r;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> u(m), v(m), w(m);
    vector<vector<int>> inc(n + 1);
    for (int i = 0; i < m; ++i) {
        cin >> u[i] >> v[i] >> w[i];
        inc[v[i]].push_back(w[i]);
    }
    vector<vector<int>> comp(n + 1);
    vector<FenwickMax> bits(n + 1);
    for (int i = 1; i <= n; ++i) {
        if (inc[i].empty()) continue;
        sort(inc[i].begin(), inc[i].end());
        inc[i].erase(unique(inc[i].begin(), inc[i].end()), inc[i].end());
        comp[i] = inc[i];
        bits[i] = FenwickMax((int)comp[i].size());
    }
    int ans = 0;
    for (int i = 0; i < m; ++i) {
        int best = 1;
        if (!comp[u[i]].empty()) {
            int k = (int)(lower_bound(comp[u[i]].begin(), comp[u[i]].end(), w[i]) - comp[u[i]].begin());
            if (k) best = 1 + bits[u[i]].qry(k);
        }
        ans = max(ans, best);
        int pos = (int)(lower_bound(comp[v[i]].begin(), comp[v[i]].end(), w[i]) - comp[v[i]].begin()) + 1;
        bits[v[i]].upd(pos, best);
    }
    cout << ans << '\n';
    return 0;
}
