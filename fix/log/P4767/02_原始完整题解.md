## 解题思路

设经过 $m$ 秒后的答案为 $f(n,m)$。

题目中的分裂规则是：

* 若当前数字为偶数 $a$，会分裂成两个数字 $\left\lfloor \dfrac{a}{2} \right\rfloor + 1$；
* 若当前数字为奇数 $a$，除了上面的两个数字外，还会额外分裂出一个数字 $2$。

由于两个主要分裂出来的数字是相同的，所以可以直接写出递推。

设

$$
b=\left\lfloor \dfrac{n}{2} \right\rfloor + 1
$$

那么：

* 当 $n$ 为偶数时：

$$
f(n,m)=2\times f(b,m-1)
$$

* 当 $n$ 为奇数时：

$$
f(n,m)=2\times f(b,m-1)+f(2,m-1)
$$

因此关键变成如何快速处理 $f(1,m)$ 和 $f(2,m)$。

### 1. 处理数字 $2$

数字 $2$ 每次都会变成两个 $2$，所以：

$$
f(2,m)=2^{m+1}
$$

### 2. 处理数字 $1$

数字 $1$ 每次都会变成两个 $1$ 和一个 $2$。

直接推几步可以发现：

* $m=0$ 时，和为 $1$
* $m=1$ 时，和为 $4$
* $m=2$ 时，和为 $12$
* $m=3$ 时，和为 $32$

可归纳得到：

$$
f(1,m)=(m+1)\times 2^m
$$

### 3. 递归何时结束

每次递归时，数字都会变成

$$
\left\lfloor \dfrac{n}{2} \right\rfloor + 1
$$

数值会很快减小，所以最多递归大约 $O(\log n)$ 层。

为了避免每层都重新计算幂，我们先算出 $2^m$，递归时同步传入当前的幂值 $p=2^m$。下一层就是：

$$
2^{m-1}=2^m \times \text{inv2}
$$

其中 $\text{inv2}$ 是模意义下的 $2$ 的逆元。

### 4. 使用的算法

这里用到两个经典算法：

* 递归
* 快速幂

核心实现方法：

* 先用快速幂求出 $2^m \bmod (10^9+7)$；
* 再递归计算答案；
* 当递归到 $n=1$ 或 $n=2$ 时，直接用公式返回。

---

## 复杂度分析

设单组数据的初始数字为 $n$。

每次递归都会把 $n$ 变成 $\left\lfloor \dfrac{n}{2} \right\rfloor + 1$，因此递归层数为 $O(\log n)$。

* 时间复杂度：$O(\log m+\log n)$
* 空间复杂度：$O(\log n)$

这个复杂度对于 $T \le 10^4$、$n,m \le 10^9$ 是完全可行的。

---

## 代码实现

### Python

```python
MOD = 10**9 + 7
INV2 = (MOD + 1) // 2  # 2 在模 MOD 下的逆元


# 快速幂：计算 a^b % MOD
def qpow(a, b):
    res = 1
    a %= MOD
    while b > 0:
        if b & 1:
            res = res * a % MOD
        a = a * a % MOD
        b >>= 1
    return res


# 递归计算 f(n, m)，其中 p = 2^m % MOD
def solve(n, m, p):
    # 递归边界：不再分裂
    if m == 0:
        return n % MOD

    # 数字 1 的特判公式：f(1, m) = (m + 1) * 2^m
    if n == 1:
        return (m + 1) % MOD * p % MOD

    # 数字 2 的特判公式：f(2, m) = 2^(m + 1) = 2 * 2^m
    if n == 2:
        return 2 * p % MOD

    # 下一层的 2^(m-1)
    next_p = p * INV2 % MOD

    # 主要分裂出的数字
    b = n // 2 + 1

    # 两个相同的 b
    ans = 2 * solve(b, m - 1, next_p) % MOD

    # 如果 n 是奇数，还会额外分裂出一个 2
    if n & 1:
        ans = (ans + p) % MOD  # f(2, m-1) = 2^m = p

    return ans


def main():
    t = int(input().strip())
    for _ in range(t):
        n, m = map(int, input().split())
        p = qpow(2, m)  # 先算出 2^m
        print(solve(n, m, p))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {
    static final long MOD = 1000000007L;
    static final long INV2 = (MOD + 1) / 2; // 2 在模 MOD 下的逆元

    // 快速幂：计算 a^b % MOD
    static long qpow(long a, long b) {
        long res = 1;
        a %= MOD;
        while (b > 0) {
            if ((b & 1) == 1) {
                res = res * a % MOD;
            }
            a = a * a % MOD;
            b >>= 1;
        }
        return res;
    }

    // 递归计算 f(n, m)，其中 p = 2^m % MOD
    static long solve(long n, long m, long p) {
        // 递归边界：不再分裂
        if (m == 0) {
            return n % MOD;
        }

        // 数字 1 的特判公式
        if (n == 1) {
            return ((m + 1) % MOD) * p % MOD;
        }

        // 数字 2 的特判公式
        if (n == 2) {
            return 2 * p % MOD;
        }

        // 下一层的 2^(m-1)
        long nextP = p * INV2 % MOD;

        // 主要分裂出的数字
        long b = n / 2 + 1;

        // 两个相同的 b
        long ans = 2 * solve(b, m - 1, nextP) % MOD;

        // 如果 n 是奇数，还会额外分裂出一个 2
        if ((n & 1) == 1) {
            ans = (ans + p) % MOD; // f(2, m-1) = 2^m = p
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int T = sc.nextInt();
        while (T-- > 0) {
            long n = sc.nextLong();
            long m = sc.nextLong();

            long p = qpow(2, m); // 先算出 2^m
            System.out.println(solve(n, m, p));
        }

        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
using namespace std;

const long long MOD = 1000000007LL;
const long long INV2 = (MOD + 1) / 2; // 2 在模 MOD 下的逆元

// 快速幂：计算 a^b % MOD
long long qpow(long long a, long long b) {
    long long res = 1;
    a %= MOD;
    while (b > 0) {
        if (b & 1) {
            res = res * a % MOD;
        }
        a = a * a % MOD;
        b >>= 1;
    }
    return res;
}

// 递归计算 f(n, m)，其中 p = 2^m % MOD
long long solve(long long n, long long m, long long p) {
    // 递归边界：不再分裂
    if (m == 0) {
        return n % MOD;
    }

    // 数字 1 的特判公式：f(1, m) = (m + 1) * 2^m
    if (n == 1) {
        return (m + 1) % MOD * p % MOD;
    }

    // 数字 2 的特判公式：f(2, m) = 2^(m + 1) = 2 * 2^m
    if (n == 2) {
        return 2 * p % MOD;
    }

    // 下一层的 2^(m-1)
    long long next_p = p * INV2 % MOD;

    // 主要分裂出的数字
    long long b = n / 2 + 1;

    // 两个相同的 b
    long long ans = 2 * solve(b, m - 1, next_p) % MOD;

    // 如果 n 是奇数，还会额外分裂出一个 2
    if (n & 1) {
        ans = (ans + p) % MOD; // f(2, m-1) = 2^m = p
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        long long n, m;
        cin >> n >> m;

        long long p = qpow(2, m); // 先算出 2^m
        cout << solve(n, m, p) << '\n';
    }

    return 0;
}
```