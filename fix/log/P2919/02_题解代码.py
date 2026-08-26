## 题目分析
给定一个长度为 $n$ 的字符串 $s$（$1 \le n \le 10^6$），由大小写混合的英文字母构成。  
小歪从第一个字符开始依次输入，每次输入一个字符时需要花费以下时间：  
1. **基础时间**  
   - 如果该字符（不区分大小写）之前未出现过，需 500 毫秒；  
   - 否则，需 100 毫秒。  
2. **额外时间**（与前一个字符比较）  
   - 若当前字符与前一个字符完全相同（区分大小写），额外 23 毫秒；  
   - 若两字符不区分大小写在字母表中相邻（如 'a' 和 'b'），额外 44 毫秒。（不把 'a' 和 'z' 视为相邻）

输出小歪输入完整字符串所需的总时间。

## 解题思路
1. **线性扫描**  
   维护一个集合 `seen` （或大小为 26 的布尔数组）记录已经出现过的字母（全部转换成小写）。  
2. **状态维护**  
   - `prev` 保存前一个字符（用于计算额外时间）；  
   - `total` 累计总时间。  
3. **算法性质**  
   - 单次遍历，所有操作均为 O(1)；  
   - 时间复杂度 O(n)，空间复杂度 O(1)（固定大小的辅助结构）。

## 复杂度分析
- **时间复杂度**：遍历字符串一次，$O(n)$。  
- **空间复杂度**：只用常数级的额外空间（记录是否出现过的 26 个字母），$O(1)$。

## 代码实现

### Python

```python
import sys

def main():
    s = sys.stdin.readline().strip()
    seen = set()           # 已输入过的字母（小写）
    prev = None            # 前一个字符
    total = 0              # 累计时间

    for c in s:
        lower = c.lower()
        # 基础时间
        if lower not in seen:
            total += 500
            seen.add(lower)
        else:
            total += 100

        # 额外时间
        if prev is not None:
            if c == prev:
                total += 23
            elif abs(ord(lower) - ord(prev.lower())) == 1:
                total += 44

        prev = c

    print(total)

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        String s = in.readLine().trim();
        boolean[] seen = new boolean[26];  // 标记 a–z 是否输入过
        char prev = 0;                     // 前一个字符，0 表示无
        long total = 0;                    // 总时间

        for (char c : s.toCharArray()) {
            char lower = Character.toLowerCase(c);
            int idx = lower - 'a';
            // 基础时间
            if (!seen[idx]) {
                total += 500;
                seen[idx] = true;
            } else {
                total += 100;
            }
            // 额外时间
            if (prev != 0) {
                if (c == prev) {
                    total += 23;
                } else if (Math.abs(lower - Character.toLowerCase(prev)) == 1) {
                    total += 44;
                }
            }
            prev = c;
        }
        System.out.println(total);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    vector<bool> seen(26, false);  // 标记 a–z 是否输入过
    char prev = 0;                  // 前一个字符
    long long total = 0;            // 总时间

    for (char c : s) {
        char lower = tolower(c);
        int idx = lower - 'a';
        // 基础时间
        if (!seen[idx]) {
            total += 500;
            seen[idx] = true;
        } else {
            total += 100;
        }
        // 额外时间
        if (prev) {
            if (c == prev) {
                total += 23;
            } else if (abs(lower - tolower(prev)) == 1) {
                total += 44;
            }
        }
        prev = c;
    }

    cout << total << "\n";
    return 0;
}
```