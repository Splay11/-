## 题解

### 题面描述

给定一个长度为 $n$ 的字符串 $s$，其中 $s$ 由小写字母构成。我们可以进行任意次如下操作：

- 选择两个不同的位置 $i$ 和 $j$（满足 $i \neq j$），要求 $s[i] \neq \texttt{’a’}$ 且 $s[j] \neq \texttt{’z’}$；
- 将 $s[i]$ 替换为其前一个字母（即字母表中前一位），同时将 $s[j]$ 替换为其后一个字母（即字母表中后一位）。

在所有可能的合法操作中，选择能够得到字典序最小的字符串作为答案。若不存在任何合法操作，则直接输出原字符串。

字典序比较时，从字符串的开始位置逐个比较，直到发现第一个不同字符，字符字母序更小的字符串字典序更小。

### 思路

1. **贪心目标**  
   要让字符串字典序最小，应尽可能地将前缀字符变得更小（尽量变成 $\texttt{’a’}$），即先处理最左侧的非 $\texttt{’a’}$ 字符。

2. **双指针配对**  
   - 用指针 $i$ 从左向右扫描，指向第一个 $s[i]\neq\texttt{’a’}$ 的位置。  
   - 用指针 $j$ 从右向左扫描，指向第一个 $s[j]\neq\texttt{’z’}$ 的位置。  
   - 若 $i<j$，可对这对 $(i,j)$ 进行操作；否则无法再配对，结束。

3. **最大化当前配对的操作次数**  
   对于当前的 $i$ 和 $j$，可以同时对 $s[i]$ 向前减以及 $s[j]$ 向后增：  
   $d$ = $\min$($s[i]-'a'$,$'z'-s[j]$).$
   将 $s[i]$ 减小 $d$，$s[j]$ 增大 $d$，恰好使用完能把要么 $s[i]$ 变为 $’a’$，要么 $s[j]$ 变为 $’z’$ 的操作额度。然后根据是否达到边界字符来移动指针。

4. **复杂度分析**  
   每次操作至少让 $i$ 前移或 $j$ 后移一次，最多各移动 $n$ 步，总操作次数 $O(n)$，字符串长度 $n\le2\times10^5$，线性可接受。

## C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    string s;
    cin >> n;
    cin >> s;

    int i = 0, j = n - 1;
    // 双指针，i 向右找非 'a'，j 向左找非 'z'
    while (i < j) {
        if (s[i] == 'a') {
            ++i;  // s[i] 已经是最小，无需处理，继续右移
            continue;
        }
        if (s[j] == 'z') {
            --j;  // s[j] 已经是最大，无需处理，继续左移
            continue;
        }
        // 计算可执行的最大步数
        int d = min(s[i] - 'a', 'z' - s[j]);
        s[i] -= d;  // 前移 d 步
        s[j] += d;  // 后移 d 步
        // 若达到边界，则相应指针移动
        if (s[i] == 'a') ++i;
        if (s[j] == 'z') --j;
    }

    cout << s << "\n";
    return 0;
}
```
## Python

```python
def make_minlex(s: str) -> str:
    n = len(s)
    arr = list(s)
    i, j = 0, n - 1

    # 通过双指针对称地减少和增加字符
    while i < j:
        if arr[i] == 'a':
            i += 1
            continue
        if arr[j] == 'z':
            j -= 1
            continue

        # 每次配对操作 d 次，最大化本次操作令一端达到边界
        d = min(ord(arr[i]) - ord('a'), ord('z') - ord(arr[j]))
        arr[i] = chr(ord(arr[i]) - d)
        arr[j] = chr(ord(arr[j]) + d)

        if arr[i] == 'a':
            i += 1
        if arr[j] == 'z':
            j -= 1

    return ''.join(arr)


if __name__ == "__main__":
    n = int(input().strip())
    s = input().strip()
    print(make_minlex(s))
```
## Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        char[] s = br.readLine().trim().toCharArray();

        int i = 0, j = n - 1;
        // 双指针策略
        while (i < j) {
            if (s[i] == 'a') {
                i++;
                continue;
            }
            if (s[j] == 'z') {
                j--;
                continue;
            }
            // 计算当前配对可操作的最大步数
            int d = Math.min(s[i] - 'a', 'z' - s[j]);
            s[i] -= d;
            s[j] += d;

            if (s[i] == 'a') i++;
            if (s[j] == 'z') j--;
        }

        System.out.println(new String(s));
    }
}
```