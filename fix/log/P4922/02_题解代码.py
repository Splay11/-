## 解题思路

设当前已经构造出的前缀中，每个小写字母出现了多少次。

对于位置 $i$，题目给出的 $a_i$ 表示：在位置 $i$ 之前，和 $s_i$ 相同的字符出现了 $a_i$ 次。

因此，在构造第 $i$ 个字符时，只需要找到一个当前出现次数恰好为 $a_i$ 的小写字母，把它放在当前位置，然后将该字母的出现次数加 $1$。

使用贪心算法即可：

* 初始时，$26$ 个小写字母出现次数都为 $0$；
* 从左到右遍历数组 $a$；
* 对于每个 $a_i$，寻找一个出现次数等于 $a_i$ 的字母；
* 如果找不到，说明无解，输出 $-1$；
* 如果找到，就把该字母加入答案，并更新它的出现次数。

因为字母之间本质上只看当前出现次数，选择任意一个满足条件的字母都可以。

## 复杂度分析

每个位置最多枚举 $26$ 个小写字母。

时间复杂度为 $O(26n)$，即 $O(n)$。

空间复杂度为 $O(26+n)$，即 $O(n)$，其中答案字符串占用 $O(n)$ 空间。

## 代码实现

### Python

```python
def build_string(n, a):
    # cnt[i] 表示第 i 个字母当前已经出现的次数
    cnt = [0] * 26
    ans = []

    for x in a:
        found = False

        # 寻找当前出现次数等于 x 的字母
        for i in range(26):
            if cnt[i] == x:
                ans.append(chr(ord('a') + i))
                cnt[i] += 1
                found = True
                break

        # 没有满足条件的字母，说明无解
        if not found:
            return "-1"

    return ''.join(ans)


def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(build_string(n, a))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {
    // 构造满足条件的字符串
    static String buildString(int n, int[] a) {
        // cnt[i] 表示第 i 个字母当前已经出现的次数
        int[] cnt = new int[26];
        StringBuilder ans = new StringBuilder();

        for (int x : a) {
            boolean found = false;

            // 寻找当前出现次数等于 x 的字母
            for (int i = 0; i < 26; i++) {
                if (cnt[i] == x) {
                    ans.append((char)('a' + i));
                    cnt[i]++;
                    found = true;
                    break;
                }
            }

            // 没有满足条件的字母，说明无解
            if (!found) {
                return "-1";
            }
        }

        return ans.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();
        while (t-- > 0) {
            int n = sc.nextInt();
            int[] a = new int[n];

            for (int i = 0; i < n; i++) {
                a[i] = sc.nextInt();
            }

            System.out.println(buildString(n, a));
        }

        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 构造满足条件的字符串
string buildString(int n, vector<int>& a) {
    // cnt[i] 表示第 i 个字母当前已经出现的次数
    vector<int> cnt(26, 0);
    string ans;

    for (int x : a) {
        bool found = false;

        // 寻找当前出现次数等于 x 的字母
        for (int i = 0; i < 26; i++) {
            if (cnt[i] == x) {
                ans.push_back(char('a' + i));
                cnt[i]++;
                found = true;
                break;
            }
        }

        // 没有满足条件的字母，说明无解
        if (!found) {
            return "-1";
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        cout << buildString(n, a) << '\n';
    }

    return 0;
}
```