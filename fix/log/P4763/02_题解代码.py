## 解题思路

先把题意抽象一下。

初始时网格全是 $0$。
一次操作只会反转一整行或一整列，因此最终某个位置 $(i,j)$ 的值只和两件事有关：

* 第 $i$ 行被反转了奇数次还是偶数次
* 第 $j$ 列被反转了奇数次还是偶数次

设：

* $r_i\in{0,1}$ 表示第 $i$ 行最终是否被反转奇数次
* $c_j\in{0,1}$ 表示第 $j$ 列最终是否被反转奇数次

那么最终格子值为：

$$
a_{i,j}=r_i\oplus c_j
$$

也就是说，整张表的最终状态只取决于“奇数次反转的行集合”和“奇数次反转的列集合”。

### 核心思路

题目要求把整个网格按行优先拼成一个二进制数，再对 $10^9+7$ 取模。

如果直接构造网格，显然不可能，因为：

* $n,m$ 最大可达 $10^9$
* $k$ 最大可达 $2\times 10^5$

所以必须只利用“被反转奇数次的行和列”来计算答案。



先看每一行长什么样。

假设列的奇偶状态已经固定，定义这一行对应的二进制值为：

* 当该行没有被反转奇数次时，这一行就是 $c_1c_2\cdots c_m$
* 当该行被反转奇数次时，这一行就是其逐位取反，即 $(1-c_1)(1-c_2)\cdots(1-c_m)$

设：

* $C$：二进制串 $c_1c_2\cdots c_m$ 的十进制值
* $U$：它的按位取反后的十进制值

则有：

$$
U=(2^m-1)-C
$$

因为长度为 $m$ 的全 $1$ 二进制数就是 $2^m-1$。



接下来考虑整张表按行拼接。

每一行相当于一个长度为 $m$ 的“块”，所以把所有行拼起来后，本质上是一个以 $2^m$ 为进位基底的表示：

$$
\text{ans} = \sum_{i=1}^{n} \text{rowVal}_i \cdot (2^m)^{,n-i}
$$

其中：

* 如果第 $i$ 行最终为偶数次反转，则 $\text{rowVal}_i=C$
* 如果第 $i$ 行最终为奇数次反转，则 $\text{rowVal}_i=U$

于是可以把答案拆成两部分：

1. 假设所有行都是 $C$
2. 对于那些被反转奇数次的行，再额外加上 $(U-C)$ 对应的贡献

即：

$$
\text{ans} = C \cdot \sum_{i=1}^{n} (2^m)^{\,n-i} \;+\; (U-C) \cdot \sum_{i \in S_r} (2^m)^{\,n-i}
$$

其中 $S_r$ 表示“被反转奇数次的行下标集合”。



### 如何计算 $C$

第 $j$ 列如果被反转奇数次，那么在二进制串 $c_1c_2\cdots c_m$ 中，第 $j$ 位就是 $1$，它的权值是：

$$
2^{m-j}
$$

所以：

$$
C=\sum_{j\in S_c}2^{m-j}
$$

其中 $S_c$ 表示“被反转奇数次的列下标集合”。

由于只有发生过操作的位置才可能进入集合，而总操作数只有 $k$，所以只需要把列编号放进集合里按奇偶切换即可，最终集合大小最多 $k$。



### 如何维护奇偶状态

对于每次操作：

* 若是反转第 $y$ 列，就把 $y$ 在列集合里“出现一次则加入，再出现一次则删除”
* 若是反转第 $y$ 行，就把 $y$ 在行集合里同样做奇偶切换

这样最后：

* 行集合里留下的就是奇数次反转的行
* 列集合里留下的就是奇数次反转的列

时间复杂度是 $O(k)$ 级别。



### 如何计算几何和

记：

$$
B=2^m \bmod MOD
$$

那么

$$
\sum_{i=1}^{n} (2^m)^{n-i}
=
\sum_{t=0}^{n-1} B^{\,t}
$$

这是等比数列：

* 当 $B\neq 1$ 时：

$$
\sum_{t=0}^{n-1}B^t=\frac{B^n-1}{B-1}
$$

* 当 $B=1$ 时：

$$
\sum_{t=0}^{n-1}B^t=n
$$

因为模数 $MOD=10^9+7$ 是质数，所以可以用快速幂求逆元。



### 实现方法

1. 用两个集合分别维护奇数次反转的行和列
2. 枚举奇数次反转的列，计算
   $$
   C=\sum 2^{m-j}
   $$
3. 计算
   $$
   U=(2^m-1)-C
   $$
4. 计算所有行都取 $C$ 时的总贡献
5. 再枚举奇数次反转的行，把每一行额外补上
   $$
   (U-C)\cdot (2^m)^{n-i}
   $$
6. 输出答案对 $10^9+7$ 取模后的结果

这样就完全不需要构造网格，能够通过数据范围。

## 复杂度分析

设最终被反转奇数次的行数为 $r$，列数为 $c$，显然有：

$$
r\le k,\quad c\le k
$$

### 时间复杂度

* 维护行列奇偶集合：$O(k)$
* 计算列贡献：$O(c\log MOD)$
* 计算奇数次反转行的额外贡献：$O(r\log MOD)$
* 其余快速幂与求逆为 $O(\log MOD)$

总时间复杂度为：

$$
O(k\log MOD)
$$

在 $k\le 2\times 10^5$ 时完全可行。

### 空间复杂度

只需要存储两个集合：

$$
O(r+c)\le O(k)
$$

空间复杂度为：

$$
O(k)
$$

## 代码实现

### Python

```python
import sys

MOD = 10 ** 9 + 7


def calc_geometric_sum(base, n):
    # 计算 1 + base + base^2 + ... + base^(n-1)
    if base == 1:
        return n % MOD
    numerator = (pow(base, n, MOD) - 1 + MOD) % MOD
    denominator_inv = pow(base - 1, MOD - 2, MOD)
    return numerator * denominator_inv % MOD


def solve(n, m, operations):
    # odd_rows 中保存被反转奇数次的行编号
    # odd_cols 中保存被反转奇数次的列编号
    odd_rows = set()
    odd_cols = set()

    for x, y in operations:
        if x == 1:
            # 反转第 y 列，使用集合维护奇偶性
            if y in odd_cols:
                odd_cols.remove(y)
            else:
                odd_cols.add(y)
        else:
            # 反转第 y 行，使用集合维护奇偶性
            if y in odd_rows:
                odd_rows.remove(y)
            else:
                odd_rows.add(y)

    # row_base = 2^m，表示每一整行作为一个长度为 m 的二进制块
    row_base = pow(2, m, MOD)

    # 计算 C：列状态对应的一整行二进制值
    # 第 j 列为 1 时，对应权值是 2^(m-j)
    c_value = 0
    for col in odd_cols:
        c_value = (c_value + pow(2, m - col, MOD)) % MOD

    # full_one = 2^m - 1，即长度为 m 的全 1 二进制数
    full_one = (row_base - 1 + MOD) % MOD

    # U 为 C 的按位取反结果
    u_value = (full_one - c_value + MOD) % MOD

    # 所有行都先按 C 计算
    total_rows_weight = calc_geometric_sum(row_base, n)
    ans = c_value * total_rows_weight % MOD

    # 对于奇数次反转的行，需要把该行从 C 改成 U
    # 额外增加 (U - C) * row_base^(n - row)
    delta = (u_value - c_value + MOD) % MOD
    for row in odd_rows:
        ans = (ans + delta * pow(row_base, n - row, MOD)) % MOD

    return ans


def main():
    input = sys.stdin.readline
    n, m, k = map(int, input().split())
    operations = []
    for _ in range(k):
        x, y = map(int, input().split())
        operations.append((x, y))
    print(solve(n, m, operations))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;

public class Main {
    static final long MOD = 1000000007L;

    static long quickPow(long a, long b) {
        // 快速幂计算 a^b % MOD
        long result = 1L;
        a %= MOD;
        while (b > 0) {
            if ((b & 1) == 1) {
                result = result * a % MOD;
            }
            a = a * a % MOD;
            b >>= 1;
        }
        return result;
    }

    static long calcGeometricSum(long base, long n) {
        // 计算 1 + base + base^2 + ... + base^(n-1)
        if (base == 1) {
            return n % MOD;
        }
        long numerator = (quickPow(base, n) - 1 + MOD) % MOD;
        long denominatorInv = quickPow(base - 1, MOD - 2);
        return numerator * denominatorInv % MOD;
    }

    static long solve(long n, long m, int k, int[][] operations) {
        // oddRows 中保存被反转奇数次的行编号
        // oddCols 中保存被反转奇数次的列编号
        Set<Long> oddRows = new HashSet<>();
        Set<Long> oddCols = new HashSet<>();

        for (int i = 0; i < k; i++) {
            int x = operations[i][0];
            long y = operations[i][1];

            if (x == 1) {
                // 反转第 y 列，使用集合维护奇偶性
                if (oddCols.contains(y)) {
                    oddCols.remove(y);
                } else {
                    oddCols.add(y);
                }
            } else {
                // 反转第 y 行，使用集合维护奇偶性
                if (oddRows.contains(y)) {
                    oddRows.remove(y);
                } else {
                    oddRows.add(y);
                }
            }
        }

        // rowBase = 2^m，表示每一整行对应的基底
        long rowBase = quickPow(2, m);

        // 计算 C：列状态对应的一整行二进制值
        long cValue = 0L;
        for (long col : oddCols) {
            cValue = (cValue + quickPow(2, m - col)) % MOD;
        }

        // fullOne = 2^m - 1，即长度为 m 的全 1 二进制数
        long fullOne = (rowBase - 1 + MOD) % MOD;

        // U 为 C 的按位取反结果
        long uValue = (fullOne - cValue + MOD) % MOD;

        // 所有行都先按 C 计算
        long totalRowsWeight = calcGeometricSum(rowBase, n);
        long ans = cValue * totalRowsWeight % MOD;

        // 奇数次反转的行补上额外贡献
        long delta = (uValue - cValue + MOD) % MOD;
        for (long row : oddRows) {
            ans = (ans + delta * quickPow(rowBase, n - row)) % MOD;
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        long n = Long.parseLong(st.nextToken());
        long m = Long.parseLong(st.nextToken());
        int k = Integer.parseInt(st.nextToken());

        int[][] operations = new int[k][2];
        for (int i = 0; i < k; i++) {
            st = new StringTokenizer(br.readLine());
            operations[i][0] = Integer.parseInt(st.nextToken());
            operations[i][1] = Integer.parseInt(st.nextToken());
        }

        System.out.println(solve(n, m, k, operations));
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

const long long MOD = 1000000007LL;

long long quickPow(long long a, long long b) {
    // 快速幂计算 a^b % MOD
    long long result = 1;
    a %= MOD;
    while (b > 0) {
        if (b & 1) {
            result = result * a % MOD;
        }
        a = a * a % MOD;
        b >>= 1;
    }
    return result;
}

long long calcGeometricSum(long long base, long long n) {
    // 计算 1 + base + base^2 + ... + base^(n-1)
    if (base == 1) {
        return n % MOD;
    }
    long long numerator = (quickPow(base, n) - 1 + MOD) % MOD;
    long long denominatorInv = quickPow(base - 1, MOD - 2);
    return numerator * denominatorInv % MOD;
}

long long solve(long long n, long long m, const vector<pair<int, long long>>& operations) {
    // oddRows 中保存被反转奇数次的行编号
    // oddCols 中保存被反转奇数次的列编号
    unordered_set<long long> oddRows;
    unordered_set<long long> oddCols;

    for (auto& op : operations) {
        int x = op.first;
        long long y = op.second;

        if (x == 1) {
            // 反转第 y 列，使用集合维护奇偶性
            if (oddCols.count(y)) {
                oddCols.erase(y);
            } else {
                oddCols.insert(y);
            }
        } else {
            // 反转第 y 行，使用集合维护奇偶性
            if (oddRows.count(y)) {
                oddRows.erase(y);
            } else {
                oddRows.insert(y);
            }
        }
    }

    // rowBase = 2^m，表示每一整行对应的基底
    long long rowBase = quickPow(2, m);

    // 计算 C：列状态对应的一整行二进制值
    long long cValue = 0;
    for (long long col : oddCols) {
        cValue = (cValue + quickPow(2, m - col)) % MOD;
    }

    // fullOne = 2^m - 1，即长度为 m 的全 1 二进制数
    long long fullOne = (rowBase - 1 + MOD) % MOD;

    // U 为 C 的按位取反结果
    long long uValue = (fullOne - cValue + MOD) % MOD;

    // 所有行都先按 C 计算
    long long totalRowsWeight = calcGeometricSum(rowBase, n);
    long long ans = cValue * totalRowsWeight % MOD;

    // 奇数次反转的行补上额外贡献
    long long delta = (uValue - cValue + MOD) % MOD;
    for (long long row : oddRows) {
        ans = (ans + delta * quickPow(rowBase, n - row)) % MOD;
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, m;
    int k;
    cin >> n >> m >> k;

    vector<pair<int, long long>> operations;
    operations.reserve(k);

    for (int i = 0; i < k; i++) {
        int x;
        long long y;
        cin >> x >> y;
        operations.push_back({x, y});
    }

    cout << solve(n, m, operations) << '\n';
    return 0;
}
```