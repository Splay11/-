## 题目理解与建模

给一棵共有 `n` 个结点的树，每个结点初始标签为 `d / p / ?`。
一次操作可以把任意结点的标签改为 `d` 或 `p`，每次改动计 1 次。
目标：通过最少的重绘，使

1. 所有结点最终均为 `d` 或 `p`；
2. 每条边两端标签不同（相邻异色）。
   输出最少需要的重绘次数。

> 说明：初始为 `?` 的结点也必须被涂成 `d/p`，因此无论最终选哪种颜色，它都需要 **1 次**重绘。

## 算法与思路

### 关键观察（树 = 二分图）

树一定是二分图。任选根，把结点按深度奇偶分成两侧（记为 `A` 与 `B`）：

* 合法的最终染色只有两种：
  ① `A→d, B→p`；② `A→p, B→d`（两侧整体对调）。
* 初始为 `?` 的结点必重绘 1 次，与选择无关，记总数为 `cntQ`。
* 对于非 `?` 结点，若它所在侧的目标色与其初始色一致，则不用重绘，否则要重绘 1 次。

于是问题变为：在两种方案中选择更少的“与目标侧不一致”的个数。

### 具体做法（BFS/DFS 分层 + 计数）

1. 用 BFS/DFS 把树按深度奇偶分为两侧，记每个结点的奇偶 `par[i]∈{0,1}`。
2. 统计四个数量：
   `c0d`：偶层上初始为 `d` 的个数；
   `c0p`：偶层上初始为 `p` 的个数；
   `c1d`：奇层上初始为 `d` 的个数；
   `c1p`：奇层上初始为 `p` 的个数；
   以及 `cntQ`：全图 `?` 的个数。
3. 两种方案的总代价：

   * 方案A（偶层 `d`，奇层 `p`）：`costA = cntQ + c0p + c1d`
   * 方案B（偶层 `p`，奇层 `d`）：`costB = cntQ + c0d + c1p`
4. 答案为 `min(costA, costB)`。

### 正确性说明（简要）

树的二分划分唯一（除了对调两侧）。任意满足相邻异色的最终染色必与上述两种之一同构，因此最优解必在两者中产生。对每个非 `?` 结点，是否需要重绘只取决于其所在侧的目标色是否匹配；对 `?` 结点必需 1 次。故上述计数即为最小重绘数。

## 复杂度分析

* 建图与 BFS/DFS：`O(n)`
* 计数与比较：`O(n)`
* 总时间：`O(n)`；空间：`O(n)`（邻接表与队列/栈）。

## 代码实现

### Python

```python
# 最少重绘使树相邻异色
# 思路：BFS分层 + 计数两种方案的代价
import sys
from collections import deque

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    s = list(next(it).strip())  # 长度为 n，只含 d/p/?
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it)); v = int(next(it))
        g[u].append(v); g[v].append(u)

    # BFS 求每个点的深度奇偶（0: 偶层，1: 奇层）
    par = [-1] * (n + 1)
    q = deque([1])
    par[1] = 0

    # 计数
    c0d = c0p = c1d = c1p = 0
    cntQ = 0

    while q:
        u = q.popleft()
        ch = s[u - 1]
        if ch == '?':
            cntQ += 1
        elif ch == 'd':
            if par[u] == 0: c0d += 1
            else: c1d += 1
        else:  # ch == 'p'
            if par[u] == 0: c0p += 1
            else: c1p += 1

        for v in g[u]:
            if par[v] == -1:
                par[v] = par[u] ^ 1
                q.append(v)

    # 两种方案取较小
    costA = cntQ + c0p + c1d  # 偶层d，奇层p
    costB = cntQ + c0d + c1p  # 偶层p，奇层d
    print(min(costA, costB))

if __name__ == "__main__":
    solve()
```

### Java

```java
// 最少重绘使树相邻异色
// 思路：BFS分层 + 统计两侧 d/p 个数，比较两种方案
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        String s = sc.next();
        List<Integer>[] g = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) g[i] = new ArrayList<>();
        for (int i = 0; i < n - 1; i++) {
            int u = sc.nextInt(), v = sc.nextInt();
            g[u].add(v); g[v].add(u);
        }

        int[] par = new int[n + 1];
        Arrays.fill(par, -1);
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(1); par[1] = 0;

        long c0d = 0, c0p = 0, c1d = 0, c1p = 0, cntQ = 0;

        while (!q.isEmpty()) {
            int u = q.poll();
            char ch = s.charAt(u - 1);
            if (ch == '?') cntQ++;
            else if (ch == 'd') {
                if (par[u] == 0) c0d++; else c1d++;
            } else { // 'p'
                if (par[u] == 0) c0p++; else c1p++;
            }
            for (int v : g[u]) if (par[v] == -1) {
                par[v] = par[u] ^ 1;
                q.add(v);
            }
        }

        long costA = cntQ + c0p + c1d; // 偶层d，奇层p
        long costB = cntQ + c0d + c1p; // 偶层p，奇层d
        System.out.println(Math.min(costA, costB));
    }
}
```

### C++

```cpp
// 最少重绘使树相邻异色
// 思路：BFS分层 + 计数两种方案的代价
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    string s; cin >> s;

    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<int> par(n + 1, -1);
    queue<int> q;
    par[1] = 0; q.push(1);

    long long c0d = 0, c0p = 0, c1d = 0, c1p = 0, cntQ = 0;

    while (!q.empty()) {
        int u = q.front(); q.pop();
        char ch = s[u - 1];
        if (ch == '?') ++cntQ;
        else if (ch == 'd') {
            if (par[u] == 0) ++c0d; else ++c1d;
        } else { // 'p'
            if (par[u] == 0) ++c0p; else ++c1p;
        }
        for (int v : g[u]) if (par[v] == -1) {
            par[v] = par[u] ^ 1;
            q.push(v);
        }
    }

    long long costA = cntQ + c0p + c1d; // 偶层d，奇层p
    long long costB = cntQ + c0d + c1p; // 偶层p，奇层d
    cout << min(costA, costB) << '\n';
    return 0;
}
```