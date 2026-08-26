## 解题思路

设数组中的最小值为 $mn$。

取模操作有一个重要性质：若当前值为 $y$，对 $b$ 取模后：

* 若 $y < b$，则 $y \bmod b = y$，结果不变；
* 若 $y \ge b$，则 $y \bmod b < b$，结果会严格变小。

最终答案一定要尽量大。考虑最终结果 $ans$：

如果 $ans \ge mn$，那么数组中一定存在一个数 $mn \le ans$。无论这个数在最终结果前还是后被使用，都会使当前值变成小于 $mn$，不可能保持最终结果为 $ans$。因此当 $x \ge mn$ 时，最终答案一定满足：

$ans < mn$

如果一开始 $x < mn$，那么所有数都大于 $x$，取模都不会改变结果，答案就是 $x$。

否则，只需要考虑哪些小于 $mn$ 的值可以通过若干次取模得到。由于每次有效取模都会让当前值变小，所以可以用 BFS 或 DP 在所有可能的当前值之间转移。

数组元素最大只有 $2000$，所以状态值最多只需要考虑 $0$ 到 $2000$。

具体做法：

1. 令 $mn$ 为数组最小值。
2. 若 $x < mn$，直接输出 $x$。
3. 否则，将所有 $x \bmod a_i$ 作为初始可达状态。
4. 对每个可达状态 $v$，枚举数组中的数 $a_i$：

   * 若 $a_i \le v$，则可以转移到 $v \bmod a_i$。
5. 最后在所有可达状态中找最大的 $v$，满足 $v < mn$。

相关算法：状态压缩范围内的 BFS / DP。

## 复杂度分析

设数组元素最大值为 $M$，这里 $M \le 2000$。

每个状态最多访问一次，状态数量为 $O(M)$。

每次访问状态时枚举数组中的不同元素，数量不超过 $n$。

因此时间复杂度为：

$O(Mn)$

由于所有测试数据的 $n$ 之和不超过 $5000$，且 $M \le 2000$，复杂度可以通过。

空间复杂度为：

$O(M)$

## 代码实现

### Python

```python
import sys
from collections import deque

def solve_one(n, x, arr):
    mn = min(arr)
    
    # 如果初始值已经小于最小模数，所有取模都不会改变结果
    if x < mn:
        return x
    
    nums = list(set(arr))
    max_a = max(arr)
    
    vis = [False] * (max_a + 1)
    q = deque()
    
    # 第一次有效取模后的结果一定小于某个 ai，因此不会超过 max_a
    for a in nums:
        if a <= x:
            r = x % a
            if not vis[r]:
                vis[r] = True
                q.append(r)
    
    # BFS 枚举所有可达的当前值
    while q:
        v = q.popleft()
        for a in nums:
            # 只有 a <= v 时，取模才可能改变当前值
            if a <= v:
                nv = v % a
                if not vis[nv]:
                    vis[nv] = True
                    q.append(nv)
    
    ans = 0
    for i in range(mn):
        if i <= max_a and vis[i]:
            ans = i
    
    return ans

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    res = []
    
    for _ in range(t):
        n = data[idx]
        x = data[idx + 1]
        idx += 2
        
        arr = data[idx:idx + n]
        idx += n
        
        res.append(str(solve_one(n, x, arr)))
    
    print("\n".join(res))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {
    static long solveOne(int n, long x, int[] arr) {
        int mn = arr[0];
        int maxA = arr[0];

        for (int v : arr) {
            mn = Math.min(mn, v);
            maxA = Math.max(maxA, v);
        }

        // 如果初始值已经小于最小模数，所有取模都不会改变结果
        if (x < mn) {
            return x;
        }

        // 去重，减少枚举次数
        boolean[] exist = new boolean[maxA + 1];
        ArrayList<Integer> nums = new ArrayList<>();
        for (int v : arr) {
            if (!exist[v]) {
                exist[v] = true;
                nums.add(v);
            }
        }

        boolean[] vis = new boolean[maxA + 1];
        Queue<Integer> q = new LinkedList<>();

        // 第一次取模得到初始状态
        for (int a : nums) {
            if (a <= x) {
                int r = (int)(x % a);
                if (!vis[r]) {
                    vis[r] = true;
                    q.offer(r);
                }
            }
        }

        // BFS 枚举所有可达状态
        while (!q.isEmpty()) {
            int v = q.poll();

            for (int a : nums) {
                // 只有 a <= v 时，取模才会改变当前值
                if (a <= v) {
                    int nv = v % a;
                    if (!vis[nv]) {
                        vis[nv] = true;
                        q.offer(nv);
                    }
                }
            }
        }

        int ans = 0;
        for (int i = 0; i < mn; i++) {
            if (vis[i]) {
                ans = i;
            }
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();

        for (int tc = 0; tc < T; tc++) {
            int n = sc.nextInt();
            long x = sc.nextLong();

            int[] arr = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }

            sb.append(solveOne(n, x, arr)).append('\n');
        }

        System.out.print(sb.toString());
        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

long long solveOne(int n, long long x, vector<int>& arr) {
    int mn = *min_element(arr.begin(), arr.end());
    int maxA = *max_element(arr.begin(), arr.end());

    // 如果初始值已经小于最小模数，所有取模都不会改变结果
    if (x < mn) {
        return x;
    }

    // 去重，减少枚举次数
    vector<int> nums;
    vector<int> exist(maxA + 1, 0);

    for (int v : arr) {
        if (!exist[v]) {
            exist[v] = 1;
            nums.push_back(v);
        }
    }

    vector<int> vis(maxA + 1, 0);
    queue<int> q;

    // 第一次取模得到初始状态
    for (int a : nums) {
        if (a <= x) {
            int r = x % a;
            if (!vis[r]) {
                vis[r] = 1;
                q.push(r);
            }
        }
    }

    // BFS 枚举所有可达状态
    while (!q.empty()) {
        int v = q.front();
        q.pop();

        for (int a : nums) {
            // 只有 a <= v 时，取模才会改变当前值
            if (a <= v) {
                int nv = v % a;
                if (!vis[nv]) {
                    vis[nv] = 1;
                    q.push(nv);
                }
            }
        }
    }

    int ans = 0;
    for (int i = 0; i < mn; i++) {
        if (vis[i]) {
            ans = i;
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
        long long x;
        cin >> n >> x;

        vector<int> arr(n);
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }

        cout << solveOne(n, x, arr) << '\n';
    }

    return 0;
}
```