## 思路

将一年 12 个月的“掉落量”形成固定模式：

* 非刮风月掉 `m`，刮风月掉 `2m`。
* 一年总掉落量：

  $Y = (12-q)\cdot m + q\cdot(2m)$ = $(12+q)\cdot m$

**做法**：

1. 先整年跳跃：设可完整经过的年数

   $k=\left\lfloor\frac{n-1}{Y}\right\rfloor$

   跳过 `k` 年（`12k` 个月），剩余 `n ← n - kY`。

   > 用 `(n-1)//Y` 可以避免“正好整年结束”的边界误差，同时不影响最优性。
2. 对下一年只需在 **最多 12 个月** 内顺序扫一遍，用前缀和（或简单累加）找到第一个使累计掉落 ≥ 剩余 `n` 的月份。

### 算法步骤

1. 构造数组 `drop[1..12]`：普通月为 `m`，`[p, p+q-1]` 为 `2m`。
2. 计算 `Y = sum(drop)`；`k=(n-1)//Y`；`ans_month = 12*k`；`rem = n - k*Y`。
3. 从 1 月到 12 月累加 `drop[i]`，首次使累计 ≥ `rem` 时，`ans_month += i` 即为答案。



### 复杂度分析

* 时间：`O(12)`（整年跳过后只需扫一年的 12 个月）。
* 空间：`O(1)`。


## 代码

### Python

```python
# 读取 n, m, p, q，计算最少月份数
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n, m, p, q = map(int, data[:4])

    # 构造一年 12 个月的掉落量
    drop = [m] * 12
    for i in range(p - 1, p - 1 + q):
        drop[i] = 2 * m

    yearly = sum(drop)                  # Y = (12 + q) * m
    years = (n - 1) // yearly           # 可整年跳过的年数
    months = years * 12
    rem = n - years * yearly            # 跳过后剩余的叶子数

    # 在下一年内顺序找首个前缀和 >= rem 的月份
    acc = 0
    for i in range(12):
        acc += drop[i]
        months += 1
        if acc >= rem:
            print(months)
            return

if __name__ == "__main__":
    solve()
```

### Java

```java
// 计算最少月份数：前缀和 + 整年跳跃
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextLong()) return;
        long n = sc.nextLong();   // 初始叶子数
        long m = sc.nextLong();   // 普通月每月掉落
        int p = sc.nextInt();     // 刮风期起始月(1..12)
        int q = sc.nextInt();     // 刮风期持续月数

        long[] drop = new long[12];
        Arrays.fill(drop, m);
        for (int i = p - 1; i < p - 1 + q; i++) drop[i] = 2 * m;

        long yearly = 0;
        for (long x : drop) yearly += x;     // 一年总掉落量

        long years = (n - 1) / yearly;       // 整年跳过
        long months = years * 12;
        long rem = n - years * yearly;       // 剩余叶子

        long acc = 0;
        for (int i = 0; i < 12; i++) {
            acc += drop[i];
            months++;
            if (acc >= rem) {
                System.out.println(months);
                return;
            }
        }
    }
}
```

### C++

```cpp
// 计算最少月份数：前缀和 + 整年跳跃
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, m;
    int p, q;
    if (!(cin >> n >> m >> p >> q)) return 0;

    vector<long long> drop(12, m);         // 一年 12 个月的掉落量
    for (int i = p - 1; i < p - 1 + q; ++i) drop[i] = 2 * m;

    long long yearly = 0;
    for (auto x : drop) yearly += x;       // 一年总掉落

    long long years = (n - 1) / yearly;    // 可整年跳过的年数
    long long months = years * 12;
    long long rem = n - years * yearly;    // 剩余

    long long acc = 0;
    for (int i = 0; i < 12; ++i) {
        acc += drop[i];
        ++months;
        if (acc >= rem) {
            cout << months;
            return 0;
        }
    }
    return 0;
}
```