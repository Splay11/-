## 解题思路

两次摘取按顺序执行，第一次选定的行/列会立刻清零，因此分类如下：

1. 两次都选行：等价于取两个不同行的行和之和；若两次选同一行，第二次为 $0$，故也要考虑只取最大行和。  
2. 两次都选列：同理。  
3. 一行一列：设选第 $i$ 行与第 $j$ 列，收益为行和 $+$ 列和 $- G_{i,j}$（交点只应计入一次）。

先算所有行和、列和，再取上述三类的最大值。

## 复杂度分析

设表为 $h\times w$，时间 $O(hw)$，空间 $O(hw)$。全体格子数合计不超过 $5\times 10^5$，可通过。

## 代码实现

### Python

```python
q = int(input())
for _ in range(q):
    h, w = map(int, input().split())
    G = []
    rs = [0] * h  # 行和
    cs = [0] * w  # 列和
    for i in range(h):
        row = list(map(int, input().split()))
        G.append(row)
        for j in range(w):
            rs[i] += row[j]
            cs[j] += row[j]
    ans = max(rs + cs)  # 同一条线摘两次 = 只取一次
    if h >= 2:
        a = b = -(10**30)
        for v in rs:
            if v >= a: b, a = a, v
            elif v > b: b = v
        ans = max(ans, a + b)  # 两行
    if w >= 2:
        a = b = -(10**30)
        for v in cs:
            if v >= a: b, a = a, v
            elif v > b: b = v
        ans = max(ans, a + b)  # 两列
    for i in range(h):
        for j in range(w):
            # 一行一列：扣掉交点重复
            ans = max(ans, rs[i] + cs[j] - G[i][j])
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
            StringTokenizer st = new StringTokenizer(br.readLine());
            int h = Integer.parseInt(st.nextToken());
            int w = Integer.parseInt(st.nextToken());
            long[][] G = new long[h][w];
            long[] rs = new long[h], cs = new long[w];
            for (int i = 0; i < h; i++) {
                st = new StringTokenizer(br.readLine());
                for (int j = 0; j < w; j++) {
                    G[i][j] = Long.parseLong(st.nextToken());
                    rs[i] += G[i][j];
                    cs[j] += G[i][j];
                }
            }
            long ans = Long.MIN_VALUE;
            for (long v : rs) ans = Math.max(ans, v);
            for (long v : cs) ans = Math.max(ans, v);
            if (h >= 2) {
                long a = Long.MIN_VALUE, b = Long.MIN_VALUE;
                for (long v : rs) {
                    if (v >= a) { b = a; a = v; }
                    else if (v > b) b = v;
                }
                ans = Math.max(ans, a + b);
            }
            if (w >= 2) {
                long a = Long.MIN_VALUE, b = Long.MIN_VALUE;
                for (long v : cs) {
                    if (v >= a) { b = a; a = v; }
                    else if (v > b) b = v;
                }
                ans = Math.max(ans, a + b);
            }
            for (int i = 0; i < h; i++)
                for (int j = 0; j < w; j++)
                    ans = Math.max(ans, rs[i] + cs[j] - G[i][j]);
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
        int h, w;
        cin >> h >> w;
        vector<vector<long long>> G(h, vector<long long>(w));
        vector<long long> rs(h, 0), cs(w, 0); // 行和、列和
        for (int i = 0; i < h; ++i)
            for (int j = 0; j < w; ++j) {
                cin >> G[i][j];
                rs[i] += G[i][j];
                cs[j] += G[i][j];
            }
        long long ans = LLONG_MIN;
        for (long long v : rs) ans = max(ans, v); // 同线摘两次
        for (long long v : cs) ans = max(ans, v);
        if (h >= 2) {
            long long a = LLONG_MIN, b = LLONG_MIN;
            for (long long v : rs) {
                if (v >= a) { b = a; a = v; }
                else if (v > b) b = v;
            }
            ans = max(ans, a + b);
        }
        if (w >= 2) {
            long long a = LLONG_MIN, b = LLONG_MIN;
            for (long long v : cs) {
                if (v >= a) { b = a; a = v; }
                else if (v > b) b = v;
            }
            ans = max(ans, a + b);
        }
        for (int i = 0; i < h; ++i)
            for (int j = 0; j < w; ++j)
                ans = max(ans, rs[i] + cs[j] - G[i][j]); // 一行一列扣交点
        cout << ans << '\n';
    }
    return 0;
}
```
