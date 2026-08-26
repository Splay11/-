# 题解

## 题面描述

给定一个有 $n$ 行 $m$ 列的矩阵，每个位置的字符要么是大写字母 $N$，要么是大写字母 $Z$。  
你可以选择一整行和一整列（即形成一个“十”字形区域），将这个区域内所有的 $Z$ 替换为 $N$。  
要求替换之后矩阵中 $N$ 的总数量尽可能多，并直接输出这个最大数量。

---

## 思路

1. **统计初始情况**  
   先统计整个矩阵中初始的 $N$ 的数量，记为 $init$。

2. **计算每行和每列中 $Z$ 的个数**  
   对于每一行 $i$，统计该行中 $Z$ 的数量，记为 $cntZ\_row[i]$；  
   对于每一列 $j$，统计该列中 $Z$ 的数量，记为 $cntZ\_col[j]$。

3. **选择“十”字区域后的增加量计算**  
   当我们选择第 $i$ 行和第 $j$ 列时，替换的区域为这行和这列的并集。  
   在这一过程中会将这行中的 $Z$ 全部变为 $N$（增加 $cntZ\_row[i]$ 个 $N$），以及这列中的 $Z$ 全部变为 $N$（增加 $cntZ\_col[j]$ 个 $N$）。  
   但是需要注意，交点 $(i, j)$ 会被重复计算，如果该位置原本为 $Z$，则多加了一次，需要减去 $1$。  
   所以对于选择的行 $i$ 和列 $j$，最终的增加量为  
   $\Delta$ = $cntZ\_row[i]$ + $cntZ\_col[j]$ - $(\text{如果 } matrix[i][j]$ = $Z \text{ 则 } 1 \text{ 否则 } 0).$

4. **答案计算**  
   对于所有 $i$ 和 $j$ 的组合，求得最大的 $\Delta_{max}$，  
   则最终的 $N$ 的最大数量为  
   $$ans = init + \Delta_{max}.$$

5. **时间复杂度分析**  
   预处理每行、每列需要 $O(n \times m)$，遍历所有组合最多 $O(n \times m)$，总体复杂度为 $O(n \times m)$，对于 $n, m \le 10^3$ 完全满足要求。

---

## 代码分析

- **预处理**  
  统计整个矩阵的 $N$ 数量，以及每一行和每一列中 $Z$ 的数量。

- **枚举选择**  
  遍历每一行 $i$ 和每一列 $j$，计算替换后增加的 $N$ 数量 $\Delta$，并保持最大值。

- **输出结果**  
  最终答案为 $init + \Delta_{max}$。

- **问题本质**  
  本题的核心在于如何利用选择一行一列能覆盖到尽可能多的 $Z$，并注意交点的重复计算问题，从而实现最大化 $N$ 数量的策略。题目本质上是对矩阵中某些统计量（$Z$ 的计数）的优化选择问题。

---

## C++ 

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, m;
    cin >> n >> m;
    vector<string> matrix(n);
    
    // 输入矩阵
    for(int i = 0; i < n; i++){
        cin >> matrix[i];
    }
    
    int init = 0; //init为初始的N数量
    vector<int> cntZ_row(n, 0); // 每行中Z的个数
    vector<int> cntZ_col(m, 0); // 每列中Z的个数
    
    // 预处理，统计初始N数量以及每行每列的Z数量
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            if(matrix[i][j] == 'N'){
                init++; // 如果是 $N$，计入初始数量
            } else {
                cntZ_row[i]++;
                cntZ_col[j]++;
            }
        }
    }
    
    int delta_max = 0; // 最大的增加量
    // 枚举每一行和每一列组合
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            // 如果交点为Z，则减去1，防止重复计算
            int cur = cntZ_row[i] + cntZ_col[j] - (matrix[i][j] == 'Z' ? 1 : 0);
            delta_max = max(delta_max, cur);
        }
    }
    
    // 最终答案
    cout << init + delta_max << "\n";
    
    return 0;
}
```
## Python

```python
# -*- coding: utf-8 -*-
# 输入读取
n, m = map(int, input().split())
matrix = [input().strip() for _ in range(n)]

init = 0  #init表示初始的N数量
cntZ_row = [0] * n  # 每行中Z的个数
cntZ_col = [0] * m  # 每列中Z的个数

# 预处理，统计初始N数量以及每行每列的Z数量
for i in range(n):
    for j in range(m):
        if matrix[i][j] == 'N':
            init += 1  # 如果是N，计入初始数量
        else:
            cntZ_row[i] += 1
            cntZ_col[j] += 1

delta_max = 0  # 最大的增加量
# 枚举每一行和每一列组合
for i in range(n):
    for j in range(m):
        # 如果交点为Z，则减去1，防止重复计算
        cur = cntZ_row[i] + cntZ_col[j] - (1 if matrix[i][j] == 'Z' else 0)
        delta_max = max(delta_max, cur)

# 最终答案
print(init + delta_max)
```
## Java

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        // 读取n和m
        int n = sc.nextInt();
        int m = sc.nextInt();
        sc.nextLine(); // 消耗换行符
        
        String[] matrix = new String[n];
        for (int i = 0; i < n; i++) {
            // 读取每一行字符串
            matrix[i] = sc.nextLine();
        }
        
        int init = 0; // $init$ 表示初始的N数量
        int[] cntZ_row = new int[n]; // 每行中Z的个数
        int[] cntZ_col = new int[m]; // 每列中Z的个数
        
        // 预处理，统计初始N数量以及每行每列的Z$数量
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                char ch = matrix[i].charAt(j);
                if (ch == 'N') {
                    init++; // 如果是N,计入初始数量
                } else {
                    cntZ_row[i]++;
                    cntZ_col[j]++;
                }
            }
        }
        
        int deltaMax = 0; // 最大的增加量
        // 枚举每一行和每一列组合
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                // 如果交点为Z，则减去1,防止重复计算
                int cur = cntZ_row[i] + cntZ_col[j] - (matrix[i].charAt(j) == 'Z' ? 1 : 0);
                deltaMax = Math.max(deltaMax, cur);
            }
        }
        
        // 输出最终答案
        System.out.println(init + deltaMax);
        sc.close();
    }
}
```