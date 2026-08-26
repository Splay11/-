# 题解

## 题目描述

小红拿到一棵节点总数为 $n$ 的树，编号为 $1$ ~ $n$，保证 $n$ 为奇数。

其中每个点的点权为 $a_i$，附属代价为 $b_i$。

每次操作，小红可以选择一个树上的连通块，再选择连通块中的一个节点，将其点权 $+1$ 或者 $-1$，代价为连通块中所有节点的附属代价之和。

小红想知道在最少操作次数的前提下，最少需要多少代价，才能将所有节点的点权变为相同（代价可以是负数）。

此题中的连通块定义为：对于树上的任意一个点集 $S$，如果 $S$ 中的任意两点 $u,v$ 之间存在一条路径，且路径上的所有点都在 $S$ 中，则称 $S$ 是一个连通块。

---

## 思路

1. **最少操作次数**：要使所有节点的点权相同，令目标点权为 $T$。每次操作仅能将某节点点权增减 $1$，故总操作次数为

   $$
   \sum_{i=1}^n |a_i - T|
   $$

   当 $n$ 为奇数时，取 $T$ 为所有 $a_i$ 的中位数可使该和最小。

2. **代价最小化**：每次对节点 $u$ 做一次增/减操作时，代价是所选连通块所有节点附属代价之和。为了使总代价最小化，对每个节点 $u$ 的每一次操作，均应选一个包含 $u$ 的连通块，使得该块附属代价之和最小。

   定义 $\text{best}[u]$ 为所有包含 $u$ 的连通块中，附属代价之和的最小值。则总最小代价为

   $$
   \sum_{i=1}^n |a_i - T| \times \text{best}[i]
   $$

3. **如何计算 $\text{best}[u]$**：在树上，计算每个节点为根的「最小连通子树和」可通过树形 DP 完成：

   - **第一遍 DFS（向下）**：令

     $f[u]$ = $b_u$ + $\sum_{v\in\mathrm{child}(u)}$ $\min(0, f[v])$

     此时 $f[u]$ 是以 $u$ 为根，仅考虑其下属子树时，包含 $u$ 的最小连通块和。

   - **第二遍 DFS（重根）**：维护 $\mathrm{ans}[u]$ 为包含 $u$ 考虑全树后的最小连通块和。初始化 $\mathrm{ans}[1]=f[1]$，向下传递：

     对于子节点 $v$：
     $\mathrm{ans}[v]$ = $b_v$ + $\sum_{w\in\mathrm{child}(v)}$ $\min(0, f[w])$ + $\min\bigl(0,\,\mathrm{ans}[u]$ - $\min(0, f[v])\bigr).$

     最终 $\mathrm{best}[u]=\mathrm{ans}[u]$。

4. **综合**：
   1. 对所有 $a_i$ 排序，取中位数 $T$。
   2. 树上跑两次 DFS 得到 $\mathrm{best}[i]$。
   3. 计算
      $$
      \sum_{i=1}^n |a_i - T| \times \mathrm{best}[i].
      $$

## C++
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int MAXN = 100000;
int n;
vector<int> a(MAXN+1), b(MAXN+1);
vector<vector<int>> adj(MAXN+1);
vector<ll> f(MAXN+1), ans_dp(MAXN+1);

// 向下 DFS，计算以 u 为根时的最小连通块和 f[u]
void dfs1(int u, int p) {
    f[u] = b[u];
    for (int v : adj[u]) {
        if (v == p) continue;
        dfs1(v, u);
        f[u] += min(0LL, f[v]);
    }
}

// 重根 DFS，计算包含 u 的全树最小连通块和 ans_dp[u]
void dfs2(int u, int p) {
    if (p == 0) ans_dp[u] = f[u];
    for (int v : adj[u]) {
        if (v == p) continue;
        // 去掉 v 对 u 的贡献，再加上 u 对 v 的父方向贡献
        ll without_v = ans_dp[u] - min(0LL, f[v]);
        ans_dp[v] = b[v];
        // v 子方向
        for (int w : adj[v]) if (w != u) ans_dp[v] += min(0LL, f[w]);
        // 加上父方向的负贡献
        ans_dp[v] += min(0LL, without_v);
        dfs2(v, u);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= n; i++) cin >> b[i];
    for (int i = 1, u, v; i < n; i++) {
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // 取中位数 T
    vector<int> sorted_a(a.begin()+1, a.begin()+n+1);
    sort(sorted_a.begin(), sorted_a.end());
    int T = sorted_a[n/2];

    // 计算每个节点的最小连通块和
    dfs1(1, 0);
    dfs2(1, 0);

    // 累加总代价
    ll totalCost = 0;
    for (int i = 1; i <= n; i++) {
        totalCost += 1LL * abs(a[i] - T) * ans_dp[i];
    }
    cout << totalCost;
    return 0;
}
```
## Python
```python
import sys
sys.setrecursionlimit(10**7)

# 读取输入
n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))
b = list(map(int, sys.stdin.readline().split()))

adj = [[] for _ in range(n)]
for _ in range(n-1):
    u, v = map(int, sys.stdin.readline().split())
    u -= 1; v -= 1
    adj[u].append(v)
    adj[v].append(u)

# 取中位数 T
sorted_a = sorted(a)
T = sorted_a[n//2]

delta = [abs(x - T) for x in a]

f = [0]*n
ans_dp = [0]*n

# 向下 DFS
def dfs1(u, p):
    f[u] = b[u]
    for v in adj[u]:
        if v == p: continue
        dfs1(v, u)
        f[u] += min(0, f[v])

def dfs2(u, p):
    global f, ans_dp
    if p == -1:
        ans_dp[u] = f[u]
    for v in adj[u]:
        if v == p: continue
        without_v = ans_dp[u] - min(0, f[v])
        # 计算 v 的 ans
        res = b[v]
        for w in adj[v]:
            if w == u: continue
            res += min(0, f[w])
        res += min(0, without_v)
        ans_dp[v] = res
        dfs2(v, u)

# 执行两次 DFS
dfs1(0, -1)
dfs2(0, -1)

# 累加总代价
total_cost = 0
for i in range(n):
    total_cost += delta[i] * ans_dp[i]
print(total_cost)
```
## Java 
```java
import java.io.*;
import java.util.*;

public class Main {
    static int n;
    static int[] a, b;
    static List<Integer>[] adj;
    static long[] f, ans;

    // 向下 DFS，计算 f[u]
    static void dfs1(int u, int p) {
        f[u] = b[u];
        for (int v : adj[u]) {
            if (v == p) continue;
            dfs1(v, u);
            f[u] += Math.min(0, f[v]);
        }
    }

    // 重根 DFS，计算 ans[v]
    static void dfs2(int u, int p) {
        if (p == -1) ans[u] = f[u];
        for (int v : adj[u]) {
            if (v == p) continue;
            long withoutV = ans[u] - Math.min(0, f[v]);
            long res = b[v];
            for (int w : adj[v]) {
                if (w == u) continue;
                res += Math.min(0, f[w]);
            }
            res += Math.min(0, withoutV);
            ans[v] = res;
            dfs2(v, u);
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        n = Integer.parseInt(br.readLine());
        a = new int[n]; b = new int[n];
        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) a[i] = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) b[i] = Integer.parseInt(st.nextToken());
        adj = new ArrayList[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int i = 0; i < n-1; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken()) - 1;
            int v = Integer.parseInt(st.nextToken()) - 1;
            adj[u].add(v);
            adj[v].add(u);
        }

        // 求中位数 T
        int[] sortedA = Arrays.copyOf(a, n);
        Arrays.sort(sortedA);
        int T = sortedA[n/2];

        long totalCost = 0;
        int[] delta = new int[n];
        for (int i = 0; i < n; i++) delta[i] = Math.abs(a[i] - T);

        f = new long[n]; ans = new long[n];
        dfs1(0, -1);
        dfs2(0, -1);

        // 累加总代价
        for (int i = 0; i < n; i++) {
            totalCost += (long)delta[i] * ans[i];
        }
        System.out.println(totalCost);
    }
}
```