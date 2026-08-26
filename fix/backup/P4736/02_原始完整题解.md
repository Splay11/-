## 解题思路

* 核心思路
  本题关键在于**将问题转化为“总数 - 平衡数”**，并用组合数优化计数。

首先定义：

* 奇数字：1,3,5,7,9
* 偶数字：0,2,4,6,8

一个子序列是“不平衡数” ⇔ 奇数个数 ≠ 偶数个数
因此我们可以转化为：

> 不平衡数 = 所有合法子序列 - 奇偶数量相等的子序列



### 一、合法子序列定义（处理前导零）

根据样例可知：

* **子序列首位不能是 0**
* **但单个 "0" 视为合法数字**

因此合法子序列分两类：

1. 首位是非零数字的子序列
2. 单个 "0"



### 二、枚举首位，统计子序列

我们枚举每一个位置 i 作为子序列的起点：

* 若 s[i] ≠ '0'：可以作为合法子序列的首位
* 若 s[i] = '0'：只能作为单独的一个子序列

对于每个合法起点 i：

* 后面的字符可以任意选或不选 → 共 $2^{后缀长度}$ 种



### 三、如何统计“平衡子序列”（关键难点）

对于固定起点 i：

设：

* 后缀中奇数个数为 O
* 后缀中偶数个数为 E

再看起点：

* 若起点是奇数：初始奇数+1
* 若起点是偶数：初始偶数+1



#### 情况1：起点是奇数

要满足最终 奇数 = 偶数：

需要从后缀中选：

* x 个奇数
* x+1 个偶数

数量为：

$$
\sum \binom{O}{x}\binom{E}{x+1}
$$

利用范德蒙德恒等式可化简为：

$$
\binom{O+E}{E-1}
$$



#### 情况2：起点是偶数

同理可得：

需要：

* x 个偶数
* x+1 个奇数

结果为：

$$
\binom{O+E}{O-1}
$$



### 四、最终计算流程

1. 预处理：

   * 组合数 C(n,k)
   * 2 的幂
   * 后缀奇偶计数

2. 遍历每个位置：

   * 若是非零：

     * 加上所有子序列数
     * 减去平衡子序列数
   * 若是 0：

     * 单独统计一个子序列

3. 取模输出



## 复杂度分析

* 时间复杂度：
  预处理组合数为 $O(n^2)$，遍历为 $O(n)$
  总复杂度：**O(n^2)**

* 空间复杂度：
  组合数表为 $O(n^2)$
  其余为 $O(n)$
  总复杂度：**O(n^2)**



## 代码实现

### Python

```python
import sys

MOD = 10**9 + 7

# 计算组合数
def init_comb(n):
    C = [[0]*(n+1) for _ in range(n+1)]
    for i in range(n+1):
        C[i][0] = 1
        for j in range(1, i+1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD
    return C

# 主逻辑
def solve(n, s):
    C = init_comb(n)
    
    # 预处理2的幂
    pow2 = [1]*(n+1)
    for i in range(1, n+1):
        pow2[i] = pow2[i-1]*2 % MOD
    
    # 后缀奇偶计数
    suf_odd = [0]*(n+1)
    suf_even = [0]*(n+1)
    
    for i in range(n-1, -1, -1):
        suf_odd[i] = suf_odd[i+1]
        suf_even[i] = suf_even[i+1]
        if int(s[i]) % 2 == 1:
            suf_odd[i] += 1
        else:
            suf_even[i] += 1
    
    ans = 0
    
    for i in range(n):
        # 单独0
        if s[i] == '0':
            ans = (ans + 1) % MOD
            continue
        
        # 总子序列数
        total = pow2[n-i-1]
        
        O = suf_odd[i+1]
        E = suf_even[i+1]
        
        # 平衡数
        if int(s[i]) % 2 == 1:
            # 起点是奇数
            if E >= 1:
                bad = C[O+E][E-1]
            else:
                bad = 0
        else:
            # 起点是偶数
            if O >= 1:
                bad = C[O+E][O-1]
            else:
                bad = 0
        
        ans = (ans + total - bad) % MOD
    
    return ans

if __name__ == "__main__":
    n = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()
    print(solve(n, s))
```



### Java

```java
import java.util.*;

public class Main {
    static final int MOD = 1000000007;

    // 初始化组合数
    static long[][] initComb(int n) {
        long[][] C = new long[n+1][n+1];
        for (int i = 0; i <= n; i++) {
            C[i][0] = 1;
            for (int j = 1; j <= i; j++) {
                C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD;
            }
        }
        return C;
    }

    static long solve(int n, String s) {
        long[][] C = initComb(n);

        long[] pow2 = new long[n+1];
        pow2[0] = 1;
        for (int i = 1; i <= n; i++) {
            pow2[i] = pow2[i-1] * 2 % MOD;
        }

        int[] sufOdd = new int[n+1];
        int[] sufEven = new int[n+1];

        for (int i = n-1; i >= 0; i--) {
            sufOdd[i] = sufOdd[i+1];
            sufEven[i] = sufEven[i+1];
            int d = s.charAt(i) - '0';
            if (d % 2 == 1) sufOdd[i]++;
            else sufEven[i]++;
        }

        long ans = 0;

        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == '0') {
                ans = (ans + 1) % MOD;
                continue;
            }

            long total = pow2[n-i-1];
            int O = sufOdd[i+1];
            int E = sufEven[i+1];

            long bad = 0;
            int d = s.charAt(i) - '0';

            if (d % 2 == 1) {
                if (E >= 1) bad = C[O+E][E-1];
            } else {
                if (O >= 1) bad = C[O+E][O-1];
            }

            ans = (ans + total - bad + MOD) % MOD;
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        String s = sc.next();
        System.out.println(solve(n, s));
    }
}
```



### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

// 初始化组合数
vector<vector<long long>> initComb(int n) {
    vector<vector<long long>> C(n+1, vector<long long>(n+1, 0));
    for (int i = 0; i <= n; i++) {
        C[i][0] = 1;
        for (int j = 1; j <= i; j++) {
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD;
        }
    }
    return C;
}

long long solve(int n, string s) {
    auto C = initComb(n);

    vector<long long> pow2(n+1, 1);
    for (int i = 1; i <= n; i++) {
        pow2[i] = pow2[i-1] * 2 % MOD;
    }

    vector<int> sufOdd(n+1, 0), sufEven(n+1, 0);

    for (int i = n-1; i >= 0; i--) {
        sufOdd[i] = sufOdd[i+1];
        sufEven[i] = sufEven[i+1];
        int d = s[i] - '0';
        if (d % 2 == 1) sufOdd[i]++;
        else sufEven[i]++;
    }

    long long ans = 0;

    for (int i = 0; i < n; i++) {
        if (s[i] == '0') {
            ans = (ans + 1) % MOD;
            continue;
        }

        long long total = pow2[n-i-1];
        int O = sufOdd[i+1];
        int E = sufEven[i+1];

        long long bad = 0;
        int d = s[i] - '0';

        if (d % 2 == 1) {
            if (E >= 1) bad = C[O+E][E-1];
        } else {
            if (O >= 1) bad = C[O+E][O-1];
        }

        ans = (ans + total - bad + MOD) % MOD;
    }

    return ans;
}

int main() {
    int n;
    string s;
    cin >> n >> s;
    cout << solve(n, s) << endl;
    return 0;
}
```