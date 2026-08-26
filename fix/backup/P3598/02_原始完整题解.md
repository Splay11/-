## 思路

1. 将两个分数相加：

   $\frac{a}{b}$ + $\frac{c}{d}$ = $\frac{a \times d + c \times b}{b \times d}$

2. 得到分子 $num = a \times d + c \times b$ 和分母 $den = b \times d$。

3. 将分子分母约分：

   $$
   g = \gcd(num, den)
   $$

   $$
   num' = \frac{num}{g},\quad den' = \frac{den}{g}
   $$

4. 检查 $den'$ 的质因子，若去掉所有 2 和 5 后：

   * 剩余部分为 1，则是有限小数，输出 **YES**
   * 否则输出 **NO**

## 代码

## C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;

// 计算最大公约数
long long gcd_ll(long long x, long long y) {
    while (y) {
        long long t = x % y;
        x = y;
        y = t;
    }
    return x;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int T;
    cin >> T;
    while (T--) {
        long long a, b, c, d;
        cin >> a >> b >> c >> d;
        
        // 分子和分母
        long long num = a * d + c * b;
        long long den = b * d;
        
        // 约分
        long long g = gcd_ll(num, den);
        num /= g;
        den /= g;
        
        // 去掉分母中的2和5
        while (den % 2 == 0) den /= 2;
        while (den % 5 == 0) den /= 5;
        
        if (den == 1) cout << "YES\n";
        else cout << "NO\n";
    }
    return 0;
}
```
## Python 

```python
import math

T = int(input())
for _ in range(T):
    a, b, c, d = map(int, input().split())
    
    # 分子分母
    num = a * d + c * b
    den = b * d
    
    # 约分
    g = math.gcd(num, den)
    num //= g
    den //= g
    
    # 去掉分母中的2和5
    while den % 2 == 0:
        den //= 2
    while den % 5 == 0:
        den //= 5
    
    if den == 1:
        print("YES")
    else:
        print("NO")
```
## Java 

```java
import java.util.*;
import java.io.*;

public class Main {
    // 计算最大公约数
    static long gcd(long a, long b) {
        while (b != 0) {
            long t = a % b;
            a = b;
            b = t;
        }
        return a;
    }
    
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine());
        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < T; i++) {
            String[] parts = br.readLine().split(" ");
            long a = Long.parseLong(parts[0]);
            long b = Long.parseLong(parts[1]);
            long c = Long.parseLong(parts[2]);
            long d = Long.parseLong(parts[3]);
            
            // 分子分母
            long num = a * d + c * b;
            long den = b * d;
            
            // 约分
            long g = gcd(num, den);
            num /= g;
            den /= g;
            
            // 去掉分母中的2和5
            while (den % 2 == 0) den /= 2;
            while (den % 5 == 0) den /= 5;
            
            if (den == 1) sb.append("YES\n");
            else sb.append("NO\n");
        }
        
        System.out.print(sb.toString());
    }
}
```