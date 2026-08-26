# 题解

## 题面描述

给定一个长度为 $n$ 的字符串 $s$，仅包含字符 $e,l,m$。如果一个字符串满足：不存在连续的子串 $ee$、$lm$、$ml$、$ll$、$mm$，则称该字符串为 **eleme 型字符串**。小红希望判断给定字符串是否可以重新排列（重排）为一个 **eleme 型字符串**，如果可以则输出任意一个重排结果，否则输出 `No`。

---

## 思路解析

由于限制条件要求字符串中不存在连续相同或不允许的相邻字符，我们仔细观察允许的相邻字符：

- 不允许出现连续 $ee$，因此两个 $e$ 不能相邻；
- 不允许出现 $lm$、$ml$、$ll$、$mm$，因此任意两个非 $e$ 字符也不能相邻。

分析后可以发现，只有合法的相邻组合为：
- $e$ 后面可以跟 $l$ 或 $m$（即非 $e$ 字符）；
- 非 $e$ 字符后面必须跟 $e$。

这说明整个合法字符串必定是交替出现 $e$ 和 非 $e$ 字符的形式。也就是说合法的排列有两种情况：

1. **模式一：以 $e$ 开头**  
   格式为：  
   $$ e, \, x, \, e, \, x, \, e, \, x, \, \ldots $$
   其中 $x$ 表示 $l$ 或 $m$。  
   令 $n$ 为字符串长度，则：  
   - 奇数位（1-indexed）必须为 $e$，个数为 $\lceil n/2 \rceil$  
   - 偶数位为非 $e$ 字符，个数为 $\lfloor n/2 \rfloor$

2. **模式二：以非 $e$ 字符开头**  
   格式为：  
   $$ x, \, e, \, x, \, e, \, x, \, e, \, \ldots $$
   此时：
   - 奇数位为非 $e$ 字符，个数为 $\lceil n/2 \rceil$
   - 偶数位为 $e$，个数为 $\lfloor n/2 \rfloor$

因此，只需统计字符串中 $e$ 的个数以及非 $e$ 的总数（即 $l$ 和 $m$ 的总和），设：
- $cnt\_e$ 为 $e$ 的个数，
- $cnt\_non = n - cnt\_e$ 为非 $e$ 字符的个数。

判断条件：
- 如果 $cnt\_e = \lceil n/2 \rceil$ 且 $cnt\_non = \lfloor n/2 \rfloor$，那么按照 **模式一** 生成答案；
- 如果 $cnt\_e = \lfloor n/2 \rfloor$ 且 $cnt\_non = \lceil n/2 \rceil$，那么按照 **模式二** 生成答案；
- 否则无法满足条件，输出 `No`。

对于非 $e$ 字符，我们需要在 $l$ 和 $m$ 中恰好使用它们原来的个数，排列时可以任意选择顺序，因为它们之间不会直接相邻。

---

## 代码分析

1. **计数统计**：遍历字符串，统计 $cnt\_e$、$cnt\_l$、$cnt\_m$，得到 $cnt\_non = cnt\_l + cnt\_m$ 。
2. **判断模式**：根据字符串长度 $n$ 与统计数比较，确定使用模式一或模式二。
3. **生成答案**：  
   - 对于每个位置，如果要求该位置为 $e$，则直接填入 $e$；  
   - 如果要求非 $e$，则根据剩余 $l$ 和 $m$ 来填入字符（先用完 $l$ 或者 $m$ 均可）。
4. **输出结果**：如果满足任一模式则输出答案，否则输出 `No`。

---

## C++

```cpp
#include <iostream>
#include <string>
using namespace std;
 
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    string s;
    cin >> s;
    int n = s.size();
    int cnt_e = 0, cnt_l = 0, cnt_m = 0;
    for(char c : s){
        if(c == 'e') cnt_e++;
        else if(c == 'l') cnt_l++;
        else if(c == 'm') cnt_m++;
    }
    int cnt_non = cnt_l + cnt_m;
    
    // 模式一：以 e 开头
    int need_e1 = (n + 1) / 2;      // 奇数位需要的 e 数量，即 ceil(n/2)
    int need_non1 = n / 2;          // 偶数位需要的非 e 数量，即 floor(n/2)
    
    // 模式二：以 非 e 开头
    int need_non2 = (n + 1) / 2;    // 奇数位需要的非 e 数量，即 ceil(n/2)
    int need_e2 = n / 2;            // 偶数位需要的 e 数量，即 floor(n/2)
    
    string ans = "";
    bool possible = false;
    
    // 尝试模式一
    if(cnt_e == need_e1 && cnt_non == need_non1){
        ans.resize(n);
        // 对于模式一，奇数位为 e, 偶数位为非 e
        // 下标从 0 开始，所以 0,2,4,... 为 e
        for(int i = 0; i < n; i++){
            if(i % 2 == 0){
                ans[i] = 'e';
            } else {
                // 如果 l 还未用完，就用 l，否则用 m
                if(cnt_l > 0){
                    ans[i] = 'l';
                    cnt_l--;
                } else {
                    ans[i] = 'm';
                    cnt_m--;
                }
            }
        }
        possible = true;
    }
    // 尝试模式二
    else if(cnt_e == need_e2 && cnt_non == need_non2){
        ans.resize(n);
        // 对于模式二，奇数位为非 e, 偶数位为 e
        for(int i = 0; i < n; i++){
            if(i % 2 == 0){
                // 非 e 的位置
                if(cnt_l > 0){
                    ans[i] = 'l';
                    cnt_l--;
                } else {
                    ans[i] = 'm';
                    cnt_m--;
                }
            } else {
                ans[i] = 'e';
            }
        }
        possible = true;
    }
    
    if(possible)
        cout << ans;
    else
        cout << "No";
        
    return 0;
}
```
## Python 

```python
# -*- coding: utf-8 -*-
# 统计字符串中字符 e, l, m 的个数
s = input().strip()
n = len(s)
cnt_e = s.count('e')
cnt_l = s.count('l')
cnt_m = s.count('m')
cnt_non = cnt_l + cnt_m

# 计算模式下需要的数量
need_e1 = (n + 1) // 2      # 模式一：以 e 开头时，e 的数量
need_non1 = n // 2          # 模式一：非 e 的数量

need_non2 = (n + 1) // 2    # 模式二：以非 e 开头时，非 e 的数量
need_e2 = n // 2            # 模式二：e 的数量

res = [''] * n
possible = False

# 尝试模式一：以 e 开头
if cnt_e == need_e1 and cnt_non == need_non1:
    for i in range(n):
        if i % 2 == 0:
            res[i] = 'e'
        else:
            if cnt_l > 0:
                res[i] = 'l'
                cnt_l -= 1
            else:
                res[i] = 'm'
                cnt_m -= 1
    possible = True
# 尝试模式二：以非 e 开头
elif cnt_e == need_e2 and cnt_non == need_non2:
    for i in range(n):
        if i % 2 == 0:
            if cnt_l > 0:
                res[i] = 'l'
                cnt_l -= 1
            else:
                res[i] = 'm'
                cnt_m -= 1
        else:
            res[i] = 'e'
    possible = True

if possible:
    print(''.join(res))
else:
    print("No")
```
## Java

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.next();
        int n = s.length();
        int cntE = 0, cntL = 0, cntM = 0;
        // 统计字符串中 e, l, m 的个数
        for (char c : s.toCharArray()) {
            if (c == 'e') {
                cntE++;
            } else if (c == 'l') {
                cntL++;
            } else if (c == 'm') {
                cntM++;
            }
        }
        int cntNon = cntL + cntM;
        
        // 模式一：以 e 开头
        int needE1 = (n + 1) / 2;    // 奇数位需要的 e 数量，即 ceil(n/2)
        int needNon1 = n / 2;        // 偶数位需要的非 e 数量，即 floor(n/2)
        
        // 模式二：以非 e 开头
        int needNon2 = (n + 1) / 2;  // 奇数位需要的非 e 数量，即 ceil(n/2)
        int needE2 = n / 2;          // 偶数位需要的 e 数量，即 floor(n/2)
        
        char[] ans = new char[n];
        boolean possible = false;
        
        // 尝试模式一：以 e 开头
        if (cntE == needE1 && cntNon == needNon1) {
            for (int i = 0; i < n; i++) {
                if (i % 2 == 0) {
                    ans[i] = 'e';
                } else {
                    if (cntL > 0) {
                        ans[i] = 'l';
                        cntL--;
                    } else {
                        ans[i] = 'm';
                        cntM--;
                    }
                }
            }
            possible = true;
        }
        // 尝试模式二：以非 e 开头
        else if (cntE == needE2 && cntNon == needNon2) {
            for (int i = 0; i < n; i++) {
                if (i % 2 == 0) {
                    if (cntL > 0) {
                        ans[i] = 'l';
                        cntL--;
                    } else {
                        ans[i] = 'm';
                        cntM--;
                    }
                } else {
                    ans[i] = 'e';
                }
            }
            possible = true;
        }
        
        if (possible) {
            System.out.println(new String(ans));
        } else {
            System.out.println("No");
        }
    }
}
```