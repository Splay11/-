## 解题思路

01 串的权值定义为：只由字符 `'1'` 构成的非空连续子串数量。

如果一段连续的 `'1'` 的长度为 $len$，那么这段内部能产生的全 `'1'` 子串数量为：

$$
1 + 2 + \cdots + len = \frac{len(len+1)}{2}
$$

因此，整个字符串的权值等于所有连续 `'1'` 段贡献之和。

每次操作只翻转一个位置 $k$，只有包含位置 $k$ 的连续段会发生变化，其他位置的贡献不变。

我们维护所有字符 `'0'` 的位置，并额外加入两个哨兵位置：

$$
0,\ n+1
$$

对于某个位置 $k$：

设它左边最近的 `'0'` 位置为 $l$，右边最近的 `'0'` 位置为 $r$。

那么 $l$ 和 $r$ 之间原本是一段连续的 `'1'` 区间，中间可能包含被翻转的位置 $k$。

如果 $s[k] = 0$，翻转后变成 $1$，相当于把左右两段连续的 `'1'` 和位置 $k$ 合并。

左侧连续 `'1'` 长度为：

$$
a = k - l - 1
$$

右侧连续 `'1'` 长度为：

$$
b = r - k - 1
$$

新增的全 `'1'` 子串数量为：

$$
(a+1)(b+1)
$$

所以答案增加 $(a+1)(b+1)$。

如果 $s[k] = 1$，翻转后变成 $0$，相当于把一整段连续的 `'1'` 拆成左右两段，减少的全 `'1'` 子串数量同样为：

$$
(a+1)(b+1)
$$

所以答案减少 $(a+1)(b+1)$。

实现时：

Python 中没有内置有序集合，因此用树状数组维护哪些位置是 `'0'`，并通过前缀和和二分查找求某个位置左右最近的 `'0'`。

Java 使用 `TreeSet` 维护 `'0'` 的位置。

C++ 使用 `set` 维护 `'0'` 的位置。

注意答案最大可能达到：

$$
\frac{2 \times 10^5(2 \times 10^5 + 1)}{2}
$$

会超过 `int` 范围，因此 Java 和 C++ 中需要使用 `long` / `long long`。

## 复杂度分析

设字符串长度为 $n$，操作次数为 $q$。

初始化时需要扫描字符串一次，时间复杂度为 $O(n)$。

每次操作需要查询左右最近的 `'0'`，并更新一个位置：

Python 使用树状数组，每次操作复杂度为 $O(\log n)$。

Java 使用 `TreeSet`，每次操作复杂度为 $O(\log n)$。

C++ 使用 `set`，每次操作复杂度为 $O(\log n)$。

因此总时间复杂度为：

$$
O((n+q)\log n)
$$

空间复杂度为：

$$
O(n)
$$

该复杂度可以满足 $n,q \le 2 \times 10^5$ 的数据范围。

## 代码实现

### Python

```python
import sys


class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i, v):
        # 单点修改：把位置 i 的计数加上 v
        while i <= self.n:
            self.tree[i] += v
            i += i & -i

    def sum(self, i):
        # 查询前缀 [1, i] 中 0 的个数
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res

    def kth(self, k):
        # 查询第 k 个 0 在树状数组中的下标
        idx = 0
        bit = 1
        while bit * 2 <= self.n:
            bit *= 2

        while bit > 0:
            nxt = idx + bit
            if nxt <= self.n and self.tree[nxt] < k:
                idx = nxt
                k -= self.tree[nxt]
            bit //= 2

        return idx + 1


def calc(n, s, ops):
    m = n + 2
    bit = BIT(m)

    # 使用 1 下标存储字符串
    arr = [' '] + list(s)

    # 加入左哨兵 0，映射到树状数组下标 1
    bit.add(1, 1)

    # 加入字符串中所有 0 的位置，原位置 pos 映射到 pos + 1
    for i in range(1, n + 1):
        if arr[i] == '0':
            bit.add(i + 1, 1)

    # 加入右哨兵 n + 1，映射到树状数组下标 n + 2
    bit.add(n + 2, 1)

    ans = 0
    cnt = 0

    # 计算初始答案：每段连续 1 的贡献为 len * (len + 1) / 2
    for ch in s:
        if ch == '1':
            cnt += 1
        else:
            ans += cnt * (cnt + 1) // 2
            cnt = 0
    ans += cnt * (cnt + 1) // 2

    res = []

    for k in ops:
        idx = k + 1

        if arr[k] == '0':
            # k 当前是 0，翻转成 1，需要删除这个 0
            left_cnt = bit.sum(idx - 1)
            right_cnt = bit.sum(idx) + 1

            l = bit.kth(left_cnt) - 1
            r = bit.kth(right_cnt) - 1

            a = k - l - 1
            b = r - k - 1

            ans += (a + 1) * (b + 1)

            bit.add(idx, -1)
            arr[k] = '1'
        else:
            # k 当前是 1，翻转成 0，需要加入这个 0
            left_cnt = bit.sum(idx - 1)
            right_cnt = bit.sum(idx) + 1

            l = bit.kth(left_cnt) - 1
            r = bit.kth(right_cnt) - 1

            a = k - l - 1
            b = r - k - 1

            ans -= (a + 1) * (b + 1)

            bit.add(idx, 1)
            arr[k] = '0'

        res.append(ans)

    return res


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()

    ops = []
    for i in range(q):
        ops.append(int(data[3 + i]))

    res = calc(n, s, ops)

    print('\n'.join(map(str, res)))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.TreeSet;

public class Main {
    static long[] calc(int n, String s, int[] ops) {
        TreeSet<Integer> zero = new TreeSet<>();
        char[] arr = new char[n + 1];

        // 使用 1 下标存储字符串，方便按题目位置访问
        for (int i = 1; i <= n; i++) {
            arr[i] = s.charAt(i - 1);
        }

        // 加入左右哨兵，保证每个位置都能找到左右最近的 0
        zero.add(0);
        zero.add(n + 1);

        // 记录所有字符 0 的位置
        for (int i = 1; i <= n; i++) {
            if (arr[i] == '0') {
                zero.add(i);
            }
        }

        long ans = 0;
        long cnt = 0;

        // 计算初始答案：每段连续 1 的贡献为 len * (len + 1) / 2
        for (int i = 1; i <= n; i++) {
            if (arr[i] == '1') {
                cnt++;
            } else {
                ans += cnt * (cnt + 1) / 2;
                cnt = 0;
            }
        }
        ans += cnt * (cnt + 1) / 2;

        long[] res = new long[ops.length];

        for (int i = 0; i < ops.length; i++) {
            int k = ops[i];

            if (arr[k] == '0') {
                // k 当前是 0，翻转成 1，会合并左右两段连续 1
                int l = zero.lower(k);
                int r = zero.higher(k);

                long a = k - l - 1L;
                long b = r - k - 1L;

                ans += (a + 1) * (b + 1);

                zero.remove(k);
                arr[k] = '1';
            } else {
                // k 当前是 1，翻转成 0，会把一段连续 1 拆成左右两段
                int l = zero.lower(k);
                int r = zero.higher(k);

                long a = k - l - 1L;
                long b = r - k - 1L;

                ans -= (a + 1) * (b + 1);

                zero.add(k);
                arr[k] = '0';
            }

            res[i] = ans;
        }

        return res;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int q = Integer.parseInt(st.nextToken());

        String s = br.readLine().trim();

        int[] ops = new int[q];
        for (int i = 0; i < q; i++) {
            ops[i] = Integer.parseInt(br.readLine().trim());
        }

        long[] res = calc(n, s, ops);

        StringBuilder sb = new StringBuilder();
        for (long x : res) {
            sb.append(x).append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<long long> calc(int n, string s, vector<int>& ops) {
    set<int> zero;
    vector<char> arr(n + 1);

    // 使用 1 下标存储字符串，方便按题目位置访问
    for (int i = 1; i <= n; i++) {
        arr[i] = s[i - 1];
    }

    // 加入左右哨兵，保证每个位置都能找到左右最近的 0
    zero.insert(0);
    zero.insert(n + 1);

    // 记录所有字符 0 的位置
    for (int i = 1; i <= n; i++) {
        if (arr[i] == '0') {
            zero.insert(i);
        }
    }

    long long ans = 0;
    long long cnt = 0;

    // 计算初始答案：每段连续 1 的贡献为 len * (len + 1) / 2
    for (int i = 1; i <= n; i++) {
        if (arr[i] == '1') {
            cnt++;
        } else {
            ans += cnt * (cnt + 1) / 2;
            cnt = 0;
        }
    }
    ans += cnt * (cnt + 1) / 2;

    vector<long long> res;

    for (int k : ops) {
        if (arr[k] == '0') {
            // k 当前是 0，翻转成 1，会合并左右两段连续 1
            auto it = zero.find(k);

            int l = *prev(it);
            int r = *next(it);

            long long a = k - l - 1LL;
            long long b = r - k - 1LL;

            ans += (a + 1) * (b + 1);

            zero.erase(it);
            arr[k] = '1';
        } else {
            // k 当前是 1，翻转成 0，会把一段连续 1 拆成左右两段
            auto it = zero.upper_bound(k);

            int r = *it;
            int l = *prev(it);

            long long a = k - l - 1LL;
            long long b = r - k - 1LL;

            ans -= (a + 1) * (b + 1);

            zero.insert(k);
            arr[k] = '0';
        }

        res.push_back(ans);
    }

    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    string s;
    cin >> s;

    vector<int> ops(q);
    for (int i = 0; i < q; i++) {
        cin >> ops[i];
    }

    vector<long long> res = calc(n, s, ops);

    for (long long x : res) {
        cout << x << '\n';
    }

    return 0;
}
```
