## 解题思路

* 本题属于 **图论** 中的 **有向图拓扑排序** 问题，可用 **Kahn 算法（BFS）** 解决；其本质也可视为一种“**贪心**”选择：每次都优先取当前 **入度为 0** 的课程（没有未完成的前置要求）。
* 建图方式：将依赖 `[a, b]` 视为一条 **b → a** 的有向边（先修 b，后修 a），并统计每个节点的入度。
* 算法步骤（Kahn）：

  1. 统计入度，所有入度为 0 的课程入队；
  2. 不断出队，加入答案序列，并把它指向的后继课程入度减 1；若减到 0，再入队；
  3. 最终若输出数量等于课程总数，得到一个可行顺序；否则存在环（如 `[ [2,1],[1,2] ]`），返回空数组。
* 课程编号推断：题面仅给出依赖对，样例用 0 开始编号，因此令 `n = (所有出现过的最大课程编号) + 1`。这样未在依赖中出现的编号也会被覆盖（若存在）。

## 复杂度分析

* 设课程数为 `n`，依赖数为 `m`。
* 时间复杂度：**O(n + m)**（建图与拓扑遍历各边各点各一次）。
* 空间复杂度：**O(n + m)**（邻接表与入度数组）。

## 代码实现

### Python

```python
# 功能函数：Kahn 拓扑排序；返回可行顺序，若无解返回空列表
def find_order(n, pairs):
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in pairs:  # 边 b -> a
        if 0 <= a < n and 0 <= b < n:
            g[b].append(a)
            indeg[a] += 1

    import heapq
    pq = [i for i in range(n) if indeg[i] == 0]  # 小根堆保证字典序尽量小
    heapq.heapify(pq)

    ans = []
    while pq:
        u = heapq.heappop(pq)
        ans.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(pq, v)
    return ans if len(ans) == n else []

if __name__ == "__main__":
    import sys
    from ast import literal_eval  # 比 eval 更安全
    s = sys.stdin.read().strip()
    pairs, n = literal_eval("(" + "".join(s.split()) + ")")
    ans = find_order(n, pairs)
    print("[" + ",".join(map(str, ans)) + "]")
```

### Java

```java
import java.io.*;
import java.util.*;

// 功能函数：Kahn 拓扑排序（用小根堆使输出更稳定）
class Main {
    public static int[] findOrder(int n, List<int[]> pairs) {
        List<List<Integer>> g = new ArrayList<>();
        for (int i = 0; i < n; i++) g.add(new ArrayList<>());
        int[] indeg = new int[n];

        for (int[] e : pairs) {
            int a = e[0], b = e[1]; // b -> a
            if (0 <= a && a < n && 0 <= b && b < n) {
                g.get(b).add(a);
                indeg[a]++;
            }
        }

        PriorityQueue<Integer> pq = new PriorityQueue<>();
        for (int i = 0; i < n; i++) if (indeg[i] == 0) pq.offer(i);

        int[] ans = new int[n];
        int idx = 0;
        while (!pq.isEmpty()) {
            int u = pq.poll();
            ans[idx++] = u;
            for (int v : g.get(u)) {
                if (--indeg[v] == 0) pq.offer(v);
            }
        }
        if (idx < n) return new int[0]; // 有环，无解
        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        for (String line; (line = br.readLine()) != null; ) sb.append(line).append('\n');
        String s = sb.toString().replaceAll("\\s+", "");
        // 把 [, ], , 全替换为空格，然后流式读所有整数
        s = s.replace('[', ' ').replace(']', ' ').replace(',', ' ').trim();

        List<Integer> nums = new ArrayList<>();
        // 用 Scanner/Tokenizer 读取所有整数
        try (Scanner sc = new Scanner(s)) {
            while (sc.hasNextInt()) nums.add(sc.nextInt());
        }

        int n = 0;
        List<int[]> pairs = new ArrayList<>();
        if (!nums.isEmpty()) {
            n = nums.get(nums.size() - 1);                  // 最后一个是 n
            for (int i = 0; i + 2 <= nums.size() - 1; i += 2) { // 之前的成对是依赖
                pairs.add(new int[]{nums.get(i), nums.get(i + 1)});
            }
        }

        int[] ans = findOrder(n, pairs);
        StringBuilder out = new StringBuilder();
        out.append("[");
        for (int i = 0; i < ans.length; i++) {
            if (i > 0) out.append(",");
            out.append(ans[i]);
        }
        out.append("]");
        System.out.println(out.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 功能函数：Kahn 拓扑排序（小根堆）
vector<int> findOrder(int n, const vector<pair<int,int>>& pairs) {
    vector<vector<int>> g(n);
    vector<int> indeg(n, 0);
    for (auto &e : pairs) {
        int a = e.first, b = e.second; // b -> a
        if (0 <= a && a < n && 0 <= b && b < n) {
            g[b].push_back(a);
            indeg[a]++;
        }
    }
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int i = 0; i < n; ++i) if (indeg[i] == 0) pq.push(i);

    vector<int> ans; ans.reserve(n);
    while (!pq.empty()) {
        int u = pq.top(); pq.pop();
        ans.push_back(u);
        for (int v : g[u]) {
            if (--indeg[v] == 0) pq.push(v);
        }
    }
    if ((int)ans.size() < n) return {}; // 有环，无解
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 读整段输入
    string all, line;
    while (getline(cin, line)) { all += line; all += '\n'; }

    // 把 '[', ']', ',' 全部替换成空格；然后流式读所有整数
    for (char &c : all) {
        if (c == '[' || c == ']' || c == ',') c = ' ';
    }
    stringstream ss(all);
    vector<long long> nums;
    long long x;
    while (ss >> x) nums.push_back(x);

    int n = 0;
    vector<pair<int,int>> pairs;
    if (!nums.empty()) {
        n = (int)nums.back();                       // 最后一个是 n
        for (size_t i = 0; i + 2 <= nums.size() - 1; i += 2) {
            pairs.push_back({(int)nums[i], (int)nums[i + 1]});
        }
    }

    auto ans = findOrder(n, pairs);

    cout << "[";
    for (size_t i = 0; i < ans.size(); ++i) {
        if (i) cout << ",";
        cout << ans[i];
    }
    cout << "]";
    return 0;
}
```