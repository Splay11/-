## 解题思路

### 问题分析
我们需要统计字符串 `t` 的所有**非空**子序列，满足以下两点才算有效：

1. **无前导零**：除单个字符 `"0"` 以外，不允许以 `'0'` 开头。
2. **数字和可被 5 整除**。

对每个有效子序列，根据其首位和末位数字分别给分：
- 若首位是质数 {2,3,5,7} 且末位是偶数 → **4 分**  
- 若首位是质数 → **3 分**  
- 其它 → **1 分**

由于 |t| 可达 $10^5$，枚举所有子序列显然不可能。我们需要 **O(n)** 或 **O(n·常数)** 的做法。

### 动态规划
我们按从左到右扫描字符，用两个长度为 5 的数组维护截至当前位置的统计：

- `dp[r]`：目前所有已选子序列（首位≠'0'）其数字和 mod 5 等于 `r` 的**数量**。
- `dpP[r]`：上述子序列中，**首位**是质数的子序列数量。

每读入一个新字符 `d`（数字 0–9）时，我们分两步处理：

1. **单字符子序列**：
   - 若 `d=='0'`，单个 `"0"` 是合法的，但不参与后续扩展；否则它首位≠0，记作一个新序列加入 `dp[d%5]`。
   - 如果 `d%5==0`，它本身是有效子序列，根据首/末位给分，累加到答案。

2. **扩展已有子序列**：
   - 旧的每个余数 `r` 对应的 `dp[r]` 序列都可以在末尾追加 `d`，新余数 `r2=(r+d)%5`。
   - 这部分新序列保留原先的“首位质数”标记：`dpP[r]` 个质数首位，`dp[r]-dpP[r]` 个非质数首位。
   - 如果 `r2==0`，它们是有效子序列，按末位 `d` 的奇偶和首位是否质数计算分值，累加到答案。
   - 最后把这些扩展加入 `dp[r2]` 与 `dpP[r2]`。

整个过程每个字符只做 O(5) 的循环，合计 O(5n)=O(n)。

### 复杂度分析
- **时间复杂度**：O(n)，其中 n=|t|，每步只更新常数大小的数组。
- **空间复杂度**：O(1)，只用大小为 5 的几个数组，常数级额外空间。

## 代码

### Python

```python
MOD = 10**9 + 7

def solve(t: str) -> int:
    dp = [0] * 5        # dp[r]: 首位≠0 的子序列中 sum%5==r 的数量
    dpP = [0] * 5       # dpP[r]: 其中首位是质数(2,3,5,7) 的数量
    primes = {'2','3','5','7'}
    ans = 0

    for ch in t:
        d = ord(ch) - ord('0')
        isP = ch in primes
        # 1. 单字符子序列
        if d % 5 == 0:
            # 单个 '0' 或 非零且 sum%5==0
            if ch == '0':
                # 单零合法，首位非质数
                ans = (ans + 1) % MOD
            else:
                # 非零单字符，首位是质数得3或4分
                if isP:
                    # 如果是2(偶)，首/末质数+偶=4，否则+3
                    ans = (ans + (4 if d % 2 == 0 else 3)) % MOD
                else:
                    ans = (ans + 1) % MOD
        # 2. 扩展已有子序列
        add_dp = [0] * 5
        add_dpP = [0] * 5
        for r in range(5):
            cnt = dp[r]
            if cnt == 0:
                continue
            cntP = dpP[r]
            r2 = (r + d) % 5
            # 2.1 先统计分数
            if r2 == 0:
                # 首位是质数的 cntP 条
                if d % 2 == 0:
                    ans = (ans + cntP * 4) % MOD
                else:
                    ans = (ans + cntP * 3) % MOD
                # 首位非质数的
                ans = (ans + (cnt - cntP) * 1) % MOD
            # 2.2 再把这些扩展加入新 dp
            add_dp[r2] = (add_dp[r2] + cnt) % MOD
            add_dpP[r2] = (add_dpP[r2] + cntP) % MOD

        # 合并 dp 更新
        for r in range(5):
            dp[r] = (dp[r] + add_dp[r]) % MOD
            dpP[r] = (dpP[r] + add_dpP[r]) % MOD

        # 3. 单字符加入 dp（首位≠0，才能扩展）
        if ch != '0':
            r0 = d % 5
            dp[r0] = (dp[r0] + 1) % MOD
            if isP:
                dpP[r0] = (dpP[r0] + 1) % MOD

    return ans

if __name__ == "__main__":
    print(solve(input().strip()))
```

### Java

```java
import java.io.*;

public class Main {
    static final int MOD = 1000000007;
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String t = br.readLine().trim();
        // dp[r]: 首位≠'0' 的子序列 sum%5==r 的数量
        long[] dp = new long[5];
        long[] dpP = new long[5]; // dpP[r]: 其中首位是质数的数量
        String primes = "2357";
        long ans = 0;

        for (char ch : t.toCharArray()) {
            int d = ch - '0';
            boolean isP = primes.indexOf(ch) >= 0;
            // 单字符
            if (d % 5 == 0) {
                if (ch == '0') {
                    ans = (ans + 1) % MOD;
                } else if (isP) {
                    ans = (ans + (d % 2 == 0 ? 4 : 3)) % MOD;
                } else {
                    ans = (ans + 1) % MOD;
                }
            }
            // 扩展已有
            long[] add = new long[5], addP = new long[5];
            for (int r = 0; r < 5; r++) {
                long cnt = dp[r];
                if (cnt == 0) continue;
                long cntP = dpP[r];
                int r2 = (r + d) % 5;
                if (r2 == 0) {
                    if (d % 2 == 0) ans = (ans + cntP * 4) % MOD;
                    else ans = (ans + cntP * 3) % MOD;
                    ans = (ans + (cnt - cntP)) % MOD;
                }
                add[r2] = (add[r2] + cnt) % MOD;
                addP[r2] = (addP[r2] + cntP) % MOD;
            }
            for (int r = 0; r < 5; r++) {
                dp[r] = (dp[r] + add[r]) % MOD;
                dpP[r] = (dpP[r] + addP[r]) % MOD;
            }
            // 单字符加入 dp（首位≠0）
            if (ch != '0') {
                int r0 = d % 5;
                dp[r0] = (dp[r0] + 1) % MOD;
                if (isP) dpP[r0] = (dpP[r0] + 1) % MOD;
            }
        }
        System.out.println(ans);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 1e9+7;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    string t;
    cin >> t;
    // dp[r]: 首位≠'0' 的子序列 sum%5==r 的数量
    long long dp[5]={0}, dpP[5]={0};
    auto isPrimeDigit = [&](char c){
        return c=='2'||c=='3'||c=='5'||c=='7';
    };
    long long ans = 0;

    for(char ch: t){
        int d = ch - '0';
        bool isP = isPrimeDigit(ch);
        // 单字符
        if(d % 5 == 0){
            if(ch=='0'){
                ans = (ans + 1) % MOD;
            } else if(isP){
                ans = (ans + (d%2==0 ? 4 : 3)) % MOD;
            } else {
                ans = (ans + 1) % MOD;
            }
        }
        // 扩展已有
        long long add[5]={0}, addP[5]={0};
        for(int r=0; r<5; r++){
            long long cnt = dp[r];
            if(!cnt) continue;
            long long cntP = dpP[r];
            int r2 = (r + d) % 5;
            if(r2==0){
                ans = (ans + cntP * (d%2==0 ? 4 : 3)) % MOD;
                ans = (ans + (cnt - cntP)) % MOD;
            }
            add[r2] = (add[r2] + cnt) % MOD;
            addP[r2] = (addP[r2] + cntP) % MOD;
        }
        for(int r=0; r<5; r++){
            dp[r] = (dp[r] + add[r]) % MOD;
            dpP[r] = (dpP[r] + addP[r]) % MOD;
        }
        // 单字符加入 dp（首位≠0）
        if(ch!='0'){
            int r0 = d % 5;
            dp[r0] = (dp[r0] + 1) % MOD;
            if(isP) dpP[r0] = (dpP[r0] + 1) % MOD;
        }
    }

    cout << ans << "\n";
    return 0;
}
```