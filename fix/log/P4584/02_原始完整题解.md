## 解题思路

### 问题转化

设最终把整数 $n$ 拆成了：

* $x$ 个素数 $2$
* $y$ 个奇素数

因为 $2$ 是唯一的偶素数，其余素数都是奇数。

题目要求奇素数的个数必须是 $m$ 的倍数，因此有：

$$
y = km \quad (k \ge 1)
$$

注意这里 $y$ 不能为 $0$，因为题目要求奇素数个数是 $m$ 的倍数，结合样例可以看出这里要求的是正整数倍，否则很多本应无解的情况会被错误判成有解。



### 为什么要尽量多用 2

要让拆出的素数总个数最多，就应该尽量让每个素数尽可能小。

最小的素数是 $2$，最小的奇素数是 $3$。
所以如果奇素数个数固定为 $y$，那么最优方案一定是：

* 这 $y$ 个奇素数全部取最小值 $3$
* 剩余部分全部拆成 $2$

这样素数总个数最多。

于是总和可以写成：

$$
n = 2x + 3y
$$

因此：

$$
x = \frac{n - 3y}{2}
$$

总素数个数为：

$$
k = x + y = \frac{n - 3y}{2} + y = \frac{n - y}{2}
$$

所以在合法的前提下，**$y$ 越小，总个数越大**。

问题就变成了：

> 找到最小的合法 $y$，然后直接计算答案。



### 合法的 $y$ 需要满足什么条件

#### 1. 必须是 $m$ 的正整数倍

$$
y = m, 2m, 3m, \dots
$$

#### 2. 必须满足奇偶性要求

因为：

* $2x$ 一定是偶数
* $3y$ 的奇偶性和 $y$ 相同

所以要使

$$
n = 2x + 3y
$$

成立，必须满足：

$$
y \equiv n \pmod 2
$$

也就是说，**奇素数个数 $y$ 的奇偶性必须和 $n$ 相同**。

#### 3. 奇素数最小总和不能超过 $n$

每个奇素数至少是 $3$，所以：

$$
3y \le n
$$



### 分类讨论

现在只需要求最小合法的 $y$。

#### 情况一：$m$ 是奇数

$m$ 的倍数有奇有偶：

* 当倍数是奇数倍时，$y$ 为奇数
* 当倍数是偶数倍时，$y$ 为偶数

所以此时总能通过调整倍数，使 $y$ 与 $n$ 同奇偶：

* 如果 $n$ 和 $m$ 同奇偶，那么最小合法值是

$$
y = m
$$

* 否则最小合法值是

$$
y = 2m
$$

#### 情况二：$m$ 是偶数

$m$ 的所有正整数倍都一定是偶数。
所以此时：

* 如果 $n$ 是奇数，那么 $y$ 不可能与 $n$ 同奇偶，**无解**
* 如果 $n$ 是偶数，那么最小合法值就是

$$
y = m
$$



### 最终做法

1. 先判断是否出现 $m$ 为偶数且 $n$ 为奇数的情况
   若是，则直接无解，输出 $-1$

2. 否则求最小合法的 $y$

   * 若 $n$ 和 $m$ 同奇偶，则 $y=m$
   * 否则 $y=2m$

3. 检查是否满足

$$
3y \le n
$$

若不满足，说明连最小的 $y$ 个奇素数都放不下，无解，输出 $-1$

4. 否则答案为

$$
\frac{n-y}{2}
$$



## 复杂度分析

每组数据只需要进行常数次判断和计算。

* 时间复杂度：

$$
O(1)
$$

* 空间复杂度：

$$
O(1)
$$


## 代码实现

### Python

```python
def solve_one(n, m):
    # 如果 m 是偶数，那么 y 只能取 m 的倍数，也就一定是偶数
    # 若 n 是奇数，则不可能满足 y 与 n 同奇偶，直接无解
    if m % 2 == 0 and n % 2 == 1:
        return -1

    # 计算最小合法的 y
    # y 需要是 m 的正整数倍，且与 n 同奇偶
    if n % 2 == m % 2:
        y = m
    else:
        y = 2 * m

    # 每个奇素数至少为 3，所以总和至少为 3y
    # 如果 3y 已经超过 n，则无解
    if 3 * y > n:
        return -1

    # 固定 y 后，最优方案是 y 个 3，剩下全部用 2
    # 此时总个数为 (n - y) // 2
    return (n - y) // 2


if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        print(solve_one(n, m))
```

### Java

```java
import java.util.Scanner;

public class Main {

    public static long solveOne(long n, long m) {
        // 如果 m 是偶数，那么 y 只能取偶数
        // 若 n 是奇数，则不可能满足 y 与 n 同奇偶
        if (m % 2 == 0 && n % 2 == 1) {
            return -1;
        }

        long y;

        // 计算最小合法的 y
        if (n % 2 == m % 2) {
            y = m;
        } else {
            y = 2 * m;
        }

        // 判断最小奇素数和是否超过 n
        if (3 * y > n) {
            return -1;
        }

        // 返回最大素数个数
        return (n - y) / 2;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();
        while (t-- > 0) {
            long n = sc.nextLong();
            long m = sc.nextLong();
            System.out.println(solveOne(n, m));
        }

        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
using namespace std;

long long solveOne(long long n, long long m) {
    // 如果 m 是偶数，那么 y 只能取偶数
    // 若 n 是奇数，则不可能满足 y 与 n 同奇偶
    if (m % 2 == 0 && n % 2 == 1) {
        return -1;
    }

    long long y;

    // 计算最小合法的 y
    if (n % 2 == m % 2) {
        y = m;
    } else {
        y = 2 * m;
    }

    // 判断最小奇素数和是否超过 n
    if (3 * y > n) {
        return -1;
    }

    // 返回最大素数个数
    return (n - y) / 2;
}

int main() {
    int t;
    cin >> t;

    while (t--) {
        long long n, m;
        cin >> n >> m;
        cout << solveOne(n, m) << '\n';
    }

    return 0;
}
```