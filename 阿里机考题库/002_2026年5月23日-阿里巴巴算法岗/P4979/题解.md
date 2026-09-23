## 解题思路

要统计满足 $1\le u\le v\le m$ 且 $x_u=y_{p_v}$ 的有序对数量。

固定右端点 $v$：此时只需知道前缀 $x_1,\dots,x_v$ 中等于 $y_{p_v}$ 的个数。从左到右枚举 $v$，先把 $x_v$ 加入哈希表，再查询 $y_{p_v}$ 的出现次数累加到答案。

注意 $p_v$ 是 $1$ 下标，代码中取 $y[p_v-1]$。

## 复杂度分析

单组长度 $m$，均摊 $O(m)$。全体 $m$ 之和不超过 $2\times 10^5$，空间 $O(m)$。

## 代码实现

### Python

```python
from collections import Counter

q = int(input())
for _ in range(q):
    m = int(input())
    x = list(map(int, input().split()))
    y = list(map(int, input().split()))
    p = list(map(int, input().split()))  # 1 下标指向 y
    freq = Counter()
    ans = 0
    for v in range(m):
        freq[x[v]] += 1  # 先纳入前缀 x_1..x_v
        ans += freq[y[p[v] - 1]]  # 统计等于 y_{p_v} 的个数
    print(ans)
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
            long[] x = new long[m], y = new long[m];
            int[] p = new int[m];
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) x[i] = Long.parseLong(st.nextToken());
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) y[i] = Long.parseLong(st.nextToken());
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) p[i] = Integer.parseInt(st.nextToken());
            HashMap<Long, Integer> freq = new HashMap<>();
            long ans = 0;
            for (int v = 0; v < m; v++) {
                freq.put(x[v], freq.getOrDefault(x[v], 0) + 1);
                ans += freq.getOrDefault(y[p[v] - 1], 0);
            }
            out.append(ans).append('\n');
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
        vector<long long> x(m), y(m);
        vector<int> p(m);
        for (int i = 0; i < m; ++i) cin >> x[i];
        for (int i = 0; i < m; ++i) cin >> y[i];
        for (int i = 0; i < m; ++i) cin >> p[i];
        unordered_map<long long, int> freq;
        freq.reserve(m * 2);
        long long ans = 0;
        for (int v = 0; v < m; ++v) {
            ++freq[x[v]]; // 前缀纳入 x_v
            ans += freq[y[p[v] - 1]]; // 累加等于 y_{p_v} 的个数
        }
        cout << ans << '\n';
    }
    return 0;
}
```
