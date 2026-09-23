#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class SegmentTree {
public:
    vector<long long> mx, lazy;
    int n;

    SegmentTree(const vector<long long>& arr, int n) : n(n) {
        mx.assign(n * 4 + 5, 0);
        lazy.assign(n * 4 + 5, 0);
        build(1, 1, n, arr);
    }

    void build(int node, int l, int r, const vector<long long>& arr) {
        if (l == r) {
            mx[node] = arr[l];
            return;
        }
        int mid = (l + r) >> 1;
        build(node << 1, l, mid, arr);
        build(node << 1 | 1, mid + 1, r, arr);
        mx[node] = max(mx[node << 1], mx[node << 1 | 1]);
    }

    void pushDown(int node) {
        if (lazy[node] != 0) {
            long long tag = lazy[node];
            mx[node << 1] += tag;
            mx[node << 1 | 1] += tag;
            lazy[node << 1] += tag;
            lazy[node << 1 | 1] += tag;
            lazy[node] = 0;
        }
    }

    void rangeAdd(int node, int l, int r, int ql, int qr, long long val) {
        if (ql <= l && r <= qr) {
            mx[node] += val;
            lazy[node] += val;
            return;
        }
        pushDown(node);
        int mid = (l + r) >> 1;
        if (ql <= mid) {
            rangeAdd(node << 1, l, mid, ql, qr, val);
        }
        if (qr > mid) {
            rangeAdd(node << 1 | 1, mid + 1, r, ql, qr, val);
        }
        mx[node] = max(mx[node << 1], mx[node << 1 | 1]);
    }

    long long queryMax() {
        return mx[1];
    }
};

long long solveCase(int n, const vector<long long>& h,
                    const vector<int>& sigma, const vector<int>& tau) {
    // 按排列 sigma 重排指标，得到采集序列 seq
    vector<long long> seq(n + 1, 0);
    vector<int> posSigma(n + 1, 0);

    for (int i = 1; i <= n; i++) {
        seq[i] = h[sigma[i]];
        posSigma[sigma[i]] = i;
    }

    // 前缀和数组
    vector<long long> pre(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        pre[i] = pre[i - 1] + seq[i];
    }

    SegmentTree seg(pre, n);
    long long ans = max(0LL, seg.queryMax());

    // 按 tau 顺序依次清零，枚举清零前缀长度
    for (int i = 1; i <= n; i++) {
        int idx = tau[i];
        int p = posSigma[idx];
        long long v = h[idx];

        // 将 seq[p] 置 0，等价于 pre[p..n] 整体加 -v
        seg.rangeAdd(1, 1, n, p, n, -v);
        ans = max(ans, seg.queryMax());
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<long long> h(n + 1, 0);
        vector<int> sigma(n + 1, 0), tau(n + 1, 0);

        for (int i = 1; i <= n; i++) {
            cin >> h[i];
        }
        for (int i = 1; i <= n; i++) {
            cin >> sigma[i];
        }
        for (int i = 1; i <= n; i++) {
            cin >> tau[i];
        }

        cout << solveCase(n, h, sigma, tau) << '\n';
    }

    return 0;
}
