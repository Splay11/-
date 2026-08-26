## 解题思路

### 基本操作

1. 读入 $s$ 和 $t$。
2. 计算 $m=|t|$，令 $h=m/2$。
3. 取 $t_{\text{前}}=t[0,..,h-1]$, $t_{\text{后}}=t[h,..,m-1]$.
4. 新 $s'=s + t_{\text{后}}$。
5. 输出 $s'$ 与 $t_{\text{前}}$。

### 算法复杂度

* 时间复杂度：$O(n+m)$，即读写与拼接字符串的线性时间。
* 空间复杂度：$O(n+m)$，用于存储结果字符串。

## 代码实现

### Python

```python
def main():
    s = input().rstrip('\n')
    t = input().rstrip('\n')
    m = len(t)
    h = m // 2
    # 前后半部分
    pre = t[:h]
    suf = t[h:]
    # 嫁接并输出
    print(s + suf)
    print(pre)

if __name__ == '__main__':
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader rd = new BufferedReader(new InputStreamReader(System.in));
        String s = rd.readLine();
        String t = rd.readLine();
        int m = t.length();
        int h = m / 2;
        String pre = t.substring(0, h);     // 前半部分
        String suf = t.substring(h);        // 后半部分
        // 嫁接并输出
        System.out.println(s + suf);
        System.out.println(pre);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    // 读取整行，包括空格
    getline(cin, s);
    getline(cin, t);
    int m = t.size();
    int h = m / 2;
    // 前后半部分
    string pre = t.substr(0, h);
    string suf = t.substr(h);
    // 嫁接并输出
    cout << s << suf << "\n";
    cout << pre << "\n";
    return 0;
}
```