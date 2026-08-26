## 题解

## 题面描述

给定一个仅由小写字母组成的字符串 $s$，长度满足 $1 \le |s| \le 10^5$。  
游游从字符串开头开始书写，每次书写的字母数依次递增：  
- 第 $1$ 行书写接下来的 $1$ 个字母  
- 第 $2$ 行书写接下来的 $2$ 个字母  
- 第 $3$ 行书写接下来的 $3$ 个字母  
- …  
- 第 $i$ 行书写接下来的 $i$ 个字母  
如果在某一行需要书写的字符数大于剩余字符数，则将剩余字符全部书写后停止。  
最后，将每一行的首字母按行从上到下依次连接形成一个新字符串，输出该字符串。
---

## 思路

1. 使用一个下标变量（例如 $index$）来记录当前在字符串中的位置。  
2. 定义一个计数器 $i$，表示当前需要书写的字符数，从 $1$ 开始递增。  
3. 每一轮判断：  
   - 如果剩余字符数（即 $|s| - index$）大于或等于 $i$，则当前组能够完整书写，取这一组的首字母并将 $index$ 增加 $i$，然后 $i$ 自增。  
   - 如果剩余字符数不足 $i$，则结束书写过程。  
4. 最后，将所有组的首字母拼接起来输出。

---

## 代码分析

- **时间复杂度**：  
  每个字符最多被访问一次，因此时间复杂度为 $O(|s|)$。

- **空间复杂度**：  
  只使用常数级别的额外空间，因此空间复杂度为 $O(1)$（不考虑存储输入字符串的空间）。

- **问题本质**：  
  题目考察的是对字符串的遍历与分组处理，以及边界条件的判断，属于简单模拟题。

---

## C++ 

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    // 输入字符串
    string s;
    cin >> s;
    
    int n = s.size();       // 字符串长度
    string ans = "";        // 存储每一行首字母构成的答案
    int idx = 0;            // 当前处理的字符索引
    int line = 1;           // 当前行需要输出的字符数
    
    // 模拟书写过程
    while (idx < n) {
        // 如果剩余字符足够填满当前行
        if (n - idx >= line) {
            // 取当前行的第一个字符
            ans.push_back(s[idx]);
            // 移动下标，跳过当前行已经书写的字符
            idx += line;
        } else {
            // 剩余字符不足以书写完整当前行，直接取剩余部分的首字符后结束
            ans.push_back(s[idx]);
            break;
        }
        // 行数加1，准备下一行
        line++;
    }
    
    // 输出结果
    cout << ans << endl;
    return 0;
}

```
## Python 

```python
# 输入字符串
s = input().strip()

ans = []    # 用于存储每一行的首字母
idx = 0     # 当前字符的索引
line = 1    # 当前行需要书写的字符数

# 模拟书写过程
while idx < len(s):
    if len(s) - idx >= line:
        # 当前行足够长，取行首字母
        ans.append(s[idx])
        # 跳过当前行的字符
        idx += line
    else:
        # 剩余字符不足以构成完整一行，取首字符后结束
        ans.append(s[idx])
        break
    # 增加行数
    line += 1

# 输出答案
print("".join(ans))

```
## Java 

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        // 创建输入对象，读取字符串
        Scanner sc = new Scanner(System.in);
        String s = sc.next();
        
        int n = s.length();              // 字符串长度
        StringBuilder ans = new StringBuilder();  // 用于存储每一行首字母构成的答案
        int idx = 0;                     // 当前处理的字符索引
        int line = 1;                    // 当前行需要书写的字符数
        
        // 模拟书写过程
        while (idx < n) {
            if (n - idx >= line) {
                // 当前行字符足够，取该行的首字母
                ans.append(s.charAt(idx));
                // 移动索引，跳过当前行的字符
                idx += line;
            } else {
                // 剩余字符不足以构成完整一行，直接取剩余部分的首字母后结束
                ans.append(s.charAt(idx));
                break;
            }
            // 增加行数，准备下一行
            line++;
        }
        
        // 输出答案
        System.out.println(ans.toString());
    }
}

```