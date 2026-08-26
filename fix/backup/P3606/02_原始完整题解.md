## 思路分析

题目要求在树上进行**一次或多次结点扩展**（每个结点最多扩展一次），以尽量增加某一层的宽度。宽度的定义是某一深度层上的结点数。

核心观察：

1. **层数统计**：用 BFS（或 DFS）可以求出每一层的结点集合及其扩展代价。
2. **扩展策略**：扩展某层的结点，只会在该层下一层新增结点，从而可能提高下一层的宽度。
3. **资源限制**：总魔力值 `k`，扩展代价不同，等价于一个“0-1 背包”优化，但因为每层独立计算，只需要对每层进行“贪心”。

   * 每层节点扩展能增加下一层结点数。
   * 按代价排序，优先选择代价小的结点扩展，直到不能扩展为止。

算法步骤：

1. BFS 求每层的结点及其扩展代价。
2. 对每一层：

   * 原始宽度 = 该层结点数。
   * 下一层宽度 = 下一层原始结点数 + 可以扩展的结点数（受限于 `k`）。
   * 用贪心（对扩展代价排序，依次加，直到超过 `k`）。
3. 取所有层次中最大的宽度。

## 复杂度分析

* BFS 求层数：`O(n)`。
* 每层排序：所有结点总和 `O(n log n)`。
* 总体复杂度：`O(n log n)`，可以通过，因为 `∑n ≤ 10^6`。


## Python

```python
import sys
from collections import deque

input = sys.stdin.readline

def func():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # BFS 计算每层结点
    q = deque([(0, 0)])
    vis = [False] * n
    vis[0] = True
    layers = [[] for _ in range(n + 1)]
    layers[0].append(a[0])

    while q:
        u, d = q.popleft()
        for v in g[u]:
            if not vis[v]:
                vis[v] = True
                q.append((v, d + 1))
                layers[d + 1].append(a[v])

    ans = 0
    for i in range(n):
        if not layers[i]:
            continue
        base = len(layers[i])
        extra = 0
        cost = sorted(layers[i])
        s = k
        for c in cost:
            if s >= c:
                s -= c
                extra += 1
            else:
                break
        ans = max(ans, base, len(layers[i + 1]) + extra)

    print(ans)


if __name__ == "__main__":
    T = int(input())
    for _ in range(T):
        func()
```


## C++

```cpp
#include <bits/stdc++.h>
using namespace std;

void func() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    vector<vector<int>> g(n);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        u--, v--;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<vector<int>> layer(n + 1);
    queue<pair<int, int>> q;
    vector<bool> vis(n, false);
    q.push({0, 0});
    vis[0] = true;
    layer[0].push_back(a[0]);

    while (!q.empty()) {
        auto [u, d] = q.front();
        q.pop();
        for (auto v : g[u]) {
            if (!vis[v]) {
                vis[v] = true;
                q.push({v, d + 1});
                layer[d + 1].push_back(a[v]);
            }
        }
    }

    int ans = 0;
    for (int i = 0; i < n; i++) {
        if (layer[i].empty()) continue;
        int base = layer[i].size();
        int extra = 0, s = k;
        sort(layer[i].begin(), layer[i].end());
        for (auto c : layer[i]) {
            if (s >= c) {
                s -= c;
                extra++;
            } else break;
        }
        ans = max(ans, max(base, (int)layer[i + 1].size() + extra));
    }
    cout << ans << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int T;
    cin >> T;
    while (T--) func();
    return 0;
}
```


## Java

```java
import java.util.*;

public class Main {
    static void func(Scanner sc) {
        int n = sc.nextInt(), k = sc.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = sc.nextInt();

        List<List<Integer>> g = new ArrayList<>();
        for (int i = 0; i < n; i++) g.add(new ArrayList<>());
        for (int i = 0; i < n - 1; i++) {
            int u = sc.nextInt() - 1, v = sc.nextInt() - 1;
            g.get(u).add(v);
            g.get(v).add(u);
        }

        List<List<Integer>> layer = new ArrayList<>();
        for (int i = 0; i <= n; i++) layer.add(new ArrayList<>());
        Queue<int[]> q = new LinkedList<>();
        boolean[] vis = new boolean[n];
        q.add(new int[]{0, 0});
        vis[0] = true;
        layer.get(0).add(a[0]);

        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int u = cur[0], d = cur[1];
            for (int v : g.get(u)) {
                if (!vis[v]) {
                    vis[v] = true;
                    q.add(new int[]{v, d + 1});
                    layer.get(d + 1).add(a[v]);
                }
            }
        }

        int ans = 0;
        for (int i = 0; i < n; i++) {
            if (layer.get(i).isEmpty()) continue;
            int base = layer.get(i).size();
            List<Integer> costs = layer.get(i);
            Collections.sort(costs);
            int s = k, extra = 0;
            for (int c : costs) {
                if (s >= c) {
                    s -= c;
                    extra++;
                } else break;
            }
            ans = Math.max(ans, Math.max(base, layer.get(i + 1).size() + extra));
        }
        System.out.println(ans);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        while (T-- > 0) func(sc);
    }
}
```