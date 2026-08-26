## 解题思路

题目给定一个长度恰好为 $5$ 的字符串，且它由 $1$ 个 $a$、$1$ 个 $b$、$1$ 个 $c$、$1$ 个 $d$、$1$ 个 $e$ 组成，因此字符串中一定存在且只存在一个字符 $a$。

这里可以使用 线性查找算法，从左到右遍历字符串，找到字符 $a$ 时，输出它的位置即可。

实现方法如下：

先读入字符串，然后依次检查每个位置上的字符是否为 $a$。
如果当前字符是 $a$，由于题目下标从 $1$ 开始，所以输出当前位置下标加 $1$ 即可。

## 复杂度分析

字符串长度固定为 $5$，最多只需要遍历一遍。

时间复杂度为 $O(n)$，其中 $n=5$。
空间复杂度为 $O(1)$。

## 代码实现

### Python

```python
def find_a_pos(s):
    # 线性查找字符 a 的位置
    for i in range(len(s)):
        if s[i] == 'a':
            return i + 1  # 题目下标从 1 开始


if __name__ == "__main__":
    # 输入字符串
    s = input().strip()
    
    # 输出结果
    print(find_a_pos(s))
```

### Java

```java
import java.util.Scanner;

public class Main {
    public static int findAPos(String s) {
        // 线性查找字符 a 的位置
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == 'a') {
                return i + 1; // 题目下标从 1 开始
            }
        }
        return -1; // 按题意不会出现
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        // 输入字符串
        String s = sc.next();
        
        // 输出结果
        System.out.println(findAPos(s));
    }
}
```

### C++

```cpp
#include <iostream>
#include <string>
using namespace std;

int findAPos(string s) {
    // 线性查找字符 a 的位置
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == 'a') {
            return i + 1; // 题目下标从 1 开始
        }
    }
    return -1; // 按题意不会出现
}

int main() {
    string s;
    
    // 输入字符串
    cin >> s;
    
    // 输出结果
    cout << findAPos(s) << endl;
    
    return 0;
}
```