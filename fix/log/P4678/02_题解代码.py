## 解题思路

只需考虑完全平方数。设 $x=i^2 \le n$，将其转为字符串 $s$，枚举所有切分点，将其分为左右两段：

* 两段都非空；
* 不允许有前导零（除单独的 `"0"`）；
* 转为整数后，两段都必须是完全平方数。

为快速判断某个数是否为完全平方数，预处理所有不超过 $10^9$ 的平方数，存入哈希集合。

将所有满足条件的数预处理出来并排序。对于每个询问 $n$，用二分查找统计不超过 $n$ 的数量。

涉及算法：

* 枚举（平方数 + 切分点）
* 哈希集合判定
* 二分查找

## 复杂度分析

设最大平方根为 $M=\lfloor \sqrt{10^9} \rfloor \approx 3\times 10^4$。

* 预处理：每个平方数最多检查 10 个切分点
  时间复杂度：$O(M)$
* 单次查询（二分）：$O(\log M)$

空间复杂度：$O(M)$


## 代码实现

### Python

```python
import sys
from bisect import bisect_right


# 判断字符串表示的一段是否满足“无前导零”要求
def valid_part(part):
    # 单个字符一定合法，例如 "0"、"4"
    if len(part) == 1:
        return True
    # 长度大于 1 时，首字符不能为 0
    return part[0] != '0'


# 预处理所有不超过 limit 的“完完全全平方数”
def build_good_numbers(limit):
    # 最大平方根
    max_root = int(limit ** 0.5)

    # 预处理所有完全平方数，放入集合中便于 O(1) 判断
    square_set = set()
    for i in range(max_root + 1):
        square_set.add(i * i)

    good = []

    # 枚举每一个完全平方数
    for i in range(1, max_root + 1):
        x = i * i
        s = str(x)
        m = len(s)

        # 枚举所有切分点
        for cut in range(1, m):
            left = s[:cut]
            right = s[cut:]

            # 若某一段存在非法前导零，则该切分无效
            if not valid_part(left) or not valid_part(right):
                continue

            # 转成整数后判断是否都是完全平方数
            a = int(left)
            b = int(right)
            if a in square_set and b in square_set:
                good.append(x)
                break

    return good


def count_not_greater(good, n):
    # 二分查找第一个大于 n 的位置，该位置下标即 <= n 的个数
    return bisect_right(good, n)


def main():
    input = sys.stdin.readline

    t = int(input().strip())

    # 题目最大上界为 1e9，预处理一次即可
    good = build_good_numbers(10 ** 9)

    for _ in range(t):
        n = int(input().strip())
        print(count_not_greater(good, n))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;


public class Main {

    // 判断字符串表示的一段是否满足“无前导零”要求
    public static boolean validPart(String part) {
        // 单个字符一定合法，例如 "0"、"9"
        if (part.length() == 1) {
            return true;
        }
        // 长度大于 1 时，首字符不能为 0
        return part.charAt(0) != '0';
    }

    // 预处理所有不超过 limit 的“完完全全平方数”
    public static List<Integer> buildGoodNumbers(int limit) {
        // 最大平方根
        int maxRoot = (int) Math.sqrt(limit);

        // 预处理所有完全平方数，放入哈希集合中便于快速判断
        HashSet<Integer> squareSet = new HashSet<>();
        for (int i = 0; i <= maxRoot; i++) {
            squareSet.add(i * i);
        }

        List<Integer> good = new ArrayList<>();

        // 枚举每一个完全平方数
        for (int i = 1; i <= maxRoot; i++) {
            int x = i * i;
            String s = String.valueOf(x);
            int m = s.length();

            // 枚举所有切分点
            for (int cut = 1; cut < m; cut++) {
                String left = s.substring(0, cut);
                String right = s.substring(cut);

                // 若某一段存在非法前导零，则该切分无效
                if (!validPart(left) || !validPart(right)) {
                    continue;
                }

                // 转成整数后判断是否都是完全平方数
                int a = Integer.parseInt(left);
                int b = Integer.parseInt(right);

                if (squareSet.contains(a) && squareSet.contains(b)) {
                    good.add(x);
                    break;
                }
            }
        }

        return good;
    }

    // 二分统计 <= n 的个数
    public static int countNotGreater(List<Integer> good, int n) {
        int left = 0;
        int right = good.size();

        // 查找第一个大于 n 的位置
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (good.get(mid) <= n) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int t = Integer.parseInt(br.readLine().trim());

        // 题目最大上界为 1e9，预处理一次即可
        List<Integer> good = buildGoodNumbers(1000000000);

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < t; i++) {
            int n = Integer.parseInt(br.readLine().trim());
            sb.append(countNotGreater(good, n)).append('\n');
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
#include <unordered_set>
#include <algorithm>

using namespace std;


// 判断字符串表示的一段是否满足“无前导零”要求
bool validPart(const string& part) {
    // 单个字符一定合法，例如 "0"、"1"
    if (part.size() == 1) {
        return true;
    }
    // 长度大于 1 时，首字符不能为 0
    return part[0] != '0';
}


// 预处理所有不超过 limit 的“完完全全平方数”
vector<int> buildGoodNumbers(int limit) {
    // 最大平方根
    int maxRoot = (int)sqrt(limit);

    // 预处理所有完全平方数，放入哈希集合中便于快速判断
    unordered_set<int> squareSet;
    for (int i = 0; i <= maxRoot; i++) {
        squareSet.insert(i * i);
    }

    vector<int> good;

    // 枚举每一个完全平方数
    for (int i = 1; i <= maxRoot; i++) {
        int x = i * i;
        string s = to_string(x);
        int m = (int)s.size();

        // 枚举所有切分点
        for (int cut = 1; cut < m; cut++) {
            string left = s.substr(0, cut);
            string right = s.substr(cut);

            // 若某一段存在非法前导零，则该切分无效
            if (!validPart(left) || !validPart(right)) {
                continue;
            }

            // 转成整数后判断是否都是完全平方数
            int a = stoi(left);
            int b = stoi(right);

            if (squareSet.count(a) && squareSet.count(b)) {
                good.push_back(x);
                break;
            }
        }
    }

    return good;
}


// 二分统计 <= n 的个数
int countNotGreater(const vector<int>& good, int n) {
    // upper_bound 返回第一个大于 n 的位置
    return upper_bound(good.begin(), good.end(), n) - good.begin();
}


int main() {
    int T;
    cin >> T;

    // 题目最大上界为 1e9，预处理一次即可
    vector<int> good = buildGoodNumbers(1000000000);

    while (T--) {
        int n;
        cin >> n;
        cout << countNotGreater(good, n) << '\n';
    }

    return 0;
}
```