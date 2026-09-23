## 题面描述:

小明有根绳子，上面挂满了玻璃球，玻璃球的颜色有红、绿、蓝三种，分别用字符`r`、`g`、`b`表示，红色球的得分为1分，绿色球为2分，蓝色球为3分。此外，若某个球的颜色与前面的球相同，则会额外获得奖励分，具体来说，与前面1个球相同奖励1分，与前面2个球都相同奖励2分，以此类推。给定一串由这些字符组成的字符串，任务是计算这串玻璃球的总得分。

## 思路：模拟遍历

由于string的长度只有1e4，可以直接暴力做，n^2也只有1e8，小常数1s内可以跑完。直接往前遍历有几个字符和它相同即可。

或者基于简单dp的方式，每个位置保存它前面与它相等且串联的字符数量，每个字符只需要看其是否与上一个字符相等即可，相等则加1，否则置为0。

### 题解

本题要求计算一串由红、绿、蓝玻璃球组成的字符串的总得分。每种颜色的玻璃球对应不同的基础分数，其中红色球为1分，绿色球为2分，蓝色球为3分。此外，当一个球的颜色与前面的球相同时，会获得额外的奖励分数。具体来说，如果一个球与前面的第n个球颜色相同，将获得n-1分的奖励。

由于字符串的最大长度为10,000，暴力算法的复杂度为O(n^2)，在最坏情况下的操作次数为1亿，这在1秒内是可以接受的。因此，我们可以采用暴力方式逐个比较字符，也可以基于动态规划的思想来优化。

以下是基于暴力法的实现思路：

1. 遍历字符串中的每一个字符。
2. 对于每个字符，向前遍历其之前的字符，判断是否与当前字符相同。
3. 若相同，则根据相同的数量增加得分；若不相同，则停止继续向前查找。
4. 每个字符的基础得分加到总得分中。
5. 输出最终得分。


### JavaScript

```javascript
// 读取输入字符串
let s = readline(); 

// 初始化总得分
let ans = 0;

// 定义每种颜色玻璃球的基础得分
let score = { "r": 1, "g": 2, "b": 3 };

// 遍历字符串中的每一个字符
for (let i = 0; i < s.length; i++) {
    // 内层循环向前查找与当前字符相同的字符
    for (let j = i - 1; j >= 0; j--) {
        // 如果当前字符与前面的字符相同
        if (s[i] == s[j]) {
            ans += 1; // 增加相同字符的奖励分
        } else {
            break; // 如果不相同，则停止查找
        }
    }
    // 加上当前字符的基础得分
    ans += score[s[i]];
}

// 输出最终得分
print(ans);

```



### Java

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        // 创建一个Scanner对象，用于读取输入
        Scanner scanner = new Scanner(System.in);
        
        // 读取输入字符串
        String s = scanner.next();

        // 初始化总得分
        int ans = 0;

        // 定义每种颜色玻璃球的基础得分
        Map<Character, Integer> score = new HashMap<>();
        score.put('r', 1); // 红色球得分1
        score.put('g', 2); // 绿色球得分2
        score.put('b', 3); // 蓝色球得分3

        // 遍历字符串中的每一个字符
        for (int i = 0; i < s.length(); i++) {
            // 内层循环向前查找与当前字符相同的字符
            for (int j = i - 1; j >= 0; j--) {
                // 如果当前字符与前面的字符相同
                if (s.charAt(i) == s.charAt(j)) {
                    ans += 1; // 增加相同字符的奖励分
                } else {
                    break; // 如果不相同，则停止查找
                }
            }
            // 加上当前字符的基础得分
            ans += score.get(s.charAt(i));
        }

        // 输出最终得分
        System.out.println(ans);
    }
}

```



### Python

```python
# 读取输入字符串
s = input()  

# 初始化总得分
ans = 0  

# 定义每种颜色玻璃球的基础得分
score = {"r": 1, "g": 2, "b": 3}  

# 遍历字符串中的每一个字符
for i in range(len(s)):
    # 内层循环向前查找与当前字符相同的字符
    for j in range(i - 1, -1, -1):
        # 如果当前字符与前面的字符相同
        if s[i] == s[j]:
            ans += 1  # 增加相同字符的奖励分
        else:
            break  # 如果不相同，则停止查找
    
    # 加上当前字符的基础得分
    ans += score[s[i]]  

# 输出最终得分
print(ans)

```



### C++

```cpp
#include <iostream>
#include <string>
#include <map>

using namespace std;

int main() {
    // 读取输入字符串
    string s;
    cin >> s;

    // 初始化总得分
    int ans = 0;

    // 定义每种颜色玻璃球的基础得分
    map<char, int> score = { {'r', 1}, {'g', 2}, {'b', 3} };

    // 遍历字符串中的每一个字符
    for (int i = 0; i < s.length(); i++) {
        // 初始化当前字符与前面相同的数量
        int sameCount = 0;
        
        // 向前遍历，判断当前字符与前面的字符是否相同
        for (int j = i - 1; j >= 0; j--) {
            if (s[i] == s[j]) {
                sameCount++; // 相同的字符数量增加
            } else {
                break; // 遇到不同的字符，停止查找
            }
        }

        // 将相同字符的数量加入总得分（相同数量会产生额外的得分）
        ans += sameCount; // 奖励分数
        ans += score[s[i]]; // 当前字符的基础得分
    }

    // 输出最终得分
    cout << ans << endl;

    return 0;
}

```