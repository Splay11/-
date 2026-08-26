## 解题思路

定义长度为 $n$ 的数组 ${a_1,a_2,\dots,a_n}$ 为回文数组，当且仅当对所有 $1 \le i \le n$ 都有：

$ a_i = a_{n-i+1} $

现在要判断：对于所有满足 $m \ge n$ 的正整数 $m$，是否都存在一个长度为 $n$ 的回文数组，使得：

* 所有元素都是正整数
* 所有元素之和恰好等于 $m$

这是一道数学构造 + 奇偶性判断题。

先看回文数组的和有什么特点：

* 当 $n$ 为偶数时，数组中的元素一定成对出现
* 例如长度为 $4$ 时，形式一定是 $[x,y,y,x]$
* 因此总和一定是：

$ 2x + 2y = 2(x+y) $

也就是偶数

所以如果 $n$ 是偶数，那么无论怎么构造，回文数组元素和都只能是偶数。
但题目要求对所有 $m \ge n$ 都能构造，而 $m \ge n$ 中一定既有奇数也有偶数，因此不可能全部满足。

再看 $n$ 为奇数时：

* 回文数组两边仍然是成对出现
* 中间有一个单独的位置可以自由调整
* 例如长度为 $5$ 时，可以写成：

$ [1,1,x,1,1] $

此时总和为：

$ 4 + x $

因为所有元素必须为正整数，所以先把两边都放成 $1$，前 $n-1$ 个位置总和固定为 $n-1$，中间位置放：

$ x = m - (n-1) $

由于 $m \ge n$，所以：

$ x = m-n+1 \ge 1 $

满足正整数要求。

这说明当 $n$ 为奇数时，任意 $m \ge n$ 都可以构造出来。

所以结论为：

* $n$ 为奇数，输出 $Yes$
* $n$ 为偶数，输出 $No$

实现时只需要判断 $n$ 的奇偶性即可，使用的核心算法就是奇偶性判断。

## 复杂度分析

每组数据只需要判断一次 $n \bmod 2$：

* 时间复杂度：$O(1)$
* 空间复杂度：$O(1)$

总时间复杂度为 $O(t)$，其中 $t$ 为测试数据组数。

## 代码实现

### Python

```python
def solve(n):
    # 奇数长度一定可以，偶数长度一定不可以
    return "Yes" if n % 2 == 1 else "No"


if __name__ == "__main__":
    # 读取测试组数
    t = int(input())
    
    # 逐组处理
    for _ in range(t):
        n = int(input())
        print(solve(n))
```

### Java

```java
import java.util.Scanner;

public class Main {
    // 判断当前 n 是否满足条件
    public static String solve(long n) {
        // 奇数返回 Yes，偶数返回 No
        return (n % 2 == 1) ? "Yes" : "No";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 读取测试组数
        int t = sc.nextInt();

        // 逐组输出答案
        while (t-- > 0) {
            long n = sc.nextLong();
            System.out.println(solve(n));
        }

        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
using namespace std;

// 判断当前 n 是否满足条件
string solve(long long n) {
    // 奇数返回 Yes，偶数返回 No
    return (n % 2 == 1) ? "Yes" : "No";
}

int main() {
    int t;
    cin >> t;  // 读取测试组数

    while (t--) {
        long long n;
        cin >> n;
        cout << solve(n) << '\n';
    }

    return 0;
}
```