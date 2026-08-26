## 解题思路

* 核心观察
  树是二分图，把树按根 1 做 BFS/DFS，按层数奇偶划分为两部分（偶层集合 A、奇层集合 B）。由于相邻点层数相反，天然满足 A—B 之间的边相连。

* 为什么只用 1 和 2 就够了
  题目给出上界 $m\ge 2$。对任意节点，只需与父节点不同即可；若父为 1，则该点取 2；否则取 1。使用更大的数不会更优（只会让总和更大），因此最优解一定只使用 $\{1,2\}$。

* 如何最小化总和
  给定二分划分 $(A,B)$，两种赋值：

  * A 取 1、B 取 2，总和为 $|A|+2|B|=n+|B|$；
  * A 取 2、B 取 1，总和为 $2|A|+|B|=n+|A|$。
    取两者较小，即把数值 1 分给规模较大的那一侧。故答案为

  $$
  \text{ans}= n + \min(|A|,|B|).
  $$

* 实现方法
  用 BFS（或 DFS）从 1 号点出发，统计偶层个数 $cnt0$ 与奇层个数 $cnt1$。输出 $n+\min(cnt0,cnt1)$。
  算法步骤：
  . 建图（邻接表）。
  2\. BFS 标记每点层数奇偶并计数。
  3\. 输出 $n+\min(cnt0,cnt1)$。

## 复杂度分析

* 时间复杂度：每条边、每个点各访问一次，$O(n)$。
* 空间复杂度：邻接表与队列、标记数组，$O(n)$。

## 代码实现

### Python

```python
import sys
from collections import deque

# 外部函数：计算最小和
def solve_one(n, edges):
    # 建图
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    # BFS 分层计数
    vis = [False] * (n + 1)
    depth_parity = [0] * (n + 1)
    cnt0, cnt1 = 0, 0
    q = deque()
    q.append(1)
    vis[1] = True
    depth_parity[1] = 0  # 根置为偶层
    cnt0 += 1
    while q:
        u = q.popleft()
        for v in g[u]:
            if not vis[v]:
                vis[v] = True
                depth_parity[v] = depth_parity[u] ^ 1  # 奇偶翻转
                if depth_parity[v] == 0:
                    cnt0 += 1
                else:
                    cnt1 += 1
                q.append(v)
    return n + min(cnt0, cnt1)

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    T = next(it)
    out_lines = []
    for _ in range(T):
        n = next(it); m = next(it)  # m≥2，结论只需{1,2}，无需额外判断
        edges = []
        for _ in range(n - 1):
            u = next(it); v = next(it)
            edges.append((u, v))
        out_lines.append(str(solve_one(n, edges)))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

// 类名统一为 Main（ACM 风格）
public class Main {

    // 外部函数：计算最小和
    static long solveOne(int n, List<int[]> edges) {
        // 建图（邻接表）
        ArrayList<Integer>[] g = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) g[i] = new ArrayList<>();
        for (int[] e : edges) {
            int u = e[0], v = e[1];
            g[u].add(v);
            g[v].add(u);
        }
        // BFS 分层计数
        boolean[] vis = new boolean[n + 1];
        int[] parity = new int[n + 1]; // 0 表示偶层, 1 表示奇层
        long cnt0 = 0, cnt1 = 0;

        Deque<Integer> q = new ArrayDeque<>();
        q.add(1);
        vis[1] = true;
        parity[1] = 0;
        cnt0++;

        while (!q.isEmpty()) {
            int u = q.pollFirst();
            for (int v : g[u]) {
                if (!vis[v]) {
                    vis[v] = true;
                    parity[v] = parity[u] ^ 1; // 层数奇偶翻转
                    if (parity[v] == 0) cnt0++; else cnt1++;
                    q.addLast(v);
                }
            }
        }
        return n + Math.min(cnt0, cnt1);
    }

    // 主函数：读取输入和输出
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder out = new StringBuilder();
        String line = br.readLine();
        int T = Integer.parseInt(line.trim());
        for (int tc = 0; tc < T; tc++) {
            // 读取 n, m
            String[] p;
            do { line = br.readLine(); } while (line != null && line.trim().isEmpty());
            p = line.trim().split("\\s+");
            int n = Integer.parseInt(p[0]);
            int m = Integer.parseInt(p[1]); // m≥2，不必特殊处理
            List<int[]> edges = new ArrayList<>();
            for (int i = 0; i < n - 1; i++) {
                line = br.readLine();
                while (line != null && line.trim().isEmpty()) line = br.readLine();
                String[] ab = line.trim().split("\\s+");
                int u = Integer.parseInt(ab[0]);
                int v = Integer.parseInt(ab[1]);
                edges.add(new int[]{u, v});
            }
            long ans = solveOne(n, edges);
            out.append(ans).append('\n');
        }
        System.out.print(out.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 外部函数：计算最小和
long long solve_one(int n, const vector<pair<int,int>>& edges) {
    // 建图（邻接表）
    vector<vector<int>> g(n + 1);
    for (auto &e : edges) {
        int u = e.first, v = e.second;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    // BFS 分层计数
    vector<char> vis(n + 1, 0);
    vector<int> parity(n + 1, 0); // 0 偶层, 1 奇层
    long long cnt0 = 0, cnt1 = 0;
    queue<int> q;
    q.push(1);
    vis[1] = 1;
    parity[1] = 0;
    cnt0++;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : g[u]) {
            if (!vis[v]) {
                vis[v] = 1;
                parity[v] = parity[u] ^ 1; // 奇偶翻转
                if (parity[v] == 0) cnt0++; else cnt1++;
                q.push(v);
            }
        }
    }
    return n + min(cnt0, cnt1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; long long m;
        cin >> n >> m; // m≥2，无需额外处理
        vector<pair<int,int>> edges;
        edges.reserve(n - 1);
        for (int i = 0; i < n - 1; ++i) {
            int u, v;
            cin >> u >> v;
            edges.emplace_back(u, v);
        }
        cout << solve_one(n, edges) << "\n";
    }
    return 0;
}
```