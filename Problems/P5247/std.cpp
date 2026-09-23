#include <bits/stdc++.h>
using namespace std;

vector<vector<long long>> enum_sums(const vector<long long>& arr) {
    int n = (int)arr.size();
    vector<vector<long long>> by_cnt(n + 1);
    for (int mask = 0; mask < (1 << n); ++mask) {
        long long s = 0;
        int c = 0;
        for (int i = 0; i < n; ++i) {
            if (mask >> i & 1) {
                s += arr[i];
                ++c;
            }
        }
        by_cnt[c].push_back(s);
    }
    for (int c = 0; c <= n; ++c) {
        sort(by_cnt[c].begin(), by_cnt[c].end());
    }
    return by_cnt;
}

long long min_diff(const vector<long long>& vals) {
    int n = (int)vals.size();
    int half = n / 2;
    long long tot = 0;
    for (int i = 0; i < n; ++i) {
        tot += vals[i];
    }
    vector<long long> left(vals.begin(), vals.begin() + half);
    vector<long long> right(vals.begin() + half, vals.end());
    vector<vector<long long>> sl = enum_sums(left);
    vector<vector<long long>> sr = enum_sums(right);
    long long best = tot;
    for (int k = 0; k <= half; ++k) {
        const vector<long long>& A = sl[k];
        const vector<long long>& B = sr[half - k];
        if (A.empty() || B.empty()) {
            continue;
        }
        for (size_t p = 0; p < A.size(); ++p) {
            long long x = A[p];
            long long t = tot / 2 - x;
            int i = (int)(lower_bound(B.begin(), B.end(), t) - B.begin());
            for (int j = i - 1; j <= i + 1; ++j) {
                if (j >= 0 && j < (int)B.size()) {
                    long long s = x + B[j];
                    long long d = tot - 2 * s;
                    if (d < 0) {
                        d = -d;
                    }
                    if (d < best) {
                        best = d;
                    }
                }
            }
        }
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int n;
        cin >> n;
        vector<long long> vals(n);
        for (int i = 0; i < n; ++i) {
            cin >> vals[i];
        }
        cout << min_diff(vals) << '\n';
    }
    return 0;
}
