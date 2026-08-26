## 解题思路

* 本题属于**模拟/字符串构造**。设记号串 `s = str(N)`（N 的十进制表示，如 `10`），第 `i` 行（从上到下）输出 `s` 连续重复 `i` 次，其中 `i` 从 `N` 递减到 `1`。
* 例如 `N=10` 时，首行是 `"10"` 重复 10 次，次行重复 9 次……直至最后一行重复 1 次。
* 实现方法：外部函数负责“将某个字符串重复 `cnt` 次并返回结果”；主函数完成读入 N、循环从 `N` 到 `1` 调用外部函数、逐行输出。

## 复杂度分析

* 设 `|s|` 为 `str(N)` 的长度（最大为 3，当 `N=100`），总输出长度为 `|s| * (N + (N-1) + ... + 1) = |s| * N(N+1)/2`。
* 时间复杂度：`O(N^2)`（以重复次数计）。
* 空间复杂度：`O(|s|)` 额外空间（每次只构造并输出当前一行，不保存全部结果）。

## 代码实现

### Python

```python
# 题面功能：构造由 N 的十进制表示组成的倒立金字塔

def repeat_token(s: str, cnt: int) -> str:
    """将字符串 s 重复 cnt 次并返回"""
    return s * cnt  # 直接使用字符串重复运算

def main():
    # 输入操作：读取正整数 N
    n = int(input().strip())
    s = str(n)  # N 的十进制表示

    # 从 N 到 1 逐行输出
    for i in range(n, 0, -1):
        line = repeat_token(s, i)  # 构造当前行
        print(line)

if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {
    // 外部函数：将字符串 s 重复 cnt 次
    public static String repeatToken(String s, int cnt) {
        StringBuilder sb = new StringBuilder(s.length() * cnt); // 预分配容量
        for (int i = 0; i < cnt; i++) {
            sb.append(s); // 追加一次 s
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // 输入操作：读取正整数 N（数据范围小，使用 Scanner 即可）
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) {
            sc.close();
            return;
        }
        int n = sc.nextInt();
        String s = String.valueOf(n); // N 的十进制表示

        // 从 N 到 1 逐行输出
        for (int i = n; i >= 1; i--) {
            String line = repeatToken(s, i); // 构造当前行
            System.out.println(line);
        }
        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <string>
using namespace std;

// 外部函数：将字符串 s 重复 cnt 次
string repeatToken(const string& s, int cnt) {
    string res;
    res.reserve(s.size() * cnt); // 预留空间，避免多次扩容
    for (int i = 0; i < cnt; ++i) {
        res += s; // 追加一次 s
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    // 输入操作：读取正整数 N
    if (!(cin >> n)) return 0;

    string s = to_string(n); // N 的十进制表示

    // 从 N 到 1 逐行输出
    for (int i = n; i >= 1; --i) {
        string line = repeatToken(s, i); // 构造当前行
        cout << line << '\n';
    }
    return 0;
}
```