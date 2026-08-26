## 解题思路

### 暴力枚举

1. 枚举所有断开位置 $k=0\ldots n-1$（按0-based下标处理更方便）。
2. 对于每个 $k$，线性扫描长度为 $n$ 的序列，累加求出$S_k$。
3. 取所有 $S_k$ 的最大值即为答案。

由于 $n\le2000$，双重循环最多做 $4\times10^6$ 次乘加运算，完全可行。

## 复杂度分析

- 枚举 $k$ 花费 $O(n)$，每次计算 $S_k$ 也花 $O(n)$，总 $O(n^2)$。  
当 $n\le2000$ 时，暴力法即可通过。

## 代码实现

### Python

```python
def max_magic(n, a):
    res = -10**18
    # 枚举断开位置 k（0-based）
    for k in range(n):
        S = 0
        sign = 1  # 用 1 或 -1 表示交替
        # 计算加权交替和
        for j in range(n):
            S += sign * (j+1) * a[(k+j) % n]
            sign *= -1
        res = max(res, S)
    return res

if __name__ == "__main__":
    n = int(input().strip())
    a = list(map(int, input().split()))
    print(max_magic(n, a))
```

### Java

```java
import java.util.*;

public class Main {
    // 计算最大魔法值
    static long maxMagic(int n, int[] a) {
        long ans = Long.MIN_VALUE;
        // 枚举断开位置 k
        for (int k = 0; k < n; k++) {
            long S = 0;
            int sign = 1; // 1 或 -1
            // 计算加权交替和
            for (int j = 0; j < n; j++) {
                S += sign * (long)(j + 1) * a[(k + j) % n];
                sign = -sign;
            }
            ans = Math.max(ans, S);
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }
        System.out.println(maxMagic(n, a));
        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 计算最大魔法值
long long maxMagic(int n, const vector<int>& a) {
    long long ans = LLONG_MIN;
    // 枚举断开位置 k
    for (int k = 0; k < n; k++) {
        long long S = 0;
        int sign = 1; // 交替符号
        // 加权交替求和
        for (int j = 0; j < n; j++) {
            S += sign * 1LL * (j + 1) * a[(k + j) % n];
            sign = -sign;
        }
        ans = max(ans, S);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    cout << maxMagic(n, a) << "\n";
    return 0;
}
```