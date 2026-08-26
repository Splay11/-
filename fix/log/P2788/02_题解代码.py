# 题解

## 题面描述

给定一棵有 $n$ 个节点的树，每个节点上都有一个整数权值 $w_i$。小红希望删除若干条边，将这棵树分割成若干个连通块，并要求每个连通块中所有节点权值之和均为偶数。  
要求对于每个 $k$，统计删除 $k$ 条边后得到的 $k+1$ 个连通块都满足条件的方案数（两组边集合不同视为不同方案），若不存在则答案记为 $0$。  
最后答案对 $10^9+7$ 取模输出。

---

## 思路

1. **必要性判断**  
   整棵树的所有节点权值之和为 $S = \sum_{i=1}^{n}w_i$。  
   如果 $S$ 为奇数，则无论如何分割，所有连通块权值之和相加必为奇数（偶数数列求和必定为偶数），因此没有任何一种方案可以使所有连通块的和均为偶数。此时对所有 $k$ 输出 $0$。

2. **寻找可拆分的边**  
   当 $S$ 为偶数时，我们可以从树中找到若干条边，删除其中任意一条边都能使得以该边为子树的一侧的节点和为偶数。  
   具体做法是：  
   - 任选一个节点（比如 $1$）作为根，进行深度优先搜索（DFS）。  
   - 对于每个边 $u\to v$（其中 $v$ 为 $u$ 的子节点），计算以 $v$ 为根的子树权值和 $S_v$。  
   - 若 $S_v$ 为偶数，则删除边 $u\to v$ 后，该子树就是一个合法的连通块（而剩余部分的和也为 $S-S_v$，由于 $S$ 为偶数，所以剩余部分也是偶数）。  

   记满足条件的边个数为 $m$。

3. **方案计数**  
   每个满足条件的边都是可以独立删除的“候选边”。  
   当删除 $k$ 条边时，只需从这 $m$ 条候选边中选出任意 $k$ 条即可。  
   因此答案为 $\binom{m}{k}$。  
   当 $k > m$ 时，答案自然为 $0$。

---

## C++ 

```cpp
#include <iostream>
#include <vector>
using namespace std;
 
const int MOD = 1000000007;
 
int n;
vector<int> weight;
vector<vector<int>> tree;
int m = 0; // 满足条件的候选边数量
 
// DFS 计算子树和的奇偶性，返回值为子树和模 2 的结果
int dfs(int u, int parent) {
    long long sum = weight[u];
    for (int v : tree[u]) {
        if (v == parent) continue;
        int sub = dfs(v, u);
        sum += sub;
        // 如果子树的权值和为偶数，则该边为候选边
        if (sub % 2 == 0) {
            m++;
        }
    }
    return sum;
}
 
// 快速幂求法，计算 a^b mod MOD
long long modExp(long long a, long long b) {
    long long res = 1;
    while(b) {
        if(b & 1) res = res * a % MOD;
        a = a * a % MOD;
        b >>= 1;
    }
    return res;
}
 
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
 
    cin >> n;
    weight.resize(n);
    tree.resize(n);
    long long total = 0;
    for (int i = 0; i < n; i++){
        cin >> weight[i];
        total += weight[i];
    }
    for (int i = 0; i < n - 1; i++){
        int u, v;
        cin >> u >> v;
        // 转为 0 基编号
        u--; v--;
        tree[u].push_back(v);
        tree[v].push_back(u);
    }
 
    // 如果整体权值和为奇数，则所有答案均为 0
    if (total % 2 == 1) {
        for (int k = 1; k <= n - 1; k++){
            cout << 0 << (k == n - 1 ? "\n" : " ");
        }
        return 0;
    }
 
    // 以节点 0 作为根，进行 DFS
    dfs(0, -1);
 
    // 预处理阶乘与逆元，用于组合数计算
    int maxN = m; // m 最大不超过 n-1
    vector<long long> fact(maxN + 1), invFact(maxN + 1);
    fact[0] = 1;
    for (int i = 1; i <= maxN; i++){
        fact[i] = fact[i - 1] * i % MOD;
    }
    invFact[maxN] = modExp(fact[maxN], MOD - 2);
    for (int i = maxN - 1; i >= 0; i--){
        invFact[i] = invFact[i + 1] * (i + 1) % MOD;
    }
 
    // 对于每个 k，若 k <= m，则答案为 C(m, k)，否则为 0
    for (int k = 1; k <= n - 1; k++){
        if(k > m) {
            cout << 0 << (k == n - 1 ? "\n" : " ");
        } else {
            long long ans = fact[m] * invFact[k] % MOD * invFact[m - k] % MOD;
            cout << ans << (k == n - 1 ? "\n" : " ");
        }
    }
    return 0;
}
```
## Python

```python
import sys
sys.setrecursionlimit(300000)
MOD = 10**9 + 7

# 输入读入
n = int(sys.stdin.readline().strip())
weight = list(map(int, sys.stdin.readline().strip().split()))
tree = [[] for _ in range(n)]
for _ in range(n-1):
    u, v = map(int, sys.stdin.readline().strip().split())
    u -= 1
    v -= 1
    tree[u].append(v)
    tree[v].append(u)

total = sum(weight)
# 如果整体权值和为奇数，则所有方案均为 0
if total % 2 == 1:
    print(" ".join(["0"]*(n-1)))
    sys.exit(0)

m = 0  # 满足条件的候选边数量

# DFS 计算子树权值和的奇偶性
def dfs(u, parent):
    global m
    s = weight[u]
    for v in tree[u]:
        if v == parent:
            continue
        sub = dfs(v, u)
        s += sub
        # 如果子树的权值和为偶数，则该边为候选边
        if sub % 2 == 0:
            m += 1
    return s

dfs(0, -1)

# 预处理阶乘与逆元，用于组合数计算
maxN = m  # m 最大不超过 n-1
fact = [1] * (maxN + 1)
invFact = [1] * (maxN + 1)
for i in range(1, maxN+1):
    fact[i] = fact[i-1] * i % MOD

# 快速幂求法，计算 a^b mod MOD
def modExp(a, b):
    res = 1
    while b:
        if b & 1:
            res = res * a % MOD
        a = a * a % MOD
        b //= 2
    return res

invFact[maxN] = modExp(fact[maxN], MOD-2)
for i in range(maxN-1, -1, -1):
    invFact[i] = invFact[i+1] * (i+1) % MOD

# 对于每个 k (1<=k<=n-1)，若 k <= m，则答案为 C(m, k)，否则为 0
ans = []
for k in range(1, n):
    if k > m:
        ans.append("0")
    else:
        comb = fact[m] * invFact[k] % MOD * invFact[m-k] % MOD
        ans.append(str(comb))
print(" ".join(ans))
```
## Java 

```java
import java.io.*;
import java.util.*;
 
public class Main {
    static final int MOD = 1000000007;
    static int n;
    static int[] weight;
    static ArrayList<Integer>[] tree;
    static int m = 0; // 满足条件的候选边数量
 
    // DFS 计算子树权值和的奇偶性
    static long dfs(int u, int parent) {
        long s = weight[u];
        for (int v : tree[u]) {
            if (v == parent) continue;
            long sub = dfs(v, u);
            s += sub;
            // 如果子树的权值和为偶数，则该边为候选边
            if (sub % 2 == 0) {
                m++;
            }
        }
        return s;
    }
 
    // 快速幂求法，计算 a^b mod MOD
    static long modExp(long a, long b) {
        long res = 1;
        while(b > 0) {
            if ((b & 1) == 1) {
                res = res * a % MOD;
            }
            a = a * a % MOD;
            b >>= 1;
        }
        return res;
    }
 
    public static void main(String[] args) throws IOException{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        n = Integer.parseInt(br.readLine().trim());
        weight = new int[n];
        tree = new ArrayList[n];
        String[] ws = br.readLine().trim().split("\\s+");
        long total = 0;
        for (int i = 0; i < n; i++){
            weight[i] = Integer.parseInt(ws[i]);
            total += weight[i];
            tree[i] = new ArrayList<>();
        }
 
        for (int i = 0; i < n - 1; i++){
            String[] parts = br.readLine().trim().split("\\s+");
            int u = Integer.parseInt(parts[0]) - 1;
            int v = Integer.parseInt(parts[1]) - 1;
            tree[u].add(v);
            tree[v].add(u);
        }
 
        // 如果整体权值和为奇数，则所有方案均为 0
        if (total % 2 == 1) {
            StringBuilder sb = new StringBuilder();
            for (int k = 1; k <= n - 1; k++){
                sb.append("0").append(k == n - 1 ? "\n" : " ");
            }
            System.out.print(sb.toString());
            return;
        }
 
        // 从节点 0 作为根进行 DFS
        dfs(0, -1);
 
        // 预处理阶乘与逆元，用于组合数计算
        int maxN = m;  // m 最大不超过 n-1
        long[] fact = new long[maxN + 1];
        long[] invFact = new long[maxN + 1];
        fact[0] = 1;
        for (int i = 1; i <= maxN; i++){
            fact[i] = fact[i - 1] * i % MOD;
        }
        invFact[maxN] = modExp(fact[maxN], MOD - 2);
        for (int i = maxN - 1; i >= 0; i--){
            invFact[i] = invFact[i + 1] * (i + 1) % MOD;
        }
 
        // 对于每个 k (1<=k<=n-1)，若 k <= m，则答案为 C(m, k)，否则为 0
        StringBuilder sb = new StringBuilder();
        for (int k = 1; k <= n - 1; k++){
            if (k > m) {
                sb.append("0");
            } else {
                long comb = fact[m] * invFact[k] % MOD * invFact[m - k] % MOD;
                sb.append(comb);
            }
            if (k != n - 1) sb.append(" ");
        }
        System.out.println(sb.toString());
    }
}
```