## 解题思路

要最小化合法子序列的最大读数，对这个最大值 $M$ 二分。判定：在所有 $v_i\le M$ 的读数中，能否选出长度为 $t$、相邻两项 $\gcd>1$ 的子序列。

从左到右做 DP：对当前读数，拆出不同质因子；维护 `best[p]` 表示以含质因子 $p$ 的读数结尾的最长合法长度。则当前长度为 $1+\max_p best[p]$（无前驱则为 $1$），再用它更新各 `best[p]`。若长度达到 $t$ 则可行。

预处理每个 $v_i$ 的质因子并压缩编号，避免反复试除与哈希。$v_i=1$ 无质因子，长度 $\ge 2$ 时不可用；$t=1$ 时答案为全局最小读数。

## 复杂度分析

设 $\omega(v_i)$ 为不同质因子个数（很小）。预处理 $O(\sum\omega)$，二分 $O(\log m)$ 次判定每次 $O(\sum\omega)$。空间 $O(\sum\omega)$。

## 代码实现

### Python

```python
def sieve(n):
    vis = [True] * (n + 1)
    ps = []
    for i in range(2, n + 1):
        if not vis[i]:
            continue
        ps.append(i)
        start = i * i
        if start > n:
            continue
        for j in range(start, n + 1, i):
            vis[j] = False
    return ps

primes = sieve(32000)

def factorize(x):
    fac = []
    for p in primes:
        if p * p > x:
            break
        if x % p == 0:
            fac.append(p)
            while x % p == 0:
                x //= p
    if x > 1:
        fac.append(x)
    return fac

m, t = map(int, input().split())
v = list(map(int, input().split()))  # 传感读数
pid, pc = {}, 0
fac_ids = [[] for _ in range(m)]
for i, x in enumerate(v):
    if x == 1:
        continue
    for p in factorize(x):
        if p not in pid:
            pid[p] = pc
            pc += 1
        fac_ids[i].append(pid[p])

vals = sorted(set(v))

def check(M):
    if t == 1:
        return any(x <= M for x in v)
    best = [0] * pc
    mx = 0
    for i, x in enumerate(v):
        if x > M or x == 1:
            continue
        dp = 1
        for j in fac_ids[i]:
            if best[j] + 1 > dp:
                dp = best[j] + 1
        if dp > mx:
            mx = dp
        if mx >= t:
            return True
        for j in fac_ids[i]:
            if best[j] < dp:
                best[j] = dp
    return False

lo, hi = 0, len(vals) - 1
res = -1
while lo <= hi:
    mid = (lo + hi) // 2
    if check(vals[mid]):
        res = vals[mid]
        hi = mid - 1
    else:
        lo = mid + 1
print(res)
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static ArrayList<Integer> primes = new ArrayList<>();
    static void initPrimes() {
        int N = 32000;
        boolean[] vis = new boolean[N + 1];
        Arrays.fill(vis, true);
        for (int i = 2; i <= N; i++) {
            if (!vis[i]) continue;
            primes.add(i);
            if ((long) i * i > N) continue;
            for (int j = i * i; j <= N; j += i) vis[j] = false;
        }
    }
    static ArrayList<Integer> factorize(long x) {
        ArrayList<Integer> fac = new ArrayList<>();
        for (int p : primes) {
            if ((long) p * p > x) break;
            if (x % p == 0) {
                fac.add(p);
                while (x % p == 0) x /= p;
            }
        }
        if (x > 1) fac.add((int) x);
        return fac;
    }
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int m = Integer.parseInt(st.nextToken());
        int t = Integer.parseInt(st.nextToken());
        long[] v = new long[m];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < m; i++) v[i] = Long.parseLong(st.nextToken());
        initPrimes();
        HashMap<Integer, Integer> pidMap = new HashMap<>();
        int pc = 0;
        int[][] facIds = new int[m][];
        for (int i = 0; i < m; i++) {
            if (v[i] == 1) { facIds[i] = new int[0]; continue; }
            ArrayList<Integer> fac = factorize(v[i]);
            facIds[i] = new int[fac.size()];
            for (int j = 0; j < fac.size(); j++) {
                int p = fac.get(j);
                Integer id = pidMap.get(p);
                if (id == null) { id = pc++; pidMap.put(p, id); }
                facIds[i][j] = id;
            }
        }
        long[] vals = v.clone();
        Arrays.sort(vals);
        int nuniq = 0;
        for (int i = 0; i < m; i++)
            if (nuniq == 0 || vals[i] != vals[nuniq - 1]) vals[nuniq++] = vals[i];
        long res = -1;
        int lo = 0, hi = nuniq - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            long M = vals[mid];
            boolean ok;
            if (t == 1) {
                ok = false;
                for (long x : v) if (x <= M) { ok = true; break; }
            } else {
                int[] best = new int[pc];
                int mx = 0;
                ok = false;
                for (int i = 0; i < m; i++) {
                    if (v[i] > M || v[i] == 1) continue;
                    int dp = 1;
                    for (int id : facIds[i]) if (best[id] + 1 > dp) dp = best[id] + 1;
                    if (dp > mx) mx = dp;
                    if (mx >= t) { ok = true; break; }
                    for (int id : facIds[i]) if (best[id] < dp) best[id] = dp;
                }
            }
            if (ok) { res = M; hi = mid - 1; }
            else lo = mid + 1;
        }
        System.out.println(res);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> primes;
void init_primes() {
    const int N = 32000;
    vector<char> vis(N + 1, 1);
    for (int i = 2; i <= N; ++i) {
        if (!vis[i]) continue;
        primes.push_back(i);
        if (1LL * i * i > N) continue;
        for (int j = i * i; j <= N; j += i) vis[j] = 0;
    }
}
vector<int> factorize(long long x) {
    vector<int> fac;
    for (int p : primes) {
        if (1LL * p * p > x) break;
        if (x % p == 0) {
            fac.push_back(p);
            while (x % p == 0) x /= p;
        }
    }
    if (x > 1) fac.push_back((int)x);
    return fac;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    init_primes();
    int m, t;
    cin >> m >> t;
    vector<long long> v(m);
    for (int i = 0; i < m; ++i) cin >> v[i];
    unordered_map<int, int> pid;
    pid.reserve(m * 4);
    int pc = 0;
    vector<vector<int>> fac_ids(m);
    for (int i = 0; i < m; ++i) {
        if (v[i] == 1) continue; // 1 无法参与长度>=2 的公约链
        for (int p : factorize(v[i])) {
            if (!pid.count(p)) pid[p] = pc++;
            fac_ids[i].push_back(pid[p]);
        }
    }
    auto check = [&](long long M) -> bool {
        if (t == 1) {
            for (long long x : v) if (x <= M) return true;
            return false;
        }
        vector<int> best(pc, 0);
        int mx = 0;
        for (int i = 0; i < m; ++i) {
            if (v[i] > M || v[i] == 1) continue;
            int dp = 1;
            for (int id : fac_ids[i]) dp = max(dp, best[id] + 1);
            mx = max(mx, dp);
            if (mx >= t) return true;
            for (int id : fac_ids[i]) if (best[id] < dp) best[id] = dp;
        }
        return false;
    };
    vector<long long> vals = v;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    long long res = -1;
    int lo = 0, hi = (int)vals.size() - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (check(vals[mid])) { res = vals[mid]; hi = mid - 1; }
        else lo = mid + 1;
    }
    cout << res << '\n';
    return 0;
}
```
