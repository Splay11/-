## 解题思路

设选择出的非空子序列元素和为 $S$，目标是最大化 $S \bmod k$。

由于子序列只要求保持相对顺序，但求和与顺序无关，所以本题本质上就是：

从数组中选一个非空子集，使得其元素和对 $k$ 取模尽量大。

### 状态设计

只关心“某个模值能否被凑出来”。

设一个长度为 $k$ 的状态集合，若模值 $r$ 可达，则记为可行。

因为最终只需要知道哪些模值能达到，所以这是一个典型的“模意义下的子集和 DP”。

### 转移方式

若当前已经能得到一些模值，加入一个新数 $a_i$ 后，设

$
x = a_i \bmod k
$

那么原来能达到的每个模值 $r$，现在都可以转移到：

$
(r + x) \bmod k
$

这相当于把整张模值状态表“循环左移” $x$ 位。

另外，单独选这个数本身，也能得到模值 $x$。

于是每次更新就是：

* 保留原状态
* 把原状态循环左移 $x$ 位
* 再把单点 $x$ 加进去

### 为什么要用位运算 / 位集

如果直接做普通 DP，复杂度是 $O(nk)$，在本题数据范围下会偏大。

注意到 $k \le 2 \times 10^4$，而我们只是在维护 $k$ 个布尔状态，因此可以用位集压缩状态：

* 第 $r$ 位为 $1$，表示模值 $r$ 可达
* 循环左移就对应位运算
* 合并状态就是按位或

这样每次转移可以压成若干个机器字操作，复杂度更合适。

### 实现要点

为了保证“非空子序列”，状态初始化不能把 $0$ 直接设为可达，否则会把空集算进去。

所以我们令初始状态为空，然后对每个数做：

1. 计算 $x = a_i \bmod k$
2. 将当前状态循环左移 $x$
3. 与原状态合并
4. 把单独选择当前数得到的模值 $x$ 加入

最后从 $k-1$ 到 $0$ 倒序找第一个可达模值，就是答案。

## 复杂度分析

设本组数据长度为 $n$。

使用位集后，每次转移的代价约为 $O(\frac{k}{w})$，其中 $w$ 是机器字长，通常可看作 $64$。

因此总时间复杂度为：

$
O\left(n \times \frac{k}{w}\right)
$

空间复杂度为：

$
O\left(\frac{k}{w}\right)
$

在本题 $k \le 2 \times 10^4$，且单个测试文件的 $n$ 总和不超过 $6 \times 10^4$，这个复杂度是可以通过的。

## 代码实现

### Python

```python
import sys


# 计算循环左移后的结果，状态总长度为 k 位
def rotate_left(dp, shift, k, mask):
    shift %= k
    if shift == 0:
        return dp
    # 高位左移后截断到前 k 位，低位从右侧补回来
    return ((dp << shift) | (dp >> (k - shift))) & mask


# 返回最大可达的模值
def solve_case(n, k, arr):
    mask = (1 << k) - 1
    dp = 0  # dp 的第 r 位为 1，表示模值 r 可达；这里只维护非空子序列

    for num in arr:
        x = num % k
        shifted = rotate_left(dp, x, k, mask)
        dp |= shifted           # 选择当前数接在已有方案后面
        dp |= (1 << x)          # 单独选择当前数
        dp &= mask              # 只保留前 k 位

    # 从大到小找最大可达模值
    for ans in range(k - 1, -1, -1):
        if (dp >> ans) & 1:
            return ans
    return 0


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        k = data[idx + 1]
        idx += 2
        arr = data[idx:idx + n]
        idx += n
        out.append(str(solve_case(n, k, arr)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.math.BigInteger;
import java.util.*;

public class Main {

    // 计算在前 k 位范围内循环左移 shift 位
    static BigInteger rotateLeft(BigInteger dp, int shift, int k, BigInteger mask) {
        shift %= k;
        if (shift == 0) {
            return dp;
        }
        // 左移部分保留前 k 位，右移部分补到低位
        BigInteger left = dp.shiftLeft(shift).and(mask);
        BigInteger right = dp.shiftRight(k - shift);
        return left.or(right);
    }

    // 返回最大可达的模值
    static int solveCase(int n, int k, int[] arr) {
        BigInteger mask = BigInteger.ONE.shiftLeft(k).subtract(BigInteger.ONE);
        BigInteger dp = BigInteger.ZERO; // 只维护非空子序列状态

        for (int num : arr) {
            int x = num % k;
            BigInteger shifted = rotateLeft(dp, x, k, mask);
            dp = dp.or(shifted);   // 选择当前数接在已有方案后面
            dp = dp.setBit(x);     // 单独选择当前数
            dp = dp.and(mask);     // 只保留前 k 位
        }

        // 从大到小找最大可达模值
        for (int ans = k - 1; ans >= 0; ans--) {
            if (dp.testBit(ans)) {
                return ans;
            }
        }
        return 0;
    }

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        StringBuilder sb = new StringBuilder();

        while (t-- > 0) {
            int n = sc.nextInt();
            int k = sc.nextInt();
            int[] arr = new int[n];

            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }

            sb.append(solveCase(n, k, arr)).append('\n');
        }

        System.out.print(sb.toString());
        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <bitset>
using namespace std;

const int MAXK = 20005;

// 返回最大可达的模值
int solveCase(int n, int k, const vector<int>& arr) {
    bitset<MAXK> dp;    // dp[r] = 1 表示模值 r 可达，只维护非空子序列
    bitset<MAXK> mask;  // 只保留前 k 位

    for (int i = 0; i < k; i++) {
        mask.set(i);
    }

    for (int num : arr) {
        int x = num % k;

        // 循环左移 x 位：高位溢出的部分补到低位
        bitset<MAXK> shifted;
        if (x == 0) {
            shifted = dp;
        } else {
            shifted = ((dp << x) & mask) | (dp >> (k - x));
        }

        dp |= shifted;   // 选择当前数接在已有方案后面
        dp.set(x);       // 单独选择当前数
        dp &= mask;      // 只保留前 k 位
    }

    // 从大到小找最大可达模值
    for (int ans = k - 1; ans >= 0; ans--) {
        if (dp.test(ans)) {
            return ans;
        }
    }
    return 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, k;
        cin >> n >> k;
        vector<int> arr(n);

        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }

        cout << solveCase(n, k, arr) << '\n';
    }

    return 0;
}
```