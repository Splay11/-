## 解题思路

### 核心思路

观察操作的本质：第 $k$ 秒选择位置 $x$ 时，若 $x$ 与 $x+1$ 颜色不同，则将 $x$ 所在的整个同色区间染成 $x+1$ 的颜色。这等价于**将 $x$ 所在连通块与 $x+1$ 所在连通合并**，合并时间为 $k$。

这提示我们使用 **Kruskal 重构树** 来维护连通块的合并过程：

1. **构建重构树**：初始时每个位置 $i$（$1\le i\le n$）为独立的叶子节点。遍历 $t$ 次操作，第 $k$ 次操作选择位置 $x$ 时：
   - 找到 $x$ 所在连通块的代表元 $fx$ 和 $x+1$ 所在连通块的代表元 $fy$
   - 若 $fx \neq fy$，新建节点 $u$（编号递增），权值 $val[u]=k$，将 $fx$ 和 $fy$ 作为 $u$ 的左右儿子，并合并两个连通块

2. **性质**：重构树中，每个内部节点代表一次合并操作，其权值为合并时间；叶子节点代表原始位置。对于任意两个位置 $l$ 和 $r$，它们首次属于同一连通块的时间即为重构树中 $l$ 和 $r$ 的 **最近公共祖先（LCA）** 的权值。

3. **查询**：对于询问 $[l,r]$：
   - 若 $l=r$，答案为 $0$（初始已同色）
   - 否则求 $l$ 和 $r$ 在重构树中的 LCA，若 LCA 存在则输出其权值，否则输出 $-1$（从未合并）

### 实现方法

- **并查集**：维护当前各位置所属连通块的代表元，支持路径压缩。
- **LCA 预处理**：使用倍增法，从重构树的根节点进行 BFS/DFS，预处理每个节点的深度 $depth[]$ 和 $2^k$ 级祖先 $up[k][u]$。
- **判断连通性**：在 LCA 查询前，先判断两节点是否属于同一棵树（通过记录每个节点所属树的根节点 $root\_id$），若不属于同一棵树则返回 $-1$。

## 复杂度分析

- **构建重构树**：每次操作并查集查询与合并均摊 $O(\alpha(n))$，最多创建 $n-1$ 个新节点，总时间 $O((n+t)\cdot \alpha(n))$。
- **LCA 预处理**：节点总数 $N \le n + \min(t, n-1) \le 2n$，预处理时间 $O(N\log N)$。
- **单次查询**：倍增 LCA 查询时间 $O(\log N)$。
- **总时间复杂度**：$O((n+t)\log n + q\log n)$，满足 $2\times 10^5$ 数据范围。
- **空间复杂度**：$O((n+t)\log n)$，用于存储重构树结构和倍增数组。

## 代码实现

### Python

```python
import sys
from collections import deque

def main():
    input = sys.stdin.readline
    n, t, q = map(int, input().split())
    ops = [int(input()) for _ in range(t)]
    
    # 并查集数组
    dsu_fa = list(range(n + t + 2))
    # 重构树结构：left, right 为子节点，val 为节点权值（合并时间），par 为父节点
    left = [0] * (n + t + 2)
    right = [0] * (n + t + 2)
    val = [0] * (n + t + 2)
    par = [0] * (n + t + 2)
    
    def dsu_find(x):
        # 带路径压缩的查找
        while dsu_fa[x] != x:
            dsu_fa[x] = dsu_fa[dsu_fa[x]]
            x = dsu_fa[x]
        return x
    
    cur = n  # 当前新节点编号，从 n+1 开始
    for k in range(1, t + 1):
        x = ops[k - 1]
        fx = dsu_find(x)
        fy = dsu_find(x + 1)
        if fx != fy:
            cur += 1
            val[cur] = k  # 记录合并时间
            left[cur] = fx
            right[cur] = fy
            par[fx] = cur
            par[fy] = cur
            dsu_fa[fx] = cur
            dsu_fa[fy] = cur
    
    # 构建图的邻接表（父节点指向子节点，用于后续 BFS）
    g = [[] for _ in range(cur + 1)]
    for i in range(n + 1, cur + 1):
        g[i].append(left[i])
        g[i].append(right[i])
    
    # LCA 倍增预处理
    LOG = 20
    up = [[0] * (cur + 1) for _ in range(LOG)]
    depth = [0] * (cur + 1)
    root_id = [0] * (cur + 1)  # 记录每个节点属于哪棵树的根
    
    # 找到所有根节点（重构树中父节点为 0 的节点）
    roots = [i for i in range(1, cur + 1) if par[i] == 0]
    
    for root in roots:
        queue = deque([root])
        root_id[root] = root
        while queue:
            u = queue.popleft()
            # 计算 up 表
            up[0][u] = par[u]
            for i in range(1, LOG):
                up[i][u] = up[i - 1][up[i - 1][u]]
            # 遍历子节点
            for v in g[u]:
                if v:  # 子节点存在
                    depth[v] = depth[u] + 1
                    root_id[v] = root
                    queue.append(v)
    
    def lca(u, v):
        # 若不在同一棵树，返回 0
        if root_id[u] != root_id[v]:
            return 0
        if depth[u] < depth[v]:
            u, v = v, u
        # 将 u 提升到与 v 同一深度
        for i in range(LOG - 1, -1, -1):
            if depth[u] - (1 << i) >= depth[v]:
                u = up[i][u]
        if u == v:
            return u
        # 同时向上提升
        for i in range(LOG - 1, -1, -1):
            if up[i][u] != up[i][v]:
                u = up[i][u]
                v = up[i][v]
        return up[0][u]
    
    # 处理询问
    out_lines = []
    for _ in range(q):
        l, r = map(int, input().split())
        if l == r:
            out_lines.append("0")
        else:
            ancestor = lca(l, r)
            if ancestor == 0:
                out_lines.append("-1")
            else:
                out_lines.append(str(val[ancestor]))
    
    print('\n'.join(out_lines))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static int[] dsuFa;  // 并查集
    static int[] left;   // 重构树左儿子
    static int[] right;  // 重构树右儿子
    static int[] val;    // 节点权值（合并时间）
    static int[] par;    // 重构树父节点
    static int[][] up;   // 倍增数组
    static int[] depth;
    static int[] rootId;
    static List<Integer>[] g;
    static int LOG = 20;
    
    static int dsuFind(int x) {
        if (dsuFa[x] != x) {
            dsuFa[x] = dsuFind(dsuFa[x]);
        }
        return dsuFa[x];
    }
    
    static void bfs(int root) {
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(root);
        rootId[root] = root;
        depth[root] = 0;
        while (!queue.isEmpty()) {
            int u = queue.poll();
            up[0][u] = par[u];
            for (int i = 1; i < LOG; i++) {
                up[i][u] = up[i-1][up[i-1][u]];
            }
            for (int v : g[u]) {
                if (v != 0) {
                    depth[v] = depth[u] + 1;
                    rootId[v] = root;
                    queue.offer(v);
                }
            }
        }
    }
    
    static int lca(int u, int v) {
        if (rootId[u] != rootId[v]) return 0;
        if (depth[u] < depth[v]) {
            int tmp = u; u = v; v = tmp;
        }
        // 提升 u
        for (int i = LOG - 1; i >= 0; i--) {
            if (depth[u] - (1 << i) >= depth[v]) {
                u = up[i][u];
            }
        }
        if (u == v) return u;
        for (int i = LOG - 1; i >= 0; i--) {
            if (up[i][u] != up[i][v]) {
                u = up[i][u];
                v = up[i][v];
            }
        }
        return up[0][u];
    }
    
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int t = Integer.parseInt(st.nextToken());
        int q = Integer.parseInt(st.nextToken());
        
        int[] ops = new int[t];
        for (int i = 0; i < t; i++) {
            ops[i] = Integer.parseInt(br.readLine());
        }
        
        int maxN = n + t + 5;
        dsuFa = new int[maxN];
        left = new int[maxN];
        right = new int[maxN];
        val = new int[maxN];
        par = new int[maxN];
        
        for (int i = 0; i < maxN; i++) dsuFa[i] = i;
        
        int cur = n;
        for (int k = 1; k <= t; k++) {
            int x = ops[k-1];
            int fx = dsuFind(x);
            int fy = dsuFind(x + 1);
            if (fx != fy) {
                cur++;
                val[cur] = k;
                left[cur] = fx;
                right[cur] = fy;
                par[fx] = cur;
                par[fy] = cur;
                dsuFa[fx] = cur;
                dsuFa[fy] = cur;
            }
        }
        
        g = new ArrayList[cur + 1];
        for (int i = 0; i <= cur; i++) g[i] = new ArrayList<>();
        for (int i = n + 1; i <= cur; i++) {
            g[i].add(left[i]);
            g[i].add(right[i]);
        }
        
        up = new int[LOG][cur + 1];
        depth = new int[cur + 1];
        rootId = new int[cur + 1];
        
        // 找到所有根节点进行 BFS
        for (int i = 1; i <= cur; i++) {
            if (par[i] == 0) {
                bfs(i);
            }
        }
        
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < q; i++) {
            st = new StringTokenizer(br.readLine());
            int l = Integer.parseInt(st.nextToken());
            int r = Integer.parseInt(st.nextToken());
            if (l == r) {
                sb.append("0\n");
            } else {
                int ancestor = lca(l, r);
                if (ancestor == 0) sb.append("-1\n");
                else sb.append(val[ancestor]).append("\n");
            }
        }
        System.out.print(sb);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 4e5 + 10;  // 最大节点数 2*(n+t)
const int LOG = 20;

int dsuFa[MAXN];  // 并查集
int Left[MAXN];   // 重构树左儿子
int Right[MAXN];  // 重构树右儿子
int val[MAXN];    // 节点权值
int par[MAXN];    // 重构树父节点
int up[LOG][MAXN];
int depth[MAXN];
int rootId[MAXN];
vector<int> g[MAXN];

int dsuFind(int x) {
    if (dsuFa[x] != x) dsuFa[x] = dsuFind(dsuFa[x]);
    return dsuFa[x];
}

void bfs(int root) {
    queue<int> q;
    q.push(root);
    rootId[root] = root;
    depth[root] = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        up[0][u] = par[u];
        for (int i = 1; i < LOG; i++) {
            up[i][u] = up[i-1][up[i-1][u]];
        }
        for (int v : g[u]) {
            if (v != 0) {
                depth[v] = depth[u] + 1;
                rootId[v] = root;
                q.push(v);
            }
        }
    }
}

int lca(int u, int v) {
    if (rootId[u] != rootId[v]) return 0;
    if (depth[u] < depth[v]) swap(u, v);
    // 提升 u
    for (int i = LOG - 1; i >= 0; i--) {
        if (depth[u] - (1 << i) >= depth[v]) {
            u = up[i][u];
        }
    }
    if (u == v) return u;
    for (int i = LOG - 1; i >= 0; i--) {
        if (up[i][u] != up[i][v]) {
            u = up[i][u];
            v = up[i][v];
        }
    }
    return up[0][u];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, t, q;
    cin >> n >> t >> q;
    vector<int> ops(t);
    for (int i = 0; i < t; i++) cin >> ops[i];
    
    for (int i = 0; i <= n + t; i++) dsuFa[i] = i;
    
    int cur = n;
    for (int k = 1; k <= t; k++) {
        int x = ops[k-1];
        int fx = dsuFind(x);
        int fy = dsuFind(x + 1);
        if (fx != fy) {
            cur++;
            val[cur] = k;
            Left[cur] = fx;
            Right[cur] = fy;
            par[fx] = cur;
            par[fy] = cur;
            dsuFa[fx] = cur;
            dsuFa[fy] = cur;
        }
    }
    
    for (int i = n + 1; i <= cur; i++) {
        g[i].push_back(Left[i]);
        g[i].push_back(Right[i]);
    }
    
    // 找到所有根节点
    for (int i = 1; i <= cur; i++) {
        if (par[i] == 0) {
            bfs(i);
        }
    }
    
    while (q--) {
        int l, r;
        cin >> l >> r;
        if (l == r) {
            cout << 0 << '\n';
        } else {
            int ancestor = lca(l, r);
            if (ancestor == 0) cout << -1 << '\n';
            else cout << val[ancestor] << '\n';
        }
    }
    return 0;
}
```