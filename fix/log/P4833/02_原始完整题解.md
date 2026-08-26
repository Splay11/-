## 解题思路

设两种彩票面值分别为$ n $和$ n+1 $，商品价格为$ m $。

如果一共买了$ k $张彩票，那么总金额最少是全买$ n $元时的

$ kn $

总金额最多是全买$ n+1 $元时的

$ k(n+1) $

并且因为每把一张$ n $元换成一张$ n+1 $元，总金额就恰好增加$ 1 $，所以买$ k $张彩票时，能够凑出的所有金额是一个连续区间：

$ [kn,\ k(n+1)] $

因此问题就变成：

* 找到最小的$ k $，使得区间右端点$ k(n+1) \ge m $
* 此时：

  * 如果$ m \ge kn $，说明$ m $就在这个区间里，可以刚好支付，答案是$ 0 $
  * 如果$ m < kn $，说明这个区间里不小于$ m $的最小值就是$ kn $，答案是$ kn-m $

所以先取最小的张数：

$ k=\left\lceil \dfrac{m}{n+1} \right\rceil $

再计算答案：

$ \max(0,\ kn-m) $

这里用到的算法本质是数学推导 + 贪心：
优先让彩票张数尽量少，因为张数越少，对应区间整体越靠左，更容易得到最小的“不少于$ m $”的金额。

## 复杂度分析

每组数据只需要进行常数次计算。

* 时间复杂度：$ O(1) $
* 空间复杂度：$ O(1) $

## 代码实现

### Python

```python
# 计算每组数据的最少多付金额
def solve_one(n, m):
    # 最少需要的彩票张数，向上取整
    k = (m + n) // (n + 1)
    # 返回最少多付的钱
    return max(0, k * n - m)


def main():
    # 读取组数
    t = int(input())
    for _ in range(t):
        # 读取 n 和 m
        n, m = map(int, input().split())
        print(solve_one(n, m))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {

    // 计算每组数据的最少多付金额
    public static long solveOne(long n, long m) {
        // 最少需要的彩票张数，向上取整
        long k = (m + n) / (n + 1);
        // 返回最少多付的钱
        return Math.max(0L, k * n - m);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 读取组数
        int t = sc.nextInt();
        while (t-- > 0) {
            // 读取 n 和 m
            long n = sc.nextLong();
            long m = sc.nextLong();

            // 输出答案
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

// 计算每组数据的最少多付金额
long long solveOne(long long n, long long m) {
    // 最少需要的彩票张数，向上取整
    long long k = (m + n) / (n + 1);
    // 返回最少多付的钱
    return max(0LL, k * n - m);
}

int main() {
    int t;
    cin >> t; // 读取组数

    while (t--) {
        long long n, m;
        cin >> n >> m; // 读取 n 和 m

        // 输出答案
        cout << solveOne(n, m) << '\n';
    }

    return 0;
}
```