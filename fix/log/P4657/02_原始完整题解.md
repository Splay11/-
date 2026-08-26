## 解题思路

这是一道构造题，目标是对每个给定的 $n$，构造两个不同的正整数 $x,y$，满足：

$$
1 \le x,y < n,\quad x \ne y,\quad n \bmod x = n \bmod y
$$

如果无法构造，则输出 $-1$。

### 关键观察

题目只要求输出任意一组合法解，所以不需要枚举所有可能，也不需要使用哈希或暴力比较余数。
我们只要找到一个稳定可行的构造方法即可，这里使用的是构造算法。

### 情况一：$n$ 是偶数

当 $n$ 为偶数且 $n \ge 4$ 时，可以直接取：

$$
x = 1,\quad y = 2
$$

因为：

* $n \bmod 1 = 0$
* $n$ 是偶数，所以 $n \bmod 2 = 0$

于是有：

$$
n \bmod 1 = n \bmod 2 = 0
$$

并且 $1,2<n$，当 $n \ge 4$ 时显然成立。



### 情况二：$n$ 是奇数

当 $n$ 为奇数且 $n \ge 5$ 时，可以直接取：

$$
x = 2,\quad y = n-1
$$

因为：

* $n$ 是奇数，所以 $n \bmod 2 = 1$
* 对于 $y=n-1$，有
  $$
  n = 1 \cdot (n-1) + 1
  $$
  所以
  $$
  n \bmod (n-1) = 1
  $$

于是：

$$
n \bmod 2 = n \bmod (n-1) = 1
$$

并且当 $n \ge 5$ 时，$2 < n$ 且 $n-1 < n$，二者不同，构造合法。



### 无解情况

只剩下很小的几个数需要单独判断：

* $n=1$：没有满足 $1 \le x,y < 1$ 的正整数
* $n=2$：只有 $x=1$，无法选出两个不同的数
* $n=3$：只能选 $1,2$

  * $3 \bmod 1 = 0$
  * $3 \bmod 2 = 1$
    二者不相等，因此无解

所以无解当且仅当：

$$
n \le 3
$$



### 核心思路总结

这题的核心是分类构造：

* 若 $n \le 3$，输出 $-1$
* 若 $n$ 为偶数，输出 $1\ 2$
* 若 $n$ 为奇数，输出 $2\ (n-1)$

整个过程不需要枚举，不需要试答案，直接按照构造输出即可。

## 复杂度分析

对于每组测试数据，只进行常数次判断与输出，因此：

* 时间复杂度：$O(1)$
* 空间复杂度：$O(1)$


## 代码实现

### Python

```python
import sys


def solve_one(n):
    # 当 n<=3 时，不存在两个不同的正整数 x,y 且都小于 n
    if n <= 3:
        return "-1"

    # 当 n 为偶数时，取 x=1,y=2
    # 因为 n mod 1=0，且偶数 n mod 2=0
    if n % 2 == 0:
        return "1 2"

    # 当 n 为奇数且 n>=5 时，取 x=2,y=n-1
    # 因为奇数 n mod 2=1，且 n mod (n-1)=1
    return f"2 {n - 1}"


def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    ans = []
    idx = 1

    for _ in range(t):
        n = int(data[idx])
        idx += 1
        ans.append(solve_one(n))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {

    public static String solveOne(long n) {
        // 当 n<=3 时，无解
        if (n <= 3) {
            return "-1";
        }

        // 当 n 为偶数时，构造 x=1,y=2
        // 此时 n mod 1=0，n mod 2=0
        if (n % 2 == 0) {
            return "1 2";
        }

        // 当 n 为奇数且 n>=5 时，构造 x=2,y=n-1
        // 此时 n mod 2=1，n mod (n-1)=1
        return "2 " + (n - 1);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int T = Integer.parseInt(br.readLine().trim());

        for (int i = 0; i < T; i++) {
            long n = Long.parseLong(br.readLine().trim());
            sb.append(solveOne(n)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <iostream>
#include <string>
using namespace std;

string solveOne(long long n) {
    // 当 n<=3 时，无解
    if (n <= 3) {
        return "-1";
    }

    // 当 n 为偶数时，构造 x=1,y=2
    // 因为 n mod 1=0，且偶数 n mod 2=0
    if (n % 2 == 0) {
        return "1 2";
    }

    // 当 n 为奇数且 n>=5 时，构造 x=2,y=n-1
    // 因为奇数 n mod 2=1，且 n mod (n-1)=1
    return "2 " + to_string(n - 1);
}

int main() {
    int T;
    cin >> T;

    while (T--) {
        long long n;
        cin >> n;
        cout << solveOne(n) << '\n';
    }

    return 0;
}
```