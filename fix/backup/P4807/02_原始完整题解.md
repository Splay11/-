## 解题思路

按排列 $\sigma$ 将指标重排为采集序列 $s_i = h_{\sigma_i}$。操作 1 等价于在 $s$ 上取最大前缀和。

两种操作各至多一次，只需考虑：

- 不做任何操作（得 $0$）；
- 仅做操作 1（初始最大前缀和）；
- 先做操作 2 清零 $\tau$ 的前 $u$ 项，再做操作 1。

设 $pre_i = \sum_{j=1}^{i} s_j$。将 $h_{\tau_j}$ 清零等价于把 $s$ 中对应位置置 $0$，即对 $pre$ 的区间 $[p,n]$ 整体加 $-v$（$p$ 为该元素在 $s$ 中的下标）。

用线段树维护 $pre$ 的区间最大值与区间加，按 $\tau$ 顺序枚举清零前缀，每次查询全局最大值，与 $0$ 取最大即为答案。

## 复杂度分析

- 时间：建树 $O(n)$，$n$ 次区间加与查询各 $O(\log n)$，总计 $O(n \log n)$。
- 空间：$O(n)$。

## 代码实现

### Python

```python
import sys


class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr) - 1
        self.mx = [0] * (self.n * 4)
        self.lazy = [0] * (self.n * 4)
        self._build(1, 1, self.n, arr)

    def _build(self, node, l, r, arr):
        if l == r:
            self.mx[node] = arr[l]
            return
        mid = (l + r) // 2
        self._build(node * 2, l, mid, arr)
        self._build(node * 2 + 1, mid + 1, r, arr)
        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def _push_down(self, node):
        if self.lazy[node]:
            tag = self.lazy[node]
            for ch in (node * 2, node * 2 + 1):
                self.mx[ch] += tag
                self.lazy[ch] += tag
            self.lazy[node] = 0

    def range_add(self, node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.mx[node] += val
            self.lazy[node] += val
            return
        self._push_down(node)
        mid = (l + r) // 2
        if ql <= mid:
            self.range_add(node * 2, l, mid, ql, qr, val)
        if qr > mid:
            self.range_add(node * 2 + 1, mid + 1, r, ql, qr, val)
        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def query_max(self):
        return self.mx[1]


def solve_case(n, h, sigma, tau):
    seq = [0] * (n + 1)
    pos_sigma = [0] * (n + 1)
    for i in range(1, n + 1):
        seq[i] = h[sigma[i]]
        pos_sigma[sigma[i]] = i
    pre = [0] * (n + 1)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] + seq[i]
    seg = SegmentTree(pre)
    ans = max(0, seg.query_max())
    for i in range(1, n + 1):
        idx, p, v = tau[i], pos_sigma[tau[i]], h[tau[i]]
        seg.range_add(1, 1, n, p, n, -v)
        ans = max(ans, seg.query_max())
    return ans


def main():
    input = sys.stdin.readline
    t = int(input().strip())
    res = []
    for _ in range(t):
        n = int(input().strip())
        h = [0] + list(map(int, input().split()))
        sigma = [0] + list(map(int, input().split()))
        tau = [0] + list(map(int, input().split()))
        res.append(str(solve_case(n, h, sigma, tau)))
    print("\n".join(res))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static class SegTree {
        long[] mx, lazy;
        int n;
        SegTree(long[] arr, int n) {
            this.n = n;
            mx = new long[n * 4];
            lazy = new long[n * 4];
            build(1, 1, n, arr);
        }
        void build(int node, int l, int r, long[] arr) {
            if (l == r) { mx[node] = arr[l]; return; }
            int mid = (l + r) >> 1;
            build(node << 1, l, mid, arr);
            build(node << 1 | 1, mid + 1, r, arr);
            mx[node] = Math.max(mx[node << 1], mx[node << 1 | 1]);
        }
        void push(int node) {
            if (lazy[node] != 0) {
                long tag = lazy[node];
                mx[node << 1] += tag; mx[node << 1 | 1] += tag;
                lazy[node << 1] += tag; lazy[node << 1 | 1] += tag;
                lazy[node] = 0;
            }
        }
        void rangeAdd(int node, int l, int r, int ql, int qr, long val) {
            if (ql <= l && r <= qr) { mx[node] += val; lazy[node] += val; return; }
            push(node);
            int mid = (l + r) >> 1;
            if (ql <= mid) rangeAdd(node << 1, l, mid, ql, qr, val);
            if (qr > mid) rangeAdd(node << 1 | 1, mid + 1, r, ql, qr, val);
            mx[node] = Math.max(mx[node << 1], mx[node << 1 | 1]);
        }
        long queryMax() { return mx[1]; }
    }

    static long solveCase(int n, long[] h, int[] sigma, int[] tau) {
        long[] seq = new long[n + 1];
        int[] posSigma = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            seq[i] = h[sigma[i]];
            posSigma[sigma[i]] = i;
        }
        long[] pre = new long[n + 1];
        for (int i = 1; i <= n; i++) pre[i] = pre[i - 1] + seq[i];
        SegTree seg = new SegTree(pre, n);
        long ans = Math.max(0L, seg.queryMax());
        for (int i = 1; i <= n; i++) {
            int idx = tau[i], p = posSigma[idx];
            seg.rangeAdd(1, 1, n, p, n, -h[idx]);
            ans = Math.max(ans, seg.queryMax());
        }
        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine());
        StringBuilder sb = new StringBuilder();
        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine());
            long[] h = new long[n + 1];
            int[] sigma = new int[n + 1], tau = new int[n + 1];
            String[] parts = br.readLine().split(" ");
            for (int i = 1; i <= n; i++) h[i] = Long.parseLong(parts[i - 1]);
            parts = br.readLine().split(" ");
            for (int i = 1; i <= n; i++) sigma[i] = Integer.parseInt(parts[i - 1]);
            parts = br.readLine().split(" ");
            for (int i = 1; i <= n; i++) tau[i] = Integer.parseInt(parts[i - 1]);
            sb.append(solveCase(n, h, sigma, tau)).append('\n');
        }
        System.out.print(sb);
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct SegTree {
    vector<long long> mx, lazy;
    int n;
    SegTree(const vector<long long>& arr, int n): n(n) {
        mx.assign(n * 4 + 5, 0);
        lazy.assign(n * 4 + 5, 0);
        build(1, 1, n, arr);
    }
    void build(int node, int l, int r, const vector<long long>& arr) {
        if (l == r) { mx[node] = arr[l]; return; }
        int mid = (l + r) >> 1;
        build(node << 1, l, mid, arr);
        build(node << 1 | 1, mid + 1, r, arr);
        mx[node] = max(mx[node << 1], mx[node << 1 | 1]);
    }
    void push(int node) {
        if (lazy[node]) {
            long long tag = lazy[node];
            mx[node<<1] += tag; mx[node<<1|1] += tag;
            lazy[node<<1] += tag; lazy[node<<1|1] += tag;
            lazy[node] = 0;
        }
    }
    void rangeAdd(int node, int l, int r, int ql, int qr, long long val) {
        if (ql <= l && r <= qr) { mx[node] += val; lazy[node] += val; return; }
        push(node);
        int mid = (l + r) >> 1;
        if (ql <= mid) rangeAdd(node<<1, l, mid, ql, qr, val);
        if (qr > mid) rangeAdd(node<<1|1, mid+1, r, ql, qr, val);
        mx[node] = max(mx[node<<1], mx[node<<1|1]);
    }
    long long queryMax() { return mx[1]; }
};

long long solveCase(int n, const vector<long long>& h,
                    const vector<int>& sigma, const vector<int>& tau) {
    vector<long long> seq(n + 1);
    vector<int> posSigma(n + 1);
    for (int i = 1; i <= n; i++) {
        seq[i] = h[sigma[i]];
        posSigma[sigma[i]] = i;
    }
    vector<long long> pre(n + 1);
    for (int i = 1; i <= n; i++) pre[i] = pre[i-1] + seq[i];
    SegTree seg(pre, n);
    long long ans = max(0LL, seg.queryMax());
    for (int i = 1; i <= n; i++) {
        int p = posSigma[tau[i]];
        seg.rangeAdd(1, 1, n, p, n, -h[tau[i]]);
        ans = max(ans, seg.queryMax());
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; cin >> T;
    while (T--) {
        int n; cin >> n;
        vector<long long> h(n + 1);
        vector<int> sigma(n + 1), tau(n + 1);
        for (int i = 1; i <= n; i++) cin >> h[i];
        for (int i = 1; i <= n; i++) cin >> sigma[i];
        for (int i = 1; i <= n; i++) cin >> tau[i];
        cout << solveCase(n, h, sigma, tau) << '\n';
    }
    return 0;
}
```