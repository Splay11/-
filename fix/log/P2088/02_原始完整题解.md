## 解题思路

设原串中 $01$ 子序列总数为 $ans$。

一个 $01$ 子序列本质上就是选一个位置上的 $0$ 作为前项，再选它后面的一个 $1$ 作为后项，所以可以理解为：

* 对每个位置 $i$：

  * 若 $s_i=0$，它对答案的贡献是它右侧 $1$ 的个数
  * 若 $s_i=1$，它本身不直接作为前项贡献，但会和左侧所有 $0$ 组成 $01$

题目要求把每个位置单独反置后，求新串中的 $01$ 子序列数量。

### 核心变化分析

假设反置位置为 $i$。

#### 情况 $1$：$s_i=0 \rightarrow 1$

原来这个位置是 $0$ 时，会贡献：

* 右侧 $1$ 的个数，记为 $rightOne[i]$

反置后这个位置变成 $1$，它不再作为前面的 $0$ 产生贡献，但会作为后面的 $1$，与左侧所有 $0$ 形成新的 $01$：

* 左侧 $0$ 的个数，记为 $leftZero[i]$

所以新答案为：

$$
ans - rightOne[i] + leftZero[i]
$$

#### 情况 $2$：$s_i=1 \rightarrow 0$

原来这个位置是 $1$，会与左侧所有 $0$ 组成 $01$：

* 左侧 $0$ 的个数为 $leftZero[i]$

反置后它变成 $0$，不再作为后面的 $1$，但会作为前面的 $0$，与右侧所有 $1$ 组成新的 $01$：

* 右侧 $1$ 的个数为 $rightOne[i]$

所以新答案为：

$$
ans - leftZero[i] + rightOne[i]
$$

### 如何预处理

为了快速计算每个位置反置后的答案，可以先预处理：

* $leftZero[i]$：位置 $i$ 左边有多少个 $0$
* $rightOne[i]$：位置 $i$ 右边有多少个 $1$

然后先求出原串总的 $01$ 子序列数 $ans$，再按上面的公式逐个输出即可。

这里用到的算法是：

* 前缀统计
* 后缀统计

这样就能在线性时间内解决问题。

## 复杂度分析

设字符串长度为 $n$。

* 预处理前缀和后缀数组需要 $O(n)$
* 计算原串的 $01$ 子序列总数需要 $O(n)$
* 枚举每个位置计算反置后的答案需要 $O(n)$

所以总时间复杂度为：

$$
O(n)
$$

空间复杂度为：

$$
O(n)
$$

在 $n \le 10^5$ 的范围内完全可行。

## 代码实现

### Python

```python
def solve(n, s):
    # left_zero[i] 表示位置 i 左侧 0 的个数
    left_zero = [0] * n
    cnt0 = 0
    for i in range(n):
        left_zero[i] = cnt0
        if s[i] == '0':
            cnt0 += 1

    # right_one[i] 表示位置 i 右侧 1 的个数
    right_one = [0] * n
    cnt1 = 0
    for i in range(n - 1, -1, -1):
        right_one[i] = cnt1
        if s[i] == '1':
            cnt1 += 1

    # 计算原串中 01 子序列总数
    total = 0
    for i in range(n):
        if s[i] == '0':
            total += right_one[i]

    # 计算每个位置反置后的答案
    res = [0] * n
    for i in range(n):
        if s[i] == '0':
            # 0 -> 1
            res[i] = total - right_one[i] + left_zero[i]
        else:
            # 1 -> 0
            res[i] = total - left_zero[i] + right_one[i]

    return res


if __name__ == "__main__":
    n = int(input())
    s = input().strip()
    ans = solve(n, s)
    print(*ans)
```

### Java

```java
import java.util.*;

public class Main {

    public static long[] solve(int n, String s) {
        // leftZero[i] 表示位置 i 左侧 0 的个数
        long[] leftZero = new long[n];
        long cnt0 = 0;
        for (int i = 0; i < n; i++) {
            leftZero[i] = cnt0;
            if (s.charAt(i) == '0') {
                cnt0++;
            }
        }

        // rightOne[i] 表示位置 i 右侧 1 的个数
        long[] rightOne = new long[n];
        long cnt1 = 0;
        for (int i = n - 1; i >= 0; i--) {
            rightOne[i] = cnt1;
            if (s.charAt(i) == '1') {
                cnt1++;
            }
        }

        // 计算原串中 01 子序列总数
        long total = 0;
        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == '0') {
                total += rightOne[i];
            }
        }

        // 计算每个位置反置后的答案
        long[] res = new long[n];
        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == '0') {
                // 0 -> 1
                res[i] = total - rightOne[i] + leftZero[i];
            } else {
                // 1 -> 0
                res[i] = total - leftZero[i] + rightOne[i];
            }
        }

        return res;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        String s = sc.next();

        long[] ans = solve(n, s);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i > 0) sb.append(' ');
            sb.append(ans[i]);
        }
        System.out.println(sb.toString());
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

vector<long long> solve(int n, const string &s) {
    // leftZero[i] 表示位置 i 左侧 0 的个数
    vector<long long> leftZero(n);
    long long cnt0 = 0;
    for (int i = 0; i < n; i++) {
        leftZero[i] = cnt0;
        if (s[i] == '0') {
            cnt0++;
        }
    }

    // rightOne[i] 表示位置 i 右侧 1 的个数
    vector<long long> rightOne(n);
    long long cnt1 = 0;
    for (int i = n - 1; i >= 0; i--) {
        rightOne[i] = cnt1;
        if (s[i] == '1') {
            cnt1++;
        }
    }

    // 计算原串中 01 子序列总数
    long long total = 0;
    for (int i = 0; i < n; i++) {
        if (s[i] == '0') {
            total += rightOne[i];
        }
    }

    // 计算每个位置反置后的答案
    vector<long long> res(n);
    for (int i = 0; i < n; i++) {
        if (s[i] == '0') {
            // 0 -> 1
            res[i] = total - rightOne[i] + leftZero[i];
        } else {
            // 1 -> 0
            res[i] = total - leftZero[i] + rightOne[i];
        }
    }

    return res;
}

int main() {
    int n;
    string s;
    cin >> n >> s;

    vector<long long> ans = solve(n, s);
    for (int i = 0; i < n; i++) {
        if (i > 0) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';

    return 0;
}
```