#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

const long long INF = 1000000000000000000LL;

struct Fenwick {
    int n;
    vector<pair<long long, long long> > a;
    Fenwick(int n_) {
        n = n_;
        a.assign(n + 2, make_pair(INF, 0));
    }
    void upd(int i, pair<long long, long long> val) {
        // 单点与 val 取更小
        while (i <= n) {
            if (val < a[i]) {
                a[i] = val;
            }
            i += i & -i;
        }
    }
    pair<long long, long long> qry(int i) {
        // 前缀 1..i 的最小值
        pair<long long, long long> r = make_pair(INF, 0);
        while (i) {
            if (a[i] < r) {
                r = a[i];
            }
            i -= i & -i;
        }
        return r;
    }
};

long long min_ops(const vector<long long>& h) {
    // 把数组分成尽量多段、段和单调不减；答案 = 长度 - 段数
    int m = (int)h.size();
    vector<long long> pre(m + 1, 0);
    for (int i = 0; i < m; i++) {
        pre[i + 1] = pre[i] + h[i];
    }
    vector<long long> uniq = pre;
    sort(uniq.begin(), uniq.end());
    uniq.erase(unique(uniq.begin(), uniq.end()), uniq.end());
    Fenwick fw((int)uniq.size() + 2);
    vector<long long> last(m + 1, 0), dp(m + 1, 0);
    int p0 = (int)(lower_bound(uniq.begin(), uniq.end(), 0LL) - uniq.begin()) + 1;
    fw.upd(p0, make_pair(0LL, 0LL));
    for (int i = 1; i <= m; i++) {
        int qi = (int)(upper_bound(uniq.begin(), uniq.end(), pre[i]) - uniq.begin());
        pair<long long, long long> best = fw.qry(qi);
        dp[i] = (i - 1) + best.first;
        long long pj = -best.second;
        last[i] = pre[i] - pj;
        long long key = last[i] + pre[i];
        int pi = (int)(lower_bound(uniq.begin(), uniq.end(), key) - uniq.begin()) + 1;
        fw.upd(pi, make_pair(dp[i] - i, -pre[i]));
    }
    return dp[m];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<long long> h(m);
        for (int i = 0; i < m; i++) {
            cin >> h[i];
        }
        cout << min_ops(h) << endl;
    }
    return 0;
}
