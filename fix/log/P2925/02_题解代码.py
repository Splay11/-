## 思路与方法

本题给定一棵以 1 号节点为根的无向树，每个节点有一个权值（可为负）。允许对任意非根节点进行两种删除操作：

1. 删除度为 1 的非根叶子节点。
2. 删除度为 2 的非根中间节点，并将其两个邻居直接连接。

操作任意次后，希望最大化剩余节点权值之和，且根节点 1 必须保留。

### 树上 DP 模型

对每个节点 v，令：

- **A[v]**：保留 v 时，以 v 为根的子树中可取得的最大权值和。
- **B[v]**：删除 v 时，以 v 为根的子树中可取得的最大权值和（相当于在 v 被删除后，其子树中只能选择一条“最优路径”保留）。

那么对于 v 的所有孩子 u：

- 若保留 v，则所有孩子都可以自由选择保留或删除，贡献为 ∑ max(A[u], B[u])。  
  因此  
  $A[v] = w[v] + ∑_{u∈children[v]} max(A[u], B[u])$

- 若删除 v，则它的多个子树会被“连通”到父亲节点，但只能保留一条路径，因此只能选择一个孩子贡献最大的 DP：  
  $B[v] = max_{u∈children[v]} max(A[u], B[u])$

根节点 1 必须保留，答案即 A[1]。

### 具体实现

1. **建树并按层序（BFS）确定父子关系**  
2. **自底向上（逆 BFS 顺序）计算 DP 值**  
3. 输出 A[1]

## 复杂度分析

- **时间复杂度**：O(n)  
  - 建树 O(n)；BFS O(n)；DP 也遍历每条边和节点各一次 O(n)。  
- **空间复杂度**：O(n)  
  - 邻接表、若干长度为 n+1 的数组。

## 代码

### Python

```python
import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        n = int(next(it))
        w = [0]*(n+1)
        for i in range(1, n+1):
            w[i] = int(next(it))
        adj = [[] for _ in range(n+1)]
        for _ in range(n-1):
            u = int(next(it)); v = int(next(it))
            adj[u].append(v)
            adj[v].append(u)

        # 1. BFS 建父子关系
        par = [0]*(n+1)
        children = [[] for _ in range(n+1)]
        order = []
        q = deque([1])
        par[1] = -1
        while q:
            v = q.popleft()
            order.append(v)
            for u in adj[v]:
                if u == par[v]:
                    continue
                par[u] = v
                children[v].append(u)
                q.append(u)

        # 2. DP 数组
        dpA = [0]*(n+1)  # 保留 v
        dpB = [0]*(n+1)  # 删除 v
        dp  = [0]*(n+1)  # max(dpA, dpB)

        # 3. 自底向上
        for v in reversed(order):
            sum_keep = 0
            best_child = float('-inf')
            if not children[v]:
                # 叶子节点：删除后无子贡献
                best_child = 0
            for u in children[v]:
                sum_keep += dp[u]
                best_child = max(best_child, dp[u])
            dpA[v] = w[v] + sum_keep
            dpB[v] = best_child
            dp[v] = max(dpA[v], dpB[v])

        # 根必须保留
        out.append(str(dpA[1]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(in.readLine());
        int T = Integer.parseInt(st.nextToken());
        StringBuilder sb = new StringBuilder();
        while (T-- > 0) {
            int n = Integer.parseInt(in.readLine());
            long[] w = new long[n+1];
            st = new StringTokenizer(in.readLine());
            for (int i = 1; i <= n; i++) {
                w[i] = Long.parseLong(st.nextToken());
            }
            List<Integer>[] adj = new List[n+1];
            for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();
            for (int i = 0; i < n-1; i++) {
                st = new StringTokenizer(in.readLine());
                int u = Integer.parseInt(st.nextToken());
                int v = Integer.parseInt(st.nextToken());
                adj[u].add(v);
                adj[v].add(u);
            }

            // BFS 建父子关系
            int[] par = new int[n+1];
            List<Integer>[] children = new List[n+1];
            for (int i = 1; i <= n; i++) children[i] = new ArrayList<>();
            int[] order = new int[n];
            Queue<Integer> q = new LinkedList<>();
            q.add(1);
            par[1] = -1;
            int idx = 0;
            while (!q.isEmpty()) {
                int v = q.poll();
                order[idx++] = v;
                for (int u : adj[v]) {
                    if (u == par[v]) continue;
                    par[u] = v;
                    children[v].add(u);
                    q.add(u);
                }
            }

            long[] dpA = new long[n+1], dpB = new long[n+1], dp = new long[n+1];
            // 自底向上
            for (int i = n-1; i >= 0; i--) {
                int v = order[i];
                long sumKeep = 0, best = Long.MIN_VALUE;
                if (children[v].isEmpty()) best = 0;
                for (int u : children[v]) {
                    sumKeep += dp[u];
                    best = Math.max(best, dp[u]);
                }
                dpA[v] = w[v] + sumKeep;
                dpB[v] = best;
                dp[v] = Math.max(dpA[v], dpB[v]);
            }
            sb.append(dpA[1]).append('\n');
        }
        System.out.print(sb);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; 
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<ll> w(n+1);
        for (int i = 1; i <= n; i++) {
            cin >> w[i];
        }
        vector<vector<int>> adj(n+1);
        for (int i = 0, u, v; i < n-1; i++) {
            cin >> u >> v;
            adj[u].push_back(v);
            adj[v].push_back(u);
        }

        // BFS 建父子关系
        vector<int> par(n+1, 0);
        vector<vector<int>> children(n+1);
        vector<int> order;
        order.reserve(n);
        queue<int> q;
        q.push(1);
        par[1] = -1;
        while (!q.empty()) {
            int v = q.front(); q.pop();
            order.push_back(v);
            for (int u : adj[v]) {
                if (u == par[v]) continue;
                par[u] = v;
                children[v].push_back(u);
                q.push(u);
            }
        }

        vector<ll> dpA(n+1), dpB(n+1), dp(n+1);
        // 自底向上计算
        for (int i = n-1; i >= 0; --i) {
            int v = order[i];
            ll sumKeep = 0, best = LLONG_MIN;
            if (children[v].empty()) best = 0;
            for (int u : children[v]) {
                sumKeep += dp[u];
                best = max(best, dp[u]);
            }
            dpA[v] = w[v] + sumKeep;
            dpB[v] = best;
            dp[v] = max(dpA[v], dpB[v]);
        }

        // 根必须保留
        cout << dpA[1] << "\n";
    }
    return 0;
}
```