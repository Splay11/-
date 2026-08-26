## 关键观察

设进行的总操作次数为 `k`。则：

* 总和变化：每次操作总和加 `2m`，故 `sum(b) = 2mk`，必须有 `sum(b)` 为偶数，且 `2m | sum(b)`。
* 每个位置被加的次数为 `x_i = b_i / m`（必须为非负整数），且 ∑x\_i = 2k 为偶数。
* 可行性的图论刻画：每次操作相当于在两个点间连一条边，`x_i` 为度数。允许多重边、禁止自环。存在这样的多重图的充要条件是
  2·max(x\_i) ≤ ∑x\_i。
  将其按 `m` 约去，得到与 `m` 无关的必要充分条件：
* 2·max(b\_i) ≤ ∑b\_i。

## 判定条件

设 `S = ∑b_i`，`M = max(b_i)`，`g = gcd(b_1, …, b_n)`。

* 若 `S` 为奇数，或 `2M > S`，则答案为 0。
* 否则，所有可行的 `m` 必须同时整除 `g` 和 `S/2`。答案为 `d = gcd(g, S/2)` 的正因子个数。

## 算法步骤

* 读入 `n` 与数组 `b`，计算 `S`、`M`、`g`。
* 若 `S` 为奇数或 `2M > S`，输出 0。
* 否则，令 `d = gcd(g, S/2)`，答案为 `d` 的因子数。用试除到 `√d` 计数。

## 复杂度分析

* 每组：`O(n + √d)`，其中 `d = gcd(g, S/2) ≤ 10^9`。总 `n` 之和 ≤ 2e5，满足时限。

## 实现
### python 
```python
import sys
import math

def count_divisors(d: int) -> int:
    if d <= 0:
        return 0
    r = int(math.isqrt(d))
    ans = 0
    for i in range(1, r + 1):
        if d % i == 0:
            ans += 2 if i * i != d else 1
    return ans

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        n = int(next(it))
        b = [int(next(it)) for _ in range(n)]
        S = sum(b)
        M = max(b)
        if (S & 1) or (2 * M > S):
            out.append("0")
            continue
        g = 0
        for x in b:
            g = math.gcd(g, x)
        d = math.gcd(g, S // 2)
        out.append(str(count_divisors(d)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```
### java
```java
import java.io.*;
import java.util.*;

public class Main {
	static class FastScanner {
		private final InputStream in;
		private final byte[] buffer = new byte[1 << 16];
		private int ptr = 0, len = 0;
		FastScanner(InputStream is) { in = is; }
		private int read() throws IOException {
			if (ptr >= len) {
				len = in.read(buffer);
				ptr = 0;
				if (len <= 0) return -1;
			}
			return buffer[ptr++];
		}
		int nextInt() throws IOException {
			int c, s = 1, x = 0;
			do { c = read(); } while (c <= 32);
			if (c == '-') { s = -1; c = read(); }
			while (c > 32) { x = x * 10 + (c - '0'); c = read(); }
			return x * s;
		}
	}
	static long gcd(long a, long b) {
		while (b != 0) {
			long t = a % b;
			a = b; b = t;
		}
		return Math.abs(a);
	}
	static long countDivisors(long d) {
		if (d <= 0) return 0;
		long r = (long)Math.sqrt(d);
		long ans = 0;
		for (long i = 1; i <= r; i++) {
			if (d % i == 0) {
				ans += (i * i == d) ? 1 : 2;
			}
		}
		return ans;
	}
	public static void main(String[] args) throws Exception {
		FastScanner fs = new FastScanner(System.in);
		StringBuilder sb = new StringBuilder();
		int T = fs.nextInt();
		while (T-- > 0) {
			int n = fs.nextInt();
			long S = 0;
			int M = 0;
			int[] b = new int[n];
			for (int i = 0; i < n; i++) {
				int x = fs.nextInt();
				b[i] = x;
				S += x;
				if (x > M) M = x;
			}
			if ((S & 1L) == 1L || 2L * M > S) {
				sb.append(0).append('\n');
				continue;
			}
			long g = 0;
			for (int x : b) g = gcd(g, x);
			long d = gcd(g, S / 2);
			sb.append(countDivisors(d)).append('\n');
		}
		System.out.print(sb.toString());
	}
}
```
### c++
```cpp
#include <bits/stdc++.h>
using namespace std;

long long count_divisors(long long d) {
	if (d <= 0) return 0;
	long long r = sqrtl((long double)d);
	long long ans = 0;
	for (long long i = 1; i <= r; ++i) {
		if (d % i == 0) ans += (i * i == d) ? 1 : 2;
	}
	return ans;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T; 
	if (!(cin >> T)) return 0;
	while (T--) {
		int n; 
		cin >> n;
		vector<long long> b(n);
		long long S = 0, M = 0, g = 0;
		for (int i = 0; i < n; ++i) {
			cin >> b[i];
			S += b[i];
			M = max(M, b[i]);
			g = std::gcd(g, b[i]);
		}
		if ((S & 1LL) || 2LL * M > S) {
			cout << 0 << "\n";
			continue;
		}
		long long d = std::gcd(g, S / 2);
		cout << count_divisors(d) << "\n";
	}
	return 0;
}
```