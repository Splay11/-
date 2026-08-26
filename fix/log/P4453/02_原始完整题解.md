## 解题思路

给定长度为 n 的数组 $a_1,\dots,a_n$。要求构造只含小写字母的字符串 $s_1\dots s_n$，并满足：

* 若 $a_i=0$：$s_i$ 必须是一个**从未出现过**的新字符；
* 若 $a_i>0$：有 $1\le a_i<i$ 且 $s_i=s_{a_i}$，并且在区间 $(a_i,i)$ 内没有与 $s_{a_i}$ 相同的字符（即 $a_i$ 正是该字符在 $i$ 之前的“上一次出现位置”）。

由题意保证数据合法且所需不同字符数不超过 26。

核心思路（贪心/直接构造）：

* 从左到右扫描：

  * 如果 $a_i=0$，分配一个未使用过的新字母（按 `a,b,c,...` 依次给即可）；
  * 否则直接令 $s_i=s_{a_i}$。
* 因为输入保证合法，若令 $s_i=s_{a_i}$，则 $a_i$ 一定就是该字符的上一位置，区间 $(a_i,i)$ 内不会再出现该字符；而当 $a_i=0$ 时分配新字母即可。这样即可构成满足条件的链式结构。

实现要点：

* 维护答案字符数组 `s`（1 基下标便于对应 $a_i$）。
* 维护下一个可用的新字母计数器 `nextChar`。
* 依次填充并输出。

此方法等价于把所有位置按 `a_i` 指向前驱形成的若干递增“链”上色：链头（`a_i=0`）给新颜色，链上其他结点继承前驱颜色。

## 复杂度分析

* 时间复杂度：$O(n)$，每个位置处理一次。
* 空间复杂度：$O(n)$ 存储答案字符串（或 $O(1)$ 额外除答案外的空间）。

## 代码实现

### Python

```python
# ACM 风格：读入 -> 调用函数 -> 输出

import sys

def construct_string(n, a):
    # s 使用 1 基下标，便于直接按 a[i] 取字符
    s = [''] * (n + 1)
    next_char = 0  # 下一个未使用的小写字母序号
    for i in range(1, n + 1):
        if a[i] == 0:
            # 分配新字符，题目保证最多 26 种
            s[i] = chr(ord('a') + next_char)
            next_char += 1
        else:
            # 继承上一出现位置的字符
            s[i] = s[a[i]]
    return ''.join(s[1:])

def main():
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    arr = [0] * (n + 1)
    for i in range(1, n + 1):
        arr[i] = int(data[i])
    ans = construct_string(n, arr)
    print(ans)

if __name__ == "__main__":
    main()
```

### Java

```java
// ACM 风格：类名 Main，主函数读写；逻辑在外部函数中
import java.io.*;
import java.util.*;

public class Main {
    // 构造函数：按题意直接构造
    static String constructString(int n, int[] a) {
        char[] s = new char[n + 1]; // 1 基
        int nextChar = 0;           // 下一个未使用的字母
        for (int i = 1; i <= n; i++) {
            if (a[i] == 0) {
                s[i] = (char) ('a' + nextChar);
                nextChar++;
            } else {
                s[i] = s[a[i]];
            }
        }
        // 输出从 1 到 n
        return new String(s, 1, n);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 读取 n
        int n = Integer.parseInt(br.readLine().trim());
        // 读取数组 a
        int[] a = new int[n + 1];
        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= n; i++) {
            a[i] = Integer.parseInt(st.nextToken());
        }
        String ans = constructString(n, a);
        System.out.println(ans);
    }
}
```

### C++

```cpp
// ACM 风格：主函数读写；外部函数实现核心逻辑
#include <bits/stdc++.h>
using namespace std;

// 构造答案字符串
string construct_string(int n, const vector<int>& a) {
    vector<char> s(n + 1); // 1 基
    int nextChar = 0;      // 下一个新字母
    for (int i = 1; i <= n; ++i) {
        if (a[i] == 0) {
            s[i] = char('a' + nextChar);
            ++nextChar;
        } else {
            s[i] = s[a[i]];
        }
    }
    // 拼成输出
    string res;
    res.reserve(n);
    for (int i = 1; i <= n; ++i) res.push_back(s[i]);
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];
    string ans = construct_string(n, a);
    cout << ans << "\n";
    return 0;
}
```