## 解题思路

设当前要判断的字符串为 $s_i$。

根据题意，若存在两个不同下标 $j,k$，满足

$$
s_j + s_k = s_i
$$

那么 $s_i$ 就是“可删去的”。

由于参与拼接的两个字符串都必须是非空字符串，所以如果一个字符串 $s_i$ 能被拼接出来，那么一定存在一个切分位置 $p$，满足：

* 前半部分是 $s_i[0:p]$
* 后半部分是 $s_i[p:]$
* 且 $1 \le p < |s_i|$

于是问题就转化成：

对于每个字符串 $s_i$，枚举它的所有非空前后缀划分，判断：

* 前缀是否在原字符串序列中出现过；
* 后缀是否在原字符串序列中出现过；
* 如果前缀和后缀相同，还需要这个字符串至少出现两次，因为要求下标不同。

### 核心思路

1. 先统计每个字符串出现的次数，记为 `cnt`。
2. 对每个字符串 `s`：

   * 枚举切分点 `p = 1 ~ len(s)-1`
   * 令：

     * `left = s[:p]`
     * `right = s[p:]`
   * 分情况判断：

     * 若 `left != right`，只要 `cnt[left] > 0 && cnt[right] > 0`，则该字符串可删去；
     * 若 `left == right`，则必须 `cnt[left] >= 2`，因为需要两个不同位置。
3. 每个字符串只要存在一种合法切分，就计入答案一次。

### 为什么这样做是对的

因为任意一个满足条件的拼接方式 $s_j + s_k = s_i$，都对应着把 $s_i$ 在 $|s_j|$ 这个位置切开：

* 左边一定是 $s_j$
* 右边一定是 $s_k$

反过来，只要某个切分后的左右两部分都能在原数组中找到，并且能保证来自不同下标，那么就能拼出该字符串。

因此，枚举所有切分点并检查是否存在这样的两部分，恰好等价于题目的要求。

### 实现方法

使用哈希表统计字符串出现次数，之后逐个字符串枚举切分点即可。

这种做法不需要复杂算法，直接利用字符串切分和哈希查询就能在线性总长度范围内完成。

## 复杂度分析

设所有测试数据中字符串总长度之和为 $L$。

对于每个字符串，最多枚举 $|s|-1$ 个切分点，因此总切分次数为：

$$
O(L)
$$

每次切分后进行哈希表查询，均摊为 $O(1)$。

因此总时间复杂度为：

$$
O(L)
$$

空间复杂度主要是哈希表存储所有字符串出现次数：

$$
O(L)
$$


## 代码实现

### Python

```python
import sys


def solve_case(strings):
    # 统计每个字符串出现次数
    cnt = {}
    for s in strings:
        cnt[s] = cnt.get(s, 0) + 1

    ans = 0

    # 逐个字符串判断是否可删去
    for s in strings:
        ok = False
        m = len(s)

        # 枚举切分点，保证左右两部分都非空
        for i in range(1, m):
            left = s[:i]
            right = s[i:]

            # 左右部分不同，只需都存在即可
            if left != right:
                if cnt.get(left, 0) > 0 and cnt.get(right, 0) > 0:
                    ok = True
                    break
            # 左右部分相同，需要至少出现两次，才能对应不同下标
            else:
                if cnt.get(left, 0) >= 2:
                    ok = True
                    break

        if ok:
            ans += 1

    return ans


def main():
    input = sys.stdin.readline
    t = int(input().strip())
    res = []

    for _ in range(t):
        n = int(input().strip())
        strings = [input().strip() for _ in range(n)]
        res.append(str(solve_case(strings)))

    print("\n".join(res))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;

public class Main {

    // 判断一组字符串中有多少个字符串是可删去的
    public static int solveCase(String[] strings) {
        // 统计每个字符串出现次数
        HashMap<String, Integer> cnt = new HashMap<>();
        for (String s : strings) {
            cnt.put(s, cnt.getOrDefault(s, 0) + 1);
        }

        int ans = 0;

        // 逐个字符串判断
        for (String s : strings) {
            boolean ok = false;
            int m = s.length();

            // 枚举切分点，保证左右部分都非空
            for (int i = 1; i < m; i++) {
                String left = s.substring(0, i);
                String right = s.substring(i);

                // 左右部分不同，只要都出现过即可
                if (!left.equals(right)) {
                    if (cnt.getOrDefault(left, 0) > 0 && cnt.getOrDefault(right, 0) > 0) {
                        ok = true;
                        break;
                    }
                }
                // 左右部分相同，需要至少有两个位置
                else {
                    if (cnt.getOrDefault(left, 0) >= 2) {
                        ok = true;
                        break;
                    }
                }
            }

            if (ok) {
                ans++;
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine());
        StringBuilder sb = new StringBuilder();

        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine());
            String[] strings = new String[n];

            for (int i = 0; i < n; i++) {
                strings[i] = br.readLine();
            }

            sb.append(solveCase(strings)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

// 判断一组字符串中有多少个字符串是可删去的
int solveCase(const vector<string>& strings) {
    // 统计每个字符串出现次数
    unordered_map<string, int> cnt;
    for (const string& s : strings) {
        cnt[s]++;
    }

    int ans = 0;

    // 逐个字符串判断
    for (const string& s : strings) {
        bool ok = false;
        int m = (int)s.size();

        // 枚举切分点，保证左右两部分都非空
        for (int i = 1; i < m; i++) {
            string left = s.substr(0, i);
            string right = s.substr(i);

            // 左右部分不同，只需都存在
            if (left != right) {
                if (cnt.count(left) && cnt.count(right)) {
                    ok = true;
                    break;
                }
            }
            // 左右部分相同，需要至少出现两次
            else {
                if (cnt[left] >= 2) {
                    ok = true;
                    break;
                }
            }
        }

        if (ok) {
            ans++;
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<string> strings(n);
        for (int i = 0; i < n; i++) {
            cin >> strings[i];
        }

        cout << solveCase(strings) << '\n';
    }

    return 0;
}
```