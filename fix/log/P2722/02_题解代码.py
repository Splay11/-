# 题解

## 题面描述

有美元符号$ n $美元符号名矿工，编号为美元符号$ 1 $到美元符号$ n $；同时有美元符号$ m $美元符号处矿，矿点$j$的高度为美元符号$ b_j $。每个矿点在高度区间美元符号$ [1,b_j] $内每个高度都有$1$单位矿物。矿工依次进入矿道挖矿，第$i$个矿工拥有挖掘高度为美元符号$ a_i $，即他可以将高度在美元符号$ [1,a_i] $内的矿物全部挖走。注意：矿洞结实，即使底部的矿物挖空，矿物上方的不会掉落；同时同一位置的矿物一旦被挖掉就不会再出现。

每个矿工到达时，将他能够挖到的所有矿物全部挖走，求每个矿工挖到的矿物数量。

---

## 思路解析

这道题的核心在于模拟矿工挖矿的过程。每个矿工根据自己的挖掘高度依次进入矿道，并尝试挖掘每个矿点的矿物。对于每个矿点，矿工只能挖掘自己能够挖到的矿物量，且同一矿点矿物只会被挖一次。通过依次更新每个矿点已被挖掘的高度，并计算每个矿工挖到的矿物数量，最终得到每个矿工的采矿量。

1. **问题建模**  
   对于每个矿点$j$，设美元符号$cur_j$表示已被挖走的矿物高度。初始时美元符号$cur_j=0$，表示该矿点所有高度的矿物均未被挖。

2. **每个矿工的操作**  
   矿工$i$的挖掘能力为美元符号$ a_i $，他能挖去矿点$j$中高度区间美元符号$ (cur_j, \min(a_i, b_j)] $内的矿物，挖掉的矿物数量为  
   $$\min(a_i, b_j)-cur_j,$$  
   但前提是美元符号$ a_i > cur_j $，否则该矿工对该矿点无效。

3. **顺序处理**  
   矿工依次进入，因此对于每个矿点，每次更新美元符号$cur_j$为美元符号$cur_j+\min(a_i, b_j)-cur_j=\min(a_i, b_j)$。矿工依次累计各矿点挖到的矿物数量即为该矿工的总收益。

4. **复杂度分析**  
   时间复杂度为美元符号$ O(n \times m) $，由于美元符号$ n,m\le 10^3 $，整体最多$10^6$次操作，满足题目要求。

## C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
 
int main(){
    // 读入矿工数 $n$ 和矿点数 $m$
    int n, m;
    cin >> n >> m;
    // 定义矿工挖掘高度数组 $a$ 和矿点高度数组 $b$
    vector<long long> a(n), b(m), cur(m, 0);
    for (int i = 0; i < n; i++){
        cin >> a[i];
    }
    for (int j = 0; j < m; j++){
        cin >> b[j];
    }
    // 对每个矿工依次模拟挖矿过程
    for (int i = 0; i < n; i++){
        long long sum = 0; // 用于累计当前矿工挖到的矿物数量
        for (int j = 0; j < m; j++){
            // 如果该矿点还有矿，并且当前矿工的高度大于已挖高度
            if (cur[j] < b[j] && a[i] > cur[j]){
                // 当前矿工可以挖走的矿物数量
                long long remove = min(a[i], b[j]) - cur[j];
                sum += remove;
                cur[j] += remove; // 更新该矿点已挖高度
            }
        }
        cout << sum << (i == n - 1 ? "\n" : " ");
    }
    return 0;
}
```
## Python

```python
# 读入矿工数 $n$ 和矿点数 $m$
n, m = map(int, input().split())
# 读入矿工挖掘高度列表 $a$
a = list(map(int, input().split()))
# 读入矿点高度列表 $b$
b = list(map(int, input().split()))

# 定义列表 cur 用于记录每个矿点已被挖走的高度
cur = [0] * m

# 对每个矿工依次模拟挖矿过程
for i in range(n):
    total = 0  # 当前矿工挖到的矿物总数
    for j in range(m):
        # 如果该矿点还有矿且当前矿工的挖掘高度大于已挖高度
        if cur[j] < b[j] and a[i] > cur[j]:
            # 当前矿工可挖走的矿物数量
            remove = min(a[i], b[j]) - cur[j]
            total += remove
            cur[j] += remove  # 更新该矿点已被挖的高度
    print(total, end=" " if i < n - 1 else "\n")
```
## Java

```java
import java.util.Scanner;
import java.util.Arrays;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // 读入矿工数 $n$ 和矿点数 $m$
        int n = sc.nextInt();
        int m = sc.nextInt();
        // 定义矿工挖掘高度数组 $a$ 和矿点高度数组 $b$
        long[] a = new long[n];
        long[] b = new long[m];
        long[] cur = new long[m]; // 用于记录每个矿点已挖走的高度，初始均为 0
        for (int i = 0; i < n; i++){
            a[i] = sc.nextLong();
        }
        for (int j = 0; j < m; j++){
            b[j] = sc.nextLong();
        }
        // 模拟每个矿工的挖矿过程
        for (int i = 0; i < n; i++){
            long total = 0; // 累计当前矿工挖到的矿物数量
            for (int j = 0; j < m; j++){
                // 如果该矿点还有矿，并且当前矿工的挖掘高度大于已挖高度
                if (cur[j] < b[j] && a[i] > cur[j]){
                    // 计算当前矿工可以挖走的矿物数量
                    long remove = Math.min(a[i], b[j]) - cur[j];
                    total += remove;
                    cur[j] += remove; // 更新该矿点已挖走的高度
                }
            }
            // 输出当前矿工挖到的矿物数量
            System.out.print(total + (i < n - 1 ? " " : "\n"));
        }
        sc.close();
    }
}
```