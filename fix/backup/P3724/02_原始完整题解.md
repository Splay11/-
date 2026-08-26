## 解题思路

本题分两步操作：

1. 替换：

* 小写字母向前循环一位（`a->z, b->a, ...`）。
* 大写字母向后循环一位（`Z->A, A->B, ...`）。
  线性遍历即可完成。

2. 删除（从右到左）：
   若当前位置字符的**右邻**（在“最新字符串”中）与它“同字母异大小写”，则删掉当前位置字符。继续向左处理。

关键在于第二步如何高效一次完成。把“从右到左”的过程看作一种**贪心 + 栈/双端队列**的模拟：

* 我们维护“当前已经确定的后缀”。从右向左扫描替换后的字符串，设当前字符为 `c`，已确定后缀的第一个字符（也就是 `c` 的右邻）记为 `r`。
* 若 `c` 与 `r` **同字母异大小写**，按规则应删掉 `c`，所以我们不把 `c` 放入后缀（相当于“跳过”）。
* 否则，`c` 必须保留并位于后缀最前端，把它加入“后缀”的**前面**。

为便于实现，我们可以维护一个**反向栈**（数组/字符串）：让栈顶（末尾）对应“后缀的第一个字符”。此时判断右邻只需看栈顶元素，若需要保留则把当前字符**压栈**，最后把栈整体反转得到答案。整个删除步骤只需**单次线性扫描**。

算法要点：

* 算法范式：**模拟 + 贪心 + 栈**
* 核心思路：先按规则替换；再右到左单扫，利用“后缀首字符 = 栈顶”判定是否删除当下字符；不出现回头或多次扫描。


## 复杂度分析

* 时间复杂度：
  第一步替换 `O(n)`，第二步单栈模拟 `O(n)`，总计 `O(n)`。
* 空间复杂度：
  需要额外栈/数组存储中间结果，`O(n)`。


## 代码实现

### Python

```python
# 题面功能写在外部函数里，主函数只做输入输出

import sys

# 将小写字母循环前驱、大写字母循环后继
def transform_string(s: str) -> str:
    res = []
    for ch in s:
        if 'a' <= ch <= 'z':
            # 小写向前一位，a 的前驱是 z
            if ch == 'a':
                res.append('z')
            else:
                res.append(chr(ord(ch) - 1))
        else:
            # 大写向后一位，Z 的后继是 A
            if ch == 'Z':
                res.append('A')
            else:
                res.append(chr(ord(ch) + 1))
    return ''.join(res)

# 判断是否同字母异大小写
def is_toggle(a: str, b: str) -> bool:
    return a.lower() == b.lower() and a.islower() != b.islower()

# 第二步：从右到左删除，栈模拟（栈顶是右邻）
def delete_by_rule(t: str) -> str:
    rev_stack = []  # 维护“后缀的反向”，栈顶为后缀第一个字符
    for i in range(len(t) - 1, -1, -1):
        c = t[i]
        if rev_stack and is_toggle(c, rev_stack[-1]):
            # 与右邻同字母异大小写 -> 删除 c（跳过）
            continue
        else:
            # 保留 c，把它放到后缀最前（反向栈中为压栈）
            rev_stack.append(c)
    # 反转栈得到最终顺序
    return ''.join(reversed(rev_stack))

def solve():
    data = sys.stdin.read().strip().split()
    n = int(data[0])  # 题目保证合法
    s = data[1]

    t = transform_string(s)
    ans = delete_by_rule(t)
    print(ans)

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {

    // 将字符按规则替换：小写前驱，大写后继
    static char transformChar(char c) {
        if (c >= 'a' && c <= 'z') {
            return c == 'a' ? 'z' : (char)(c - 1);
        } else {
            return c == 'Z' ? 'A' : (char)(c + 1);
        }
    }

    // 判断是否同字母异大小写
    static boolean isToggle(char a, char b) {
        return Character.toLowerCase(a) == Character.toLowerCase(b)
                && Character.isLowerCase(a) != Character.isLowerCase(b);
    }

    // 替换整串
    static String transformString(String s) {
        char[] arr = s.toCharArray();
        for (int i = 0; i < arr.length; i++) {
            arr[i] = transformChar(arr[i]);
        }
        return new String(arr);
    }

    // 第二步：从右到左扫描，栈模拟（用 StringBuilder 做反向栈）
    static String deleteByRule(String t) {
        StringBuilder rev = new StringBuilder(); // 栈顶是最后一个字符
        for (int i = t.length() - 1; i >= 0; i--) {
            char c = t.charAt(i);
            if (rev.length() > 0) {
                char rightNeighbor = rev.charAt(rev.length() - 1); // 后缀首字符
                if (isToggle(c, rightNeighbor)) {
                    // 删除 c：跳过
                    continue;
                }
            }
            // 保留 c：压栈
            rev.append(c);
        }
        // 反转得到最终答案
        return rev.reverse().toString();
    }

    public static void main(String[] args) throws IOException {
        // 读取输入（数据量较大，使用 BufferedReader）
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String s = br.readLine().trim();

        String t = transformString(s);
        String ans = deleteByRule(t);
        System.out.println(ans);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 将字符按规则替换：小写前驱，大写后继
char transformChar(char c) {
    if ('a' <= c && c <= 'z') {
        return (c == 'a') ? 'z' : char(c - 1);
    } else {
        return (c == 'Z') ? 'A' : char(c + 1);
    }
}

// 判断是否同字母异大小写
bool isToggle(char a, char b) {
    return (tolower(a) == tolower(b)) &&
           (islower(a) != islower(b));
}

// 替换整串
string transformString(const string &s) {
    string t = s;
    for (char &c : t) c = transformChar(c);
    return t;
}

// 第二步：从右到左扫描，栈模拟（用字符串作为反向栈）
string deleteByRule(const string &t) {
    string rev; // rev 的末尾是“后缀首字符”
    rev.reserve(t.size());
    for (int i = (int)t.size() - 1; i >= 0; --i) {
        char c = t[i];
        if (!rev.empty() && isToggle(c, rev.back())) {
            // 删除 c（跳过）
            continue;
        } else {
            // 保留 c（压栈）
            rev.push_back(c);
        }
    }
    // 反转得到最终答案
    reverse(rev.begin(), rev.end());
    return rev;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    string s;
    if (!(cin >> n)) return 0;
    cin >> s;

    string t = transformString(s);
    string ans = deleteByRule(t);
    cout << ans << '\n';
    return 0;
}
```