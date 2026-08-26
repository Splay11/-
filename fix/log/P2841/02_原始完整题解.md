# 题解

## 题面描述
 
给定两个只包含小写字母的字符串，对于每个字符串，要求去除重复字母，即只保留该字母第一次出现的位置。然后判断处理后的两个字符串是否相同。若相同，输出 $"YES"$，否则输出 $"NO"$。  

---

## 思路

1. **去重操作**  
   对于每个字符串，我们只保留该字符串中第 $"1"$ 次出现的每个字母，即采用顺序扫描法，并利用一个数组或哈希表记录每个字母是否已经出现。  

2. **比较处理后的字符串**  
   分别对两个字符串进行上述操作后，再比较结果是否相等。  

3. **时间复杂度**  
   对于每个字符串，处理时间为 $"O(N)"$，其中 $"N"$ 为字符串长度。由于所有字符串总长度不超过 $"10^5"$，因此整体运行时间足够高效。

---

## 代码分析

- **变量说明**  
  - $"T"$：测试数据组数。  
  - $"s"$：输入的原始字符串。  
  - $"result"$：存储去重处理后的字符串。  
  - $"visited$"：大小为 $"26"$ 的布尔数组，用于记录是否遇到过某个字母。  

- **核心步骤**  
  1. 对每个字符串扫描，判断当前字母是否已出现（通过 $"visited$" 数组）。  
  2. 如果未出现，则添加到 $"result"$ 中，并标记为已出现。  
  3. 分别处理两个字符串后，对结果进行比较。  


## C++

```cpp
#include <iostream>
#include <string>
using namespace std;

// 去重函数，保留每个字母第一次出现的顺序
string removeDuplicates(const string &s) {
    // 用来标记26个字母是否出现过，初始均为false
    bool visited[26] = {false};  
    string result = "";
    // 遍历字符串中的每个字符
    for (char ch : s) {
        // 计算字母对应的索引
        int idx = ch - 'a';  
        // 如果该字符未出现过，则加入结果字符串，并标记为已出现
        if (!visited[idx]) {
            result.push_back(ch);
            visited[idx] = true;
        }
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;  // 测试组数T
    cin >> T;
    while (T--) {
        string s1, s2;
        cin >> s1 >> s2;  // 读取两组字符串
        // 分别对两个字符串进行去重处理
        string res1 = removeDuplicates(s1);
        string res2 = removeDuplicates(s2);
        // 判断两个处理后的字符串是否相同
        if (res1 == res2)
            cout << "YES" << "\n";
        else
            cout << "NO" << "\n";
    }
    return 0;
}
```
## Python

```python
# 定义函数去重处理字符串，保留每个字母第一次出现的顺序
def remove_duplicates(s: str) -> str:
    visited = [False] * 26  # 用列表记录26个小写字母是否已经出现过
    result = []  # 用于存放处理后的字符列表
    for ch in s:
        idx = ord(ch) - ord('a')  # 计算字母对应的索引
        if not visited[idx]:
            result.append(ch)  # 如果没有出现过则添加到结果中
            visited[idx] = True  # 标记为已出现
    return "".join(result)

if __name__ == '__main__':
    T = int(input().strip())  # 输入测试组数T
    for _ in range(T):
        s1 = input().strip()  # 输入字符串1
        s2 = input().strip()  # 输入字符串2
        # 处理字符串后比较
        if remove_duplicates(s1) == remove_duplicates(s2):
            print("YES")
        else:
            print("NO")
```
## Java

```java
import java.util.Scanner;

public class Main {
    // 定义方法去重处理字符串，保留每个字母第一次出现的顺序
    public static String removeDuplicates(String s) {
        boolean[] visited = new boolean[26];  // 用于标记26个小写字母是否已出现过
        StringBuilder result = new StringBuilder();  // 用于存放处理后的字符串
        for (char ch : s.toCharArray()) {
            int idx = ch - 'a';  // 计算字母对应的索引
            if (!visited[idx]) {  // 如果该字符没有出现过
                result.append(ch);  // 添加到结果中
                visited[idx] = true;  // 标记为已出现
            }
        }
        return result.toString();
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();  // 读取测试组数T
        // 循环处理每组测试数据
        for (int i = 0; i < T; i++) {
            String s1 = sc.next();  // 读取字符串1
            String s2 = sc.next();  // 读取字符串2
            // 比较两个处理后的字符串是否相同
            if (removeDuplicates(s1).equals(removeDuplicates(s2))) {
                System.out.println("YES");
            } else {
                System.out.println("NO");
            }
        }
        sc.close();
    }
}
```