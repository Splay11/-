## 解题思路

段累计分定义为：

$$
score(L,R)=\sum_{i=L}^{R}\left(\sum_{t=L}^{i} load_t\right)
$$

等价于每个 $load_i$ 在区间 $[L,R]$ 内出现 $(R-i+1)$ 次，故：

$$
score(L,R)=(R-L+1)load_L+(R-L)load_{L+1}+\cdots+1\cdot load_R
$$

求第 $rank$ 小的 $score$，转化为：统计有多少个区间满足 $score(L,R)\le x$。

若不少于 $rank$，则答案 $\le x$；否则 $> x$。对 $x$ 二分即可。

**双指针统计**

因 $load_i\ge 0$，固定左端点 $L$ 时，$score(L,R)$ 随 $R$ 单调不减。

维护窗口 $[L,R)$ 的负载和 $windowSum$ 与段累计分 $curScore$：

- 右扩：先 $windowSum \leftarrow windowSum + load_R$，再 $curScore \leftarrow curScore + windowSum$；
- 左缩：$curScore \leftarrow curScore - (R-L)\cdot load_L$，$windowSum \leftarrow windowSum - load_L$。

`count_leq(x)` 在线性时间内统计 $score\le x$ 的区间数；二分上界取整段 $score(1,len)$。

## 复杂度分析

设单组长度为 $len$。

- 单次 `count_leq`：$O(len)$；
- 二分约 $O(\log V)$ 轮，$V$ 为答案上界；
- 单组时间：$O(len \log V)$；
- 空间：$O(len)$（输入数组），辅助 $O(1)$。

所有测试中 $\sum len \le 5\times 10^5$。中间值可达 $10^{17}$，须用 `long` / `long long`。

## 代码实现

### Python

```python
def count_leq(load, limit):
    length = len(load)

    # r 为右端点开区间，当前窗口为 [l, r)
    r = 0

    # window_sum 为当前窗口内负载之和
    window_sum = 0

    # cur_score 为当前窗口的段累计分
    cur_score = 0

    cnt = 0

    for l in range(length):
        # 尽量右扩窗口，保证段累计分不超过 limit
        while r < length:
            new_sum = window_sum + load[r]
            new_score = cur_score + new_sum

            if new_score > limit:
                break

            window_sum = new_sum
            cur_score = new_score
            r += 1

        cnt += r - l

        if r > l:
            cur_score -= (r - l) * load[l]
            window_sum -= load[l]
        else:
            r = l + 1

    return cnt


def kth_score(load, rank):
    length = len(load)

    # 上界取整段 [1, length] 的段累计分
    running = 0
    high = 0
    for x in load:
        running += x
        high += running

    low = 0

    # 二分最小的 ans，使 score <= ans 的区间数不少于 rank
    while low < high:
        mid = (low + high) // 2
        if count_leq(load, mid) >= rank:
            high = mid
        else:
            low = mid + 1

    return low


def main():
    tc = int(input())
    for _ in range(tc):
        length, rank = map(int, input().split())
        load = list(map(int, input().split()))
        print(kth_score(load, rank))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static class InputReader {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String next() throws Exception {
            while (st == null || !st.hasMoreTokens()) {
                st = new StringTokenizer(br.readLine());
            }
            return st.nextToken();
        }

        int nextInt() throws Exception {
            return Integer.parseInt(next());
        }

        long nextLong() throws Exception {
            return Long.parseLong(next());
        }
    }

    static long countLeq(long[] load, long limit) {
        int length = load.length;

        // r 为右端点开区间，当前窗口为 [l, r)
        int r = 0;

        // windowSum 为当前窗口内负载之和
        long windowSum = 0;

        // curScore 为当前窗口的段累计分
        long curScore = 0;

        long cnt = 0;

        for (int l = 0; l < length; l++) {
            // 尽量右扩窗口，保证段累计分不超过 limit
            while (r < length) {
                long newSum = windowSum + load[r];
                long newScore = curScore + newSum;

                if (newScore > limit) {
                    break;
                }

                windowSum = newSum;
                curScore = newScore;
                r++;
            }

            cnt += r - l;

            if (r > l) {
                curScore -= (long) (r - l) * load[l];
                windowSum -= load[l];
            } else {
                r = l + 1;
            }
        }

        return cnt;
    }

    static long kthScore(long[] load, long rank) {
        // 上界取整段 [1, length] 的段累计分
        long running = 0;
        long high = 0;

        for (long x : load) {
            running += x;
            high += running;
        }

        long low = 0;

        // 二分最小的 ans，使 score <= ans 的区间数不少于 rank
        while (low < high) {
            long mid = low + (high - low) / 2;

            if (countLeq(load, mid) >= rank) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }

        return low;
    }

    public static void main(String[] args) throws Exception {
        InputReader in = new InputReader();
        StringBuilder sb = new StringBuilder();

        int tc = in.nextInt();

        for (int caseId = 0; caseId < tc; caseId++) {
            int length = in.nextInt();
            long rank = in.nextLong();

            long[] load = new long[length];
            for (int i = 0; i < length; i++) {
                load[i] = in.nextLong();
            }

            sb.append(kthScore(load, rank)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

long long countLeq(const vector<long long>& load, long long limit) {
    int length = load.size();

    // r 为右端点开区间，当前窗口为 [l, r)
    int r = 0;

    // windowSum 为当前窗口内负载之和
    long long windowSum = 0;

    // curScore 为当前窗口的段累计分
    long long curScore = 0;

    long long cnt = 0;

    for (int l = 0; l < length; l++) {
        // 尽量右扩窗口，保证段累计分不超过 limit
        while (r < length) {
            long long newSum = windowSum + load[r];
            long long newScore = curScore + newSum;

            if (newScore > limit) {
                break;
            }

            windowSum = newSum;
            curScore = newScore;
            r++;
        }

        cnt += r - l;

        if (r > l) {
            curScore -= 1LL * (r - l) * load[l];
            windowSum -= load[l];
        } else {
            r = l + 1;
        }
    }

    return cnt;
}

long long kthScore(const vector<long long>& load, long long rank) {
    // 上界取整段 [1, length] 的段累计分
    long long running = 0;
    long long high = 0;

    for (long long x : load) {
        running += x;
        high += running;
    }

    long long low = 0;

    // 二分最小的 ans，使 score <= ans 的区间数不少于 rank
    while (low < high) {
        long long mid = low + (high - low) / 2;

        if (countLeq(load, mid) >= rank) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }

    return low;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int tc;
    cin >> tc;

    while (tc--) {
        int length;
        long long rank;
        cin >> length >> rank;

        vector<long long> load(length);
        for (int i = 0; i < length; i++) {
            cin >> load[i];
        }

        cout << kthScore(load, rank) << '\n';
    }

    return 0;
}
```