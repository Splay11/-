## 解题思路

先观察操作本质：

* 初始时每个点 $i$ 的权值为 $a_i=i$。
* 第 $j$ 次操作会把某个点的权值改成 $n+j$。

因此每次新赋的值都严格大于所有初始权值，而且也严格大于之前修改过的值。
所以每次在子树中找“当前权值最小的点”，就是在这个子树里找当前权值最小的位置，然后做一次单点修改。

这题的关键是把“子树”转成“区间”。

### 相关算法

用到两个经典算法：

* $DFS$ 序
* 线段树

### 核心思路

1. 题目给的是一棵以 $1$ 为根的树，但输入边是无向边。
   所以先从根节点 $1$ 开始遍历整棵树，求出每个点的 $DFS$ 序编号 $dfn[u]$，以及子树结束位置 $out[u]$。

2. 在 $DFS$ 序中，一个点 $u$ 的整棵子树恰好对应一个连续区间：
   $$
   [dfn[u],,out[u]]
   $$

3. 按照 $DFS$ 序建线段树。
   线段树每个位置存一个二元组：
   $$
   (\text{当前权值},\ \text{节点编号})
   $$
   这样就能在一个区间里查询最小权值对应的节点。

4. 对于每次操作给出的节点 $x$：

   * 在线段树上查询区间 $[dfn[x], out[x]]$ 的最小值，得到节点 $u$
   * 把节点 $u$ 的权值改成 $n+j$
   * 在线段树上做单点更新

5. 最后输出每个节点的最终权值即可。

### 实现方法

* 用邻接表存树
* 用一次 $DFS$ 求出：

  * $dfn[u]$
  * $out[u]$
  * $order[t]$：$DFS$ 序位置 $t$ 对应哪个节点
* 用线段树维护区间最小值
* 每次操作做一次区间查询和一次单点修改

---

## 复杂度分析

设点数为 $n$，操作数为 $m$。

* 建树和求 $DFS$ 序：$O(n)$
* 建线段树：$O(n)$
* 每次操作：

  * 区间最小值查询：$O(\log n)$
  * 单点修改：$O(\log n)$

总时间复杂度为：
$$
O((n+m)\log n)
$$

空间复杂度为：
$$
O(n)
$$

这个复杂度对 $n,m\le 10^5$ 是完全可行的。

---

## 代码实现

### Python

```python
import sys
sys.setrecursionlimit(1 << 25)

INF = 10**18


# 线段树：维护区间最小值 (权值, 节点编号)
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr) - 1  # arr 从 1 开始
        self.tree = [(INF, 0)] * (self.n * 4)
        self.build(1, 1, self.n, arr)

    def build(self, idx, l, r, arr):
        if l == r:
            self.tree[idx] = arr[l]
            return
        mid = (l + r) // 2
        self.build(idx * 2, l, mid, arr)
        self.build(idx * 2 + 1, mid + 1, r, arr)
        self.tree[idx] = min(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def update(self, idx, l, r, pos, val):
        if l == r:
            self.tree[idx] = val
            return
        mid = (l + r) // 2
        if pos <= mid:
            self.update(idx * 2, l, mid, pos, val)
        else:
            self.update(idx * 2 + 1, mid + 1, r, pos, val)
        self.tree[idx] = min(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def query(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.tree[idx]
        mid = (l + r) // 2
        res = (INF, 0)
        if ql <= mid:
            res = min(res, self.query(idx * 2, l, mid, ql, qr))
        if qr > mid:
            res = min(res, self.query(idx * 2 + 1, mid + 1, r, ql, qr))
        return res


# 求 DFS 序，把子树转成区间
def dfs(u, parent, graph, dfn, out, order, timer):
    timer[0] += 1
    dfn[u] = timer[0]
    order[timer[0]] = u
    for v in graph[u]:
        if v != parent:
            dfs(v, u, graph, dfn, out, order, timer)
    out[u] = timer[0]


# 处理题目要求的功能
def solve(n, m, edges, ops):
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    dfn = [0] * (n + 1)
    out = [0] * (n + 1)
    order = [0] * (n + 1)
    timer = [0]

    dfs(1, 0, graph, dfn, out, order, timer)

    # 按 DFS 序建初始数组
    arr = [None] * (n + 1)
    ans = [0] * (n + 1)
    for pos in range(1, n + 1):
        u = order[pos]
        arr[pos] = (u, u)  # 初始权值就是节点编号
        ans[u] = u

    seg = SegmentTree(arr)

    # 依次处理操作
    for j in range(1, m + 1):
        x = ops[j - 1]
        l, r = dfn[x], out[x]
        _, u = seg.query(1, 1, n, l, r)  # 找到子树中最小权值对应的节点
        new_val = n + j
        ans[u] = new_val
        seg.update(1, 1, n, dfn[u], (new_val, u))  # 单点更新

    return ans[1:]


def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(n - 1)]
    ops = [int(input()) for _ in range(m)]

    res = solve(n, m, edges, ops)
    print(*res)


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

    static class Pair {
        int val;
        int node;

        Pair(int val, int node) {
            this.val = val;
            this.node = node;
        }
    }

    static class SegmentTree {
        Pair[] tree;

        SegmentTree(Pair[] arr, int n) {
            tree = new Pair[n * 4];
            build(1, 1, n, arr);
        }

        void build(int idx, int l, int r, Pair[] arr) {
            if (l == r) {
                tree[idx] = arr[l];
                return;
            }
            int mid = (l + r) >> 1;
            build(idx << 1, l, mid, arr);
            build(idx << 1 | 1, mid + 1, r, arr);
            tree[idx] = minPair(tree[idx << 1], tree[idx << 1 | 1]);
        }

        void update(int idx, int l, int r, int pos, Pair val) {
            if (l == r) {
                tree[idx] = val;
                return;
            }
            int mid = (l + r) >> 1;
            if (pos <= mid) {
                update(idx << 1, l, mid, pos, val);
            } else {
                update(idx << 1 | 1, mid + 1, r, pos, val);
            }
            tree[idx] = minPair(tree[idx << 1], tree[idx << 1 | 1]);
        }

        Pair query(int idx, int l, int r, int ql, int qr) {
            if (ql <= l && r <= qr) {
                return tree[idx];
            }
            int mid = (l + r) >> 1;
            Pair res = new Pair(Integer.MAX_VALUE, 0);
            if (ql <= mid) {
                res = minPair(res, query(idx << 1, l, mid, ql, qr));
            }
            if (qr > mid) {
                res = minPair(res, query(idx << 1 | 1, mid + 1, r, ql, qr));
            }
            return res;
        }

        Pair minPair(Pair a, Pair b) {
            if (a.val != b.val) {
                return a.val < b.val ? a : b;
            }
            return a.node < b.node ? a : b;
        }
    }

    static List<Integer>[] graph;
    static int[] dfn, out, order;
    static int timer = 0;

    // 求 DFS 序，把子树映射成连续区间
    static void dfs(int u, int parent) {
        dfn[u] = ++timer;
        order[timer] = u;
        for (int v : graph[u]) {
            if (v != parent) {
                dfs(v, u);
            }
        }
        out[u] = timer;
    }

    // 处理题目要求的功能
    static int[] solve(int n, int m, int[][] edges, int[] ops) {
        graph = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) {
            graph[i] = new ArrayList<>();
        }

        for (int[] e : edges) {
            int u = e[0], v = e[1];
            graph[u].add(v);
            graph[v].add(u);
        }

        dfn = new int[n + 1];
        out = new int[n + 1];
        order = new int[n + 1];
        timer = 0;
        dfs(1, 0);

        Pair[] arr = new Pair[n + 1];
        int[] ans = new int[n + 1];

        // 按 DFS 序建立初始数组
        for (int pos = 1; pos <= n; pos++) {
            int u = order[pos];
            arr[pos] = new Pair(u, u); // 初始权值就是节点编号
            ans[u] = u;
        }

        SegmentTree seg = new SegmentTree(arr, n);

        // 依次处理每次操作
        for (int j = 1; j <= m; j++) {
            int x = ops[j];
            Pair p = seg.query(1, 1, n, dfn[x], out[x]);
            int u = p.node;
            int newVal = n + j;
            ans[u] = newVal;
            seg.update(1, 1, n, dfn[u], new Pair(newVal, u));
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        int n = fs.nextInt();
        int m = fs.nextInt();

        int[][] edges = new int[n - 1][2];
        for (int i = 0; i < n - 1; i++) {
            edges[i][0] = fs.nextInt();
            edges[i][1] = fs.nextInt();
        }

        int[] ops = new int[m + 1];
        for (int i = 1; i <= m; i++) {
            ops[i] = fs.nextInt();
        }

        int[] res = solve(n, m, edges, ops);

        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append(' ');
            sb.append(res[i]);
        }
        System.out.println(sb);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int val, id;
    // 线段树里按权值最小比较
    bool operator < (const Node& other) const {
        if (val != other.val) return val < other.val;
        return id < other.id;
    }
};

class SegmentTree {
public:
    vector<Node> tree;

    SegmentTree(const vector<Node>& arr, int n) {
        tree.resize(n * 4 + 5);
        build(1, 1, n, arr);
    }

    void build(int idx, int l, int r, const vector<Node>& arr) {
        if (l == r) {
            tree[idx] = arr[l];
            return;
        }
        int mid = (l + r) >> 1;
        build(idx << 1, l, mid, arr);
        build(idx << 1 | 1, mid + 1, r, arr);
        tree[idx] = min(tree[idx << 1], tree[idx << 1 | 1]);
    }

    void update(int idx, int l, int r, int pos, Node val) {
        if (l == r) {
            tree[idx] = val;
            return;
        }
        int mid = (l + r) >> 1;
        if (pos <= mid) update(idx << 1, l, mid, pos, val);
        else update(idx << 1 | 1, mid + 1, r, pos, val);
        tree[idx] = min(tree[idx << 1], tree[idx << 1 | 1]);
    }

    Node query(int idx, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tree[idx];
        int mid = (l + r) >> 1;
        Node res = {INT_MAX, 0};
        if (ql <= mid) res = min(res, query(idx << 1, l, mid, ql, qr));
        if (qr > mid) res = min(res, query(idx << 1 | 1, mid + 1, r, ql, qr));
        return res;
    }
};

vector<vector<int>> graph;
vector<int> dfn, outPos, order;
int timer = 0;

// 求 DFS 序，把子树转成区间
void dfs(int u, int parent) {
    dfn[u] = ++timer;
    order[timer] = u;
    for (int v : graph[u]) {
        if (v != parent) {
            dfs(v, u);
        }
    }
    outPos[u] = timer;
}

// 处理题目要求的功能
vector<int> solve(int n, int m, const vector<pair<int, int>>& edges, const vector<int>& ops) {
    graph.assign(n + 1, vector<int>());
    for (auto e : edges) {
        int u = e.first, v = e.second;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    dfn.assign(n + 1, 0);
    outPos.assign(n + 1, 0);
    order.assign(n + 1, 0);
    timer = 0;
    dfs(1, 0);

    vector<Node> arr(n + 1);
    vector<int> ans(n + 1);

    // 按 DFS 序建立初始数组
    for (int pos = 1; pos <= n; pos++) {
        int u = order[pos];
        arr[pos] = {u, u}; // 初始权值就是节点编号
        ans[u] = u;
    }

    SegmentTree seg(arr, n);

    // 依次处理每次操作
    for (int j = 1; j <= m; j++) {
        int x = ops[j - 1];
        Node p = seg.query(1, 1, n, dfn[x], outPos[x]);
        int u = p.id;
        int newVal = n + j;
        ans[u] = newVal;
        seg.update(1, 1, n, dfn[u], {newVal, u});
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<pair<int, int>> edges;
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        edges.push_back({u, v});
    }

    vector<int> ops(m);
    for (int i = 0; i < m; i++) {
        cin >> ops[i];
    }

    vector<int> res = solve(n, m, edges, ops);

    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << res[i];
    }
    cout << '\n';

    return 0;
}
```