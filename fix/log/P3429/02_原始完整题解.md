## 题解思路
- 设 $a_i = x \cdot c_i $，则条件转化为：
  - $\forall i \neq j,$ $\text{lcm}(c_i, c_j)$ = $\text{lcm}(i, j) $
  - $\forall i, c_i \neq i $


- 通过分析质因数指数发现：当 $n \geq 3 $ 时，必须满足 $c_i = i $ 对所有 $i $ 成立（否则存在矛盾），但这违反了 $c_i \neq i $ 的要求。因此，**当 $n \geq 3 $ 时无解**。
- 当 $n = 2 $ 时，可以构造 $c_1 = 2, c_2 = 1 $（或交换），即 $a_1 = 2x, a_2 = x $，此时满足：
  - $\text{lcm}(a_1, a_2)$ = $\text{lcm}(2x, x)$ $= 2x =$ $\text{lcm}(1,2) \times x $
  - $a_1 \neq 1 \cdot x $, $a_2 \neq 2 \cdot x $

## 结论
- 若 $n \geq 3 $，输出 "No"。
- 若 $n = 2 $，输出 "Yes"，然后输出 $2x $ 和 $x $（或 $x $ 和 $2x $，但注意必须满足 $a_i \neq i \cdot x $）。


## 代码

### Python 3

```python
# 读入
import sys
n, x = map(int, sys.stdin.readline().split())

if n == 2:
    # 构造解：a1=2x, a2=x
    print("Yes")
    print(2 * x, x)
else:
    print("No")
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n, x;        // 2*x ≤ 2e18 < 9e18，long long 足够
    if (!(cin >> n >> x)) return 0;
    if (n == 2) {
        cout << "Yes\n" << 2 * x << ' ' << x << '\n';
    } else {
        cout << "No\n";
    }
    return 0;
}
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        long n = Long.parseLong(st.nextToken());
        long x = Long.parseLong(st.nextToken());
        if (n == 2) {
            System.out.println("Yes");
            System.out.println((2 * x) + " " + x);
        } else {
            System.out.println("No");
        }
    }
}
```