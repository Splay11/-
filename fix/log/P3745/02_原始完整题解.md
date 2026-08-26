## 解题思路

本题属于数论 + 构造类问题。核心利用如下事实与策略：

1. 若 $n<8$，无解。因为四个最小质数之和为 $2+2+2+2=8$。
2. 当 $n\ge 8$ 时，构造分解只需把问题化为“偶数拆成两个质数之和”：

   * 如果 $n$ 为偶数：先取 $2,2$，剩下的 $m=n-4$ 必为偶数；再把 $m$ 拆成两个质数之和；
   * 如果 $n$ 为奇数：先取 $2,3$，剩下的 $m=n-5$ 必为偶数；再把 $m$ 拆成两个质数之和。
3. 对“偶数 $m$ 拆成两个质数之和”的求解策略（构造）：

   * 先尝试 $m=2+(m-2)$ 是否可行（判断 $m-2$ 是否为质数）；若可行直接输出；
   * 否则从奇数 $p=3,5,7,\dots$ 依次判断：若 $p$ 与 $m-p$ 同为质数，则得到一组解。
4. 质数判定采用 试除法。




## 代码实现。

### Python

```python
import sys

# 简单素数判定：试除到 sqrt(n)，使用 6k±1 加速
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    if n % 3 == 0:
        return n == 3
    i = 5
    # 只检查 6k-1 与 6k+1
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# 将偶数 m 拆为两个质数之和（构造）
def two_primes_sum(m: int):
    # 特判 m=4
    if m == 4:
        return 2, 2
    # 先尝试 2 + (m-2)
    if is_prime(m - 2):
        return 2, m - 2
    # 依次枚举奇数 p，检查 p 与 m-p 是否同时为质数
    p = 3
    while p <= m - 3:
        if is_prime(p) and is_prime(m - p):
            return p, m - p
        p += 2
    return None  # 理论上不会到达

def solve_case(n: int) -> str:
    if n < 8:
        return "-1"
    if n % 2 == 0:
        a, b = two_primes_sum(n - 4)
        return f"2 2 {a} {b}"
    else:
        a, b = two_primes_sum(n - 5)
        return f"2 3 {a} {b}"

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out = []
    for _ in range(t):
        n = data[idx]; idx += 1
        out.append(solve_case(n))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    // 简单判素：返回 n 是否为质数
    static boolean isPrime(long n) {
        if (n < 2) return false;
        if (n % 2 == 0) return n == 2;
        if (n % 3 == 0) return n == 3;
        long i = 5;
        // 只检查 6k-1 与 6k+1
        while (i * i <= n) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
            i += 6;
        }
        return true;
    }

    // 将偶数 m 拆为两个质数之和
    static long[] twoPrimesSum(long m) {
        if (m == 4) return new long[]{2, 2};
        if (isPrime(m - 2)) return new long[]{2, m - 2};
        for (long p = 3; p <= m - 3; p += 2) {
            if (isPrime(p) && isPrime(m - p)) {
                return new long[]{p, m - p};
            }
        }
        return null; // 理论上不会到达
    }

    static String solveCase(long n) {
        if (n < 8) return "-1";
        if ((n & 1) == 0) {
            long[] ab = twoPrimesSum(n - 4);
            return "2 2 " + ab[0] + " " + ab[1];
        } else {
            long[] ab = twoPrimesSum(n - 5);
            return "2 3 " + ab[0] + " " + ab[1];
        }
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int t = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < t; i++) {
            long n = Long.parseLong(br.readLine().trim());
            sb.append(solveCase(n)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 简单判素：返回 n 是否为质数
bool is_prime(long long n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    if (n % 3 == 0) return n == 3;
    long long i = 5;
    // 只检查 6k-1 与 6k+1
    while (i * i <= n) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
        i += 6;
    }
    return true;
}

// 将偶数 m 拆为两个质数之和
pair<long long, long long> two_primes_sum(long long m) {
    if (m == 4) return {2, 2};
    if (is_prime(m - 2)) return {2, m - 2};
    for (long long p = 3; p <= m - 3; p += 2) {
        if (is_prime(p) && is_prime(m - p)) {
            return {p, m - p};
        }
    }
    return {0, 0}; // 理论上不会到达
}

string solve_case(long long n) {
    if (n < 8) return "-1";
    if ((n & 1) == 0) {
        auto ab = two_primes_sum(n - 4);
        return "2 2 " + to_string(ab.first) + " " + to_string(ab.second);
    } else {
        auto ab = two_primes_sum(n - 5);
        return "2 3 " + to_string(ab.first) + " " + to_string(ab.second);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        long long n;
        cin >> n;
        cout << solve_case(n) << "\n";
    }
    return 0;
}
```