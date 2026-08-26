## 解题思路

目标是让字符串中**至少存在一个长度为$5$的子串**，经过修改后恰好变成$AcMer$，并且总代价最小。

因为目标子串固定为$AcMer$，所以我们只需要枚举原串中每一个长度为$5$的子串，计算把它改成$AcMer$的代价，取最小值即可。

设目标串为：

$target = "AcMer"$

对于某个位置$i$开始的长度为$5$的子串$str[i:i+5]$，逐位比较：

* 如果当前字符和目标字符完全相同，代价为$0$
* 如果两个字符不同，但大小写相同，说明只是同为大写或同为小写的字母替换，代价为$5$
* 如果两个字符大小写不同，代价为$6$

这样每个长度为$5$的子串都能在$O(5)$时间内算出修改代价。

由于$5$是常数，所以整体做法本质上是一次线性扫描，使用的算法就是**枚举子串 + 模拟计算代价**。

实现时写一个函数专门计算答案，主函数只负责输入输出即可。

## 复杂度分析

字符串长度为$n$。

需要枚举$n-4$个长度为$5$的子串，每个子串比较$5$个字符，因此时间复杂度为：

$O(n)$

只使用了若干常量变量，空间复杂度为：

$O(1)$

对于$|str| \le 200000$的数据范围，这个复杂度完全合适。

## 代码实现

### Python

```python
# 计算最小修改代价
def solve(s):
    target = "AcMer"
    ans = float('inf')

    # 枚举每个长度为5的子串
    for i in range(len(s) - 4):
        cost = 0
        for j in range(5):
            # 当前字符与目标字符相同，不需要代价
            if s[i + j] == target[j]:
                continue
            # 大小写相同，代价为5
            elif s[i + j].islower() == target[j].islower():
                cost += 5
            # 大小写不同，代价为6
            else:
                cost += 6
        ans = min(ans, cost)

    return ans


if __name__ == "__main__":
    s = input().strip()
    print(solve(s))
```

### Java

```java
import java.util.Scanner;

public class Main {

    // 计算最小修改代价
    public static int solve(String s) {
        String target = "AcMer";
        int ans = Integer.MAX_VALUE;

        // 枚举每个长度为5的子串
        for (int i = 0; i <= s.length() - 5; i++) {
            int cost = 0;
            for (int j = 0; j < 5; j++) {
                char a = s.charAt(i + j);
                char b = target.charAt(j);

                // 字符相同，不需要代价
                if (a == b) {
                    continue;
                }

                // 判断大小写是否相同
                boolean sameCase = Character.isLowerCase(a) == Character.isLowerCase(b);

                // 大小写相同代价为5，否则为6
                if (sameCase) {
                    cost += 5;
                } else {
                    cost += 6;
                }
            }
            ans = Math.min(ans, cost);
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();
        System.out.println(solve(s));
    }
}
```

### C++

```cpp
#include <iostream>
#include <string>
#include <climits>
using namespace std;

// 判断是否为小写字母
bool isLower(char c) {
    return c >= 'a' && c <= 'z';
}

// 计算最小修改代价
int solve(const string& s) {
    string target = "AcMer";
    int ans = INT_MAX;

    // 枚举每个长度为5的子串
    for (int i = 0; i <= (int)s.size() - 5; i++) {
        int cost = 0;
        for (int j = 0; j < 5; j++) {
            char a = s[i + j];
            char b = target[j];

            // 字符相同，不需要代价
            if (a == b) continue;

            // 大小写相同，代价为5；否则代价为6
            if (isLower(a) == isLower(b)) {
                cost += 5;
            } else {
                cost += 6;
            }
        }
        ans = min(ans, cost);
    }

    return ans;
}

int main() {
    string s;
    cin >> s;
    cout << solve(s) << endl;
    return 0;
}
```