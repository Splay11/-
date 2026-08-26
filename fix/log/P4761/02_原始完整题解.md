## 解题思路

先设原字符串中大写字母的个数为 $cnt$。

每次操作只能把一个字符在大小写之间切换，因此会产生两种效果：

* 把一个小写字母变成大写字母，则大写字母数量 $+1$
* 把一个大写字母变成小写字母，则大写字母数量 $-1$

题目要求“恰好”进行 $k$ 次操作，并让最终大写字母数量尽可能多。

要想让大写字母数量尽量多，显然应优先把小写字母变成大写字母。设小写字母数量为

$$
low=n-cnt
$$

### 核心思路

分情况讨论：

#### 情况一：$k \le low$

说明操作次数不超过小写字母数量，那么这 $k$ 次操作都可以用于把小写变成大写。

最终答案就是：

$$
cnt+k
$$

#### 情况二：$k > low$

先把所有小写字母都变成大写，此时字符串已经全部是大写字母，共进行了 $low$ 次操作，当前大写字母数量为 $n$。

但题目要求恰好做满 $k$ 次，还剩下

$$
rem = k-low
$$

次操作。

这时字符串里已经没有小写字母了，只能对某个大写字母继续切换：

* 一次操作：大写 $\to$ 小写，大写数量减少 $1$
* 再一次操作：小写 $\to$ 大写，大写数量增加 $1$

也就是说，多出来的两次操作可以互相抵消，不影响最终答案。

因此只需要看 $rem$ 的奇偶性：

* 如果 $rem$ 是偶数，最终仍然可以保持全部大写，答案为 $n$
* 如果 $rem$ 是奇数，最后一定会有一个字符处于小写，答案为 $n-1$

### 实现方法

1. 遍历字符串，统计初始大写字母数量 $cnt$
2. 计算小写字母数量 $low=n-cnt$
3. 若 $k \le low$，输出 $cnt+k$
4. 否则计算 $rem=k-low$

   * 若 $rem$ 为偶数，输出 $n$
   * 若 $rem$ 为奇数，输出 $n-1$

这个方法只需一次遍历字符串即可完成，复杂度很优。

## 复杂度分析

遍历一次字符串统计大写字母数量即可，其余均为常数时间操作。

* 时间复杂度：$O(n)$
* 空间复杂度：$O(1)$


## 代码实现

### Python

```python
def max_uppercase_count(n, k, s):
    # 统计初始大写字母个数
    cnt = 0
    for ch in s:
        if 'A' <= ch <= 'Z':
            cnt += 1

    # 计算小写字母个数
    low = n - cnt

    # 如果操作次数不超过小写字母数量
    # 直接把这些小写字母变成大写即可
    if k <= low:
        return cnt + k

    # 先把所有小写字母变成大写后，还剩余 rem 次操作
    rem = k - low

    # 剩余操作为偶数，可以两两抵消，最终仍全部为大写
    if rem % 2 == 0:
        return n

    # 剩余操作为奇数，最终必然有一个字母为小写
    return n - 1


def main():
    # 读入 n 和 k
    n, k = map(int, input().split())

    # 读入字符串
    s = input().strip()

    # 输出答案
    print(max_uppercase_count(n, k, s))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {

    public static int maxUppercaseCount(int n, long k, String s) {
        // 统计初始大写字母个数
        int cnt = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch >= 'A' && ch <= 'Z') {
                cnt++;
            }
        }

        // 计算小写字母个数
        int low = n - cnt;

        // 如果操作次数不超过小写字母数量
        // 直接把这些小写字母变成大写即可
        if (k <= low) {
            return cnt + (int) k;
        }

        // 先把所有小写字母变成大写后，还剩余 rem 次操作
        long rem = k - low;

        // 剩余操作为偶数，可以两两抵消，最终仍全部为大写
        if (rem % 2 == 0) {
            return n;
        }

        // 剩余操作为奇数，最终必然有一个字母为小写
        return n - 1;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 读入 n 和 k
        int n = sc.nextInt();
        long k = sc.nextLong();

        // 读入字符串
        String s = sc.next();

        // 输出答案
        System.out.println(maxUppercaseCount(n, k, s));
    }
}
```

### C++

```cpp
#include <iostream>
#include <string>
using namespace std;

int maxUppercaseCount(int n, long long k, const string& s) {
    // 统计初始大写字母个数
    int cnt = 0;
    for (char ch : s) {
        if (ch >= 'A' && ch <= 'Z') {
            cnt++;
        }
    }

    // 计算小写字母个数
    int low = n - cnt;

    // 如果操作次数不超过小写字母数量
    // 直接把这些小写字母变成大写即可
    if (k <= low) {
        return cnt + (int)k;
    }

    // 先把所有小写字母变成大写后，还剩余 rem 次操作
    long long rem = k - low;

    // 剩余操作为偶数，可以两两抵消，最终仍全部为大写
    if (rem % 2 == 0) {
        return n;
    }

    // 剩余操作为奇数，最终必然有一个字母为小写
    return n - 1;
}

int main() {
    // 读入 n 和 k
    int n;
    long long k;
    cin >> n >> k;

    // 读入字符串
    string s;
    cin >> s;

    // 输出答案
    cout << maxUppercaseCount(n, k, s) << endl;

    return 0;
}
```