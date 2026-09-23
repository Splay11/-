#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

static bool feasible(int n, int64 m, const vector<int64> &s, int64 G) {
    if (G <= 0) {
        return true;
    }
    vector<int64> gap(max(0, n - 1));
    for (int i = 0; i + 1 < n; ++i) {
        gap[i] = s[i + 1] - s[i];
    }
    int tot_bad = 0;
    for (int i = 0; i + 1 < n; ++i) {
        if (gap[i] < G) {
            ++tot_bad;
        }
    }
    vector<int> pref_bad(n - 1, 0);
    for (int i = 0; i + 1 < n; ++i) {
        pref_bad[i] = (i ? pref_bad[i - 1] : 0) + (gap[i] < G ? 1 : 0);
    }
    vector<int64> pref_max = gap;
    for (int i = 1; i + 1 < n; ++i) {
        pref_max[i] = max(pref_max[i - 1], pref_max[i]);
    }
    vector<int64> suf_max = gap;
    for (int i = (int)gap.size() - 2; i >= 0; --i) {
        suf_max[i] = max(suf_max[i], suf_max[i + 1]);
    }
    vector<int> pref_large(n - 1, -1);
    for (int i = 0; i + 1 < n; ++i) {
        if (gap[i] < G) {
            pref_large[i] = max((i ? pref_large[i - 1] : -1), i);
        } else {
            pref_large[i] = (i ? pref_large[i - 1] : -1);
        }
    }
    vector<int> suf_small(n - 1, INT_MAX);
    for (int i = (int)gap.size() - 1; i >= 0; --i) {
        if (gap[i] < G) {
            int nxt = (i + 1 < (int)suf_small.size() ? suf_small[i + 1] : INT_MAX);
            suf_small[i] = min(nxt, i);
        } else {
            suf_small[i] = (i + 1 < (int)suf_small.size() ? suf_small[i + 1] : INT_MAX);
        }
    }

    auto bad_left = [&](int k) -> int {
        if (k < 2) {
            return 0;
        }
        return pref_bad[k - 2];
    };
    auto bad_right = [&](int k) -> int {
        if (k >= n - 1) {
            return 0;
        }
        return tot_bad - pref_bad[k];
    };
    auto bad_bridge = [&](int k) -> int {
        if (k <= 0 || k >= n - 1) {
            return 0;
        }
        return (s[k + 1] - s[k - 1] < G) ? 1 : 0;
    };

    for (int k = 0; k < n; ++k) {
        int bl = bad_left(k);
        int br = bad_right(k);
        int bb = bad_bridge(k);
        int tb = bl + br + bb;
        if (tb > 1) {
            continue;
        }
        int64 first_t = (k != 0 ? s[0] : s[1]);
        int64 last_t = (k != n - 1 ? s[n - 1] : s[n - 2]);
        if (tb == 0) {
            if (first_t >= G + 1) {
                return true;
            }
            if (last_t <= m - G) {
                return true;
            }
            int64 mx = -1;
            if (k >= 2) {
                mx = max(mx, pref_max[k - 2]);
            }
            if (k + 1 <= n - 2) {
                mx = max(mx, suf_max[k + 1]);
            }
            if (k > 0 && k < n - 1) {
                mx = max(mx, s[k + 1] - s[k - 1]);
            }
            if (mx >= 2 * G) {
                return true;
            }
            continue;
        }
        int64 u = 0, v = 0;
        bool ok = false;
        if (bb == 1 && bl == 0 && br == 0) {
            u = s[k - 1];
            v = s[k + 1];
            ok = true;
        } else if (bl == 1 && br == 0 && bb == 0) {
            int idx = pref_large[k - 2];
            u = s[idx];
            v = s[idx + 1];
            ok = true;
        } else if (br == 1 && bl == 0 && bb == 0) {
            int idx = suf_small[k + 1];
            if (idx == INT_MAX) {
                continue;
            }
            u = s[idx];
            v = s[idx + 1];
            ok = true;
        }
        if (!ok) {
            continue;
        }
        if (v - u < 2 * G) {
            continue;
        }
        int64 L = max<int64>(1, u + G);
        int64 R = min(m, v - G);
        if (L <= R) {
            return true;
        }
    }
    return false;
}

static int64 solve_one(int n, int64 m, vector<int64> a) {
    sort(a.begin(), a.end());
    int64 lo = 0, hi = m;
    while (lo < hi) {
        int64 mid = (lo + hi + 1) / 2;
        if (feasible(n, m, a, mid)) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    return lo;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) {
        return 0;
    }
    while (T--) {
        int n;
        int64 m;
        cin >> n >> m;
        vector<int64> a(n);
        for (int i = 0; i < n; ++i) {
            cin >> a[i];
        }
        cout << solve_one(n, m, std::move(a)) << '\n';
    }
    return 0;
}
