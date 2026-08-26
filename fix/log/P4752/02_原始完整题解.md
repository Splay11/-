## 解题思路

你说得对，我上一版理解错题意了。

这题不是看二进制，而是看 $x$ 的十进制表示的第一位数字和最后一位数字是否相等。
例如 $1 \sim 10$ 中满足条件的是：

$1,2,3,4,5,6,7,8,9$

共 $9$ 个，所以样例输出确实应为 $9$。

这题适合用数学计数。

设 $f(n)$ 表示区间 $[1,n]$ 中，十进制首尾数字相等的数的个数，那么答案就是：

$f(r)-f(l-1)$

下面考虑如何求 $f(n)$。

对于位数小于当前数字位数的所有数：

* $1$ 位数共有 $9$ 个，全部满足
* 对于长度为 $len \ge 2$ 的数：

  * 首位可以选 $1 \sim 9$，共 $9$ 种
  * 末位必须和首位相同
  * 中间 $len-2$ 位可以随便填，共 $10^{len-2}$ 种

所以这部分贡献为：

$9 \times 10^{len-2}$

然后再统计与 $n$ 位数相同、且不超过 $n$ 的满足条件的数。

设 $n$ 的十进制串为 $s$，长度为 $m$。

* 首位记为 $first$
* 末位记为 $last$
* 中间部分记为 $mid$

对于长度为 $m$ 的合法数：

1. 若首位比 $first$ 小，那么这样的数一定小于 $n$
   共有：

   $(first-1)\times 10^{m-2}$

2. 若首位等于 $first$，那么只需要比较中间部分和末位

   * 中间部分比 $mid$ 小：一定合法
   * 中间部分等于 $mid$ 时，只有当 $last \ge first$ 才合法

因此长度为 $m$ 的贡献为：

$(first-1)\times 10^{m-2} + mid + [last \ge first]$

其中 $[condition]$ 表示条件成立时取 $1$，否则取 $0$。

这样就能在 $O(\log n)$ 时间内求出 $f(n)$。

这里使用的算法本质上是数学计数。

## 复杂度分析

设数字 $n$ 的位数为 $k$。

时间复杂度为 $O(k)$，其中 $k \le 19$，因为 $r \le 10^{18}$。

空间复杂度为 $O(k)$，主要是把数字转成字符串；若不计字符串也可视为 $O(1)$。

## 代码实现

### Python

```python
# 计算 1 到 n 中首尾数字相等的数字个数
def count_same(n):
    if n <= 0:
        return 0

    s = str(n)
    m = len(s)

    # 1 位数全部满足
    if m == 1:
        return n

    ans = 0

    # 先统计位数小于 m 的所有合法数字
    ans += 9  # 1 位数
    p = 1
    for length in range(2, m):
        ans += 9 * p
        p *= 10

    # 再统计位数等于 m 的合法数字
    first = int(s[0])
    last = int(s[-1])

    # 处理中间部分
    if m == 2:
        mid = 0
    else:
        mid = int(s[1:-1])

    # 首位比 first 小的情况
    ans += (first - 1) * (10 ** (m - 2))

    # 首位等于 first 的情况
    ans += mid
    if last >= first:
        ans += 1

    return ans


def main():
    l, r = map(int, input().split())
    print(count_same(r) - count_same(l - 1))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {

    // 计算 1 到 n 中首尾数字相等的数字个数
    public static long countSame(long n) {
        if (n <= 0) {
            return 0;
        }

        String s = String.valueOf(n);
        int m = s.length();

        // 1 位数全部满足
        if (m == 1) {
            return n;
        }

        long ans = 0;

        // 先统计位数小于 m 的所有合法数字
        ans += 9; // 1 位数
        long p = 1;
        for (int len = 2; len < m; len++) {
            ans += 9 * p;
            p *= 10;
        }

        // 再统计位数等于 m 的合法数字
        int first = s.charAt(0) - '0';
        int last = s.charAt(m - 1) - '0';

        // 处理中间部分
        long mid = 0;
        if (m > 2) {
            mid = Long.parseLong(s.substring(1, m - 1));
        }

        // 首位比 first 小的情况
        long pow = 1;
        for (int i = 0; i < m - 2; i++) {
            pow *= 10;
        }
        ans += (long) (first - 1) * pow;

        // 首位等于 first 的情况
        ans += mid;
        if (last >= first) {
            ans += 1;
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        long l = sc.nextLong();
        long r = sc.nextLong();

        System.out.println(countSame(r) - countSame(l - 1));
    }
}
```

### C++

```cpp
#include <iostream>
#include <string>
using namespace std;

// 计算 1 到 n 中首尾数字相等的数字个数
long long countSame(long long n) {
    if (n <= 0) {
        return 0;
    }

    string s = to_string(n);
    int m = (int)s.size();

    // 1 位数全部满足
    if (m == 1) {
        return n;
    }

    long long ans = 0;

    // 先统计位数小于 m 的所有合法数字
    ans += 9; // 1 位数
    long long p = 1;
    for (int len = 2; len < m; len++) {
        ans += 9 * p;
        p *= 10;
    }

    // 再统计位数等于 m 的合法数字
    int first = s[0] - '0';
    int last = s[m - 1] - '0';

    // 处理中间部分
    long long mid = 0;
    if (m > 2) {
        string midStr = s.substr(1, m - 2);
        mid = stoll(midStr);
    }

    // 计算 10^(m-2)
    long long pow10 = 1;
    for (int i = 0; i < m - 2; i++) {
        pow10 *= 10;
    }

    // 首位比 first 小的情况
    ans += 1LL * (first - 1) * pow10;

    // 首位等于 first 的情况
    ans += mid;
    if (last >= first) {
        ans += 1;
    }

    return ans;
}

int main() {
    long long l, r;
    cin >> l >> r;

    cout << countSame(r) - countSame(l - 1) << endl;
    return 0;
}
```