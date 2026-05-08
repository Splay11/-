#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

// 在区间端点包含的情况下，两区间不冲突当且仅当后一段的起点严格大于上一段的终点。
int solve_interval_scheduling(int n, const vector<pair<int64, int64>> &intervals) {
    vector<pair<int64, int64>> a = intervals;
    sort(a.begin(), a.end(), [](const pair<int64, int64> &x, const pair<int64, int64> &y) {
        if (x.second != y.second) {
            return x.second < y.second;
        }
        return x.first < y.first;
    });
    int64 last_end = (int64)-4e18;
    int cnt = 0;
    for (const auto &pr : a) {
        int64 s = pr.first;
        int64 e = pr.second;
        if (s > last_end) {
            ++cnt;
            last_end = e;
        }
    }
    return cnt;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }
    vector<int64> flat(2 * n);
    for (int i = 0; i < 2 * n; ++i) {
        cin >> flat[i];
    }
    vector<pair<int64, int64>> intervals;
    intervals.reserve(n);
    for (int i = 0; i < n; ++i) {
        intervals.emplace_back(flat[2 * i], flat[2 * i + 1]);
    }
    cout << solve_interval_scheduling(n, intervals) << '\n';
    return 0;
}
