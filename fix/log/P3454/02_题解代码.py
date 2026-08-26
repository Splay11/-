## 题解思路

### 结论

* 设 `cover[p]` 为数组里**被质数 p 整除的元素个数（计重）**，则最长长度

  $$
  L=\max_{p\ \text{为质数}} \text{cover}[p]
  $$
* 若 `L=1`：方案就是“任选一个值>1的数”，因为不区分下标，仅看多重集合，**方案数 = 值>1的不同取值个数**。
* 若 `L>1`：所有达到 `L` 的质数 `p` 都对应一个极长方案 `S_p`（取所有可被 `p` 整除的元素）。
  不同质数可能产生**相同多重集合**。判重做法：令

  $$
  g_p=\gcd(\text{出现在 }S_p\text{ 中的不同取值})
  $$

  将 `g_p` 的不同质因子全标记为同一类；最终**等价类个数**即为方案数。

### 实现要点

* 仅对**不同取值**做一次分解，避免对所有整数范围做筛倍数统计。
* 预筛 $\le\sqrt{\max a_i}$ 的质数作试除分解。
* 对每个不同取值 `x`（频次 `f`）：

  * 对 `x` 的不同质因子 `p`：`cover[p]+=f`，`base[p]=gcd(base[p], x)`。
* 得到 `L` 后：

  * `L==1` 直接输出。
  * 否则收集 `cover[p]==L` 的质数，按 `factor(g_p)` 把它们并入同一类，类数即方案数。

### 复杂度

* 质数筛：$O(\sqrt{A}\log\log\sqrt{A})$，$A=\max a_i\le 2\times10^8$。
* 对每个不同取值做一次分解，整体约 $O(U\log A)$，其中 $U$ 为不同取值数（$U\le n$）。
* 额外空间与出现过的质因子规模同量级。


## 代码

### Python

```python
import sys, math

def read_ints():
    for b in sys.stdin.buffer.read().split():
        yield int(b)

it = iter(read_ints())
n = next(it, 0)

# 频次（只保留>1）
freq = {}
mx = 0
for _ in range(n):
    v = next(it)
    if v > 1:
        freq[v] = freq.get(v, 0) + 1
        if v > mx: mx = v

if not freq:
    print("0 0"); sys.exit(0)

# 筛 <= sqrt(mx) 的质数
lim = int(math.isqrt(mx)) + 1
is_p = [True]*(lim+1)
pr = []
for i in range(2, lim+1):
    if is_p[i]:
        pr.append(i)
        if i*i <= lim:
            for j in range(i*i, lim+1, i):
                is_p[j] = False

def factors_distinct(x):
    res = []
    t = x
    for p in pr:
        if p*p > t: break
        if t % p == 0:
            res.append(p)
            while t % p == 0: t //= p
    if t > 1: res.append(t)
    return res

# 统计 cover 与 base（gcd 仅在不同取值层面）
cover = {}
base = {}
for x, c in freq.items():
    fs = factors_distinct(x)
    for p in fs:
        cover[p] = cover.get(p, 0) + c
        base[p] = x if p not in base else math.gcd(base[p], x)

L = max(cover.values(), default=1)

# L==1：方案数为“>1的不同取值个数”
if L <= 1:
    print(1, len(freq)); sys.exit(0)

# L>1：候选质数并类
cands = [p for p, v in cover.items() if v == L]
seen = set()
ways = 0
for p in cands:
    if p in seen: continue
    g = base[p]
    for q in factors_distinct(g):
        seen.add(q)
    ways += 1

print(L, ways)
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static class FastIn {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in), 1<<20);
        int c = -1;
        int read() throws IOException { return br.read(); }
        int nextInt() throws IOException {
            int sgn = 1, x = 0, ch;
            do { ch = read(); } while (ch <= 32 && ch != -1);
            if (ch == '-') { sgn = -1; ch = read(); }
            for (; ch > 32 && ch != -1; ch = read()) x = x * 10 + (ch - '0');
            return x * sgn;
        }
    }

    static ArrayList<Integer> sieve(int up) {
        boolean[] is = new boolean[up + 1];
        Arrays.fill(is, true);
        ArrayList<Integer> ps = new ArrayList<>();
        for (int i = 2; i <= up; i++) {
            if (is[i]) {
                ps.add(i);
                long s = 1L * i * i;
                if (s <= up) for (int j = (int)s; j <= up; j += i) is[j] = false;
            }
        }
        return ps;
    }

    static ArrayList<Integer> factorsDistinct(int x, ArrayList<Integer> ps) {
        ArrayList<Integer> res = new ArrayList<>();
        int t = x;
        for (int p : ps) {
            if (1L * p * p > t) break;
            if (t % p == 0) {
                res.add(p);
                while (t % p == 0) t /= p;
            }
        }
        if (t > 1) res.add(t);
        return res;
    }

    static int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }

    public static void main(String[] args) throws Exception {
        FastIn in = new FastIn();
        int n = in.nextInt();

        // 频次表（仅值>1）
        HashMap<Integer,Integer> freq = new HashMap<>();
        int mx = 0;
        for (int i = 0; i < n; i++) {
            int v = in.nextInt();
            if (v > 1) {
                freq.put(v, freq.getOrDefault(v, 0) + 1);
                if (v > mx) mx = v;
            }
        }
        if (freq.isEmpty()) { System.out.println("0 0"); return; }

        int lim = (int)Math.sqrt(mx) + 1;
        ArrayList<Integer> primes = sieve(lim);

        HashMap<Integer,Integer> cover = new HashMap<>();
        HashMap<Integer,Integer> base = new HashMap<>();

        for (var e : freq.entrySet()) {
            int x = e.getKey(), c = e.getValue();
            ArrayList<Integer> fs = factorsDistinct(x, primes);
            for (int p : fs) {
                cover.put(p, cover.getOrDefault(p, 0) + c);
                base.put(p, base.containsKey(p) ? gcd(base.get(p), x) : x);
            }
        }

        int L = 0;
        for (int v : cover.values()) if (v > L) L = v;

        if (L <= 1) {
            System.out.println("1 " + freq.size());
            return;
        }

        ArrayList<Integer> cands = new ArrayList<>();
        for (var e : cover.entrySet()) if (e.getValue() == L) cands.add(e.getKey());

        HashSet<Integer> vis = new HashSet<>();
        int ways = 0;
        for (int p : cands) {
            if (vis.contains(p)) continue;
            int g = base.get(p);
            ArrayList<Integer> qs = factorsDistinct(g, primes);
            for (int q : qs) vis.add(q);
            ways++;
        }

        System.out.println(L + " " + ways);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> sieve(int up){
    vector<char> is(up+1, true);
    vector<int> ps;
    for(int i=2;i<=up;i++){
        if(is[i]){
            ps.push_back(i);
            if(1LL*i*i<=up)
                for(long long j=1LL*i*i;j<=up;j+=i) is[(int)j]=false;
        }
    }
    return ps;
}

static inline void factorsDistinct(int x, const vector<int>& ps, vector<int>& out){
    out.clear();
    int t=x;
    for(int p: ps){
        if(1LL*p*p>t) break;
        if(t%p==0){
            out.push_back(p);
            while(t%p==0) t/=p;
        }
    }
    if(t>1) out.push_back(t);
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; 
    if(!(cin>>n)){ cout<<"0 0\n"; return 0; }

    unordered_map<int,int> freq;
    freq.reserve(n*2);
    int mx=0;
    for(int i=0;i<n;i++){
        int v; cin>>v;
        if(v>1){ freq[v]++; if(v>mx) mx=v; }
    }
    if(freq.empty()){ cout<<"0 0\n"; return 0; }

    int lim = (int) sqrt((double)mx) + 1;
    vector<int> primes = sieve(lim);

    unordered_map<int,int> cover, base;
    cover.reserve(freq.size()*2);
    base.reserve(freq.size()*2);

    vector<int> fs;
    for(auto &kv: freq){
        int x=kv.first, c=kv.second;
        factorsDistinct(x, primes, fs);
        for(int p: fs){
            cover[p] += c;
            auto it = base.find(p);
            if(it==base.end()) base[p]=x;
            else it->second = std::gcd(it->second, x);
        }
    }

    int L=0;
    for(auto &kv: cover) L = max(L, kv.second);

    if(L<=1){
        cout<<1<<' '<<freq.size()<<'\n';
        return 0;
    }

    vector<int> cand;
    for(auto &kv: cover) if(kv.second==L) cand.push_back(kv.first);

    unordered_set<int> vis; vis.reserve(cand.size()*2);
    int ways=0;
    for(int p: cand){
        if(vis.count(p)) continue;
        int g = base[p];
        factorsDistinct(g, primes, fs);
        for(int q: fs) vis.insert(q);
        ++ways;
    }

    cout<<L<<' '<<ways<<'\n';
    return 0;
}
```