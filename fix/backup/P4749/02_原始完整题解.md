## 解题思路

设节点 $u$ 的子树为 $T_u$，题目要求的是：

$$
\sum_{x,y \in T_u,\ x<y}(a_x \oplus a_y)
$$

直接枚举子树内所有点对显然不行，因为点对数量太多。

### 关键转化

异或可以按二进制位分别计算。

对于某一位 $b$，如果子树中这一位为 $1$ 的节点个数是 $cnt_1$，为 $0$ 的节点个数是 $cnt_0$，那么这一位对答案的贡献就是：

$$
cnt_1 \times cnt_0 \times 2^b
$$

因为只有一个是 $0$、一个是 $1$ 时，这一位异或结果才是 $1$。

所以只要我们能快速求出每个节点子树内，每一位上有多少个 $1$，就能得到答案。

### 如何快速统计子树信息

这里用到 树的 $DFS$ 序（欧拉序）。

把整棵树按根节点 $1$ 做一次遍历，记录每个节点：

* 进入时间 $tin[u]$
* 离开时间 $tout[u]$

这样，节点 $u$ 的整棵子树在 $DFS$ 序上一定对应一个连续区间：

$$
[tin[u],\ tout[u]]
$$

再把每个节点的权值按照 $DFS$ 序放进数组中。
对于每一位 $b$，建立前缀和数组，表示当前位上前多少个数里有多少个 $1$。

这样就能在 $O(1)$ 时间求出某个子树区间内这一位有多少个 $1$：

$$
cnt_1 = pre[tout[u]] - pre[tin[u]-1]
$$

子树大小为：

$$
sz = tout[u] - tin[u] + 1
$$

于是：

$$
cnt_0 = sz - cnt_1
$$

该位贡献为：

$$
cnt_1 \times cnt_0 \times 2^b
$$

把所有二进制位累加即可。

### 相关算法

本题用到的核心算法是：

* 树的遍历
* $DFS$ 序（欧拉序）
* 前缀和
* 按位统计贡献

### 实现方法

1. 建图存树。
2. 用非递归 $DFS$ 求出每个节点的 $tin$、$tout$，并得到 $DFS$ 序对应的节点权值数组。
3. 枚举每一位二进制位，建立前缀和。
4. 对每个节点根据其子树区间计算这一位的贡献，累加到答案中。
5. 输出所有节点答案。

之所以使用非递归 $DFS$，是因为 $n \le 2 \times 10^5$，递归可能爆栈。

## 复杂度分析

设二进制位数为 $B$。由于 $a_i \le 10^6$，取 $B=20$ 即可。

* 建树和求 $DFS$ 序的时间复杂度：$O(n)$
* 按位做前缀和并统计答案的时间复杂度：$O(Bn)$

总时间复杂度：

$$
O(Bn)
$$

代入 $B=20$，可以认为是：

$$
O(n)
$$

空间复杂度：

* 邻接表：$O(n)$
* 欧拉序、前缀和、答案数组：$O(n)$

总空间复杂度：

$$
O(n)
$$

复杂度完全适合本题数据范围。

## 代码实现

### Python

```python
import sys


def solve(n, a, edges):
    # 建图
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 非递归 DFS，求每个点的 tin、tout，并得到 DFS 序上的权值
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    euler_val = [0] * (n + 1)  # 1 下标，euler_val[tin[u]] = a[u]
    parent = [0] * (n + 1)

    timer = 0
    stack = [(1, 0, 0)]  # (当前点, 父节点, 状态) 0=首次到达, 1=准备退出
    while stack:
        u, fa, state = stack.pop()
        if state == 0:
            parent[u] = fa
            timer += 1
            tin[u] = timer
            euler_val[timer] = a[u]

            # 退出时记录 tout
            stack.append((u, fa, 1))

            # 子节点入栈
            for v in graph[u]:
                if v != fa:
                    stack.append((v, u, 0))
        else:
            tout[u] = timer

    ans = [0] * (n + 1)
    B = 20  # 因为 a[i] <= 10^6

    # 按位统计贡献
    for b in range(B):
        pre = [0] * (n + 1)

        # 这一位的前缀和
        for i in range(1, n + 1):
            pre[i] = pre[i - 1] + ((euler_val[i] >> b) & 1)

        # 计算每个点子树在这一位上的贡献
        bit_value = 1 << b
        for u in range(1, n + 1):
            l = tin[u]
            r = tout[u]
            ones = pre[r] - pre[l - 1]
            size = r - l + 1
            zeros = size - ones
            ans[u] += ones * zeros * bit_value

    return ans[1:]


def main():
    input = sys.stdin.readline
    n = int(input().strip())
    vals = [0] + list(map(int, input().split()))
    edges = [tuple(map(int, input().split())) for _ in range(n - 1)]

    res = solve(n, vals, edges)
    print(*res)


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    // 题面功能写在外部函数里
    static long[] solve(int n, int[] a, List<Integer>[] graph) {
        int[] tin = new int[n + 1];
        int[] tout = new int[n + 1];
        int[] eulerVal = new int[n + 1];

        int timer = 0;

        // 非递归 DFS
        // state = 0 表示首次到达，state = 1 表示退出节点
        int[] stackU = new int[2 * n + 5];
        int[] stackFa = new int[2 * n + 5];
        int[] stackState = new int[2 * n + 5];
        int top = 0;

        stackU[top] = 1;
        stackFa[top] = 0;
        stackState[top] = 0;
        top++;

        while (top > 0) {
            top--;
            int u = stackU[top];
            int fa = stackFa[top];
            int state = stackState[top];

            if (state == 0) {
                timer++;
                tin[u] = timer;
                eulerVal[timer] = a[u];

                // 退出节点时再处理 tout
                stackU[top] = u;
                stackFa[top] = fa;
                stackState[top] = 1;
                top++;

                // 子节点入栈
                List<Integer> list = graph[u];
                for (int i = 0; i < list.size(); i++) {
                    int v = list.get(i);
                    if (v != fa) {
                        stackU[top] = v;
                        stackFa[top] = u;
                        stackState[top] = 0;
                        top++;
                    }
                }
            } else {
                tout[u] = timer;
            }
        }

        long[] ans = new long[n + 1];
        int B = 20; // 因为 a[i] <= 10^6

        // 按位统计答案
        for (int b = 0; b < B; b++) {
            int[] pre = new int[n + 1];

            // 当前位的前缀和
            for (int i = 1; i <= n; i++) {
                pre[i] = pre[i - 1] + ((eulerVal[i] >> b) & 1);
            }

            long bitValue = 1L << b;

            // 计算每个节点子树在这一位上的贡献
            for (int u = 1; u <= n; u++) {
                int l = tin[u];
                int r = tout[u];
                int ones = pre[r] - pre[l - 1];
                int size = r - l + 1;
                int zeros = size - ones;
                ans[u] += 1L * ones * zeros * bitValue;
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);

        int n = fs.nextInt();
        int[] a = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            a[i] = fs.nextInt();
        }

        List<Integer>[] graph = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) {
            graph[i] = new ArrayList<>();
        }

        for (int i = 0; i < n - 1; i++) {
            int u = fs.nextInt();
            int v = fs.nextInt();
            graph[u].add(v);
            graph[v].add(u);
        }

        long[] ans = solve(n, a, graph);

        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append(' ');
            sb.append(ans[i]);
        }
        System.out.println(sb);
    }

    // 根据数据范围使用更稳妥的输入方式
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        FastScanner(InputStream is) {
            in = is;
        }

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
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 题面功能写在外部函数里
vector<long long> solve(int n, const vector<int>& a, const vector<vector<int>>& graph) {
    vector<int> tin(n + 1), tout(n + 1), eulerVal(n + 1);
    int timer = 0;

    // 非递归 DFS
    struct Node {
        int u, fa, state; // state: 0=首次到达, 1=退出节点
    };

    vector<Node> st;
    st.push_back({1, 0, 0});

    while (!st.empty()) {
        Node cur = st.back();
        st.pop_back();

        int u = cur.u;
        int fa = cur.fa;
        int state = cur.state;

        if (state == 0) {
            ++timer;
            tin[u] = timer;
            eulerVal[timer] = a[u];

            // 退出时处理 tout
            st.push_back({u, fa, 1});

            // 子节点入栈
            for (int v : graph[u]) {
                if (v != fa) {
                    st.push_back({v, u, 0});
                }
            }
        } else {
            tout[u] = timer;
        }
    }

    vector<long long> ans(n + 1, 0);
    const int B = 20; // 因为 a[i] <= 10^6

    // 按位统计贡献
    for (int b = 0; b < B; b++) {
        vector<int> pre(n + 1, 0);

        // 当前位的前缀和
        for (int i = 1; i <= n; i++) {
            pre[i] = pre[i - 1] + ((eulerVal[i] >> b) & 1);
        }

        long long bitValue = 1LL << b;

        // 计算每个点子树在这一位上的贡献
        for (int u = 1; u <= n; u++) {
            int l = tin[u];
            int r = tout[u];
            int ones = pre[r] - pre[l - 1];
            int size = r - l + 1;
            int zeros = size - ones;
            ans[u] += 1LL * ones * zeros * bitValue;
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    vector<vector<int>> graph(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    vector<long long> ans = solve(n, a, graph);

    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';

    return 0;
}
```