## 题解

## 题面描述

给定一个长度为 $n$ 的数组，每个数的权值定义为其质因子的个数（注意：质因子只计算不同的质数，例如 $4$ 的质因子只有 $2$，权值为 $1$）。现在要求删除数组中**连续**的一段长度恰好为 $k$ 的子数组，使得剩余数组中所有数字的权值和最大。求最大的权值和。


## 思路

 
首先对数组中的每个数字计算其质因子个数，记为它的权值（数字 $1$ 的权值为 $0$）；然后计算整个数组的权值和 $S$。接着使用滑动窗口方法遍历所有长度为 $k$ 的连续子数组，找出权值和最小的子数组，其权值和记为 $m$。由于删除这段子数组后，剩余部分的权值和为 $S-m$，因此最大剩余权值和即为 $S-m$。

1. **预处理权值**  
   由于每个数字 $a_i$ 的范围为 $[1,10^4]$，我们可以预先使用类似于筛法的方法求出 $[1,10^4]$ 内每个数的质因子个数，作为它的权值。

2. **计算总权值和**  
   对于数组中的所有数，计算它们的权值和，记作 $\text{total}$。

2. **滑动窗口求最小子数组权值和**  
   因为删除的子数组长度固定为 $k$，要使得剩下的权值和最大，就等价于让被删除的子数组的权值和最小。  
   因此，可以用滑动窗口的方法计算所有长度为 $k$ 的连续子数组的权值和，找到最小值。

3. **求解答案**  
   答案即为 $n$ 个数的总权值和减去最小的子数组权值和。

---

## cpp
```cpp
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

// 计算数字的质因子个数
int countPrimeFactors(int a) {
    int cnt = 0;
    if(a == 1) return 0;
    for (int j = 2; j * j <= a; j++) {
        if(a % j == 0){
            ++cnt;
            while(a % j == 0) {
                a /= j;
            }
        }
    }
    if(a > 1) ++cnt;
    return cnt;
}

int main(){
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    vector<int> w(n, 0);
    int totalSum = 0;
    
    // 读取数组，并预处理每个数的权值
    for(int i = 0; i < n; i++){
        cin >> a[i];
        w[i] = countPrimeFactors(a[i]);
        totalSum += w[i];
    }
    
    // 使用滑动窗口求长度为 k 的子数组中权值和的最小值
    int windowSum = 0;
    for(int i = 0; i < k; i++){
        windowSum += w[i];
    }
    int minWindowSum = windowSum;
    for (int i = k; i < n; i++){
        windowSum += w[i] - w[i - k];
        if(windowSum < minWindowSum)
            minWindowSum = windowSum;
    }
    
    // 最大的剩余权值和 = 总权值和 - 被删除子数组最小的权值和
    cout << totalSum - minWindowSum << endl;
    return 0;
}

```
## python
```python
# 计算数的质因子个数的函数
def count_prime_factors(a):
    cnt = 0
    if a == 1:
        return 0
    i = 2
    while i * i <= a:
        if a % i == 0:
            cnt += 1
            while a % i == 0:
                a //= i
        i += 1
    if a > 1:
        cnt += 1
    return cnt

# 主函数
def main():
    import sys
    input = sys.stdin.readline
    # 读取 n 和 k
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    # 计算每个数字的权值和总权值
    weights = []
    total_sum = 0
    for num in arr:
        w = count_prime_factors(num)
        weights.append(w)
        total_sum += w
    
    # 滑动窗口求长度为 k 的子数组中权值和的最小值
    window_sum = sum(weights[:k])
    min_window_sum = window_sum
    for i in range(k, n):
        window_sum += weights[i] - weights[i - k]
        if window_sum < min_window_sum:
            min_window_sum = window_sum
            
    # 输出答案：总权值和减去最小窗口权值和
    print(total_sum - min_window_sum)

if __name__ == '__main__':
    main()

```
## java
```java
import java.io.*;
import java.util.*;

public class Main {
    // 计算数字的质因子个数的函数
    public static int countPrimeFactors(int a) {
        int cnt = 0;
        if(a == 1) return 0;
        for (int i = 2; i * i <= a; i++) {
            if(a % i == 0) {
                cnt++;
                while(a % i == 0) {
                    a /= i;
                }
            }
        }
        if(a > 1) cnt++;
        return cnt;
    }
    
    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 加快输入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] s = br.readLine().split(" ");
        int n = Integer.parseInt(s[0]);
        int k = Integer.parseInt(s[1]);
        int[] a = new int[n];
        String[] nums = br.readLine().split(" ");
        for (int i = 0; i < n; i++) {
            a[i] = Integer.parseInt(nums[i]);
        }
        
        int[] weights = new int[n];
        int totalSum = 0;
        // 计算每个数字的权值
        for (int i = 0; i < n; i++) {
            weights[i] = countPrimeFactors(a[i]);
            totalSum += weights[i];
        }
        
        // 滑动窗口求长度为 k 的子数组中权值和的最小值
        int windowSum = 0;
        for (int i = 0; i < k; i++) {
            windowSum += weights[i];
        }
        int minWindowSum = windowSum;
        for (int i = k; i < n; i++) {
            windowSum += weights[i] - weights[i - k];
            minWindowSum = Math.min(minWindowSum, windowSum);
        }
        
        // 输出答案：总权值和减去最小窗口权值和
        System.out.println(totalSum - minWindowSum);
    }
}

```