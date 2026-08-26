## 题面描述

给定一个长度为 $n$ 的数组 $a$，其中每个元素 $a_i$ 满足 $1 \le a_i \le n$。定义一个子序列的**权值**如下：

- 如果这个子序列不是**严格递增**的，那么它的权值为 $0$。  
- 如果这个子序列是严格递增的，并且恰好是一个“排列子序列”（即：子序列本身的元素恰好构成 $\{1,2,\dots,k\}$ 的一个排列，且由于必须严格递增，因此只能是 $[1,2,\dots,k]$ 的形式），那么它的权值定义为该子序列的长度 $k$。  

现在，我们要计算：数组 $a$ 中，所有满足上述“排列子序列”条件的子序列，它们的权值之和。最后结果需对 $10^9+7$ 取模。


## 思路与问题本质分析

### 问题本质

1. **什么是“排列子序列”？**  
   若子序列长度为 $k$，要满足它能表示为 $\{1,2,\dots,k\}$ 的某个排列。但题目额外要求子序列必须**严格递增**，因此这样的子序列只能是 **严格递增的 $[1,2,\dots,k]$**。也就是说，一个子序列想要贡献权值 $k$，它的内容必须正好是按顺序出现的 $1,2,\dots,k$。

2. **如何统计？**  
   要数清数组 $a$ 中，出现了多少次子序列 $[1,2,\dots,k]$。子序列不要求连续，但顺序不能乱：  
   - 先从 $a$ 中某些位置选出一个“1”，  
   - 再从它之后的某些位置选一个“2”，  
   - 再选“3”，以此类推，直到“$k$”。  
   只要能按顺序找出 $1,2,\dots,k$ 这些值，我们就得到一个有效的子序列 $[1,2,\dots,k]$。

3. **动态规划思路**  
   我们定义一个 DP 数组 $\text{dp}[x]$，表示在读到当前位置之前，能形成子序列 $[1,2,\dots,x]$ 的**总个数**。我们从左到右遍历数组 $a$ 的每个元素 $v$：  
   - 如果 $v = 1$，那么就可以新增一种只包含“1”的子序列，所以 $\text{dp}[1]$ 要加 $1$。  
   - 如果 $v > 1$，那么它可以把所有 $[1,2,\dots,v-1]$ 的子序列继续扩展出一个 $[1,2,\dots,v]$。因此 $\text{dp}[v] += \text{dp}[v-1]$。  
   - 每一步都对结果取模，以免溢出。

   遍历结束后，$\text{dp}[x]$ 就是数组中能找到的子序列 $[1,2,\dots,x]$ 的数量。然后**权值和**就是  
   $\sum_{x=1}^{n} x \times \text{dp}[x].$  
   最终再对 $10^9+7$ 取模。

## cpp
```cpp
#include <bits/stdc++.h>
using namespace std;

static const long long MOD = 1000000007;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; // 测试组数
    cin >> T;
    while(T--){
        int n; 
        cin >> n;
        vector<int> a(n);
        for(int i = 0; i < n; i++){
            cin >> a[i];
        }

        // dp[x] 表示子序列 [1,2,...,x] 的个数
        vector<long long> dp(n+1, 0LL);

        for(int i = 0; i < n; i++){
            int v = a[i];
            if(v == 1){
                // 可以新开一个子序列，只含 "1"
                dp[1] = (dp[1] + 1) % MOD;
            } else {
                // 扩展之前的 [1,2,...,v-1] 子序列
                // 注意这里 v > 1
                dp[v] = (dp[v] + dp[v-1]) % MOD;
            }
        }

        // 计算权值总和
        long long ans = 0;
        for(int x = 1; x <= n; x++){
            ans = (ans + x * dp[x]) % MOD;
        }

        cout << ans << "\n";
    }

    return 0;
}

```
## python
```python
MOD = 10**9 + 7

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    idx = 0
    T = int(data[idx])  # 测试组数
    idx += 1
    for _ in range(T):
        n = int(data[idx])  # 数组长度
        idx += 1
        a = list(map(int, data[idx:idx + n]))  # 数组 a
        idx += n

        # dp[x] 表示子序列 [1,2,...,x] 的个数
        dp = [0] * (n + 1)

        for v in a:
            if v == 1:
                # 可以新开一个子序列，只含 "1"
                dp[1] = (dp[1] + 1) % MOD
            else:
                # 扩展之前的 [1,2,...,v-1] 子序列
                # 注意这里 v > 1
                dp[v] = (dp[v] + dp[v - 1]) % MOD

        # 计算权值总和
        ans = 0
        for x in range(1, n + 1):
            ans = (ans + x * dp[x]) % MOD

        print(ans)

if __name__ == "__main__":
    main()
```
## java
```java
import java.util.*;
import java.io.*;

public class Main {
    static final long MOD = 1000000007;

    public static void main(String[] args) throws IOException {
        // 为了快速输入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int T = Integer.parseInt(br.readLine().trim()); // 测试组数
        while(T-- > 0){
            int n = Integer.parseInt(br.readLine().trim());
            String[] tokens = br.readLine().trim().split(" ");
            int[] a = new int[n];
            for(int i = 0; i < n; i++){
                a[i] = Integer.parseInt(tokens[i]);
            }

            long[] dp = new long[n+1]; 
            // dp[x] 表示子序列 [1,2,...,x] 的个数

            for(int i = 0; i < n; i++){
                int v = a[i];
                if(v == 1){
                    // 新的子序列仅包含 "1"
                    dp[1] = (dp[1] + 1) % MOD;
                } else {
                    if(v <= n){
                        dp[v] = (dp[v] + dp[v-1]) % MOD;
                    }
                }
            }

            long ans = 0;
            for(int x = 1; x <= n; x++){
                ans = (ans + x * dp[x]) % MOD;
            }

            sb.append(ans).append("\n");
        }

        // 输出所有结果
        System.out.print(sb);
    }
}

```