# 题解

## 题面描述

试卷由$ n $道单项选择题构成，每道题只有$ a $, $ b $, $ c $, $ d $四个选项。小红在批改试卷时，如果在答案序列中存在一个**子序列**恰好等于字符串$ "abc" $，她会产生一定的愤怒值。其中，子序列是指从原字符串中删除任意个（可以为零、也可以为全部）字符后保留剩余字符的顺序。如果答案序列中存在多个不同的方式可以得到$ "abc" $这个子序列，那么小红的愤怒值就是所有方式的数量。

---

## 思路

我们可以利用动态规划（或累加统计）的思想，从左至右遍历字符串，同时维护以下三个变量：

- **$ count\_a $**：记录遍历过程中出现的字符$ a $的个数。  
- **$ count\_ab $**：记录能够构成子序列$ "ab" $的种数。对于每个新出现的$ b $，它可以与之前的所有$ a $组合，所以更新方式为：$ count\_ab += count\_a $。  
- **$ count\_abc $**：记录子序列$ "abc" $的种数。每当遍历到一个$ c $时，它可以和之前的$ "ab" $组合，因此更新方式为：$ count\_abc += count\_ab $。

对于字符 $ d $或其他字符，不会影响计数，因此忽略它们。

该方法时间复杂度为$ O(n) $，空间复杂度为$ O(1) $。

---

## 代码分析

- **变量定义：**  
  使用$ count\_a $, $ count\_ab $, $ count\_abc $三个变量分别统计$ a $、$ "ab" $、$ "abc" $的出现方式。

- **状态转移：**  
  - 若当前字符为$ a $，则$ count\_a $自增。  
  - 若当前字符为$ b $，则所有之前的$ a $均可构成$ "ab" $组合，即$ count\_ab += count\_a $。  
  - 若当前字符为$ c $，则所有之前的$ "ab" $均可构成$ "abc" $组合，即$ count\_abc += count\_ab $。

- **输出结果：**  
  最终答案为$ count\_abc $。

---

## C++ 解法

```cpp
#include <iostream>
#include <string>
using namespace std;

int main(){
    // 输入字符串答案序列, 字符串长度为n
    string s;
    cin >> s;
    
    // 定义变量, 分别统计字符a, 子序列"ab", 子序列"abc"
    long long count_a = 0, count_ab = 0, count_abc = 0;
    
    // 遍历整个字符串
    for(char ch : s){
        if(ch == 'a'){
            // 对于字符a, 自增计数
            count_a++;
        }
        else if(ch == 'b'){
            // 对于字符b, 可以与之前所有a组合得到"ab"子序列
            count_ab += count_a;
        }
        else if(ch == 'c'){
            // 对于字符c, 可以与之前所有"ab"组合得到"abc"子序列
            count_abc += count_ab;
        }
        // 字符d不会影响子序列的统计, 故忽略
    }
    
    // 输出子序列"abc"的统计值, 即小红的愤怒值
    cout << count_abc << endl;
    
    return 0;
}
```
## Python

```python
# 读入答案序列, 字符串长度为n
s = input().strip()

# 初始化变量, 用于分别统计a, 子序列"ab", 子序列"abc"
count_a = 0       # 统计字符a出现次数
count_ab = 0      # 统计子序列"ab"出现的种数
count_abc = 0     # 统计子序列"abc"出现的种数

# 遍历字符串中每个字符
for ch in s:
    if ch == 'a':
        # 遇到a, 更新count_a自增1
        count_a += 1
    elif ch == 'b':
        # 遇到b, 可与之前所有的a组合得到"ab"子序列
        count_ab += count_a
    elif ch == 'c':
        # 遇到c, 可与之前所有的"ab"组合得到"abc"子序列
        count_abc += count_ab
    #d字符不影响计数, 所以直接跳过

# 输出结果, 即子序列"abc"的总种数
print(count_abc)
```
## Java

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        // 创建 Scanner 读取输入, 输入字符串为只包含a, b, c, d的序列
        Scanner scanner = new Scanner(System.in);
        String s = scanner.nextLine().trim();
        scanner.close();
        
        // 初始化用于分别统计a, 子序列"ab", 子序列"abc"的变量
        long countA = 0;     // 记录a的累计个数
        long countAB = 0;    // 记录子序列"ab"的累计种数
        long countABC = 0;   // 记录子序列"abc"的累计种数
        
        // 遍历整个字符串
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == 'a') {
                // 当字符为a, 增加countA
                countA++;
            } else if (ch == 'b') {
                // 当字符为b, 所有之前的a均可与该b组合成"ab"子序列, 累加至countAB
                countAB += countA;
            } else if (ch == 'c') {
                // 当字符为c, 所有之前的"ab"均可与该c组合成"abc"子序列, 累加至countABC
                countABC += countAB;
            }
            // $d$ 字符不影响子序列统计, 因此直接忽略
        }
        
        // 输出结果, 即子序列"abc"的总数
        System.out.println(countABC);
    }
}
```