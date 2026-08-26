# 题解

## 题面描述

给定一个长度为 $n$ 的数组 $a=[a_1,a_2,\dots,a_n]$。可以任意交换数组中任意两个元素任意次（也可以不交换），使得可以自由调整顺序。然后定义一次“合井”操作：  
- 选取相邻的两个数 $a_i$ 和 $a_{i+1}$，合并成一个数，该数等于 $\max\{a_i,a_{i+1}\}$，合并时花费代价也等于 $\max\{a_i,a_{i+1}\}$。  
- 数组合并后顺序不变，但长度减少 $1$。  

要求经过恰好 $n-1$ 次“合井”操作，使得最终数组只有一个数，问最少花费多少代价？

---

## 思路分析

由于在正式执行合并操作前允许任意交换，我们实际上可以任意安排元素的顺序。观察合并操作有以下性质：

- 每次合并选取相邻两个数，并以两者中的较大值作为合并结果，同时花费同样的较大值；
- 一旦两个数合并，较小的数被“消耗”，而较大的数会继续存在于后续的合并中；
- 如果在一次合并中较大数参与过合并，那么其可能会在后续合并中再次被花费。

因此，为了降低总花费，尽量让较小的数尽可能长时间地被“吸收”，而较大的数尽量只出现一次。设数组排序后的结果为  
$$b_1 \le b_2 \le \dots \le b_n$$  
一种最优的合并策略是总是先合并最小的两个数。例如：

- 先将 $b_1$ 与 $b_2$ 合并：花费 $b_2$，结果变为 $b_2$；
- 接下来 $b_2$ 与 $b_3$ 合并：花费 $b_3$；
- ……
- 最后合并时花费 $b_n$。

这样，每次合并的花费正好是排序后除 $b_1$ 外的每个数各出现一次。  
因此最优的总花费为  
$$\text{总花费} = b_2 + b_3 + \cdots + b_n$$

证明思路：由于任意交换后可以任意调整顺序，使得每一次合并都能选取两个尽可能小的数，而合并后留下的数必然是这两个数中的较大值。如果把所有合并看作构造一棵二叉树（叶子为初始数组），那么内部节点的值正好是两子树中较大者。最优时，除了最大值外，其余每个数都只在一次合并中作为较大值出现，从而总花费就是排序后除最小值外的所有数之和。

---

## 代码分析

- **输入输出**：读入 $n$ 和数组 $a$。当 $n=1$ 时没有合并操作，输出 $0$。
- **排序**：将数组 $a$ 排序得到数组 $b$。
- **求和**：计算 $b_2+b_3+\cdots+b_n$，即除最小值之外的所有元素之和。
- **时间复杂度**：排序时间复杂度为 $O(n\log n)$，满足 $n\le 10^5$ 的要求。

## C++ 

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
 
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++){
        cin >> a[i];
    }
    
    // 当只有一个元素时，无需合并，花费为0
    if(n == 1){
        cout << 0;
        return 0;
    }
    
    sort(a.begin(), a.end());
    
    long long ans = 0;
    for(int i = 1; i < n; i++){
        ans += a[i];
    }
    cout << ans;
    return 0;
}
```
## Python

```python
# 读取输入
n = int(input().strip())  # 读取整数 n
a = list(map(int, input().split())) 

# 当只有一个元素时，无需合并，花费为0
if n == 1:
    print(0)
else:
    a.sort()
    ans = sum(a[1:])
    print(ans)
```
## Java

```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(); // 读取整数 n
        int[] a = new int[n];
        for(int i = 0; i < n; i++){
            a[i] = sc.nextInt(); // 读取数组 
        }
        // 当只有一个元素时，无需合并，花费为0
        if(n == 1){
            System.out.println(0);
            return;
        }
        Arrays.sort(a);
        long ans = 0;
        for(int i = 1; i < n; i++){
            ans += a[i];
        }
        System.out.println(ans);
    }
}
```