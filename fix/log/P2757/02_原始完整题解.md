# 题解

## 题面描述

题目给定了$ n $个密匙片段，每个片段均为长度为$ m $的二进制字符串（仅含字符$'0'$和$'1'$）。要求从这$ n $个片段中任意选择若干（至少一个），将选择的片段进行**按位或**运算，得到一个二进制数。把这个二进制数转换为十进制后，只有当其正好为质数时才被视为一个合法的密钥。要求统计所有能够构造出的**不同**质数密钥的个数。

---

## 思路

1. **枚举子集**  
   由于可以任意选择片段（至少选一个），总共有$2^n-1$种选择方案。可以使用位掩码来枚举所有非空子集。

2. **片段转数字及按位或运算**  
   对于每个子集，遍历其中的每个片段，将二进制字符串转换为数字后，将所有数字做**按位或**运算得到最终密钥。  
   例如：对于子集$\{S_1, S_2\}$，有  
   $\text{key}$ = $\text{value}(S_1)\ $|$\ \text{value}(S_2)$  
   其中$\text{value}(S_i)$表示第$ i $个片段对应的十进制数值。

3. **判断质数**  
   得到的密钥数值不超过$2^m-1$（由于每个片段的最大值为$2^m-1$），因此可以采用简单的试除法判断质数。

4. **去重统计**  
   使用集合记录所有满足条件的质数密钥，最后输出集合的大小即为答案。

---

## 代码分析

- **变量说明**  
  - $n$：片段数量  
  - $m$：每个片段的长度  
  - $S_i$：第$ i $个片段（一个由$ m $个字符组成的字符串）  
  - $key$：由选中片段按位或得到的二进制数值  
  - $mask$：用于枚举子集的位掩码，若$ mask $的第$ i $位为$1$则表示选择第$ i $个片段

- **核心流程**  
  1. 使用循环枚举$ mask $从$1$到$2^n-1$。  
  2. 对于每个$ mask $，初始化$ key=0 $，遍历所有位，对于选中的片段将其二进制值转换为整数，然后做按位或：  
     $$ key\mathrel{|}= \text{value}(S_i) $$
  3. 判断$ key $是否为质数，若是则加入集合中。  
  4. 最后输出集合中质数的个数。

- **时间复杂度**  
  枚举子集的时间复杂度为$ O(2^n\cdot n\cdot m)$，由于$ n\le 20, m\le 14 $，总体运算量在允许范围内。

- **问题本质分析**  
  该问题的本质在于利用枚举子集的方法求出所有可能的组合结果，并利用位运算（按位或）进行合并，再通过判断质数来筛选合法结果。题目考察了对二进制运算、枚举子集以及质数判断算法的综合应用。

## C++ 

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <set>
using namespace std;

// 判断是否为质数
bool isPrime(int num) {
    if(num < 2) return false;
    for(int i = 2; i * i <= num; i++){
        if(num % i == 0) return false;
    }
    return true;
}

int main(){
    int n, m;
    cin >> n >> m;
    vector<string> fragments(n);
    for(int i = 0; i < n; i++){
        cin >> fragments[i];
    }
    
    set<int> primes; // 存储所有得到的质数密钥
    int total = 1 << n; // 总共2^n种子集
    // 枚举所有非空子集，mask从1开始
    for(int mask = 1; mask < total; mask++){
        int key = 0;
        // 遍历每个片段，判断是否选中
        for(int i = 0; i < n; i++){
            if(mask & (1 << i)){
                int fragmentValue = 0;
                // 将二进制字符串转换成整数
                for(char c : fragments[i]){
                    fragmentValue = (fragmentValue << 1) | (c - '0');
                }
                key |= fragmentValue; // 按位或运算合并片段
            }
        }
        if(isPrime(key)){
            primes.insert(key);
        }
    }
    cout << primes.size() << endl;
    return 0;
}
```
## Python 

```python
# 判断是否为质数
def is_prime(num):
    if num < 2:
        return False
    i = 2
    while i * i <= num:
        if num % i == 0:
            return False
        i += 1
    return True

# 读取输入n和m 
n, m = map(int, input().split())
fragments = [input().strip() for _ in range(n)]
prime_set = set()  # 用于存储质数密钥

total = 1 << n  # 总共2^n种子集
# 枚举所有非空子集，mask从1开始
for mask in range(1, total):
    key = 0
    for i in range(n):
        if mask & (1 << i):
            # 直接将二进制字符串转换为整数
            fragment_value = int(fragments[i], 2)
            key |= fragment_value  # 按位或运算合并片段
    if is_prime(key):
        prime_set.add(key)
print(len(prime_set))
```
## Java 

```java
import java.util.*;
public class Main {
    // 判断是否为质数
    public static boolean isPrime(int num) {
        if(num < 2) return false;
        for(int i = 2; i * i <= num; i++){
            if(num % i == 0) return false;
        }
        return true;
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), m = sc.nextInt();
        String[] fragments = new String[n];
        for(int i = 0; i < n; i++){
            fragments[i] = sc.next();
        }
        HashSet<Integer> primeSet = new HashSet<>();
        int total = 1 << n;  // 总共2^n种子集
        // 枚举所有非空子集，mask从1开始
        for(int mask = 1; mask < total; mask++){
            int key = 0;
            for(int i = 0; i < n; i++){
                if((mask & (1 << i)) != 0){
                    // 将二进制字符串转换成整数
                    int fragmentValue = Integer.parseInt(fragments[i], 2);
                    key |= fragmentValue;  // 按位或运算合并片段
                }
            }
            if(isPrime(key)){
                primeSet.add(key);
            }
        }
        System.out.println(primeSet.size());
    }
}
```