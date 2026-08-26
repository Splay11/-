## 解题思路

给一棵含 $n$ 个点的树。对每个 $k(1\le k\le n)$ 构造图 $G_k$：当且仅当树上两点距离 $d(u,v)\ge k$ 时，在 $G_k$ 中连边。要求输出 $G_k$ 的极大连通块（连通分量）个数。

关键观察（树的性质）：

* 设树的直径两端为 $s,t$，直径长度为 $D=d(s,t)$。对任意点 $v$，其离得最远的点一定是 $s$ 或 $t$，故点 $v$ 的离心率

  $$
  \mathrm{ecc}(v)=\max(d(v,s),\,d(v,t)).
  $$
* 若 $\mathrm{ecc}(v)<k$，则对任意点 $u$ 有 $d(u,v)<k$，所以 $v$ 在 $G_k$ 中没有任何边——成为一个**孤立点**。
* 若 $\mathrm{ecc}(v)\ge k$，则 $d(v,s)\ge k$ 或 $d(v,t)\ge k$，故 $v$ 与端点 $s$ 或 $t$ 在 $G_k$ 中有边。而当 $k\le D$ 时，$s$ 与 $t$ 之间也有边（因为 $d(s,t)=D\ge k$）。因此所有非孤立点通过 $s,t$ 连接在一起，形成**唯一的一个大连通块**。

由此可得：

* 当 $k>D$：图中无边，答案为 $n$。
* 当 $k\le D$：答案为

  $$
  1+\#\{v\mid \mathrm{ecc}(v)\le k-1\}.
  $$

  即“孤立点个数 + 1（大块）”。

实现方法：

1. 两次 BFS/DFS 求树的直径：任取点出发到达最远点 $s$，再从 $s$ 出发到达最远点 $t$，得直径长度 $D$；同时获得到 $s,t$ 的距离数组 $d_s,d_t$。
2. 计算每个点离心率 $\mathrm{ecc}(v)=\max(d_s[v],d_t[v])$，统计每个离心率出现次数，做前缀和 $pref[x]=\#\{\mathrm{ecc}\le x\}$。
3. 依次输出：若 $k\le D$ 输出 $1+pref[k-1]$，否则输出 $n$。

## 复杂度分析

* 时间复杂度：两次 BFS/DFS $O(n)$，统计与输出 $O(n)$。总计 $O(n)$。
* 空间复杂度：邻接表与若干数组 $O(n)$。

## 代码实现

### Python

```python
# -*- coding: utf-8 -*-
# 题意：树上两点距离>=k连边，求每个k的连通分量个数
import sys
from collections import deque

def bfs(start, g, n):
    """从start出发的BFS，返回距离数组"""
    dist = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    n = next(it)
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = next(it); v = next(it)
        g[u].append(v); g[v].append(u)

    # 第一次BFS：找一个直径端点 s
    d1 = bfs(1, g, n)
    s = max(range(1, n + 1), key=lambda x: d1[x])

    # 第二次BFS：从 s 出发得到 ds，并找另一端 t
    ds = bfs(s, g, n)
    t = max(range(1, n + 1), key=lambda x: ds[x])
    D = ds[t]

    # 第三次BFS：从 t 出发得到 dt
    dt = bfs(t, g, n)

    # 统计离心率
    freq = [0] * (D + 1)  # 只需到 D
    for v in range(1, n + 1):
        ecc = max(ds[v], dt[v])
        freq[ecc] += 1

    # 前缀和：ecc <= x 的点数
    pref = [0] * (D + 1)
    ssum = 0
    for x in range(D + 1):
        ssum += freq[x]
        pref[x] = ssum

    # 输出答案
    ans = []
    for k in range(1, n + 1):
        if k <= D:
            ans.append(str(1 + pref[k - 1]))
        else:
            ans.append(str(n))
    print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

### Java

```java
// 题意：树上两点距离>=k连边，求每个k的连通分量个数
import java.io.*;
import java.util.*;

public class Main {
    // 简单快读（字节流），适配 n<=2e5
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        FastScanner(InputStream is) { in = is; }
        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        int nextInt() throws IOException {
            int c, sgn = 1, x = 0;
            do { c = read(); } while (c <= 32);
            if (c == '-') { sgn = -1; c = read(); }
            while (c > 32) { x = x * 10 + (c - '0'); c = read(); }
            return x * sgn;
        }
    }

    static int n, idx;
    static int[] head, to, next;
    static void addEdge(int u, int v) {
        to[idx] = v; next[idx] = head[u]; head[u] = idx++;
        to[idx] = u; next[idx] = head[v]; head[v] = idx++;
    }

    // 从 start 出发 BFS，返回距离数组
    static int[] bfs(int start) {
        int[] dist = new int[n + 1];
        Arrays.fill(dist, -1);
        int[] q = new int[n];
        int hh = 0, tt = 0;
        q[tt++] = start;
        dist[start] = 0;
        while (hh < tt) {
            int u = q[hh++];
            for (int e = head[u]; e != -1; e = next[e]) {
                int v = to[e];
                if (dist[v] == -1) {
                    dist[v] = dist[u] + 1;
                    q[tt++] = v;
                }
            }
        }
        return dist;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        n = fs.nextInt();
        head = new int[n + 1];
        Arrays.fill(head, -1);
        to = new int[2 * (n - 1)];
        next = new int[2 * (n - 1)];
        idx = 0;

        for (int i = 0; i < n - 1; i++) {
            int u = fs.nextInt(), v = fs.nextInt();
            addEdge(u, v);
        }

        // 第一次 BFS：随便取1，找直径端点 s
        int[] d1 = bfs(1);
        int s = 1;
        for (int i = 1; i <= n; i++) if (d1[i] > d1[s]) s = i;

        // 第二次 BFS：从 s 出发
        int[] ds = bfs(s);
        int t = s;
        for (int i = 1; i <= n; i++) if (ds[i] > ds[t]) t = i;
        int D = ds[t];

        // 第三次 BFS：从 t 出发
        int[] dt = bfs(t);

        // 统计离心率并做前缀
        int[] freq = new int[D + 1];
        for (int v = 1; v <= n; v++) {
            int ecc = Math.max(ds[v], dt[v]);
            freq[ecc]++;
        }
        int[] pref = new int[D + 1];
        int ssum = 0;
        for (int x = 0; x <= D; x++) {
            ssum += freq[x];
            pref[x] = ssum;
        }

        // 输出
        StringBuilder sb = new StringBuilder();
        for (int k = 1; k <= n; k++) {
            if (k <= D) sb.append(1 + pref[k - 1]);
            else sb.append(n);
            if (k < n) sb.append(' ');
        }
        System.out.println(sb.toString());
    }
}
```

### C++

```cpp
// 题意：树上两点距离>=k连边，求每个k的连通分量个数
#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> g;

vector<int> bfs(int start) {
    int n = (int)g.size() - 1;
    vector<int> dist(n + 1, -1);
    queue<int> q;
    q.push(start);
    dist[start] = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : g[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    g.assign(n + 1, {});
    for (int i = 0; i < n - 1; ++i) {
        int u, v; cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    // 第一次BFS：找直径端点 s
    auto d1 = bfs(1);
    int s = 1;
    for (int i = 1; i <= n; ++i) if (d1[i] > d1[s]) s = i;

    // 第二次BFS：从 s 出发
    auto ds = bfs(s);
    int t = s;
    for (int i = 1; i <= n; ++i) if (ds[i] > ds[t]) t = i;
    int D = ds[t];

    // 第三次BFS：从 t 出发
    auto dt = bfs(t);

    // 统计离心率并前缀和
    vector<long long> freq(D + 1, 0);
    for (int v = 1; v <= n; ++v) {
        int ecc = max(ds[v], dt[v]);
        freq[ecc]++;
    }
    vector<long long> pref(D + 1, 0);
    long long ssum = 0;
    for (int x = 0; x <= D; ++x) {
        ssum += freq[x];
        pref[x] = ssum;
    }

    // 输出
    for (int k = 1; k <= n; ++k) {
        long long ans = (k <= D) ? (1 + pref[k - 1]) : (long long)n;
        if (k > 1) cout << ' ';
        cout << ans;
    }
    cout << '\n';
    return 0;
}
```