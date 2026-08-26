## 解题思路

给定长度为 $n$ 的 01 串 $s=s_1s_2\ldots s_n$，要求对每个位置 $i$，统计在它左侧（下标 $< i$）与 $s_i$ 不同的字符个数。
我们可以采用**前缀计数**的方法：

1. 定义两个变量 `cnt0` 和 `cnt1`，分别记录当前已遍历字符中 `'0'` 和 `'1'` 的个数。
2. 对每个位置 $i$：

   * 若 $s_i='0'$，则左侧与它不同的字符即为所有已出现的 `'1'`，即 $a_i = \text{cnt1}$；
   * 若 $s_i='1'$，则 $a_i = \text{cnt0}$。
3. 将对应的计数器自增：若 $s_i='0'$，则 `cnt0++`；若 $s_i='1'$，则 `cnt1++`。

这种方法只需一次扫描，时间复杂度 $O(n)$，空间复杂度 $O(1)$。

## 算法步骤

1. 初始化 `cnt0=0, cnt1=0`，并准备数组 `ans` 长度为 $n$。
2. 从 $i=1$ 到 $n$ 依次遍历：

   1. 如果 $s_i='0'$，则 `ans[i]=cnt1`，同时 `cnt0++`；
   2. 否则 `ans[i]=cnt0`，同时 `cnt1++`。
3. 输出 `ans` 数组。

## 复杂度分析

* **时间复杂度**：遍历一次字符串，进行常数次操作，故为 $O(n)$。
* **空间复杂度**：只使用常数个额外变量与输出数组，故为 $O(n)$。

## 代码实现

### Python

```python
def count_diff(s):
    n = len(s)
    ans = [0] * n
    cnt0, cnt1 = 0, 0
    for i, ch in enumerate(s):
        if ch == '0':
            ans[i] = cnt1      # 左侧所有 '1'
            cnt0 += 1          # 更新 '0' 计数
        else:
            ans[i] = cnt0      # 左侧所有 '0'
            cnt1 += 1          # 更新 '1' 计数
    return ans

if __name__ == '__main__':
    T = int(input().strip())
    for _ in range(T):
        n = int(input().strip())
        s = input().strip()
        res = count_diff(s)
        print(' '.join(map(str, res)))
```

### Java

```java
import java.util.Scanner;

public class Main {
    // 计算每个位置左侧与当前字符不同的数量
    static int[] countDiff(String s) {
        int n = s.length();
        int[] ans = new int[n];
        int cnt0 = 0, cnt1 = 0;
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (c == '0') {
                ans[i] = cnt1;  // 左侧所有 '1'
                cnt0++;         // 更新 '0' 计数
            } else {
                ans[i] = cnt0;  // 左侧所有 '0'
                cnt1++;         // 更新 '1' 计数
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        while (T-- > 0) {
            int n = sc.nextInt();
            String s = sc.next();
            int[] res = countDiff(s);
            for (int i = 0; i < n; i++) {
                System.out.print(res[i] + (i+1<n ? " " : ""));
            }
            System.out.println();
        }
        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 计算每个位置左侧与当前字符不同的数量
vector<int> countDiff(const string &s) {
    int n = s.size();
    vector<int> ans(n);
    int cnt0 = 0, cnt1 = 0;
    for (int i = 0; i < n; i++) {
        if (s[i] == '0') {
            ans[i] = cnt1;  // 左侧所有 '1'
            cnt0++;         // 更新 '0' 计数
        } else {
            ans[i] = cnt0;  // 左侧所有 '0'
            cnt1++;         // 更新 '1' 计数
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        string s;
        cin >> n >> s;
        vector<int> res = countDiff(s);
        for (int i = 0; i < n; i++) {
            cout << res[i] << (i+1<n ? ' ' : '\n');
        }
    }
    return 0;
}
```