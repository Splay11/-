## 解题思路

把每个站点看成点。从 $i$ 有两种边：

- 传送：$i\to g_i$，权为 $0$；
- 右移：若 $i<m$，则 $i\to i+1$，权为 $1$。

问题转化为求 $1$ 到 $m$ 的最短路。

边权只有 $0/1$，使用 $0$-$1$ BFS：

- 双端队列维护待扩展点；
- 走 $0$ 边时加入队首；
- 走 $1$ 边时加入队尾。

最终 $dis[m]$ 即为答案。

## 复杂度分析

每点边数常数，单组时间 $O(m)$，空间 $O(m)$。

全体 $\sum m \le 5\times 10^5$，可通过。

## 代码实现

### Python

```python
from collections import deque

q = int(input())
for _ in range(q):
    m = int(input())
    g = [0] + list(map(int, input().split()))  # g[i] 为站点 i 的传送目标
    INF = 10**18
    dis = [INF] * (m + 1)
    dis[1] = 0
    dq = deque([1])
    while dq:
        x = dq.popleft()
        y = g[x]
        if dis[y] > dis[x]:  # 花费 0 的传送
            dis[y] = dis[x]
            dq.appendleft(y)
        if x < m and dis[x + 1] > dis[x] + 1:  # 花费 1 的右移
            dis[x + 1] = dis[x] + 1
            dq.append(x + 1)
    print(dis[m])
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            int m = Integer.parseInt(br.readLine().trim());
            int[] g = new int[m + 1];
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int i = 1; i <= m; i++) g[i] = Integer.parseInt(st.nextToken());
            long[] dis = new long[m + 1];
            Arrays.fill(dis, (long) 1e18);
            dis[1] = 0;
            ArrayDeque<Integer> dq = new ArrayDeque<>();
            dq.add(1);
            while (!dq.isEmpty()) {
                int x = dq.pollFirst();
                int y = g[x];
                if (dis[y] > dis[x]) { // 传送
                    dis[y] = dis[x];
                    dq.addFirst(y);
                }
                if (x < m && dis[x + 1] > dis[x] + 1) { // 右移
                    dis[x + 1] = dis[x] + 1;
                    dq.addLast(x + 1);
                }
            }
            out.append(dis[m]).append('\n');
        }
        System.out.print(out);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<int> g(m + 1);
        for (int i = 1; i <= m; ++i) cin >> g[i];
        const long long INF = 1e18;
        vector<long long> dis(m + 1, INF);
        dis[1] = 0;
        deque<int> dq;
        dq.push_back(1);
        while (!dq.empty()) {
            int x = dq.front();
            dq.pop_front();
            int y = g[x];
            if (dis[y] > dis[x]) { // 传送花费 0
                dis[y] = dis[x];
                dq.push_front(y);
            }
            if (x < m && dis[x + 1] > dis[x] + 1) { // 右移花费 1
                dis[x + 1] = dis[x] + 1;
                dq.push_back(x + 1);
            }
        }
        cout << dis[m] << '\n';
    }
    return 0;
}
```
