## 解题思路

设相邻位置 $j$ 的交换代价为 $c_j$：

当 $b_j < b_{j+1}$ 时，$c_j = 1$；否则 $c_j = 0$。

题目中的冒泡排序是从左到右扫描。对于原数组中第 $i$ 个元素 $a_i$，只考虑它左边比它大的元素数量，记为 $cnt_i$。这些元素都会在冒泡排序过程中与 $a_i$ 发生交换。

关键性质：

第 $i$ 个元素每次向左最多移动 $1$ 格，因此它会依次经过边：

$ i - 1, i - 2, \dots, i - cnt_i $

所以第 $i$ 个元素贡献的代价为这些边的 $c$ 值之和。

预处理前缀和：

$pre_i = c_1 + c_2 + \dots + c_i$

则第 $i$ 个元素的贡献为：

$pre_{i-1} - pre_{i-cnt_i-1}$

现在问题转化为：对每个 $a_i$，快速求左边有多少个数严格大于它。

由于 $a_i$ 范围很大，需要先进行离散化，然后用树状数组维护已经出现过的数的数量。

对于当前 $a_i$：

左边元素总数为 $i - 1$；

左边小于等于 $a_i$ 的数量可由树状数组查询；

所以：

$cnt_i = i - 1 - count(\le a_i)$

最后累加所有位置的贡献即可。

## 复杂度分析

设单组数据长度为 $n$。

离散化需要 $O(n \log n)$。

每个元素进行一次树状数组查询和修改，复杂度为 $O(\log n)$。

因此总时间复杂度为：

$O(n \log n)$

空间复杂度为：

$O(n)$

满足所有测试数据 $n$ 之和不超过 $5 \times 10^5$ 的要求。

## 代码实现

### Python

```python
import sys
from bisect import bisect_left

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    # 在位置 idx 加上 val
    def add(self, idx, val):
        while idx <= self.n:
            self.tree[idx] += val
            idx += idx & -idx

    # 查询前缀和
    def query(self, idx):
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res


def solve_case(n, a, b):
    # 计算每条边的代价前缀和
    pre = [0] * n
    for i in range(1, n):
        pre[i] = pre[i - 1] + (1 if b[i - 1] < b[i] else 0)

    # 离散化数组 a
    vals = sorted(set(a))
    bit = Fenwick(len(vals))

    ans = 0

    for i in range(n):
        # 当前值的离散化排名
        rank = bisect_left(vals, a[i]) + 1

        # 左边小于等于 a[i] 的数量
        leq = bit.query(rank)

        # 左边严格大于 a[i] 的数量
        cnt = i - leq

        # 第 i 个元素会经过边 i-cnt 到 i-1
        ans += pre[i] - pre[i - cnt]

        # 将当前元素加入树状数组
        bit.add(rank, 1)

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    res = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        a = data[idx:idx + n]
        idx += n

        b = data[idx:idx + n]
        idx += n

        res.append(str(solve_case(n, a, b)))

    print("\n".join(res))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    static class FastScanner {
        private final InputStream in = System.in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }

        int nextInt() throws IOException {
            int c;
            do {
                c = read();
            } while (c <= ' ');

            int sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            int val = 0;
            while (c > ' ') {
                val = val * 10 + c - '0';
                c = read();
            }
            return val * sign;
        }
    }

    static class Fenwick {
        int n;
        int[] tree;

        Fenwick(int n) {
            this.n = n;
            this.tree = new int[n + 1];
        }

        // 在位置 idx 加上 val
        void add(int idx, int val) {
            while (idx <= n) {
                tree[idx] += val;
                idx += idx & -idx;
            }
        }

        // 查询前缀和
        int query(int idx) {
            int res = 0;
            while (idx > 0) {
                res += tree[idx];
                idx -= idx & -idx;
            }
            return res;
        }
    }

    static int lowerBound(int[] arr, int size, int target) {
        int l = 0, r = size;
        while (l < r) {
            int mid = (l + r) >> 1;
            if (arr[mid] >= target) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }

    static long solveCase(int n, int[] a, int[] b) {
        // 计算每条边的代价前缀和
        long[] pre = new long[n];
        for (int i = 1; i < n; i++) {
            pre[i] = pre[i - 1] + (b[i - 1] < b[i] ? 1 : 0);
        }

        // 离散化数组 a
        int[] vals = a.clone();
        Arrays.sort(vals);

        int m = 0;
        for (int x : vals) {
            if (m == 0 || vals[m - 1] != x) {
                vals[m++] = x;
            }
        }

        Fenwick bit = new Fenwick(m);
        long ans = 0;

        for (int i = 0; i < n; i++) {
            // 当前值的离散化排名
            int rank = lowerBound(vals, m, a[i]) + 1;

            // 左边小于等于 a[i] 的数量
            int leq = bit.query(rank);

            // 左边严格大于 a[i] 的数量
            int cnt = i - leq;

            // 第 i 个元素会经过边 i-cnt 到 i-1
            ans += pre[i] - pre[i - cnt];

            // 将当前元素加入树状数组
            bit.add(rank, 1);
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        StringBuilder sb = new StringBuilder();

        int T = fs.nextInt();

        for (int tc = 0; tc < T; tc++) {
            int n = fs.nextInt();

            int[] a = new int[n];
            int[] b = new int[n];

            for (int i = 0; i < n; i++) {
                a[i] = fs.nextInt();
            }

            for (int i = 0; i < n; i++) {
                b[i] = fs.nextInt();
            }

            sb.append(solveCase(n, a, b)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

class Fenwick {
public:
    int n;
    vector<int> tree;

    Fenwick(int n) {
        this->n = n;
        tree.assign(n + 1, 0);
    }

    // 在位置 idx 加上 val
    void add(int idx, int val) {
        while (idx <= n) {
            tree[idx] += val;
            idx += idx & -idx;
        }
    }

    // 查询前缀和
    int query(int idx) {
        int res = 0;
        while (idx > 0) {
            res += tree[idx];
            idx -= idx & -idx;
        }
        return res;
    }
};

long long solveCase(int n, vector<int>& a, vector<int>& b) {
    // 计算每条边的代价前缀和
    vector<long long> pre(n, 0);
    for (int i = 1; i < n; i++) {
        pre[i] = pre[i - 1] + (b[i - 1] < b[i] ? 1 : 0);
    }

    // 离散化数组 a
    vector<int> vals = a;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());

    Fenwick bit((int)vals.size());
    long long ans = 0;

    for (int i = 0; i < n; i++) {
        // 当前值的离散化排名
        int rank = lower_bound(vals.begin(), vals.end(), a[i]) - vals.begin() + 1;

        // 左边小于等于 a[i] 的数量
        int leq = bit.query(rank);

        // 左边严格大于 a[i] 的数量
        int cnt = i - leq;

        // 第 i 个元素会经过边 i-cnt 到 i-1
        ans += pre[i] - pre[i - cnt];

        // 将当前元素加入树状数组
        bit.add(rank, 1);
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

        vector<int> a(n), b(n);

        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        for (int i = 0; i < n; i++) {
            cin >> b[i];
        }

        cout << solveCase(n, a, b) << '\n';
    }

    return 0;
}
```