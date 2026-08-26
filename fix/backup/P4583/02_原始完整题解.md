## 解题思路

题目要求输出 $n!$ 的个位数字，其中

$$
n! = 1 \times 2 \times 3 \times \cdots \times n
$$

如果直接把 $1$ 到 $n$ 全部乘起来，再取个位，虽然思路简单，但当 $n$ 很大时没有必要这样做。

这道题的关键在于观察阶乘个位数的变化规律，核心算法是 数学规律分析。

当 $n \ge 5$ 时，阶乘中一定同时包含因子 $2$ 和 $5$，而

$$
2 \times 5 = 10
$$

只要乘积中出现因子 $10$，个位数字就一定是 $0$。并且对于 $n!$ 来说，$n \ge 5$ 时一定满足这一条件，所以：

* 当 $n = 1$ 时，$1! = 1$，个位是 $1$
* 当 $n = 2$ 时，$2! = 2$，个位是 $2$
* 当 $n = 3$ 时，$3! = 6$，个位是 $6$
* 当 $n = 4$ 时，$4! = 24$，个位是 $4$
* 当 $n \ge 5$ 时，个位一定是 $0$

因此，实现方法非常直接：

1. 读入整数 $n$
2. 如果 $n \ge 5$，直接输出 $0$
3. 否则根据 $n$ 的值返回对应答案即可

这种做法不需要真的计算阶乘，效率非常高，也完全满足数据范围要求。

## 复杂度分析

由于整个过程只进行了有限次判断，没有循环和递归，因此：

* 时间复杂度：$O(1)$
* 空间复杂度：$O(1)$

该复杂度非常合适，能够轻松处理 $1 \le n \le 10^9$ 的数据范围。

## 代码实现

### Python

```python
def get_last_digit(n):
    # 当 n 大于等于 5 时，n! 一定含有因子 10，个位为 0
    if n >= 5:
        return 0

    # 处理 n 小于 5 的情况
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 6
    return 4


def main():
    # 读入整数 n
    n = int(input())

    # 输出 n! 的个位数字
    print(get_last_digit(n))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {

    public static int getLastDigit(int n) {
        // 当 n 大于等于 5 时，n! 一定含有因子 10，个位为 0
        if (n >= 5) {
            return 0;
        }

        // 处理 n 小于 5 的情况
        if (n == 1) {
            return 1;
        }
        if (n == 2) {
            return 2;
        }
        if (n == 3) {
            return 6;
        }
        return 4;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 读入整数 n
        int n = sc.nextInt();

        // 输出 n! 的个位数字
        System.out.println(getLastDigit(n));
    }
}
```

### C++

```cpp
#include <iostream>
using namespace std;

int getLastDigit(int n) {
    // 当 n 大于等于 5 时，n! 一定含有因子 10，个位为 0
    if (n >= 5) {
        return 0;
    }

    // 处理 n 小于 5 的情况
    if (n == 1) {
        return 1;
    }
    if (n == 2) {
        return 2;
    }
    if (n == 3) {
        return 6;
    }
    return 4;
}

int main() {
    // 读入整数 n
    int n;
    cin >> n;

    // 输出 n! 的个位数字
    cout << getLastDigit(n) << endl;

    return 0;
}
```