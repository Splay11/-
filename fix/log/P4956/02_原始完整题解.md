## 解题思路

先用埃氏筛预处理出所有不超过 $10^6$ 的纯净数。

因为 $n \le 10^{18}$，如果存在纯净数 $p$ 满足 $p^2 \mid n$，那么 $p \le 10^9$。

分两类讨论：

1. 若 $p \le 10^6$
   直接用预处理出的纯净数试除 $n$，统计每个纯净因子的次数，如果次数不少于 $2$，就把 $p^2$ 加入答案。

2. 若 $p > 10^6$
   那么 $p^2 > 10^{12}$。在把所有小于等于 $10^6$ 的纯净因子都除掉后，剩下的部分如果还能贡献答案，只可能是某个大纯净数的平方。
   因此只需要判断剩余部分 $x$ 是否为完全平方数，并判断 $\sqrt x$ 是否为纯净数即可。

答案按照纯净数从小到大处理，所以输出的 $p^2$ 也是从小到大。

## 复杂度分析

设 $M = 10^6$。

预处理纯净数的时间复杂度为 $O(M \log \log M)$，空间复杂度为 $O(M)$。

每组数据最多枚举不超过 $10^6$ 的纯净数，数量约为 $78498$，因此单组时间复杂度为 $O(\pi(M))$，可以通过 $T \le 300$ 的数据范围。

## 代码实现

### Python

```python
import sys
from math import isqrt

LIMIT = 10 ** 6

def get_primes():
    # 埃氏筛预处理纯净数
    is_prime = [True] * (LIMIT + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, isqrt(LIMIT) + 1):
        if is_prime[i]:
            for j in range(i * i, LIMIT + 1, i):
                is_prime[j] = False

    primes = []
    for i in range(2, LIMIT + 1):
        if is_prime[i]:
            primes.append(i)
    return primes

PRIMES = get_primes()

def check_prime(x):
    # 判断 x 是否为纯净数，这里 x 最大不超过 10^9
    if x < 2:
        return False
    for p in PRIMES:
        if p * p > x:
            break
        if x % p == 0:
            return False
    return True

def solve_one(n):
    ans = []
    x = n

    # 处理所有不超过 10^6 的纯净因子
    for p in PRIMES:
        if p * p > x:
            break

        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1

        # 如果 p 至少出现 2 次，则 p^2 是答案
        if cnt >= 2:
            ans.append(p * p)

    # 剩余部分可能是一个大纯净数的平方
    r = isqrt(x)
    if r * r == x and check_prime(r):
        ans.append(x)

    return ans

def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    res = []

    for i in range(1, t + 1):
        n = int(data[i])
        ans = solve_one(n)

        if ans:
            res.append(" ".join(map(str, ans)))
        else:
            res.append("-1")

    print("\n".join(res))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static final int LIMIT = 1000000;
    static ArrayList<Integer> primes = new ArrayList<>();

    static void getPrimes() {
        // 埃氏筛预处理纯净数
        boolean[] isPrime = new boolean[LIMIT + 1];
        Arrays.fill(isPrime, true);
        isPrime[0] = false;
        isPrime[1] = false;

        for (int i = 2; i * i <= LIMIT; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j <= LIMIT; j += i) {
                    isPrime[j] = false;
                }
            }
        }

        for (int i = 2; i <= LIMIT; i++) {
            if (isPrime[i]) {
                primes.add(i);
            }
        }
    }

    static boolean checkPrime(long x) {
        // 判断 x 是否为纯净数，这里 x 最大不超过 10^9
        if (x < 2) return false;

        for (int p : primes) {
            if ((long) p * p > x) break;
            if (x % p == 0) return false;
        }

        return true;
    }

    static ArrayList<Long> solveOne(long n) {
        ArrayList<Long> ans = new ArrayList<>();
        long x = n;

        // 处理所有不超过 10^6 的纯净因子
        for (int p : primes) {
            long pp = (long) p * p;
            if (pp > x) break;

            int cnt = 0;
            while (x % p == 0) {
                x /= p;
                cnt++;
            }

            // 如果 p 至少出现 2 次，则 p^2 是答案
            if (cnt >= 2) {
                ans.add(pp);
            }
        }

        // 剩余部分可能是一个大纯净数的平方
        long r = (long) Math.sqrt(x);
        while ((r + 1) * (r + 1) <= x) r++;
        while (r * r > x) r--;

        if (r * r == x && checkPrime(r)) {
            ans.add(x);
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        getPrimes();

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder out = new StringBuilder();

        int T = Integer.parseInt(br.readLine().trim());

        for (int i = 0; i < T; i++) {
            long n = Long.parseLong(br.readLine().trim());
            ArrayList<Long> ans = solveOne(n);

            if (ans.isEmpty()) {
                out.append("-1");
            } else {
                for (int j = 0; j < ans.size(); j++) {
                    if (j > 0) out.append(' ');
                    out.append(ans.get(j));
                }
            }

            if (i + 1 < T) out.append('\n');
        }

        System.out.print(out.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const int LIMIT = 1000000;
vector<int> primes;

void get_primes() {
    // 埃氏筛预处理纯净数
    vector<bool> is_prime(LIMIT + 1, true);
    is_prime[0] = false;
    is_prime[1] = false;

    for (int i = 2; i * i <= LIMIT; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= LIMIT; j += i) {
                is_prime[j] = false;
            }
        }
    }

    for (int i = 2; i <= LIMIT; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
        }
    }
}

bool check_prime(long long x) {
    // 判断 x 是否为纯净数，这里 x 最大不超过 10^9
    if (x < 2) return false;

    for (int p : primes) {
        if (1LL * p * p > x) break;
        if (x % p == 0) return false;
    }

    return true;
}

vector<long long> solve_one(long long n) {
    vector<long long> ans;
    long long x = n;

    // 处理所有不超过 10^6 的纯净因子
    for (int p : primes) {
        long long pp = 1LL * p * p;
        if (pp > x) break;

        int cnt = 0;
        while (x % p == 0) {
            x /= p;
            cnt++;
        }

        // 如果 p 至少出现 2 次，则 p^2 是答案
        if (cnt >= 2) {
            ans.push_back(pp);
        }
    }

    // 剩余部分可能是一个大纯净数的平方
    long long r = sqrt((long double)x);
    while ((r + 1) <= x / (r + 1)) r++;
    while (r > x / r) r--;

    if (r * r == x && check_prime(r)) {
        ans.push_back(x);
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    get_primes();

    int T;
    cin >> T;

    while (T--) {
        long long n;
        cin >> n;

        vector<long long> ans = solve_one(n);

        if (ans.empty()) {
            cout << -1;
        } else {
            for (int i = 0; i < (int)ans.size(); i++) {
                if (i) cout << ' ';
                cout << ans[i];
            }
        }

        if (T) cout << '\n';
    }

    return 0;
}
```