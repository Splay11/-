## 解题思路

题目要求对于每个给定的正整数 $n$，找到两个正整数 $x,y$，满足：

* $x+y=2n$
* $x,y$ 都是合数
* 若不存在，输出 $-1$

先观察几个最小情况：

* $n=1$ 时，$2n=2$，不可能拆成两个正合数之和
* $n=2$ 时，$2n=4$，只能想到 $2+2$，但 $2$ 是质数，不是合数
* $n=3$ 时，$2n=6$，可尝试的合数组合没有满足条件的

所以当 $n \le 3$ 时，无解。

当 $n \ge 4$ 时，可以直接构造：

$$
x=4,\quad y=2n-4
$$

因为：

* $4$ 是合数
* 当 $n=4$ 时，$y=4$，也是合数
* 当 $n\ge 5$ 时，$y=2n-4=2(n-2)$，且 $n-2\ge 3$，所以 $y$ 是一个大于 $2$ 的偶数，一定是合数

因此，$n\ge 4$ 时总有解，直接输出 $4$ 和 $2n-4$ 即可。

这里使用的是构造算法，核心就是固定一个合数 $4$，再证明另一个数也一定是合数。

## 复杂度分析

每组数据只需要进行一次判断和一次构造，因此：

* 时间复杂度：$O(1)$
* 总时间复杂度：$O(T)$
* 空间复杂度：$O(1)$

该复杂度对于 $T \le 2\times 10^5$ 完全合适。

## 代码实现

### Python

```python
def solve_one(n):
    # 当 n<=3 时无解
    if n <= 3:
        return "-1"
    # 当 n>=4 时，直接构造 4 和 2n-4
    return f"4 {2 * n - 4}"


def main():
    # 读入数据
    T = int(input())
    ans = []

    for _ in range(T):
        n = int(input())
        ans.append(solve_one(n))

    # 按要求输出
    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {

    // 处理一组数据
    public static String solveOne(int n) {
        // 当 n<=3 时无解
        if (n <= 3) {
            return "-1";
        }
        // 当 n>=4 时，直接构造 4 和 2n-4
        return "4 " + (2 * n - 4);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 输入组数
        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < T; i++) {
            int n = sc.nextInt();
            sb.append(solveOne(n));
            if (i != T - 1) {
                sb.append('\n');
            }
        }

        // 输出答案
        System.out.print(sb.toString());
        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <string>
using namespace std;

// 处理一组数据
string solveOne(int n) {
    // 当 n<=3 时无解
    if (n <= 3) {
        return "-1";
    }
    // 当 n>=4 时，直接构造 4 和 2n-4
    return "4 " + to_string(2 * n - 4);
}

int main() {
    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;
        cout << solveOne(n) << '\n';
    }

    return 0;
}
```