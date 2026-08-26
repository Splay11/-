# 题解

## 题目描述

给定三个小写字母 $a,b,c$ 和一个小写字母 $p$，定义它们到字母 $p$ 之间的距离之和为：  
- 在字母表中，字符 $p$ 到字符 $a$ 之间相差的字母数量  
- 加上字符 $p$ 到字符 $b$ 之间相差的字母数量  
- 再加上字符 $p$ 到字符 $c$ 之间相差的字母数量  

注意字母表是线性的，‘$a$’和‘$z$’不相邻。  
输入第一行包含整数 $T\;(1\le T\le10^3)$ 表示测试组数。每组测试数据第一行给出三个小写字母 $a,b,c$；第二行给出小写字母 $p$。  
输出每组测试数据计算得到的距离和。  

---

## 思路

1. 先将字母映射到数字位置：令字符 $x$ 对应位置  
   $$\mathrm{pos}(x)=x-'a'+1$$  
2. 对于任意两个字母 $x$ 和 $y$，它们之间的距离（中间字母数）为  
   $$d(x,y)=|\mathrm{pos}(x)-\mathrm{pos}(y)|-1$$  
3. 题目要求计算  
   $$S=d(p,a)+d(p,b)+d(p,c)$$  
4. 对每组数据直接按上述公式累加即可。由于 $T\le10^3$，且每组只做常数次运算，时间复杂度为 $O(T)$。

## C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 将小写字母 ch 转换为 1~26 的数字
int toPos(char ch) {
    return ch - 'a' + 1;
}

// 计算两个字母 x 和 y 之间中间字母的数量
int dist(char x, char y) {
    int dx = abs(toPos(x) - toPos(y)) - 1;
    return max(0, dx);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        char a, b, c, p;
        cin >> a >> b >> c;
        cin >> p;
        int ans = dist(p, a) + dist(p, b) + dist(p, c);
        cout << ans << "\n";
    }
    return 0;
}
```
## Python

```python
# 将小写字母 ch 转换为 1~26 的数字
def to_pos(ch):
    return ord(ch) - ord('a') + 1

# 计算两个字母 x 和 y 之间中间字母的数量
def dist(x, y):
    dx = abs(to_pos(x) - to_pos(y)) - 1
    return max(0, dx)

def main():
    import sys
    data = sys.stdin.read().split()
    T = int(data[0])
    idx = 1
    for _ in range(T):
        a, b, c = data[idx], data[idx+1], data[idx+2]
        p = data[idx+3]
        idx += 4
        ans = dist(p, a) + dist(p, b) + dist(p, c)
        print(ans)

if __name__ == "__main__":
    main()
```
## Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 将小写字母 ch 转换为 1~26 的数字
    static int toPos(char ch) {
        return ch - 'a' + 1;
    }

    // 计算两个字母 x 和 y 之间中间字母的数量
    static int dist(char x, char y) {
        int dx = Math.abs(toPos(x) - toPos(y)) - 1;
        return Math.max(0, dx);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine());
        while (T-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            char a = st.nextToken().charAt(0);
            char b = st.nextToken().charAt(0);
            char c = st.nextToken().charAt(0);
            char p = br.readLine().charAt(0);
            int ans = dist(p, a) + dist(p, b) + dist(p, c);
            System.out.println(ans);
        }
    }
}
```