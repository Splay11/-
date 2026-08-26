# 思路

关键观察：
只要$s$ 中有某个字母出现至少 $2$ 次，就能取这两个位置各自形成长度为 $1$ 的子串（例如两个 $a$），这两个子串显然字符构成相同，答案为 `Yes`。
反之，若 $s$ 中每个字母都只出现 $1$ 次，则：

* 设存在两个不同的子串 $s[i,..,i+k-1]$ 与 $s[j,..,j+k-1]$（$k \ge 1$、$i \ne j$）互为异位词。
* 因为整个 $s$ 内所有字母都只出现 $1$ 次，所以这两个子串包含的字母集合完全相同就意味着它们包含 **同一组唯一的位置**。
* 但两个长度为 $k$ 的连续区间若覆盖的是同一组位置，则只能是同一段，即必须有 $i=j$，与 $i \ne j$ 矛盾。

因此问题 **等价** 于判断 $s$ 是否存在重复字符。
实现上用大小为 $26$ 的布尔数组线性扫描即可，时间复杂度 $O(n)$，额外空间 $O(1)$。

# C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n;
    string s;
    if (!(cin >> n)) return 0;
    cin >> s;

    // 只需判断是否有重复字符（小写字母）
    bool seen[26] = {false};
    for (char c : s) {
        int x = c - 'a';
        if (seen[x]) {
            cout << "Yes\n"; // 出现过 -> 存在两个长度为1的相同子串
            return 0;
        }
        seen[x] = true;
    }
    cout << "No\n"; // 无重复字符 -> 不存在两个构成相同的不同子串
    return 0;
}
```
# Python 

```python
import sys

data = sys.stdin.read().strip().split()
if not data:
    sys.exit(0)
# 输入格式：n, s
n = int(data[0])
s = data[1]

# 用布尔数组判断是否有重复字符
seen = [False] * 26
for ch in s:
    idx = ord(ch) - 97  # 'a' -> 0
    if seen[idx]:
        print("Yes")  # 有重复字符 -> 两个长度为1的相同子串
        break
    seen[idx] = True
else:
    print("No")  # 全部不同 -> 不存在两个构成相同的不同子串
```

# Java 

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line1 = br.readLine();
        if (line1 == null) return;
        String line2 = br.readLine();
        long n = Long.parseLong(line1.trim());
        String s = line2.trim();

        // 判断是否存在重复字符（小写字母）
        boolean[] seen = new boolean[26];
        for (int i = 0; i < s.length(); i++) {
            int idx = s.charAt(i) - 'a';
            if (seen[idx]) {
                System.out.println("Yes"); // 有重复 -> 存在两个长度为1的相同子串
                return;
            }
            seen[idx] = true;
        }
        System.out.println("No"); // 无重复 -> 不存在两个构成相同的不同子串
    }
}
```