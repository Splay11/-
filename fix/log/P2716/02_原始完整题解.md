# 题解

## 题面描述

给定一个字符串$ s $和一个正整数$ k $（$1 \leq k \leq 10$），以及$ q $个询问。对于每个询问给定一个字符串$ t $，若$ t $的某个**前缀**或**后缀**（要求长度至少为$ k $）是$ s $的子串，则输出“YES”，否则输出“NO”。  

---

## 思路

首先，我们通过遍历字符串$ s $提取出所有长度为$ k $的子串并存入集合，然后对于每个查询字符串$ t $，若其长度不小于$ k $，只需判断$ t $的前$ k $字符或后$ k $字符是否存在于集合中，从而高效地确定是否满足条件。

观察题目条件，对于任一字符串$ t $，其所有长度至少为$ k $的前缀都拥有相同的前$ k $个字符，同理，所有后缀都拥有相同的后$ k $个字符。因此，判断$ t $是否满足条件，只需要检查$ t $的前$ k $字符和后$ k $字符是否出现在$ s $中即可。  

具体步骤如下：
- **预处理**：遍历$ s $，提取所有长度为$ k $的连续子串，将其存入哈希集合（或其他快速查询数据结构）中。
- **查询**：对于每个询问字符串$ t $，若$ |t| < k $则必然不满足；否则，取$ t $的前$ k $字符和后$ k $字符，检查是否存在于预处理得到的集合中，满足任一条件则输出“YES”，否则输出“NO”。

这种方法利用了题目中$ k $较小的性质，降低了查询时的复杂度，并且整体时间复杂度为$ O(|s| + \sum|t|) $。

## C++ 
```cpp
#include <iostream>
#include <string>
#include <unordered_set>
using namespace std;

int main(){
    ios::sync_with_stdio(false); // 加速输入输出
    cin.tie(nullptr);
    
    string s;
    cin >> s;
    int q, k;
    cin >> q >> k;
    
    // 预处理：将字符串  s  中所有长度为  k  的子串存入集合
    unordered_set<string> substrSet;
    int len = s.size();
    for(int i = 0; i <= len - k; i++){
        substrSet.insert(s.substr(i, k)); // 截取从  i  开始的长度为  k  的子串
    }
    
    // 处理每个查询
    while(q--){
        string t;
        cin >> t;
        // 如果 $ t $ 长度小于  k ，则无法构成符合要求的前缀或后缀
        if(t.size() < k){
            cout << "NO\n";
            continue;
        }
        // 获取  t  的前  k  字符串和后  k  字符串
        string pre = t.substr(0, k);
        string suf = t.substr(t.size() - k, k);
        
        // 判断是否存在于  s  的子串集合中
        if(substrSet.count(pre) || substrSet.count(suf))
            cout << "YES\n";
        else
            cout << "NO\n";
    }
    return 0;
}
```
## Python

```python
def main():
    import sys
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    s = input_data[0]
    q = int(input_data[1])
    k = int(input_data[2])
    
    # 预处理：构造  s  中所有长度为  k  的子串集合
    substrSet = set()
    for i in range(len(s) - k + 1):
        substrSet.add(s[i:i+k])
    
    index = 3  # 后续数据的起始下标
    res = []
    for _ in range(q):
        t = input_data[index]
        index += 1
        # 若  t  长度小于  k ，则直接输出 "NO"
        if len(t) < k:
            res.append("NO")
        else:
            # 获取  t  的前  k  和后  k  子串
            pre = t[:k]
            suf = t[-k:]
            # 判断是否存在于  s  的子串集合中
            if pre in substrSet or suf in substrSet:
                res.append("YES")
            else:
                res.append("NO")
    # 输出所有结果
    sys.stdout.write("\n".join(res))

if __name__ == '__main__':
    main()
```
## Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 加速输入读取
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 读取字符串  s 
        String s = br.readLine().trim();
        // 读取第二行：询问次数  q  和长度限制  k 
        String[] secondLine = br.readLine().trim().split(" ");
        int q = Integer.parseInt(secondLine[0]);
        int k = Integer.parseInt(secondLine[1]);
        
        // 预处理：将  s  中所有长度为  k  的子串加入 HashSet
        HashSet<String> set = new HashSet<>();
        for (int i = 0; i <= s.length() - k; i++){
            set.add(s.substring(i, i + k));
        }
        
        StringBuilder sb = new StringBuilder();
        // 处理每个查询
        for (int i = 0; i < q; i++){
            String t = br.readLine().trim();
            // 如果  t  的长度小于  k ，则输出 "NO"
            if(t.length() < k){
                sb.append("NO\n");
            } else {
                // 获取  t  的前 k  和后  k  子串
                String pre = t.substring(0, k);
                String suf = t.substring(t.length() - k);
                // 判断是否存在于  s  的子串集合中
                if(set.contains(pre) || set.contains(suf))
                    sb.append("YES\n");
                else
                    sb.append("NO\n");
            }
        }
        // 输出所有结果
        System.out.print(sb);
    }
}
```