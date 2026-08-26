# 思路
题目要求最终的 a 数组中每个数都必须在 b 中出现过，且 a 数组最终是一个单调不降的数组，所以可以考虑确定 a 数组中最大的值，即第 n 个数的最终值。

状态定义
考虑 dp[i][j] 表示 a 的第 i 个数为 j ，前 i 个数是单调不降的最小操作次数。
状态转移
- 第 i-1 个数为 j：dp[i][j] = dp[i - 1][j] + abs(a[i]-j)
- 第 i-1 个数为 j-1 ：dp[i][j] = dp[i - 1][j - 2] + abs(a[i]-j)
- 第 i-1 个数为 j-2 ：dp[i][j] = dp[i - 1][j - 1] + abs(a[i]-j)
- ...
- 第 i-1 个数为 1 ：dp[i][j] = dp[i - 1][1] + abs(a[i]-j)
最终答案就是 min(dp[n][1:])

但是这里还需要有一个限定条件，即每个数都得在 b 中出现过。
那么可以将 b 进行一个排序，
改变一下状态定义：dp[i][j] 表示 a 的第 i 个数为 b[j] ，前 i 个数均在 b 中出现过，且单调不降的最小操作次数。
状态转移
- 第 i-1 个数为 b[j]：dp[i][j] = dp[i - 1][j] + abs(a[i]-b[j])
- 第 i-1 个数为 b[j-1] ：dp[i][j] = dp[i - 1][j - 1] + abs(a[i]-(b[j]))
- 第 i-1 个数为 b[j-2] ：dp[i][j] = dp[i - 1][j - 2] + abs(a[i]-(b[j]))
- ...
- 第 i-1 个数为 b[1] ：dp[i][j] = dp[i - 1][1] + abs(a[i]-b[j])
最终答案仍为 max(dp[n][1:])

但是这样的状态枚举是 $O(nm)$ ，状态转移是 $O(m)$ 的，总时间复杂度为 $O(nm^2)$ ，无法通过本题。

考虑如何优化，可以发现 dp[i][j] = min(dp[i-1][1:j+1]) + abs(a[i]-b[j])

所以我们可以动态维护一个 dp[i-1] 的最小值，这样就可以优化为 $O(nm)$ 了。

时间复杂度：$O(nm)$

# 代码
## C++
```cpp
#include<bits/stdc++.h>
using namespace std;
const int N=2e3+10;
long long a[N],b[N],n,m;
long long f[N][N];
int main(){
    cin>>n>>m;
    for(int i=1;i<=n;i++)cin>>a[i];
    for(int i=1;i<=m;i++)cin>>b[i];
    sort(b+1,b+1+m);
    memset(f,0x3f,sizeof f);
    for(int j=0;j<=m;j++)f[0][j]=0;
    for(int i=1;i<=n;i++){
        vector<long long>pre(m+1,1e18);   //维护前缀和的最小值
        pre[0]=f[i-1][0];
        for(int j=1;j<=m;j++){
            pre[j]=min(pre[j-1],f[i-1][j]);
        }
        for(int j=1;j<=m;j++){
            f[i][j] = pre[j]+ abs(a[i]-b[j]);
        }
    }
    long long res=1e18;
    for(int i=1;i<=m;i++)res=min(res,f[n][i]);
    cout<<res<<endl;
    return 0;
}

```

## Python
```python
INF = 10 ** 18

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

b.sort()

dp = [[INF for _ in range(m + 1)] for _ in range(n + 1)]
dp[0][:] = [0] * (m + 1)

for i in range(1, n + 1):
    prefix_min = INF
    for j in range(1, m + 1):
        val = abs(a[i - 1] - b[j - 1])
        prefix_min = min(prefix_min, dp[i - 1][j])
        dp[i][j] = prefix_min + val


print(min(dp[n][1:]))

```

### java
``` java
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        final int N = 2000 + 10;
        long[] a = new long[N];
        long[] b = new long[N];
        long[][] f = new long[N][N];
        int n, m;

        Scanner scanner = new Scanner(System.in);
        n = scanner.nextInt();
        m = scanner.nextInt();

        for (int i = 1; i <= n; i++) {
            a[i] = scanner.nextLong();
        }
        for (int i = 1; i <= m; i++) {
            b[i] = scanner.nextLong();
        }

        // 排序
        Arrays.sort(b, 1, m + 1);

        // 初始化f数组
        for (long[] row : f) {
            Arrays.fill(row, Long.MAX_VALUE / 2); // 使用大的数值初始化
        }

        for (int j = 0; j <= m; j++) {
            f[0][j] = 0; // 边界条件
        }

        for (int i = 1; i <= n; i++) {
            long[] pre = new long[m + 1];
            Arrays.fill(pre, Long.MAX_VALUE / 2);
            pre[0] = f[i - 1][0];

            for (int j = 1; j <= m; j++) {
                pre[j] = Math.min(pre[j - 1], f[i - 1][j]);
            }

            for (int j = 1; j <= m; j++) {
                f[i][j] = pre[j] + Math.abs(a[i] - b[j]);
            }
        }

        long res = Long.MAX_VALUE / 2;
        for (int i = 1; i <= m; i++) {
            res = Math.min(res, f[n][i]);
        }

        System.out.println(res);
        scanner.close();
    }
}
```