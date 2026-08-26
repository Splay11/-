## 解题思路

这是典型的字符串动态规划问题。设 `str1` 长度为 `n`，`str2` 长度为 `m`，我们用**最长公共后缀**的思想做 **动态规划（DP）**：

* 定义：`dp[j]` 表示在当前处理到 `str1` 的第 `i` 个字符、`str2` 的第 `j` 个字符时（均为下标从 1 开始），两者**以这两个位置结尾**的最长公共子串长度。
* 转移：

  * 若 `str1[i-1] == str2[j-1]`，则 `dp[j] = dp[j-1] + 1`；
  * 否则 `dp[j] = 0`（以当前两个位置结尾的公共子串被中断）。
* 为了做到**空间复杂度 O(m)**，我们用**一维滚动数组**并让 `j` **从右往左**遍历，这样 `dp[j-1]` 仍是上一行（上一轮 `i-1`）的值。
* 同时维护当前最大长度 `bestLen` 及其在 `str1` 中的结束位置 `endPos`，最后返回 `str1[endPos-bestLen : endPos]`。

题目保证**最长公共子串存在且唯一**，因此只需记录全局最优一次即可。

## 复杂度分析

* 时间复杂度：`O(n * m)`，双重循环扫描两串。
* 空间复杂度：`O(m)`（一维滚动数组），亦即 `O(min(n,m))` 若根据较短串开数组。

## 代码实现

### Python

```python
# 功能函数：返回最长公共子串（滚动 DP，空间 O(m)）
def longest_common_substring(s1, s2):
    m = len(s2)
    dp = [0] * (m + 1)  # dp[j]：以 s2[j-1] 结尾的公共后缀长度（当前行）
    best_len, end_pos = 0, 0  # 记录全局最优长度及其在 s1 中的结束位置

    for i in range(1, len(s1) + 1):
        c = s1[i - 1]
        # 从右往左，确保 dp[j-1] 仍是上一行值
        for j in range(m, 0, -1):
            if c == s2[j - 1]:
                dp[j] = dp[j - 1] + 1
                if dp[j] > best_len:
                    best_len = dp[j]
                    end_pos = i
            else:
                dp[j] = 0
    return s1[end_pos - best_len: end_pos]

if __name__ == "__main__":
    import sys
    from ast import literal_eval  
    s = sys.stdin.read().strip()
    str1, str2 = literal_eval("(" + "".join(s.split()) + ")")
    ans = longest_common_substring(str1, str2)
    print(f"\"{ans}\"")  
```

### Java

```java
import java.io.*;
import java.util.*;

// 类名要求：Main
class Main {

    // 功能函数：一维滚动 DP 求最长公共子串
    public static String lcsSubstring(String a, String b) {
        int m = b.length();
        int[] dp = new int[m + 1];  // dp[j]：以 b[j-1] 结尾的公共后缀长度（当前行）
        int bestLen = 0, endPos = 0; // 记录最大长度及其在 a 中的结束位置

        for (int i = 1; i <= a.length(); i++) {
            char c = a.charAt(i - 1);
            // 从右往左更新，确保 dp[j-1] 仍是上一行的值
            for (int j = m; j >= 1; j--) {
                if (c == b.charAt(j - 1)) {
                    dp[j] = dp[j - 1] + 1;
                    if (dp[j] > bestLen) {
                        bestLen = dp[j];
                        endPos = i;
                    }
                } else {
                    dp[j] = 0;
                }
            }
        }
        return a.substring(endPos - bestLen, endPos);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder raw = new StringBuilder();
        for (String line; (line = br.readLine()) != null; ) raw.append(line).append('\n');

        // 将引号和逗号替换为空格，然后流式读取两个字符串
        String s = raw.toString().replace('\"', ' ').replace(',', ' ');
        StringTokenizer st = new StringTokenizer(s);
        String str1 = st.hasMoreTokens() ? st.nextToken() : "";
        String str2 = st.hasMoreTokens() ? st.nextToken() : "";

        String ans = lcsSubstring(str1, str2);
        System.out.println("\"" + ans + "\""); // 按样例输出带引号
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 功能函数：一维滚动 DP 求最长公共子串
string lcsSubstring(const string& a, const string& b) {
    int m = (int)b.size();
    vector<int> dp(m + 1, 0); // dp[j]：以 b[j-1] 结尾的公共后缀长度（当前行）
    int bestLen = 0, endPos = 0; // 记录最大长度及其在 a 中的结束位置

    for (int i = 1; i <= (int)a.size(); ++i) {
        char c = a[i - 1];
        // 从右往左更新，确保 dp[j-1] 仍是上一行的值
        for (int j = m; j >= 1; --j) {
            if (c == b[j - 1]) {
                dp[j] = dp[j - 1] + 1;
                if (dp[j] > bestLen) {
                    bestLen = dp[j];
                    endPos = i;
                }
            } else {
                dp[j] = 0;
            }
        }
    }
    return a.substr(endPos - bestLen, bestLen);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 按题意：替换字符 + 输入流
    string all, line;
    while (getline(cin, line)) {
        all += line;
        all += '\n';
    }
    // 将引号和逗号替换为空格，然后流式读取两个字符串
    for (char &ch : all) {
        if (ch == '\"' || ch == ',') ch = ' ';
    }
    stringstream ss(all);
    string str1, str2;
    ss >> str1 >> str2;

    string ans = lcsSubstring(str1, str2);
    cout << "\"" << ans << "\""; // 按样例输出带引号
    return 0;
}
```