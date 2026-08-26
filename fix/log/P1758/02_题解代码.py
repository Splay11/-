### Step1.求单个数的因子个数

根据素数分解定理，我们知道一个数的约数个数是一个数的唯一分解定理表示法后的每个质数的指数 + 1 的 累乘积
例如:
60 = 2^2 * 3 * 5 = 2^2 * 3^1 * 5^1
那么因数个数就是 (2 + 1)  * (1 + 1) * (1 + 1) = 12

### Step2.求单个数的阶乘的因子的个数

N! = 1 * 2 * 3 * ... * N

受到Step1的启发，我们希望能够将N!表示为唯一分解形式。
由于阶乘本身的特性，我们可以利用类似埃式筛的思路

1.先把[1,N]里面的素数求出来

2.枚举每个素数p，我们求出N!中p的指数。对于N!的p的指数,这些$p$的指数贡献于 $p , 2p , 3p , .. , \lfloor\frac{n}{p}\rfloor * p$ 这些数中.

3.所以自然的我们去枚举p的倍数，对于$k * p$ , 我们去累加他里面的$p$的指数。

怎么得知$k * p$ 里有多少个$p$ 呢？ 类似筛法，或者你可以理解为**动态规划**.

$dp[x] = dp[x / p] + 1$

也就是$x$里面p的个数一定是$x/p$ 这个数里的p的个数 + 1.(下方的pw数组就是起这个作用的)

### Step3.求多个数的阶乘的乘法的因子的个数

我们考虑用前缀和的思路，先去统计[1, n] 中每个数会在乘法里出现多少次。这个用pre存储。
然后我们对于每个素数p，我们去统计N1! * N2! * ... * Nn! 中p的指数。 

枚举1到N里的所有素数p，对于每个素数p:

就是去看 pre[p] * dp[p] + pre[2*p] * dp[2 * p] + pre[3*p] * dp[3 * p] + ... + pre[N / p * p] * dp[N / p * p] 这个和。

其中dp[i]是取整数i中唯一分解定理中p的指数。这个可以在筛法的过程中转移出来,具体看代码(对这个感兴趣的可以进一步了解：质性函数)。
### python
```python
mod = 10 ** 9 + 7
ans = 1

n = int(input())
arr = list(map(int, input().split()))
mx = max(arr)
# 埃式筛
def sieve_of_eratosthenes(n):
    primes = []
    is_prime = [True] * (n + 1)
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return primes

primes = sieve_of_eratosthenes(mx)
# pre存储
prefix_sum = [0] * (mx + 2)

for x in arr:
    prefix_sum[1] += 1
    prefix_sum[x + 1] -= 1

for i in range(1, mx + 1):
    prefix_sum[i] += prefix_sum[i - 1]

res = []
power = [0] * (mx + 1)
# 去统计N1! * N2! * ... * Nn! 中p的指数
for p in primes:
    power[p] = 1
    now = 0# 用来存储p在 N1! * N2! * ... * Nn! 的 唯一分解定理表示法 的指数
    # 枚举p的倍数， 因为只有p的倍数的数，他的唯一分解定理的表示法中才会有p
    for i in range(p, mx + 1, p):
        power[i] = power[i // p] + 1 # 递推公式
        now += prefix_sum[i] * power[i] # 前缀和
    res.append(now) # 存储
    for i in range(p, mx + 1, p):
        power[i] = 0


for x in res:# 根据step1的公式，求出最终的结果
    ans = ans * (x + 1) % mod

print(ans)
```
### C++
```C++
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;
const int V = 1e6;

vector<int> primes;
vector<long long> dp(V + 1, 0);
vector<long long> ns(V + 1, 0);
vector<bool> is_composite(V + 1, false);

void sieve() {
    for (int i = 2; i * i <= V; i++) {
        if (!is_composite[i]) {
            for (int j = i * i; j <= V; j += i) {
                is_composite[j] = true;
            }
        }
    }
    for (int i = 2; i <= V; i++) {
        if (!is_composite[i]) {
            primes.push_back(i);
        }
    }
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
        dp[arr[i]]++;
    }

    sieve();

    for (int i = V - 1; i >= 0; i--) {
        dp[i] = (dp[i] + dp[i + 1]) % MOD;
    }

    for (int i = 2; i <= V; i++) {
        if (dp[i] == 0) break;
        int z = i;
        for (auto j : primes) {
            while (z % j == 0) {
                z /= j;
                ns[j] = (ns[j] + dp[i]) % MOD;
            }
            if (j * j > z) break;
        }
        if (z > 1) {
            ns[z] = (ns[z] + dp[i]) % MOD;
        }
    }

    long long ans = 1;
    for (auto i : ns) {
        ans = (ans * (i + 1)) % MOD;
    }

    cout << ans << endl;
    return 0;
}
```
### java
```java
import java.util.*;

class Main {

    static int N = (int)1e6+10;
    static int[] b = new int[N];
    static int mod = (int)1e9+7;
    static int[] c = new int[N];
    static boolean[] st = new boolean[N];

    public static void main(String[] args){
        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();
        for (int i=0; i<n; i++){
            int a = scan.nextInt();
            insert(1, a, 1);
        }
        int M = (int)1e6;
        for (int i=1; i<=M; i++){
            b[i]+=b[i-1];
        }

        int ans = 1;
        for (int i=2; i<=M; i++){
            if (st[i]) continue;
            long s = 0;
            for (int j=i; j<=M; j+=i){
                st[j] = true;
                c[j] = c[j/i]+1;
                s = (s + (long) c[j]*b[j])%mod;
            }
            ans = (int)(ans * (long)(1+s)%mod);
            // System.out.println(s);
            for (int j=i; j<=M; j+=i) c[j]=0;
            // Arrays.fill(c, 0);
        }
        System.out.println(ans);
        scan.close();
    }

    public static void insert(int l, int r, int c){
        b[l]+=c;
        b[r+1]-=c;
    }

    public static int cal(int x, int p){
        int s = 0;
        while (x%p==0){
            x/=p;
            s++;
        }
        return s;
    }

}
```