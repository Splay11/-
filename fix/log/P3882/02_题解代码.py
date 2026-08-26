## 解题思路

* 观察：满足“相邻字符大小写必须不同”的串，其大小写分布在下标奇偶上必然固定成两种模式之一：
  模式 A：下标偶位为大写、奇位为小写；
  模式 B：下标偶位为小写、奇位为大写。
  因此一个串是“好”，等价于它完全匹配模式 A 或完全匹配模式 B。

* “不错”定义为：至多翻转一个字符的大小写后能变成“好”。
  设串与两种模式的“失配数”分别为 `misA`、`misB`，则最少需要的翻转次数为 `min(misA, misB)`。
  于是：“不错”等价于 `min(misA, misB) ≤ 1`；“好”等价于 `min(misA, misB) = 0`。
  这一步是本题核心：把相邻约束转化为与两种全局交替模式的失配计数。

* 实现细节：

  1. 对每个字符串，线性扫描一次，判断每一位是否为大写（`isupper`），与两种模式的期望是否一致，分别累计 `misA` 与 `misB`。
  2. 若 `min(misA, misB) == 0`，好串计数加一；若 `min(misA, misB) ≤ 1`，不错串计数加一。
  3. 单字符串天然是好串（没有相邻对，也等价于至少有一种模式完全匹配）。

* 相关算法：贪心 / 枚举两种模式 + 失配计数（本质是模式匹配的计数判断），每个串 O(m) 线性判断。

## 复杂度分析

* 设共有 `n` 个串、每个长度不超过 `m (m ≤ 10)`，总长度为 `Σm`。
* 时间复杂度：对每个字符常数次判断，整体 **O(Σm)**（在数据范围内约 2×10⁵ 级别）。
* 空间复杂度：只用到常数额外变量，**O(1)**。

## 代码实现

### Python

```python
# 题意：统计“好串”和“不错串”的数量
# 方法：与两种交替模式比较，统计失配数 misA、misB
# 好串：min(misA, misB) == 0
# 不错串：min(misA, misB) <= 1

import sys

def analyze_string(s: str):
    # 统计与两种模式的失配数
    misA = 0  # 模式A：偶位大写、奇位小写
    misB = 0  # 模式B：偶位小写、奇位大写
    for i, ch in enumerate(s):
        is_up = ch.isupper()
        expect_up_A = (i % 2 == 0)  # 偶位应为大写
        expect_up_B = not expect_up_A  # 另一种模式
        if is_up != expect_up_A:
            misA += 1
        if is_up != expect_up_B:
            misB += 1
    good = 1 if min(misA, misB) == 0 else 0
    nice = 1 if min(misA, misB) <= 1 else 0
    return good, nice

def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    idx = 1
    good_cnt = 0
    nice_cnt = 0
    for _ in range(t):
        m = int(data[idx]); idx += 1
        s = data[idx]; idx += 1
        # 题面保证 s 只含英文字母，长度为 m
        g, n = analyze_string(s)
        good_cnt += g
        nice_cnt += n
    print(f"{good_cnt} {nice_cnt}")

if __name__ == "__main__":
    main()
```

### Java

```java
// 题意：对每个字符串，与两种交替模式比较，统计“好串”“不错串”数量
// 好串：min(misA, misB) == 0
// 不错串：min(misA, misB) <= 1

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // 判断字符串的好/不错
    // 返回：int[]{good(0/1), nice(0/1)}
    static int[] analyzeString(String s) {
        int misA = 0; // 模式A：偶位大写、奇位小写
        int misB = 0; // 模式B：偶位小写、奇位大写
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            boolean isUp = Character.isUpperCase(ch);
            boolean expectUpA = (i % 2 == 0); // 偶位应为大写
            boolean expectUpB = !expectUpA;   // 另一种模式
            if (isUp != expectUpA) misA++;
            if (isUp != expectUpB) misB++;
        }
        int good = (Math.min(misA, misB) == 0) ? 1 : 0;
        int nice = (Math.min(misA, misB) <= 1) ? 1 : 0;
        return new int[]{good, nice};
    }

    public static void main(String[] args) throws IOException {
        // 读取输入（BufferedReader 简洁高效，数据量也完全足够）
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        int n = Integer.parseInt(line.trim());
        int goodCnt = 0, niceCnt = 0;
        for (int i = 0; i < n; i++) {
            // 每组两行：m 和 s
            int m = Integer.parseInt(br.readLine().trim());
            String s = br.readLine().trim();
            int[] res = analyzeString(s);
            goodCnt += res[0];
            niceCnt += res[1];
        }
        System.out.println(goodCnt + " " + niceCnt);
    }
}
```

### C++

```cpp
// 题意：判断每个串是否为“好串”或“不错串”
// 方法：与两种交替模式比较失配数
// 好串：min(misA, misB) == 0
// 不错串：min(misA, misB) <= 1

#include <bits/stdc++.h>
using namespace std;

// 分析单个字符串，返回 {good(0/1), nice(0/1)}
pair<int,int> analyzeString(const string& s) {
    int misA = 0; // 模式A：偶位大写、奇位小写
    int misB = 0; // 模式B：偶位小写、奇位大写
    for (int i = 0; i < (int)s.size(); ++i) {
        char ch = s[i];
        bool isUp = isupper(static_cast<unsigned char>(ch));
        bool expectUpA = (i % 2 == 0); // 偶位应为大写
        bool expectUpB = !expectUpA;   // 另一种模式
        if (isUp != expectUpA) ++misA;
        if (isUp != expectUpB) ++misB;
    }
    int good = (min(misA, misB) == 0) ? 1 : 0;
    int nice = (min(misA, misB) <= 1) ? 1 : 0;
    return {good, nice};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    int goodCnt = 0, niceCnt = 0;
    for (int i = 0; i < n; ++i) {
        int m;
        string s;
        cin >> m;
        cin >> s; // 输入保证只含英文字母，长度为 m
        auto res = analyzeString(s);
        goodCnt += res.first;
        niceCnt += res.second;
    }
    cout << goodCnt << " " << niceCnt << "\n";
    return 0;
}
```