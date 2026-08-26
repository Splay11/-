## 解题思路

### 关键性质

* 合并相邻两个数，用它们的**乘积**替换。乘积的奇偶只由因子决定：

  * 只要其中一个是**偶数**，乘积就是偶数；
  * 两个都是奇数，乘积才是奇数。
* 因而：

  1. **一旦数组里出现偶数，就永远不可能把它“变成奇数”**——任何包含该偶数的乘积仍为偶数。所以想要最终“全奇”，**必须一开始全是奇数**。
  2. 若数组中有偶数，最终只可能做到“全偶”。每次操作至多让奇数的个数减少 1（`奇×奇→奇` 使奇数数目减 1；`奇×偶→偶` 也使奇数数目减 1；`偶×偶→偶` 不变）。

### 转化为计数

* 设数组中奇数的个数为 `cntOdd`，是否存在偶数为 `hasEven`。
* 若 `hasEven == false`（全奇）：已满足要求，答案为 `0`。
* 若 `hasEven == true`：要变为“全偶”，下界是 `cntOdd`（一次操作最多消去 1 个奇数）。
  这个下界可以达到：选择任意一个偶数，从它开始向左右相邻不断合并（偶×任意=偶），**每次把相邻的一个奇数“吸收”成偶数**，总共正好进行 `cntOdd` 次。

因此答案：

* 若存在偶数：`ans = cntOdd`
* 否则：`ans = 0`

该策略不依赖具体位置，只需统计奇偶即可。

## 复杂度分析

* 对每个测试用例一次线性扫描统计奇数和是否有偶数。
* 时间复杂度：`O(n)`（整份输入为 `O(Σn)`），空间复杂度：`O(1)`。

## 代码实现

### Python

```python
# 读取输入，按题意求解
import sys

data = list(map(int, sys.stdin.buffer.read().split()))
it = iter(data)
t = next(it)
out = []
for _ in range(t):
    n = next(it)
    cnt_odd = 0       # 记录奇数个数
    has_even = False  # 是否出现偶数
    for _ in range(n):
        x = next(it)
        if x % 2 == 0:
            has_even = True
        else:
            cnt_odd += 1
    # 若存在偶数，最少操作为奇数个数；否则已全奇，答案为0
    out.append(str(cnt_odd if has_even else 0))

print("\n".join(out))
```

### Java

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt(); // 读取测试组数
        StringBuilder sb = new StringBuilder();
        while (T-- > 0) {
            int n = sc.nextInt(); 
            int cntOdd = 0;      // 统计奇数个数
            boolean hasEven = false; // 是否存在偶数
            for (int i = 0; i < n; i++) {
                int x = sc.nextInt();
                if ((x & 1) == 0) hasEven = true; // 偶数
                else cntOdd++; // 奇数
            }
            // 若存在偶数，答案为奇数个数；否则已全奇，答案为0
            sb.append(hasEven ? cntOdd : 0).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
// 统计奇偶并输出答案
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; 
        cin >> n;
        long long x;
        int cntOdd = 0;     // 奇数个数
        bool hasEven = false; // 是否出现偶数
        for (int i = 0; i < n; ++i) {
            cin >> x;
            if (x % 2 == 0) hasEven = true;
            else cntOdd++;
        }
        // 若存在偶数，最少操作为奇数个数，否则已全奇
        cout << (hasEven ? cntOdd : 0) << "\n";
    }
    return 0;
}
```