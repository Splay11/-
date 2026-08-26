## 解题思路

先把整棵树固定以节点 $1$ 为根，预处理出任意两点的最近公共祖先（$LCA$）。

对于一次查询给定 $(r,u,v)$，要求的是：如果把整棵树改成以 $r$ 为根时，$u$ 和 $v$ 的最近公共祖先是谁。

设：

* $a=LCA(u,v)$
* $b=LCA(u,r)$
* $c=LCA(v,r)$

这里的 $LCA$ 都是基于原始根节点 $1$ 计算的。

结论是：

* 如果 $a=b$，答案就是 $c$
* 如果 $a=c$，答案就是 $b$
* 否则答案就是 $a$

这是这道题的核心结论。

原因可以这样理解：

把树换根时，只有 $u,v,r$ 三点路径关系会影响答案。
而 $a,b,c$ 一定都落在这三条相关路径上。进一步分析可以发现，真正的新根下的最近公共祖先，恰好就是这三个点中“最深的那个特殊点”，按上面的分类讨论后就能直接得到答案。

为了快速求普通 $LCA$，使用：

* $DFS$ 预处理深度
* 倍增算法预处理祖先表

这样每次查询只需要求 $3$ 次 $LCA$，就能在 $O(\log n)$ 时间内得到答案。

实现方法如下：

1. 建树。
2. 以节点 $1$ 为根做一次 $DFS/BFS$，求出每个点深度和倍增祖先表。
3. 实现普通 $LCA(u,v)$。
4. 对每个查询：

   * 先求 $a,b,c$
   * 按上述公式输出答案

---

## 复杂度分析

设单组数据有 $n$ 个点，$q$ 次查询。

预处理部分：

* 建树：$O(n)$
* 倍增预处理：$O(n\log n)$

查询部分：

* 每次查询求 $3$ 次 $LCA$，复杂度为 $O(\log n)$
* 总查询复杂度为 $O(q\log n)$

总时间复杂度为：

$$
O((n+q)\log n)
$$

空间复杂度为：

$$
O(n\log n)
$$

对于题目的数据范围是完全合适的。

---

## 代码实现

### Python

```python
import sys

# 求解功能写在外部函数里
def solve():
    input = sys.stdin.readline
    T = int(input())
    LOG = 20  # 因为 n <= 2e5，2^18 > 2e5，开到 20 足够

    for _ in range(T):
        n, q = map(int, input().split())
        g = [[] for _ in range(n + 1)]

        # 建树
        for _ in range(n - 1):
            x, y = map(int, input().split())
            g[x].append(y)
            g[y].append(x)

        # 倍增祖先表和深度
        up = [[0] * (n + 1) for _ in range(LOG)]
        depth = [0] * (n + 1)

        # 用栈模拟 DFS，避免递归过深
        stack = [1]
        parent = [0] * (n + 1)
        parent[1] = 0
        order = []

        while stack:
            u = stack.pop()
            order.append(u)
            for v in g[u]:
                if v == parent[u]:
                    continue
                parent[v] = u
                depth[v] = depth[u] + 1
                stack.append(v)

        # 初始化第 0 层祖先
        for i in range(1, n + 1):
            up[0][i] = parent[i]

        # 倍增预处理
        for k in range(1, LOG):
            for i in range(1, n + 1):
                up[k][i] = up[k - 1][up[k - 1][i]]

        # 普通 LCA
        def lca(u, v):
            if depth[u] < depth[v]:
                u, v = v, u

            # 先把 u 跳到和 v 同一深度
            diff = depth[u] - depth[v]
            for k in range(LOG):
                if diff >> k & 1:
                    u = up[k][u]

            if u == v:
                return u

            # 一起向上跳
            for k in range(LOG - 1, -1, -1):
                if up[k][u] != up[k][v]:
                    u = up[k][u]
                    v = up[k][v]

            return up[0][u]

        ans = []
        for _ in range(q):
            r, u, v = map(int, input().split())

            a = lca(u, v)
            b = lca(u, r)
            c = lca(v, r)

            # 按结论分类讨论
            if a == b:
                ans.append(str(c))
            elif a == c:
                ans.append(str(b))
            else:
                ans.append(str(a))

        sys.stdout.write("\n".join(ans) + "\n")


# 输入输出写在主函数里
if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static List<Integer>[] g;
    static int[][] up;
    static int[] depth;
    static int[] parent;
    static int LOG;

    // 普通 LCA
    static int lca(int u, int v) {
        if (depth[u] < depth[v]) {
            int temp = u;
            u = v;
            v = temp;
        }

        // 先把 u 提到和 v 同一深度
        int diff = depth[u] - depth[v];
        for (int k = 0; k < LOG; k++) {
            if (((diff >> k) & 1) == 1) {
                u = up[k][u];
            }
        }

        if (u == v) {
            return u;
        }

        // 一起向上跳
        for (int k = LOG - 1; k >= 0; k--) {
            if (up[k][u] != up[k][v]) {
                u = up[k][u];
                v = up[k][v];
            }
        }

        return up[0][u];
    }

    // 求解功能写在外部函数里
    static void solve(BufferedReader br) throws Exception {
        int T = Integer.parseInt(br.readLine());

        while (T-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());
            int q = Integer.parseInt(st.nextToken());

            LOG = 20;
            g = new ArrayList[n + 1];
            for (int i = 1; i <= n; i++) {
                g[i] = new ArrayList<>();
            }

            // 建树
            for (int i = 0; i < n - 1; i++) {
                st = new StringTokenizer(br.readLine());
                int x = Integer.parseInt(st.nextToken());
                int y = Integer.parseInt(st.nextToken());
                g[x].add(y);
                g[y].add(x);
            }

            up = new int[LOG][n + 1];
            depth = new int[n + 1];
            parent = new int[n + 1];

            // 用栈模拟 DFS，避免递归过深
            int[] stack = new int[n];
            int top = 0;
            stack[top++] = 1;
            parent[1] = 0;

            while (top > 0) {
                int u = stack[--top];
                for (int v : g[u]) {
                    if (v == parent[u]) {
                        continue;
                    }
                    parent[v] = u;
                    depth[v] = depth[u] + 1;
                    stack[top++] = v;
                }
            }

            // 初始化第 0 层祖先
            for (int i = 1; i <= n; i++) {
                up[0][i] = parent[i];
            }

            // 倍增预处理
            for (int k = 1; k < LOG; k++) {
                for (int i = 1; i <= n; i++) {
                    up[k][i] = up[k - 1][up[k - 1][i]];
                }
            }

            StringBuilder sb = new StringBuilder();

            for (int i = 0; i < q; i++) {
                st = new StringTokenizer(br.readLine());
                int r = Integer.parseInt(st.nextToken());
                int u = Integer.parseInt(st.nextToken());
                int v = Integer.parseInt(st.nextToken());

                int a = lca(u, v);
                int b = lca(u, r);
                int c = lca(v, r);

                // 按结论分类讨论
                if (a == b) {
                    sb.append(c).append('\n');
                } else if (a == c) {
                    sb.append(b).append('\n');
                } else {
                    sb.append(a).append('\n');
                }
            }

            System.out.print(sb.toString());
        }
    }

    // 输入输出写在主函数里
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        solve(br);
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

const int LOG = 20;

vector<vector<int> > g;
vector<vector<int> > up;
vector<int> depth, parent;

// 普通 LCA
int lca(int u, int v) {
    if (depth[u] < depth[v]) {
        swap(u, v);
    }

    // 先把 u 提到和 v 同一深度
    int diff = depth[u] - depth[v];
    for (int k = 0; k < LOG; k++) {
        if ((diff >> k) & 1) {
            u = up[k][u];
        }
    }

    if (u == v) {
        return u;
    }

    // 一起向上跳
    for (int k = LOG - 1; k >= 0; k--) {
        if (up[k][u] != up[k][v]) {
            u = up[k][u];
            v = up[k][v];
        }
    }

    return up[0][u];
}

// 求解功能写在外部函数里
void solve() {
    int T;
    cin >> T;

    while (T--) {
        int n, q;
        cin >> n >> q;

        g.assign(n + 1, vector<int>());
        for (int i = 0; i < n - 1; i++) {
            int x, y;
            cin >> x >> y;
            g[x].push_back(y);
            g[y].push_back(x);
        }

        up.assign(LOG, vector<int>(n + 1, 0));
        depth.assign(n + 1, 0);
        parent.assign(n + 1, 0);

        // 用栈模拟 DFS，避免递归爆栈
        vector<int> stack;
        stack.push_back(1);
        parent[1] = 0;

        while (!stack.empty()) {
            int u = stack.back();
            stack.pop_back();

            for (int v : g[u]) {
                if (v == parent[u]) {
                    continue;
                }
                parent[v] = u;
                depth[v] = depth[u] + 1;
                stack.push_back(v);
            }
        }

        // 初始化第 0 层祖先
        for (int i = 1; i <= n; i++) {
            up[0][i] = parent[i];
        }

        // 倍增预处理
        for (int k = 1; k < LOG; k++) {
            for (int i = 1; i <= n; i++) {
                up[k][i] = up[k - 1][up[k - 1][i]];
            }
        }

        while (q--) {
            int r, u, v;
            cin >> r >> u >> v;

            int a = lca(u, v);
            int b = lca(u, r);
            int c = lca(v, r);

            // 按结论分类讨论
            if (a == b) {
                cout << c << '\n';
            } else if (a == c) {
                cout << b << '\n';
            } else {
                cout << a << '\n';
            }
        }
    }
}

// 输入输出写在主函数里
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();
    return 0;
}
```