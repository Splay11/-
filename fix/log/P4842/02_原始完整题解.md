## 解题思路

本题可以使用贪心算法。

对于字符 $c$，其伙伴字母为：

$partner(c) = 'a' + ('z' - c)$

也就是：

$a \leftrightarrow z$，$b \leftrightarrow y$，$c \leftrightarrow x$，$\dots$

观察每个字符替换为伙伴后的变化：

* 若字符在 $'a'$ 到 $'m'$ 之间，替换为伙伴后会变大，不应该主动选择。
* 若字符在 $'n'$ 到 $'z'$ 之间，替换为伙伴后会变小，选择它可以让字符串字典序变小。

为了让最终字符串字典序最小，应尽量让靠前的位置变小。

因此策略是：

1. 从左到右找到第一个满足 $s_i \ge 'n'$ 的位置。
2. 从这个位置开始，连续进行伙伴替换所有满足 $s_i \ge 'n'$ 的字符。
3. 一旦遇到 $s_i \le 'm'$ 的字符就停止，因为继续替换为伙伴会让该位置变大。
4. 如果不存在 $s_i \ge 'n'$ 的位置，则不进行操作。

这是因为字典序比较优先看最靠前不同的位置，所以第一个能变小的位置一定要操作；操作区间应尽量延伸到连续能变小的位置，但不能包含会变大的字符。

## 复杂度分析

设字符串长度为 $n$。

时间复杂度为 $O(n)$，每个字符最多被访问一次。

空间复杂度为 $O(n)$，需要将字符串转成字符数组进行修改。

所有测试数据字符串长度总和不超过 $2 \times 10^5$，该复杂度可以通过。

## 代码实现

### Python

```python
import sys


def get_min_string(s):
    # 将字符串转成列表，方便修改字符
    chars = list(s)
    n = len(chars)

    # 找到第一个替换为伙伴后会变小的字符，即 'n' 到 'z'
    i = 0
    while i < n and chars[i] <= 'm':
        i += 1

    # 从该位置开始，连续进行伙伴替换所有会变小的字符
    while i < n and chars[i] >= 'n':
        chars[i] = chr(ord('a') + ord('z') - ord(chars[i]))
        i += 1

    return ''.join(chars)


def main():
    input_data = sys.stdin.read().strip().split()
    t = int(input_data[0])
    ans = []

    for i in range(1, t + 1):
        s = input_data[i]
        ans.append(get_min_string(s))

    print('\n'.join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {

    static String getMinString(String s) {
        // 转成字符数组，方便原地修改
        char[] chars = s.toCharArray();
        int n = chars.length;

        // 找到第一个替换为伙伴后会变小的字符，即 'n' 到 'z'
        int i = 0;
        while (i < n && chars[i] <= 'm') {
            i++;
        }

        // 从该位置开始，连续进行伙伴替换所有会变小的字符
        while (i < n && chars[i] >= 'n') {
            chars[i] = (char)('a' + 'z' - chars[i]);
            i++;
        }

        return new String(chars);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int t = Integer.parseInt(br.readLine().trim());
        StringBuilder ans = new StringBuilder();

        for (int i = 0; i < t; i++) {
            String s = br.readLine().trim();
            ans.append(getMinString(s)).append('\n');
        }

        System.out.print(ans.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string getMinString(string s) {
    int n = s.size();

    // 找到第一个替换为伙伴后会变小的字符，即 'n' 到 'z'
    int i = 0;
    while (i < n && s[i] <= 'm') {
        i++;
    }

    // 从该位置开始，连续进行伙伴替换所有会变小的字符
    while (i < n && s[i] >= 'n') {
        s[i] = char('a' + 'z' - s[i]);
        i++;
    }

    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        string s;
        cin >> s;

        cout << getMinString(s) << '\n';
    }

    return 0;
}
```