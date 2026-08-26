## 题解思路

### 问题抽象

固定一棵无向树，总节点数为 $n$。
若以节点 $r$ 为根，则每个节点 $u$ 都对应一棵子树，大小记为 $\text{sz}_r(u)$。
题目要求：对每个根 $r$，统计满足

$$
\text{sz}_r(u)\bmod 2 = 0
$$

的节点个数。

### 两次 DFS + 换根 DP

1. **第一次 DFS（以 1 为根）**

   * 计算

     * `sz[u]`：以 1 为根时，节点 $u$ 子树大小；
     * `evenCnt[1]`：根为 1 时，偶子树节点的总数。
   * 时间 $O(n)$。

2. **第二次 DFS（换根传递答案）**

   * 沿着树边将根从父 `p` 移动到子 `v`。
   * 受影响的节点只有 **p 与 v**（其它节点的子树结构不变）。
   * 记

     * `oldPu = (sz[p] % 2==0)`：移动前 `p` 子树是否偶数；
     * `oldPv = (sz[v] % 2==0)`；
     * `newPu = ((n - sz[v]) % 2==0)`：移动后 `p` 子树大小变为去掉 `v` 子树；
     * `newPv = (n % 2==0)`：新根 `v` 子树为整个树。
   * 偶节点总数改变量

     $$
       \Delta = (newPu - oldPu) + (newPv - oldPv).
     $$
   * 故

     $$
       \text{evenCnt}[v] = \text{evenCnt}[p] + \Delta.
     $$
   * 同时更新 `sz[p]`、`sz[v]` 并向下递归。
   * 整体仍是 $O(n)$。

### 正确性说明

换根只影响根与其子之间的两棵互补子树，其余节点子树结构完全一致；因此仅需要考虑 `p`、`v` 偶偶性变化，上式即为偶节点总数的精确增量。

### 复杂度分析

* **时间复杂度**：两次 DFS，$O(n)$。
* **空间复杂度**：邻接表 + 递归栈，$O(n)$。

## 代码

### Python

```python
import sys
sys.setrecursionlimit(1 << 20)
it = sys.stdin.buffer
n = int(it.readline())
g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, it.readline().split())
    g[u].append(v)
    g[v].append(u)

sz = [0] * (n + 1)
ans = [0] * (n + 1)

def dfs1(u, fa):
    """第一次 DFS：计算 sz 与根为1时的偶节点数"""
    sz[u] = 1
    for v in g[u]:
        if v == fa:
            continue
        dfs1(v, u)
        sz[u] += sz[v]
    if sz[u] % 2 == 0:
        ans[1] += 1

def dfs2(u, fa):
    """第二次 DFS：换根 DP 推导答案"""
    for v in g[u]:
        if v == fa:
            continue
        # 计算增量
        oldPu = (sz[u] % 2 == 0)
        oldPv = (sz[v] % 2 == 0)
        newPv = (n % 2 == 0)
        newPu = ((n - sz[v]) % 2 == 0)

        ans[v] = ans[u] + (newPu - oldPu) + (newPv - oldPv)

        # 临时修改子树大小以继续向下
        prev_sz_u = sz[u]
        sz[u] -= sz[v]
        sz[v] = n
        dfs2(v, u)
        # 还原
        sz[v] = oldPv * 0 + (n if v == u else sz[v])  # 实际不再访问，可省
        sz[u] = prev_sz_u

dfs1(1, 0)
dfs2(1, 0)

out = '\n'.join(map(str, ans[1:]))
sys.stdout.write(out)
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
const int N = 100005;

vector<int> g[N];
int n, sz[N], evenCnt[N];

void dfs1(int u, int fa) {
    sz[u] = 1;
    for (int v : g[u])
        if (v != fa) {
            dfs1(v, u);
            sz[u] += sz[v];
        }
    if (!(sz[u] & 1)) ++evenCnt[1];
}

void dfs2(int u, int fa) {
    for (int v : g[u])
        if (v != fa) {
            bool oldPu = !(sz[u] & 1);
            bool oldPv = !(sz[v] & 1);
            bool newPv = !(n & 1);
            bool newPu = !((n - sz[v]) & 1);
            evenCnt[v] = evenCnt[u] + (newPu - oldPu) + (newPv - oldPv);

            int prev_sz_u = sz[u];
            sz[u] -= sz[v];
            sz[v] = n;
            dfs2(v, u);
            sz[v] = oldPv ? 0 : 0;         // 不再访问，可略
            sz[u] = prev_sz_u;
        }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    for (int i = 0, u, v; i < n - 1; ++i) {
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    dfs1(1, 0);
    dfs2(1, 0);
    for (int i = 1; i <= n; ++i)
        cout << evenCnt[i] << '\n';
    return 0;
}
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
    static final int MAX = 100_005;
    static ArrayList<Integer>[] g = new ArrayList[MAX];
    static int[] sz = new int[MAX];
    static int[] ans = new int[MAX];
    static int n;

    static void dfs1(int u, int fa) {
        sz[u] = 1;
        for (int v : g[u])
            if (v != fa) {
                dfs1(v, u);
                sz[u] += sz[v];
            }
        if ((sz[u] & 1) == 0) ans[1]++;
    }

    static void dfs2(int u, int fa) {
        for (int v : g[u])
            if (v != fa) {
                boolean oldPu = (sz[u] & 1) == 0;
                boolean oldPv = (sz[v] & 1) == 0;
                boolean newPv = (n & 1) == 0;
                boolean newPu = ((n - sz[v]) & 1) == 0;
                ans[v] = ans[u] + (newPu ? 1 : 0) - (oldPu ? 1 : 0)
                                   + (newPv ? 1 : 0) - (oldPv ? 1 : 0);

                int prev = sz[u];
                sz[u] -= sz[v];
                sz[v] = n;
                dfs2(v, u);
                sz[u] = prev;           // 恢复，后续不再用，可省
            }
    }

    public static void main(String[] args) throws Exception {
        for (int i = 0; i < MAX; ++i) g[i] = new ArrayList<>();
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        n = Integer.parseInt(br.readLine().trim());
        for (int i = 0; i < n - 1; ++i) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            g[u].add(v);
            g[v].add(u);
        }
        dfs1(1, 0);
        dfs2(1, 0);
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; ++i)
            sb.append(ans[i]).append('\n');
        System.out.print(sb.toString());
    }
}
```