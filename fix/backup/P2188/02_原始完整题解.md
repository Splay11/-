本题直接看很难看出规律，打表可以发现当$n$为偶数时规律很明显,如下图:
![](/file/3/e_MIkQF3XvT9yy9iVpitP.png)

不难看出最后每个$a_i$的系数跟杨辉三角有关,手玩几个样例可以发现当$n$为$4$的倍数时最后一列是相减,非$4$的倍数时最后一列是相加,当$n$为奇数时可以先算一列转换成偶数来做.

记组合数$c(n,m)$,那么当n为偶数时最后一列的系数每两个数一组依次为$c(n/2-1,i/2)$,直接预处理组合数再根据上述规律算即可

c++
```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N=1e5+10,mod=1e9+7;
ll a[N],f[N],g[N];
int n;
ll qmi(ll a,ll b)
{
    ll res=1;
    while(b)
    {
        if(b&1)res=res*a%mod;
        b>>=1;
        a=a*a%mod;
    }
    return res;
}
void init()//预处理
{
    g[0]=f[0]=1;
    for(int i=1;i<N;i++)
    {
        f[i]=f[i-1]*i%mod;
        g[i]=g[i-1]*qmi(i,mod-2)%mod;
    }
}
ll c(ll n,ll m)
{
    if(n<m)return 0;
    return f[n]*g[n-m]%mod*g[m]%mod;
}
signed main()
{
    ios::sync_with_stdio(0);
    cin.tie(0),cout.tie(0);
    init();
    cin>>n;
    for(int i=1;i<=n;i++)cin>>a[i];
    if(n<=2)//特判n<=2的情况
    {
        cout<<(a[1]+a[2])%mod<<endl;
        return 0;
    }
    if(n&1)//n为奇数时可以转化成偶数来做
    {
        int mk=1;
        for(int i=1;i<n;i++)
        {
            a[i]=a[i]+a[i+1]*mk;
            mk=-mk;
        }
        n--;
    }
    int mk=(n%4)?1:-1;//打表可得
    ll res=0;
    for(int i=1;i<=n;i+=2)
    {
        ll temp=c(n/2-1,i/2);//本质是杨辉三角
        res=(res+(a[i]+mk*a[i+1])*temp+mod)%mod;
    }
    cout<<(res+mod)%mod<<endl;
}
```
python
```python
import sys
sys.setrecursionlimit(10**5)
MOD = 10**9 + 7
N = 10**5 + 10
a = [0] * N
f = [0] * N
g = [0] * N

def qmi(a, b):
    res = 1
    while b:
        if b & 1:
            res = res * a % MOD
        b >>= 1
        a = a * a % MOD
    return res

def init():  # 预处理
    g[0] = f[0] = 1
    for i in range(1, N):
        f[i] = f[i - 1] * i % MOD
        g[i] = g[i - 1] * qmi(i, MOD - 2) % MOD

def c(n, m):
    if n < m:
        return 0
    return f[n] * g[n - m] % MOD * g[m] % MOD

def main():
    init()
    n = int(input())
    input_list = list(map(int, input().split()))  # 将一行输入按空格分割并转为整数列表
    for i in range(1, n + 1):
        a[i] = input_list[i - 1]  # 把输入列表的值赋给 a 数组

    if n <= 2:  # 特判n<=2的情况
        print((a[1] + a[2]) % MOD)
        return

    if n & 1:  # n为奇数时可以转化成偶数来做
        mk = 1
        for i in range(1, n):
            a[i] = a[i] + a[i + 1] * mk
            mk = -mk
        n -= 1

    mk = 1 if (n % 4) else -1  # 打表可得
    res = 0
    for i in range(1, n + 1, 2):
        temp = c(n // 2 - 1, i // 2)  # 本质是杨辉三角
        res = (res + (a[i] + mk * a[i + 1]) * temp + MOD) % MOD

    print((res + MOD) % MOD)

if __name__ == "__main__":
    main()
```
java
```java
import java.util.*;
public class Main {
    static final int N = 100010, mod = 1000000007;
    static long[] a = new long[N], f = new long[N], g = new long[N];
    static int n;

    static long qmi(long a, long b) {
        long res = 1;
        while (b != 0) {
            if ((b & 1) != 0) res = res * a % mod;
            b >>= 1;
            a = a * a % mod;
        }
        return res;
    }

    static void init() { // 预处理
        g[0] = f[0] = 1;
        for (int i = 1; i < N; i++) {
            f[i] = f[i - 1] * i % mod;
            g[i] = g[i - 1] * qmi(i, mod - 2) % mod;
        }
    }

    static long c(long n, long m) {
        if (n < m) return 0;
        return f[(int) n] * g[(int) (n - m)] % mod * g[(int) m] % mod;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        init();
        n = sc.nextInt();
        for (int i = 1; i <= n; i++) a[i] = sc.nextLong();
        if (n <= 2) { // 特判n<=2的情况
            System.out.println((a[1] + a[2]) % mod);
            return;
        }
        if ((n & 1) != 0) { // n为奇数时可以转化成偶数来做
            int mk = 1;
            for (int i = 1; i < n; i++) {
                a[i] = a[i] + a[i + 1] * mk;
                mk = -mk;
            }
            n--;
        }
        int mk = (n % 4 != 0) ? 1 : -1; // 打表可得
        long res = 0;
        for (int i = 1; i <= n; i += 2) {
            long temp = c(n / 2 - 1, i / 2); // 本质是杨辉三角
            res = (res + (a[i] + mk * a[i + 1]) * temp + mod) % mod;
        }
        System.out.println((res + mod) % mod);
    }
}
```