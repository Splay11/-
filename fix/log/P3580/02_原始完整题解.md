## 题解

由于每次操作都是**基于原始数组**，且只需要判断总和的**奇偶性**，因此不必真正修改数组。

### 1. 预处理

首先计算原始数组的总和：

$S = \sum_{i=1}^{n} a_i$

同时使用前缀和（prefix sum）数组快速求原始某一段区间 $[l,r]$ 的和：

$\text{sum}_{l,r} = \text{pre}[r] - \text{pre}[l-1]$

### 2. 操作后区间和的计算

区间 $[l,r]$ 的长度：

$m = r - l + 1$

根据规则，新区间的值是**交替序列**：

* 偶数位置（从 $l$ 开始计）：值为 $k$
* 奇数位置：值为 $k + 1$

偶数位置个数：

$\text{cnt}_k$ = $\left\lceil \frac{m}{2} \right\rceil$

奇数位置个数：

$\text{cnt}_{k+1}$ = $\left\lfloor \frac{m}{2} \right\rfloor$

因此新区间的和为：

$\text{new\_sum}$ = $\text{cnt}_k \cdot k$ + $\text{cnt}_{k+1} \cdot (k+1)$

### 3. 总和更新及奇偶判断

原数组换成新数组后，全局总和为：

$S'$ = $S$ - $\text{sum}_{l,r}$ + $\text{new\_sum}$

我们只需判断 $S'$ 的奇偶性，若为奇数输出 `"YES"`，否则 `"NO"`。

这种做法保证了**每次询问 O(1)** 复杂度，通过前缀和数组实现。

---

## **复杂度分析**

* 前缀和预处理： $O(n)$
* 每次查询： $O(1)$
* 总复杂度： $O(n + q)$

由于 $\sum n$ 和 $\sum q$ 都不超过 $2\times 10^5$，本方法足够快速。

---

## C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n, q;
        cin >> n >> q;
        vector<long long> a(n + 1), pre(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            cin >> a[i];
            pre[i] = pre[i - 1] + a[i]; // 前缀和
        }
        long long total_sum = pre[n]; // 原数组总和
        while (q--) {
            int l, r;
            long long k;
            cin >> l >> r >> k;
            long long seg_sum = pre[r] - pre[l - 1]; // 原区间和
            long long len = r - l + 1;
            long long cnt_k = (len + 1) / 2; // k 出现次数
            long long cnt_k1 = len / 2;      // k+1 出现次数
            long long new_sum = cnt_k * k + cnt_k1 * (k + 1);
            long long new_total = total_sum - seg_sum + new_sum;
            if (new_total % 2 == 1)
                cout << "YES\n";
            else
                cout << "NO\n";
        }
    }
    return 0;
}
```

## Python 

```python
import sys
input = sys.stdin.read

data = input().split()
t = int(data[0])
idx = 1
out = []

for _ in range(t):
    n = int(data[idx]); idx += 1
    q = int(data[idx]); idx += 1
    a = [0] + list(map(int, data[idx: idx + n])); idx += n
    pre = [0] * (n + 1)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] + a[i]  # 前缀和
    total_sum = pre[n]

    for __ in range(q):
        l = int(data[idx]); idx += 1
        r = int(data[idx]); idx += 1
        k = int(data[idx]); idx += 1
        seg_sum = pre[r] - pre[l - 1]
        length = r - l + 1
        cnt_k = (length + 1) // 2
        cnt_k1 = length // 2
        new_sum = cnt_k * k + cnt_k1 * (k + 1)
        new_total = total_sum - seg_sum + new_sum
        if new_total % 2 == 1:
            out.append("YES")
        else:
            out.append("NO")

print("\n".join(out))
```
## *ava 

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;
        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());
            int q = Integer.parseInt(st.nextToken());
            long[] a = new long[n + 1];
            long[] pre = new long[n + 1];
            st = new StringTokenizer(br.readLine());
            for (int i = 1; i <= n; i++) {
                a[i] = Long.parseLong(st.nextToken());
                pre[i] = pre[i - 1] + a[i]; // 前缀和
            }
            long total_sum = pre[n];
            for (int i = 0; i < q; i++) {
                st = new StringTokenizer(br.readLine());
                int l = Integer.parseInt(st.nextToken());
                int r = Integer.parseInt(st.nextToken());
                long k = Long.parseLong(st.nextToken());
                long seg_sum = pre[r] - pre[l - 1];
                long len = r - l + 1;
                long cnt_k = (len + 1) / 2; // k 出现的个数
                long cnt_k1 = len / 2;      // k+1 出现的个数
                long new_sum = cnt_k * k + cnt_k1 * (k + 1);
                long new_total = total_sum - seg_sum + new_sum;
                if (new_total % 2 == 1)
                    sb.append("YES\n");
                else
                    sb.append("NO\n");
            }
        }
        System.out.print(sb.toString());
    }
}
```