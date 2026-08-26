# 题解

## 题面描述

给定一个长度为$n$的整数数组$[a_1,a_2,\dots,a_n]$，我们称一个数组是“好数组”，当且仅当将该数组的一个后缀整体移动到最前面后，该数组变成非降序。举例：

- $[3,7,7,9,2,3]$ 是好数组，因为可以将后缀 $[2,3]$ 移到前面，得到 $[2,3,3,7,7,9]$，这是非降序的。
- $[1,2,3,4,5]$ 是好数组，因为可以将整个数组（后缀长度为$n$）移动至前面后保持不变，仍然是非降序的。
- $[5,2,2,1]$ 不是好数组，任意后缀移动后都无法得到非降序数组。

现在给定一个数组，求其所有**非空连续子数组**中有多少是好数组。连续子数组即原数组中任意一段连续元素。返回满足条件的子数组个数。

---

## 思路

1. 任何一个长度为$m$的子数组，我们只需判断它自身是否存在一个后缀，使得移到前面后数组变为非降序。
2. 对于一个数组$b[1..m]$，若它是好数组，则它最多只能出现一次“降”——即位置$i$使得$b[i]>b[i+1]$，而且将从第一次降处$(i+1)$到末尾的元素移动到前面后，整体非降序。
3. 更具体地，对于$b[1..m]$，记所有索引$i$使得$b[i]>b[i+1]$的集合为$D$：
   - 若$|D|>1$，则不可能只靠一次循环移位得到非降序。
   - 若$|D|=0$，本身就非降序，是好数组。
   - 若$|D|=1$，设唯一的下降点为$i$，需要额外满足$b[m]\le b[1]$，才能拼接后序和前序仍非降序。

因此，可在线性时间内判断任意子数组是否为好数组。当子数组过多，直接枚举会$O(n^2)$导致超时。我们需利用双指针或单调结构快速统计。

**高效统计方法（双指针）**

- 维护窗口$[l,r]$，保持子数组$b[l..r]$是“好数组”。
- 当$r$向右增加时，检查新增后是否仍满足好数组条件：只出现至多一次下降，并且如有下降点$i$，满足$b[r]\le b[l]$。
- 利用两个指标：
  - `cnt`：当前下降点数量。
  - `pos`：若`cnt==1`，记录该下降点位置。
- 若`cnt`超过1，移动左指针$l$，同步更新`cnt`和`pos`。
- 对每个$l`，可找到最大`r`使得子数组好数组，则贡献`r-l+1`个子数组。

该方法时间$O(n)$。

## cpp
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    ll ans = 0;
    int cnt = 0;        // 当前区间下降次数
    int drop = -1;      // 记录唯一下降的位置
    int l = 0;
    
    for (int r = 0; r < n; r++) {
        // 检查 a[r-1] > a[r] 是否构成下降
        if (r > 0 && a[r-1] > a[r]) {
            cnt++;
            drop = r - 1;
        }
        // 如果超过一次下降，移动左指针
        while (cnt > 1 || (cnt == 1 && a[r] > a[l])) {
            // 若移除的边界是下降点，需要重置
            if (l < n-1 && a[l] > a[l+1]) {
                cnt--;
            }
            l++;
        }
        ans += (r - l + 1);
    }

    cout << ans << "\n";
    return 0;
}
```
## python

```python
import sys

# 读取输入
n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))

ans = 0
cnt = 0         # 当前区间下降次数
drop = -1       # 唯一下降点位置
l = 0

for r in range(n):
    if r > 0 and a[r-1] > a[r]:
        cnt += 1
        drop = r - 1
    # 若不满足好数组条件，移动左指针
    while cnt > 1 or (cnt == 1 and a[r] > a[l]):
        if l < n-1 and a[l] > a[l+1]:
            cnt -= 1
        l += 1
    ans += (r - l + 1)

print(ans)
```
## java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());
        StringTokenizer st = new StringTokenizer(br.readLine());
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = Long.parseLong(st.nextToken());
        }

        long ans = 0;
        int cnt = 0;      // 当前区间下降次数
        int l = 0;        // 左指针
        
        for (int r = 0; r < n; r++) {
            if (r > 0 && a[r-1] > a[r]) {
                cnt++;
            }
            while (cnt > 1 || (cnt == 1 && a[r] > a[l])) {
                if (l < n-1 && a[l] > a[l+1]) {
                    cnt--;  
                }
                l++;
            }
            ans += (r - l + 1);
        }

        System.out.println(ans);
    }
}
```