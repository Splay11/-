## 思路与证明

### 1）核心定义

对每个结点$u$ 维护两个量：

* $down[u]$：从 $u$ 向下走，到达其子树内**某个红点**的最大距离；若子树内不存在红点，设为负无穷（实现时用常数 $-\text{INF}$ 代表，例如 $-10^9$）。
* $ans[u]$：以 $u$ 为根的子树内红点直径的答案。

### 2）子问题合并

设 $u$ 的所有儿子为 $v$ 集合。对每个儿子 $v$，若 $down[v]\neq -\text{INF}$，则 $v$ 能提供一条“向下通往某个红点”的链，且到 $u$ 的距离为 $down[v]+1$。
在结点 $u$ 的子树中，最大直径可能来自两种情况：

1. 完全落在某个儿子 $v$ 的子树内，即 $ans[v]$。
2. 一条路径经过 $u$：取所有“可用的向下深度”（每个儿子贡献 $down[v]+1$，若 $u$ 自身为红点还可贡献 $0$），把其中最大的两条相加，得到候选值 $best_1+best_2$。

于是有转移：

![](/file/2/DDKG2KUFkL4EYANY2OEQ8.png)

![](/file/2/eED_CqEk3DzZhXYWSz1FD.png)

其中 $S$ 为 $u$ 处全部“可用向下深度”的集合（儿子贡献与 $u$ 自身是否为红点的 $0$），$\text{top2}(S)$ 表示取 $S$ 中前两大且都有效的和；若 $S$ 中不足两条有效深度，则该项按 $0$ 计。

### 3）计算顺序

只需一次**自底向上**的遍历即可。为避免递归栈风险（$n$ 可能达到 $2\times 10^5$），用栈生成从根 $1$ 出发的父子关系与遍历顺序，再按逆序（后序）计算上述转移。


## C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> color(n + 1);
    for (int i = 1; i <= n; ++i) cin >> color[i];

    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    const int NEG_INF = -1000000000; // 表示子树内没有红点
    vector<int> parent(n + 1, 0), order; order.reserve(n);
    // 用栈生成父子关系与遍历顺序（前序）
    vector<int> st; st.push_back(1); parent[1] = 0;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        order.push_back(u);
        for (int v : g[u]) if (v != parent[u]) {
            parent[v] = u;
            st.push_back(v);
        }
    }

    vector<int> down(n + 1, NEG_INF); // 最大向下到红点的距离
    vector<int> ans(n + 1, 0);        // 子树红点直径

    // 按后序（逆序）处理
    for (int i = (int)order.size() - 1; i >= 0; --i) {
        int u = order[i];

        // 候选向下深度集合：儿子提供 down[child]+1，若 u 为红点，还包含 0
        int best1 = NEG_INF, best2 = NEG_INF; // 记录两条最大的有效深度
        if (color[u] == 1) {
            best1 = 0; // u 自身为红点，提供深度 0
        }

        int bestChildAns = 0; // 子树内部直径（不经过 u）
        for (int v : g[u]) if (v != parent[u]) {
            bestChildAns = max(bestChildAns, ans[v]);
            if (down[v] != NEG_INF) {
                int cand = down[v] + 1;
                // 更新 top2
                if (cand > best1) { best2 = best1; best1 = cand; }
                else if (cand > best2) { best2 = cand; }
            }
        }

        // 计算 down[u]
        down[u] = (color[u] ? 0 : NEG_INF);
        for (int v : g[u]) if (v != parent[u]) {
            if (down[v] != NEG_INF)
                down[u] = max(down[u], down[v] + 1);
        }

        // 经过 u 的直径：需要两条有效深度
        int throughU = 0;
        if (best2 != NEG_INF) {
            // 两条都有效
            throughU = best1 + best2;
        } else if (best1 != NEG_INF && color[u] == 1) {
            // 只有一条来自儿子，另一条是 u 自身 0，已包含在 best1=0 的情形；
            // 但若只有一条有效深度，意味着子树红点不足两枚，则按 0 处理
            // 这里不额外处理即可
        }

        ans[u] = max(bestChildAns, throughU);
    }

    for (int i = 1; i <= n; ++i) {
        if (i > 1) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```
## Python 

```python
import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    color = [0] * (n + 1)
    for i in range(1, n + 1):
        color[i] = int(next(it))

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it)); v = int(next(it))
        g[u].append(v); g[v].append(u)

    NEG_INF = -10**9
    parent = [0] * (n + 1)
    order = []
    # 用栈建立父子关系与顺序
    st = [1]
    parent[1] = 0
    while st:
        u = st.pop()
        order.append(u)
        for v in g[u]:
            if v != parent[u]:
                parent[v] = u
                st.append(v)

    down = [NEG_INF] * (n + 1)  # 到子树内红点的最大向下距离
    ans = [0] * (n + 1)         # 子树红点直径

    # 逆序处理得到后序
    for u in reversed(order):
        # 维护 top2
        best1, best2 = (0, NEG_INF) if color[u] == 1 else (NEG_INF, NEG_INF)
        best_child_ans = 0
        # 先遍历儿子，更新 top2 与子树内部直径
        for v in g[u]:
            if v == parent[u]:
                continue
            best_child_ans = max(best_child_ans, ans[v])
            if down[v] != NEG_INF:
                cand = down[v] + 1
                if cand > best1:
                    best2 = best1; best1 = cand
                elif cand > best2:
                    best2 = cand

        # 计算 down[u]
        down[u] = 0 if color[u] == 1 else NEG_INF
        for v in g[u]:
            if v == parent[u]:
                continue
            if down[v] != NEG_INF:
                down[u] = max(down[u], down[v] + 1)

        # 经过 u 的直径（需要两条有效深度）
        through_u = 0
        if best2 != NEG_INF:
            through_u = best1 + best2

        ans[u] = max(best_child_ans, through_u)

    print(" ".join(str(ans[i]) for i in range(1, n + 1)))

if __name__ == "__main__":
    main()
```
## Java 

```java
import java.io.*;
import java.util.*;

/*
  说明：
  - 使用迭代生成父子关系与后序顺序，避免递归栈溢出
  - down[u] 表示从 u 向下到达子树中某个红点的最大距离；若不存在则为 NEG_INF
  - ans[u] 表示以 u 为根的子树的红点直径
*/
public class Main {
    static class FastScanner {
        BufferedInputStream in = new BufferedInputStream(System.in);
        byte[] buffer = new byte[1 << 16];
        int ptr = 0, len = 0;
        int read() throws IOException {
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
            while (c > 32) {
                x = x * 10 + (c - '0');
                c = read();
            }
            return x * sgn;
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        int n;
        try {
            n = fs.nextInt();
        } catch (Exception e) {
            return;
        }
        int[] color = new int[n + 1];
        for (int i = 1; i <= n; i++) color[i] = fs.nextInt();

        ArrayList<Integer>[] g = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) g[i] = new ArrayList<>();
        for (int i = 0; i < n - 1; i++) {
            int u = fs.nextInt(), v = fs.nextInt();
            g[u].add(v); g[v].add(u);
        }

        final int NEG_INF = -1000000000; // 没有红点的标记

        int[] parent = new int[n + 1];
        int[] order = new int[n];
        int idx = 0;

        // 迭代建立父子关系与前序
        Deque<Integer> st = new ArrayDeque<>();
        st.push(1); parent[1] = 0;
        while (!st.isEmpty()) {
            int u = st.pop();
            order[idx++] = u;
            for (int v : g[u]) if (v != parent[u]) {
                parent[v] = u;
                st.push(v);
            }
        }

        int[] down = new int[n + 1];
        int[] ans = new int[n + 1];
        Arrays.fill(down, NEG_INF);

        // 按后序（逆序）计算
        for (int t = n - 1; t >= 0; t--) {
            int u = order[t];

            int best1 = (color[u] == 1 ? 0 : NEG_INF);
            int best2 = NEG_INF;
            int bestChildAns = 0;

            // 收集儿子贡献
            for (int v : g[u]) if (v != parent[u]) {
                bestChildAns = Math.max(bestChildAns, ans[v]);
                if (down[v] != NEG_INF) {
                    int cand = down[v] + 1;
                    if (cand > best1) { best2 = best1; best1 = cand; }
                    else if (cand > best2) { best2 = cand; }
                }
            }

            // 计算 down[u]
            down[u] = (color[u] == 1 ? 0 : NEG_INF);
            for (int v : g[u]) if (v != parent[u]) {
                if (down[v] != NEG_INF)
                    down[u] = Math.max(down[u], down[v] + 1);
            }

            // 经过 u 的直径
            int throughU = 0;
            if (best2 != NEG_INF) {
                throughU = best1 + best2;
            }

            ans[u] = Math.max(bestChildAns, throughU);
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append(' ');
            sb.append(ans[i]);
        }
        sb.append('\n');
        System.out.print(sb.toString());
    }
}
```