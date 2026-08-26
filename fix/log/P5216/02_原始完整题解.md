# 最小对冲值

## 解题思路

本题考查**位运算恒等式**与对「拆分后异或」的一次观察，不必对每个 $m$ 枚举 $y$。

1. 设 $a=y$，$b=m-y$，则 $a+b=m$，且目标为
   $$\min_{0\le a\le m}(a\oplus b)$$
2. 利用恒等式
   $$a+b=(a\oplus b)+2(a\land b)$$
   可得
   $$a\oplus b=m-2(a\land b)$$
   因此最小化异或等价于最大化 $a\land (m-a)$。
3. 取 $a=\lfloor m/2\rfloor$（即尽量均分）时，$a\land (m-a)$ 达到最大。于是答案为
   $$\lfloor m/2\rfloor\oplus\lceil m/2\rceil=\lfloor m/2\rfloor\oplus\lfloor(m+1)/2\rfloor$$
4. 特例：当 $m$ 为偶数时，$\lfloor m/2\rfloor=\lceil m/2\rceil$，答案恒为 $0$；当 $m=2^k-1$（二进制全 $1$）时，任意拆分都有 $a\land b=0$，答案为 $m$ 本身。

常见假解：

- 对每个 $m$ 暴力枚举 $y$（$m\le 10^{18}$ 直接超时）；
- 误以为答案恒为 $m$ 的最低位 $m\&-m$（对 $m=11$ 会得到 $1$，正确为 $3$）；
- 只处理偶数得 $0$，奇数直接输出 $1$（漏掉 $m=7,11$ 等更大答案）；
- 用 $32$ 位整数读 $m$（$m$ 可达 $10^{18}$）。

## 复杂度分析

- 时间复杂度：$O(n)$，每个额度 $O(1)$ 计算。
- 空间复杂度：$O(1)$ 额外空间。

## 代码实现

### Python

```python
def min_hedge(m: int) -> int:
    # 均分后异或即为最小对冲值
    return (m // 2) ^ ((m + 1) // 2)


def main() -> None:
    n = int(input())
    for _ in range(n):
        m = int(input())
        print(min_hedge(m))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;

public class Main {
    // 均分后异或即为最小对冲值
    static long minHedge(long m) {
        return (m / 2) ^ ((m + 1) / 2); // 必须用 64 位读 m
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            long m = Long.parseLong(br.readLine().trim());
            sb.append(minHedge(m)).append('\n');
        }
        System.out.print(sb);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

// 均分后异或即为最小对冲值
int64 min_hedge(int64 m) {
    return (m / 2) ^ ((m + 1) / 2); // 必须用 64 位读 m
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 0; i < n; ++i) {
        int64 m;
        cin >> m;
        cout << min_hedge(m) << '\n';
    }
    return 0;
}
```
