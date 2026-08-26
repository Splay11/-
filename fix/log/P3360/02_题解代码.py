## 思路

### 关键等价

设整体 LCM 的质因数分解为

$$
\text{LCM}(a_1,\dots,a_n)=\prod_{p} p^{E_p},
$$

其中 $E_p=\max_i v_p(a_i)$（$v_p(x)$ 是 $x$ 中质因数 $p$ 的指数）。

一个子数组 $[l,r]$ 的 LCM 等于整体 LCM，当且仅当对每个质数 $p$，在 $[l,r]$ 中至少有**一个**元素的 $p$ 指数达到 **$E_p$**。
——因为子数组 LCM 的 $p$ 指数就是该区间内各元素 $v_p$ 的最大值。

于是问题转化为：

> 对每个质数 $p$，收集满足 $v_p(a_i)=E_p$ 的所有下标集合 $S_p$。
> 求最短区间 $[l,r]$ 使得对所有 $p$，区间内至少包含一个 $S_p$ 中的下标。

这就是一维上的“多类别命中”的最短窗口问题，和最小覆盖子串类似。

### 做法步骤

1. **预处理质数表**：筛到 $\sqrt{10^9}=31623$。
2. **分解所有数（有缓存）**：对每个 $a_i$ 做质因数分解，得到若干 $(p,e)$。

   * 用哈希缓存相同数的分解结果，避免重复分解。
3. **求整体 LCM 的指数需求**：对每个质数 $p$，记 $E_p=\max_i e$。
4. **给每个位置打“标签”**：对每个下标 $i$，把满足“该位置上 $p$ 的指数 **等于** $E_p$”的所有质数 $p$ 收集成一个列表 `tags[i]`。这表示：选到位置 $i$ 就“满足/覆盖”了这些质数的需求。
5. **双指针最小覆盖**：用计数表维护当前窗口覆盖了多少个不同的质数需求。右指针右移累加，满足全部需求后，尽量左移收缩并更新答案。

> 特判：如果所有数都是 1，则整体 LCM 为 1，没有任何质因数需求，答案就是 1（任取一个元素即可）。

### 为什么不直接算 LCM？

* 乘法极易溢出 64 位；
* 在滑窗中移除左端元素时，LCM **不可**“除回去”；
* 因子法只做除法与计数，不做大数乘法，稳定安全。




## 代码

### Python

```python
import sys
import math

# 生成 <=31623 的质数表（埃氏筛）
def sieve(limit=31623):
    bs = [True] * (limit + 1)
    ps = []
    for i in range(2, limit + 1):
        if bs[i]:
            ps.append(i)
            step = i
            start = i * i
            if start <= limit:
                bs[start:limit + 1:step] = [False] * (((limit - start) // step) + 1)
    return ps

PRIMES = sieve()

# 质因数分解（带缓存），返回 dict: p->e
def factorize(x, cache):
    if x in cache:
        return cache[x]
    y = x
    res = {}
    for p in PRIMES:
        if p * p > y:
            break
        if y % p == 0:
            e = 0
            while y % p == 0:
                y //= p
                e += 1
            res[p] = e
    if y > 1:  # y 剩下的是一个 > sqrt(x) 的质因子
        res[y] = res.get(y, 0) + 1
    cache[x] = res
    return res

def solve():
    input_data = sys.stdin.read().strip().split()
    t = int(input_data[0])
    idx = 1
    out_lines = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        arr = list(map(int, input_data[idx:idx+n])); idx += n

        # 特判全为 1
        if all(a == 1 for a in arr):
            out_lines.append("1")
            continue

        fcache = {}
        need = {}  # p -> E_p（整体需要的最大指数）
        facts = [None] * n

        # 第一次遍历：收集每个位置的分解，并统计每个质数的最大指数
        for i, a in enumerate(arr):
            fac = factorize(a, fcache)
            facts[i] = fac
            for p, e in fac.items():
                if e > need.get(p, 0):
                    need[p] = e

        # 需要覆盖的质数集合
        primes_needed = list(need.keys())
        m = len(primes_needed)
        if m == 0:
            out_lines.append("1")
            continue

        # 给每个位置打“满足哪些质数达到最大指数”的标签
        tags = [[] for _ in range(n)]
        # 为了更快的计数，把质数映射成 0..m-1 的编号
        pid = {p: k for k, p in enumerate(primes_needed)}
        for i in range(n):
            fac = facts[i]
            for p, E in need.items():
                if fac.get(p, 0) == E:
                    tags[i].append(pid[p])

        # 最小覆盖窗口（双指针）
        cnt = [0] * m
        have = 0
        need_all = m
        ans = n + 1
        l = 0
        for r in range(n):
            for k in tags[r]:
                cnt[k] += 1
                if cnt[k] == 1:
                    have += 1
            # 若已覆盖全部质数，尝试收缩左端
            while have == need_all:
                ans = min(ans, r - l + 1)
                for k in tags[l]:
                    cnt[k] -= 1
                    if cnt[k] == 0:
                        have -= 1
                l += 1

        # 理论上必可覆盖（因为整体 LCM 的所有质数都出现在数组中）
        out_lines.append(str(ans if ans <= n else n))
    print("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

// 解决：最短子数组的 LCM 等于整体 LCM（不做大数乘法）
public class Main {
    static ArrayList<Integer> primes = new ArrayList<>();

    // 埃氏筛到 31623
    static void sieve(int limit) {
        boolean[] bs = new boolean[limit + 1];
        Arrays.fill(bs, true);
        for (int i = 2; i <= limit; i++) {
            if (bs[i]) {
                primes.add(i);
                long start = 1L * i * i;
                if (start <= limit) {
                    for (int j = (int) start; j <= limit; j += i) bs[j] = false;
                }
            }
        }
    }

    // 质因数分解，返回 Map<p, e>，带缓存
    static Map<Integer, Integer> factorize(int x, HashMap<Integer, Map<Integer, Integer>> cache) {
        Map<Integer, Integer> res = cache.get(x);
        if (res != null) return res;
        int y = x;
        HashMap<Integer, Integer> f = new HashMap<>();
        for (int p : primes) {
            if (1L * p * p > y) break;
            if (y % p == 0) {
                int e = 0;
                while (y % p == 0) {
                    y /= p; e++;
                }
                f.put(p, e);
            }
        }
        if (y > 1) {
            f.put(y, f.getOrDefault(y, 0) + 1);
        }
        cache.put(x, f);
        return f;
    }

    public static void main(String[] args) throws Exception {
        sieve(31623);
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder out = new StringBuilder();
        int T = Integer.parseInt(br.readLine().trim());
        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            String[] ss = br.readLine().trim().split("\\s+");
            int[] a = new int[n];
            boolean allOne = true;
            for (int i = 0; i < n; i++) {
                a[i] = Integer.parseInt(ss[i]);
                if (a[i] != 1) allOne = false;
            }
            if (allOne) {
                out.append(1).append('\n');
                continue;
            }
            HashMap<Integer, Map<Integer, Integer>> cache = new HashMap<>();
            HashMap<Integer, Integer> need = new HashMap<>(); // p -> E_p
            @SuppressWarnings("unchecked")
            Map<Integer, Integer>[] facts = new Map[n];

            // 统计整体需要的最大指数
            for (int i = 0; i < n; i++) {
                Map<Integer, Integer> fac = factorize(a[i], cache);
                facts[i] = fac;
                for (Map.Entry<Integer, Integer> e : fac.entrySet()) {
                    int p = e.getKey(), v = e.getValue();
                    need.put(p, Math.max(need.getOrDefault(p, 0), v));
                }
            }

            if (need.isEmpty()) { // 其实 allOne 已判，稳妥再判一次
                out.append(1).append('\n');
                continue;
            }

            // 为质数分配编号，便于用数组计数
            int m = need.size();
            HashMap<Integer, Integer> pid = new HashMap<>();
            int id = 0;
            for (int p : need.keySet()) pid.put(p, id++);

            // tags[i]：位置 i 覆盖的质数编号列表（其指数达到 E_p）
            ArrayList<Integer>[] tags = new ArrayList[n];
            for (int i = 0; i < n; i++) tags[i] = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                Map<Integer, Integer> fac = facts[i];
                for (Map.Entry<Integer, Integer> e : need.entrySet()) {
                    int p = e.getKey(), E = e.getValue();
                    if (fac.getOrDefault(p, 0) == E) {
                        tags[i].add(pid.get(p));
                    }
                }
            }

            // 双指针最小覆盖
            int[] cnt = new int[m];
            int have = 0, needAll = m;
            int ans = n + 1;
            int l = 0;
            for (int r = 0; r < n; r++) {
                for (int k : tags[r]) {
                    if (cnt[k] == 0) have++;
                    cnt[k]++;
                }
                while (have == needAll) {
                    ans = Math.min(ans, r - l + 1);
                    for (int k : tags[l]) {
                        cnt[k]--;
                        if (cnt[k] == 0) have--;
                    }
                    l++;
                }
            }
            out.append(ans <= n ? ans : n).append('\n');
        }
        System.out.print(out.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 筛到 31623
vector<int> primes;
void sieve(int limit = 31623) {
    vector<bool> bs(limit + 1, true);
    for (int i = 2; i <= limit; ++i) {
        if (bs[i]) {
            primes.push_back(i);
            long long start = 1LL * i * i;
            if (start <= limit) {
                for (int j = (int)start; j <= limit; j += i) bs[j] = false;
            }
        }
    }
}

// 分解（带缓存），返回 vector<pair<p,e>>
vector<pair<int,int>> factorize(int x, unordered_map<int, vector<pair<int,int>>> &cache) {
    auto it = cache.find(x);
    if (it != cache.end()) return it->second;
    int y = x;
    vector<pair<int,int>> res;
    for (int p : primes) {
        if (1LL * p * p > y) break;
        if (y % p == 0) {
            int e = 0;
            while (y % p == 0) { y /= p; ++e; }
            res.push_back({p, e});
        }
    }
    if (y > 1) res.push_back({y, 1});
    cache.emplace(x, res);
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    sieve();
    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; cin >> n;
        vector<int> a(n);
        bool allOne = true;
        for (int i = 0; i < n; ++i) {
            cin >> a[i];
            if (a[i] != 1) allOne = false;
        }
        if (allOne) {
            cout << 1 << "\n";
            continue;
        }

        unordered_map<int, vector<pair<int,int>>> cache;
        vector<vector<pair<int,int>>> facts(n);
        unordered_map<int,int> need; // p -> E_p

        // 统计每个质数的最大指数
        for (int i = 0; i < n; ++i) {
            auto fac = factorize(a[i], cache);
            facts[i] = fac;
            for (auto &pe : fac) {
                int p = pe.first, e = pe.second;
                auto it = need.find(p);
                if (it == need.end()) need[p] = e;
                else if (e > it->second) it->second = e;
            }
        }

        if (need.empty()) {
            cout << 1 << "\n";
            continue;
        }

        // 质数映射成编号 0..m-1
        int m = (int)need.size();
        unordered_map<int,int> pid;
        pid.reserve(m * 2);
        int id = 0;
        for (auto &kv : need) pid[kv.first] = id++;

        // tags[i]：位置 i 覆盖的质数编号列表
        vector<vector<int>> tags(n);
        for (int i = 0; i < n; ++i) {
            for (auto &kv : need) {
                int p = kv.first, E = kv.second;
                int ehere = 0;
                // 在 facts[i] 中找 p 的指数
                for (auto &pe : facts[i]) if (pe.first == p) { ehere = pe.second; break; }
                if (ehere == E) tags[i].push_back(pid[p]);
            }
        }

        // 双指针最小覆盖
        vector<int> cnt(m, 0);
        int have = 0, needAll = m;
        int ans = n + 1;
        int l = 0;
        for (int r = 0; r < n; ++r) {
            for (int k : tags[r]) {
                if (cnt[k] == 0) ++have;
                ++cnt[k];
            }
            while (have == needAll) {
                ans = min(ans, r - l + 1);
                for (int k : tags[l]) {
                    --cnt[k];
                    if (cnt[k] == 0) --have;
                }
                ++l;
            }
        }
        cout << (ans <= n ? ans : n) << "\n";
    }
    return 0;
}
```