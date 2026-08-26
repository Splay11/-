## 题解

### 题面描述

给定一个长度为 $n$ 的数组 $\{a_1, a_2, \dots, a_n\}$，定义数组的权值为数组所有元素之和。你可以执行任意次以下操作，以使数组权值最小化：

- 选择两个索引 $i$ 和 $j$；
- 任意选取两个正整数 $x$ 和 $y$，但需满足  
  $$\gcd(x, y) = \gcd(a_i, a_j);$$
- 将 $a_i \leftarrow x$，$a_j \leftarrow y$。

输出经过任意次操作后能得到的最小数组权值。

---

### 思路

1. **观察操作效果**  
   对于任意一对元素 $(a_i, a_j)$，设  
   $$g = \gcd(a_i, a_j).$$  
   则可以将它们都替换为任意两正数 $x,y$，只要  
   $$\gcd(x,y)=g.$$  
   特别地，我们可以取  
   $$x = y = g,$$  
   这样就能将 $a_i, a_j$ 同时降至 $g$。

2. **递推到全局**  
   - 先任意选择一对，将它们都降到它们的 $\gcd$；  
   - 随后再与其它元素配对，继续降到新的 $\gcd$。  
   最终，所有元素都可以降到全数组的**全局 gcd**。  

3. **答案**  
   设全局 gcd 为  
   $$g_0 = \gcd(a_1, a_2, \dots, a_n).$$  
   则最小权值为  
   $$n \times g_0.$$

## C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;  // 测试组数
    while (T--) {
        long long n;
        cin >> n;  // 数组长度
        long long g = 0;  // 用于累积 gcd
        for (int i = 0; i < n; i++) {
            long long a;
            cin >> a;
            if (i == 0) g = a;
            else g = gcd(g, a);  // 迭代求 gcd
        }
        // 最小权值 = n * 全局 gcd
        cout << g * n << "\n";
    }
    return 0;
}
```
## Python

```python
import sys
import math

def main():
    data = sys.stdin.read().split()
    T = int(data[0])  # 测试组数
    idx = 1
    out = []
    for _ in range(T):
        n = int(data[idx]); idx += 1  # 数组长度
        # 计算全局 gcd
        g = 0
        for i in range(n):
            a = int(data[idx]); idx += 1
            g = a if g == 0 else math.gcd(g, a)
        # 最小权值 = n * 全局 gcd
        out.append(str(g * n))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```
## Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine().trim());  // 测试组数
        StringBuilder sb = new StringBuilder();
        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());  // 数组长度
            StringTokenizer st = new StringTokenizer(br.readLine());
            long g = 0;  // 全局 gcd
            for (int i = 0; i < n; i++) {
                long a = Long.parseLong(st.nextToken());
                if (i == 0) g = a;
                else g = gcd(g, a);  // 迭代求 gcd
            }
            // 最小权值 = n * 全局 gcd
            sb.append(g * n).append("\n");
        }
        System.out.print(sb);
    }

    // 计算两个数的 gcd
    private static long gcd(long a, long b) {
        return b == 0 ? a : gcd(b, a % b);
    }
}
```