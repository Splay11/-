# 思路

考虑一下有多种质因子和一种质因子的情况。

- 只有一种质因子 $a$

    $x=a^y$， 假设拆成了 $a^{p_1}, a^{p_2},...,a^{p_k}$ ，那么这 $k$ 个数的因子数总和为
    $\sum_{i=1}^k (p_i+1)=k+\sum_{i=1}^k p_i=k+y$

    所以需要 $k$ 越大越好，就是将 $x$ 拆分为 $y$ 个 $a$ 即可，此时答案是 $2y$

- 有多种质因子 $a_1,a_2,...,a_m$
    
    $x=a_1^{y_1}\cdot a_2^{y_2}\cdots\ a_m^{y_m}$ ，此时 $y_i$ 均大于 $0$ 

    在不拆的条件下，因子数为 $\prod_{i=1}^m(y_i+1)$

    其中 $(y_i+1)\geq 2$ ，所有大于等于 2 的整数相乘的积很大

    我们来考虑这么一个问题：因为 $a\times b\geq a+b$ ，在 $a\geq 2, b\geq 2$ 的情况下
    那么对于多个大于等于 2 的数 $a, b, c, d...$ 相乘，也必然有 $a\times b\times c\times d\times ... \geq a + b + c + d + ...$

    所以如果将一个这样的 $x$ 拆分成两个或多个数，然后将他们的因子数相加，这样的因子总数，必然小于等于 $x$ 的因子数。

时间复杂度：$O(T\times \sqrt{x})$

# 代码
### python
```python
def solve():
    x = int(input())
    u = 2
    res = []
    while u * u <= x:
        if x % u == 0:
            c = 0
            while x % u == 0:
                c += 1
                x /= u
            res.append((u, c))
        u += 1

    if x > 1:
        res.append((x, 1))

    if len(res) == 1:
        print(res[0][1] * 2)
    else:
        ans = 1
        for x, y in res:
            ans *= (y + 1)
        print(ans)

T = int(input())
for i in range(T):
    solve()

```
### C++
```C++
#include <iostream>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    cin >> n; // Read the number of test cases

    for (int i = 0; i < n; i++) {
        int x;
        cin >> x; // Read the integer x

        unordered_map<int, int> factor; // To store prime factors and their counts

        if (x == 2) {
            cout << 2 << endl; // Special case for x = 2
            continue;
        } else {
            int index = 2;
            while (index <= x) {
                if (x % index == 0) {
                    factor[index]++; // Increment the count of the prime factor
                    x /= index; // Divide x by the prime factor
                } else {
                    index++; // Move to the next potential factor
                }
                if (x == 1) {
                    break; // Exit if x is fully factored
                }
            }
        }

        long long var1 = 1; // To calculate the number of divisors
        long long var2 = 0; // To calculate the sum of the exponents

        for (const auto& j : factor) {
            var1 *= (j.second + 1); // Number of divisors
            var2 += 2 * j.second; // Sum of the exponents
        }

        cout << max(var2, var1) << endl; // Print the maximum of var1 and var2
    }

    return 0;
}
```
### java
```java
import java.util.*;
class Main{
   // x只有一个质因子 x=a^k
   // 1.拆分:k个a=>2k 2.不拆分:1,a,a^2,a^k=>k+1
   // k>=1  2k>=k+1 权值更大选拆分
   // x有多个质因子 x=a1^k1*a2^k2*am^km
   // 1.拆分:sum(ki+1) 2.不拆分:multi(ki+1)
   // ki >= 1 ki+1 >= 2
   // a,b>=2 a*b >= a+b => 不拆分权值更大
   public static void main(String[] args){
      Scanner sc = new Scanner(System.in);
      int T = sc.nextInt();
      while(T-- > 0){
         int n = sc.nextInt();
         System.out.println(solve(n));
      }
   }
   public static long solve(int x){ // 求因数个数
      // 求x的所有质因子和次幂
      List<int[]> list = new ArrayList<>();
      for(int i = 2;i * i <= x;i++){
         if(x % i == 0){
            int cnt = 0;
            while(x % i == 0){
               cnt++;
               x /= i;
            }
            list.add(new int[]{i,cnt});
         }
      }
      if(x > 1){
         list.add(new int[]{x,1});
      }
      if(list.size() == 1){ // 只有一个质因子
         return 1L * 2 * list.get(0)[1];
      }
      long ans = 1L; // 多个质因子
      for(int[] a : list){
         ans = ans * (a[1] + 1);
      }
      return ans;
   }
}
```