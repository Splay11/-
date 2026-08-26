## 解题思路

对每个可能成为等距峰点的下标 $p$（$1 < p < m$），需要左侧区间最大值里距 $p$ 最近的位置 $u$，以及右侧同理的位置 $v$，判断是否 $p-u=v-p$。

从左到右扫一遍：维护当前前缀最大值及其最靠右下标，即可得到每个 $p$ 的 $u$（记为 $L_p$）。

从右到左扫一遍：维护当前后缀最大值及其最靠左下标，即可得到每个 $p$ 的 $v$（记为 $R_p$）。

统计满足 $p-L_p=R_p-p$ 的中间下标个数即可。首尾没有双侧，不参与统计。

## 复杂度分析

每组对长度为 $m$ 的序列各扫两遍，时间 $O(m)$，空间 $O(m)$。全体 $m$ 之和不超过 $2\times 10^5$，可通过。

## 代码实现

### Python

```python
q = int(input())
for _ in range(q):
    m = int(input())
    h = list(map(int, input().split()))  # 温感读数序列
    L = [0] * m
    R = [0] * m
    mx, pos = -1, -1
    # 左扫：L[p] = 左侧最大值中距 p 最近（最右）的下标
    for i in range(m):
        L[i] = pos
        if h[i] > mx:
            mx, pos = h[i], i
        elif h[i] == mx:
            pos = i
    mx, pos = -1, -1
    # 右扫：R[p] = 右侧最大值中距 p 最近（最左）的下标
    for i in range(m - 1, -1, -1):
        R[i] = pos
        if h[i] > mx:
            mx, pos = h[i], i
        elif h[i] == mx:
            pos = i
    ans = 0
    for p in range(1, m - 1):
        if p - L[p] == R[p] - p:  # 等距峰点
            ans += 1
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
            long[] h = new long[m];
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) h[i] = Long.parseLong(st.nextToken());
            int[] L = new int[m], R = new int[m];
            long mx = -1;
            int pos = -1;
            // 左扫求每个位置左侧最近峰值下标
            for (int i = 0; i < m; i++) {
                L[i] = pos;
                if (h[i] > mx) { mx = h[i]; pos = i; }
                else if (h[i] == mx) pos = i;
            }
            mx = -1; pos = -1;
            // 右扫求每个位置右侧最近峰值下标
            for (int i = m - 1; i >= 0; i--) {
                R[i] = pos;
                if (h[i] > mx) { mx = h[i]; pos = i; }
                else if (h[i] == mx) pos = i;
            }
            int ans = 0;
            for (int p = 1; p + 1 < m; p++) {
                if (p - L[p] == R[p] - p) ans++;
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
        vector<long long> h(m);
        for (int i = 0; i < m; ++i) cin >> h[i];
        vector<int> L(m), R(m);
        long long mx = -1;
        int pos = -1;
        // 左扫：左侧最大值最近下标
        for (int i = 0; i < m; ++i) {
            L[i] = pos;
            if (h[i] > mx) { mx = h[i]; pos = i; }
            else if (h[i] == mx) pos = i;
        }
        mx = -1; pos = -1;
        // 右扫：右侧最大值最近下标
        for (int i = m - 1; i >= 0; --i) {
            R[i] = pos;
            if (h[i] > mx) { mx = h[i]; pos = i; }
            else if (h[i] == mx) pos = i;
        }
        int ans = 0;
        for (int p = 1; p + 1 < m; ++p)
            if (p - L[p] == R[p] - p) ++ans; // 等距峰点
        cout << ans << '\n';
    }
    return 0;
}
```
