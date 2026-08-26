## 解法总览

### 关键观察

若把 $b$ 定义为把 $a$ **整体向左循环平移一位**：

$$
b_i=a_{i+1}\ (1\le i < n),\qquad b_n=a_1 .
$$

对任意区间 $[l,r]$，有

$$
\sum_{i=l}^{r} b_i-\sum_{i=l}^{r} a_i
$$
$$
=\sum_{i=l}^{r} (a_{i+1}-a_i)
$$
$$
= a_{r+1}-a_l.
$$

* 当 $[l,r]=[1,n]$ 时，差为 $a_{n+1}-a_1=a_1-a_1=0$（允许相等）。
* 当 $[l,r]$ 是**真子区间**时，$r+1\notin[l,r]$。由于 $a$ 是排列，所有元素互异，故 $a_{r+1}\ne a_l$，于是
  $\sum b \ne \sum a$。

因此该 $b$ 与 $a$ 必定相似。

### 算法步骤

对每组数据：

1. 读入 $n$ 与排列 $a$；
2. 输出 $b_1=a_2, b_2=a_3, \ldots, b_{n-1}=a_n, b_n=a_1$。

### 复杂度

仅一次线性循环，时间 $O(n)$，空间 $O(1)$（除输出外）。整份数据总复杂度 $O(\sum n)$。
## 代码

### Python

```python
import sys

it = iter(sys.stdin.read().strip().split())
t = int(next(it))
out = []
for _ in range(t):
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    # 循环左移一位
    b = a[1:] + a[:1]
    out.append(" ".join(map(str, b)))
print("\n".join(out))
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        int T = Integer.parseInt(br.readLine().trim());
        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            st = new StringTokenizer(br.readLine());
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = Integer.parseInt(st.nextToken());

            // 循环左移一位：b[i] = a[i+1]，b[n-1] = a[0]
            for (int i = 0; i < n - 1; i++) {
                if (i > 0) sb.append(' ');
                sb.append(a[i + 1]);
            }
            if (n > 1) sb.append(' ');
            sb.append(a[0]);

            if (T > 0) sb.append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
// C++17，ACM风格
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; 
    if(!(cin >> T)) return 0;
    while (T--) {
        int n; cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];

        // 循环左移一位输出
        for (int i = 1; i < n; ++i) {
            if (i > 1) cout << ' ';
            cout << a[i];
        }
        if (n > 1) cout << ' ';
        cout << a[0];

        if (T) cout << '\n';
    }
    return 0;
}
```