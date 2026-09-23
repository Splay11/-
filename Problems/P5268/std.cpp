#include <cmath>
#include <iostream>
#include <map>
#include <tuple>
#include <vector>
using namespace std;

static int n, m, p, q, y;
static vector<long long> a, b;
static map<tuple<int, int, int, int, long long>, long long> memo;

static long long isqrt_ll(long long x) {
    if (x <= 0) return 0;
    long long r = (long long)sqrt((long double)x);
    while (r > 0 && r > x / r) r--;
    while (r + 1 > 0 && r + 1 <= x / (r + 1)) r++;
    return r;
}

static bool dfs(long long hp, int ma, int mb, int u3, int u4, long long pend) {
    if (hp < 1) return true;
    auto key = make_tuple(ma, mb, u3, u4, pend);
    auto it = memo.find(key);
    if (it != memo.end() && it->second <= hp) return false;
    memo[key] = hp;

    if (pend == 1) {
        for (int i = 0; i < n; i++) {
            if ((ma >> i) & 1) continue;
            if (dfs(hp, ma | (1 << i), mb, u3, u4, a[i])) return true;
        }
    }

    long long mult = pend;
    for (int j = 0; j < m; j++) {
        if ((mb >> j) & 1) continue;
        long long nhp;
        if (mult != 0 && b[j] > (hp - 1) / mult) nhp = 0;
        else nhp = hp - b[j] * mult;
        if (dfs(nhp, ma, mb | (1 << j), u3, u4, 1)) return true;
    }
    if (!u3) {
        long long dmg = hp * p / q;
        if (dfs(hp - dmg, ma, mb, 1, u4, 1)) return true;
    }
    if (!u4) {
        long long dmg = isqrt_ll(hp);
        if (dfs(hp - dmg, ma, mb, u3, 1, 1)) return true;
    }
    return false;
}

static bool solve_one() {
    memo.clear();
    long long hp = 1;
    for (int i = 0; i < y; i++) hp *= 10;
    return dfs(hp, 0, 0, 0, 0, 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        cin >> n >> m >> p >> q >> y;
        a.assign(n, 0);
        b.assign(m, 0);
        for (int i = 0; i < n; i++) cin >> a[i];
        for (int i = 0; i < m; i++) cin >> b[i];
        cout << (solve_one() ? "Yes" : "No") << '\n';
    }
    return 0;
}
