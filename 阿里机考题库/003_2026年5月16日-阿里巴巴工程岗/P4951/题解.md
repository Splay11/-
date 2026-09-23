## 解题思路

所求为

$$
\sum_{1\le L\le R\le m} F(L,R),
$$

其中

$$
F(L,R)=\sum_{k=L}^{R}\min(h_L,\ldots,h_k)。
$$

一项 $\min(h_L,\ldots,h_k)$ 与 $R$ 无关。固定 $L,k$ 时，$R$ 可取 $k,\ldots,m$ 共 $m-k+1$ 种，故总和等于

$$
\sum_{k=1}^{m}(m-k+1)\,G(k),
$$

其中

$$
G(k)=\sum_{L=1}^{k}\min(h_L,\ldots,h_k)。
$$

用单调栈维护 $G(k)$：

- 栈中存 $(v,c)$：表示以当前右端点结尾、最小值为 $v$ 的子段有 $c$ 个，且 $v$ 严格递增；
- 加入 $h_k$ 时，弹出所有 $v\ge h_k$ 的栈顶并合并数量；
- 动态维护当前 $G(k)$，再累加 $G(k)\times(m-k+1)$。

全程对 $1000000007$ 取模。

## 复杂度分析

每元素进出栈各至多一次，单组时间 $O(m)$，空间 $O(m)$。

全体 $\sum m \le 3\times 10^5$，可通过。

## 代码实现

### Python

```python
MOD = 10**9 + 7
q = int(input())
for _ in range(q):
    m = int(input())
    h = list(map(int, input().split()))
    st = []  # (最小值, 段数)
    cur = 0  # 当前 G(k)
    ans = 0
    for k, x in enumerate(h, 1):
        cnt = 1
        while st and st[-1][0] >= x:
            v, c = st.pop()
            cur -= v * c  # 旧最小值失效
            cnt += c
        st.append((x, cnt))
        cur += x * cnt
        cur %= MOD
        ans = (ans + cur * (m - k + 1)) % MOD
    print(ans)
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static final long MOD = 1000000007L;
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            int m = Integer.parseInt(br.readLine().trim());
            long[] h = new long[m];
            StringTokenizer stok = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) h[i] = Long.parseLong(stok.nextToken());
            ArrayDeque<long[]> st = new ArrayDeque<>(); // {v, c}
            long cur = 0, ans = 0;
            for (int k = 1; k <= m; k++) {
                long x = h[k - 1];
                long cnt = 1;
                while (!st.isEmpty() && st.peekLast()[0] >= x) {
                    long[] top = st.pollLast();
                    cur -= top[0] * top[1];
                    cnt += top[1];
                }
                st.addLast(new long[]{x, cnt});
                cur += x * cnt;
                cur %= MOD;
                if (cur < 0) cur += MOD;
                ans = (ans + cur * (m - k + 1)) % MOD;
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
    const long long MOD = 1000000007;
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<long long> h(m);
        for (int i = 0; i < m; ++i) cin >> h[i];
        vector<pair<long long, long long>> st; // (最小值, 段数)
        long long cur = 0, ans = 0;
        for (int k = 1; k <= m; ++k) {
            long long x = h[k - 1];
            long long cnt = 1;
            while (!st.empty() && st.back().first >= x) {
                cur -= st.back().first * st.back().second;
                cnt += st.back().second;
                st.pop_back();
            }
            st.push_back({x, cnt});
            cur += x * cnt;
            cur %= MOD;
            if (cur < 0) cur += MOD;
            ans = (ans + cur * (m - k + 1)) % MOD;
        }
        cout << ans << '\n';
    }
    return 0;
}
```
