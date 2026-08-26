# 题面描述  
游游有一个长度为 $n$ 的数组 $a$。定义两个函数：  
- $f(a)=a_1+a_2+\dots+a_m$（数组所有元素之和，其中 $m$ 为数组长度）；  
- $g(a)=a_1\mid a_2\mid\dots\mid a_m$（数组所有元素的按位或）。  
现将数组 $a$ 恰好分割成两个非空数组 $b$ 和 $c$，要求最小化  
$$\bigl|\,f(b)-g(c)\bigr|\,. $$  

---

# 思路  

1. **前缀和与后缀或**  
   - 令  
     $$S_i = \sum_{k=1}^i a_k,\quad 1\le i\le n;$$  
   - 令  
     ![image](/file/2/mkh1YSr18ExsUriY9Dzr1.png) 
2. 分割在位置 $i$ （即$b=a[1..i],\,c=a[i+1..n]$），则  
   $$f(b)=S_i,\quad g(c)=O_{i+1},$$  
   目标值为  
   $$\bigl|S_i - O_{i+1}\bigr|. $$
3. 只需枚举 $i=1,2,\dots,n-1$，维护前缀和和后缀或，取最小值。  
4. 时间复杂度 $O(n)$，空间复杂度 $O(n)$。  

# C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<long long> a(n+2), pre(n+2), suf(n+2);
        for (int i = 1; i <= n; i++) {
            cin >> a[i];
        }
        // 构造前缀和 pre[i] = a[1] + ... + a[i]
        for (int i = 1; i <= n; i++) {
            pre[i] = pre[i-1] + a[i];
        }
        // 构造后缀或 suf[i] = a[i] | a[i+1] | ... | a[n]
        suf[n+1] = 0;
        for (int i = n; i >= 1; i--) {
            suf[i] = suf[i+1] | a[i];
        }
        long long ans = LLONG_MAX;
        // 枚举切割点 i，将 b = a[1..i], c = a[i+1..n]
        for (int i = 1; i < n; i++) {
            long long diff = llabs(pre[i] - suf[i+1]);
            ans = min(ans, diff);
        }
        cout << ans << "\n";
    }

    return 0;
}
```
# Python  

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))
        # 前缀和
        pre = [0] * (n+1)
        for i in range(n):
            pre[i+1] = pre[i] + a[i]
        # 后缀或
        suf = [0] * (n+2)
        for i in range(n-1, -1, -1):
            suf[i+1] = suf[i+2] | a[i]
        ans = float('inf')
        # 枚举切割点 i：b = a[0..i-1], c = a[i..n-1]
        for i in range(1, n):
            diff = abs(pre[i] - suf[i+1])
            if diff < ans:
                ans = diff
        print(ans)

if __name__ == "__main__":
    solve()
```
# Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine().trim());
        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            String[] parts = br.readLine().split(" ");
            long[] a = new long[n+2];
            for (int i = 1; i <= n; i++) {
                a[i] = Long.parseLong(parts[i-1]);
            }
            // 前缀和
            long[] pre = new long[n+2];
            for (int i = 1; i <= n; i++) {
                pre[i] = pre[i-1] + a[i];
            }
            // 后缀或
            long[] suf = new long[n+3];
            for (int i = n; i >= 1; i--) {
                suf[i] = suf[i+1] | a[i];
            }
            long ans = Long.MAX_VALUE;
            // 枚举切割点 i
            for (int i = 1; i < n; i++) {
                long diff = Math.abs(pre[i] - suf[i+1]);
                ans = Math.min(ans, diff);
            }
            System.out.println(ans);
        }
    }
}
```