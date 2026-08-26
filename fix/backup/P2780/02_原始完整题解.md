# 题解

## 题面描述

给定一个长度为 $n$ 的数组 $a$。  
每次操作可以选择任意的下标 $i,j$（$1 \leq i,j \leq n$），同时进行如下变换：  
- 将 $a_i$ 变为 $a_i \times a_j$  
- 将 $a_j$ 变为 $\operatorname{lcm}(a_i,a_j)$  

目标是使整个数组中的元素全部变成偶数。求最少需要的操作次数；若始终无法全部变为偶数，则输出 $-1$。

---

## 思路

- **奇偶性质观察**  
  由于我们只关心是否为偶数，因此可以忽略其他因素。  
  - 若 $a_i$ 为奇数，而 $a_j$ 为偶数，则  
    - $a_i \times a_j$ 为偶数  
    - $\operatorname{lcm}(a_i, a_j)$ 必然包含偶数因子，所以也是偶数  
  - 若两个数均为奇数，则它们的乘积与最小公倍数均为奇数  
- **操作策略**  
  如果数组中至少存在一个偶数，则可以用该偶数和每个奇数进行一次操作，将奇数转化为偶数。  
  因此最少操作次数即为数组中奇数的个数。  
- **特殊情况**  
  如果数组全为奇数，则无论如何操作都无法产生偶数，答案输出 $-1$。

---

## 代码分析

- **时间复杂度**  
  遍历一次数组即可确定答案，时间复杂度为 $O(n)$。  
- **空间复杂度**  
  只需使用常数级别的辅助空间，空间复杂度为 $O(1)$。  
- **问题本质分析**  
  本题的本质在于利用偶数和奇数的乘法性质来进行传递，只要有一个偶数便能将所有奇数转变为偶数；若全为奇数，则永远无法生成偶数。

## C++ 

```cpp
#include <iostream>
using namespace std;
 
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    // 读取数组长度 n
    cin >> n;
    int cntOdd = 0;
    bool hasEven = false;
    for (int i = 0; i < n; i++){
        int a;
        // 读取数组中的元素 a
        cin >> a;
        // 判断 a 是否为偶数
        if(a % 2 == 0){
            hasEven = true;
        } else {
            cntOdd++; // 累计奇数个数
        }
    }
    // 若不存在偶数，则无法将所有数变为偶数
    if(!hasEven){
        cout << -1 << "\n";
    } else {
        // 答案即为奇数的个数
        cout << cntOdd << "\n";
    }
    return 0;
}
```
## Python 

```python
# 读取数组长度 n
n = int(input())
# 读取数组 a，使用 map 转换为整数列表
a = list(map(int, input().split()))

cnt_odd = 0  # 奇数计数
has_even = False  # 是否存在偶数

# 遍历数组 a
for num in a:
    # 判断是否为偶数
    if num % 2 == 0:
        has_even = True
    else:
        cnt_odd += 1  # 奇数计数加一

# 如果没有偶数，则输出-1
if not has_even:
    print(-1)
else:
    # 否则输出奇数的个数
    print(cnt_odd)
```
## Java 

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // 读取数组长度n
        int n = sc.nextInt();
        int cntOdd = 0; // 奇数计数
        boolean hasEven = false; // 是否存在偶数

        // 遍历数组中的每个元素
        for (int i = 0; i < n; i++) {
            int a = sc.nextInt();
            // 判断a是否为偶数
            if (a % 2 == 0) {
                hasEven = true;
            } else {
                cntOdd++; // 奇数计数加一
            }
        }
        // 如果数组中没有偶数，则输出-1
        if (!hasEven) {
            System.out.println(-1);
        } else {
            // 否则输出奇数的个数
            System.out.println(cntOdd);
        }
        sc.close();
    }
}
```