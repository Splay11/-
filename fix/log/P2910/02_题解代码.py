# 题解

## 题面描述

给定一个长度为 $n$ 的字符串 $s$（下标从 1 开始），字符串仅由大小写字母组成。  
你有一个字符转换器，具有“阴”“阳”两种状态，初始状态为“阴”。  
按下标从小到大依次处理字符串中的每个字符：

- 如果当前状态为“阴”且字符为小写字母，则将其转换为对应的大写字母，并将状态切换为“阳”；
- 如果当前状态为“阳”且字符为大写字母，则将其转换为对应的小写字母，并将状态切换为“阴”；
- 否则，不做任何操作，状态保持不变。

输出操作完成后的字符串。

---

## 思路

1. 使用一个布尔变量 `state` 来表示转换器状态：  
   - `false` 表示“阴”态  
   - `true` 表示“阳”态  
2. 遍历字符串的每个位置 $i$（$1 \le i \le n$）：  
   - 若 `state == false` 且当前字符为小写，则将其转换为大写，`state = true`；  
   - 若 `state == true` 且当前字符为大写，则将其转换为小写，`state = false`；  
   - 其他情况直接跳过。  
3. 由于只需一次遍历，时间复杂度为 $O(n)$，额外空间为常数级。

---

## C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;                // 读取字符串长度
    string s;
    cin >> s;                // 读取输入字符串

    bool state = false;      // false 表示阴态，true 表示阳态
    for(int i = 0; i < n; i++){
        if(!state && islower(s[i])){    // 当前为阴态且字符为小写
            s[i] = toupper(s[i]);      // 转换为大写
            state = true;              // 切换为阳态
        }
        else if(state && isupper(s[i])){ // 当前为阳态且字符为大写
            s[i] = tolower(s[i]);      // 转换为小写
            state = false;             // 切换为阴态
        }
    }

    cout << s << "\n";       // 输出结果
    return 0;
}
```
## Python

```python
def main():
    import sys
    input = sys.stdin.readline

    n = int(input())           # 读取字符串长度
    s = list(input().strip())  # 读取并转为字符列表

    state = False              # False 表示阴态，True 表示阳态
    for i in range(n):
        if not state and s[i].islower():  # 阴态且当前字符为小写
            s[i] = s[i].upper()           # 转换为大写
            state = True                  # 切换为阳态
        elif state and s[i].isupper():    # 阳态且当前字符为大写
            s[i] = s[i].lower()           # 转换为小写
            state = False                 # 切换为阴态

    print(''.join(s))          # 输出结果

if __name__ == "__main__":
    main()
```
## Java 

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());         // 读取字符串长度
        StringBuilder sb = new StringBuilder(br.readLine().trim()); // 读取字符串

        boolean state = false;  // false 表示阴态，true 表示阳态
        for(int i = 0; i < n; i++){
            char c = sb.charAt(i);
            if(!state && Character.isLowerCase(c)){     // 阴态且字符为小写
                sb.setCharAt(i, Character.toUpperCase(c)); // 转为大写
                state = true;                           // 切换为阳态
            }
            else if(state && Character.isUpperCase(c)){ // 阳态且字符为大写
                sb.setCharAt(i, Character.toLowerCase(c)); // 转为小写
                state = false;                          // 切换为阴态
            }
        }

        System.out.println(sb.toString()); // 输出结果
    }
}
```