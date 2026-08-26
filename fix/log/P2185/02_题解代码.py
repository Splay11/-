定义$dp[i]$为以$i$结尾的$(1,i)$范围内的最大子段和,定义$udp[i]$为以$i$为起点,$(i,n)$范围内的最大子段和，那么根据题意，全局最大两段不重叠的子段和即为`res=max(res,dp[i]+udp[i+k+1])`

注意$i+k+1$需小于等于$n$

c++
```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
signed main()
{
	ios::sync_with_stdio(0);
    cin.tie(0),cout.tie(0);
    int t;
    cin>>t;
    while(t--)
    {
       int n,k;
       cin>>n>>k;
       vector<int>a(n+1),s(n+1);
       vector<int>dp(n+2),udp(n+2);
       dp[0]=-100000;
       udp[n+1]=-100000;
       for(int i=1;i<=n;i++)cin>>a[i],s[i]=s[i-1]+a[i];
       for(int i=1;i<=n;i++)
       {
        dp[i]=max(a[i],dp[i-1]+a[i]);//计算最大前缀和
       
       }
       for(int i=1;i<=n;i++)
       {
        dp[i]=max(dp[i],dp[i-1]);//计算最大字段和
       }
    
       for(int i=n;i>=1;i--)
       {
        udp[i]=max(a[i],udp[i+1]+a[i]);//计算最大后缀和
       }
       for(int i=n;i>=1;i--)
       {
        udp[i]=max(udp[i+1],udp[i]);//计算最大字段和
       }
       int res=-2e9;
       for(int i=1;i+k+1<=n;i++)
       {
        res=max(res,dp[i]+udp[i+k+1]);
       }
       cout<<res<<endl;
    }
}
```
python
```python
def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        k = int(data[index + 1])
        index += 2
        
        a = list(map(int, data[index:index + n]))
        index += n
        
        s = [0] * (n + 1)
        dp = [-100000] * (n + 2)
        udp = [-100000] * (n + 2)
        
        for i in range(1, n + 1):
            s[i] = s[i - 1] + a[i - 1]
        
        for i in range(1, n + 1):
            dp[i] = max(a[i - 1], dp[i - 1] + a[i - 1])  # 计算最大前缀和

        for i in range(1, n + 1):
            dp[i] = max(dp[i], dp[i - 1])  # 计算最大字段和

        for i in range(n, 0, -1):
            udp[i] = max(a[i - 1], udp[i + 1] + a[i - 1])  # 计算最大后缀和

        for i in range(n, 0, -1):
            udp[i] = max(udp[i + 1], udp[i])  # 计算最大字段和

        res = -2e9
        for i in range(1, n - k + 1):
            res = max(res, dp[i] + udp[i + k + 1])

        results.append(res)
    
    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    main()
```
java
```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int t = scanner.nextInt();
        
        while (t-- > 0) {
            int n = scanner.nextInt();
            int k = scanner.nextInt();
            int[] a = new int[n + 1];
            long[] s = new long[n + 1];
            long[] dp = new long[n + 2];
            long[] udp = new long[n + 2];
            Arrays.fill(dp, -100000);
            Arrays.fill(udp, -100000);
            
            for (int i = 1; i <= n; i++) {
                a[i] = scanner.nextInt();
                s[i] = s[i - 1] + a[i];
            }

            for (int i = 1; i <= n; i++) {
                dp[i] = Math.max(a[i], dp[i - 1] + a[i]); // 计算最大前缀和
            }
            for (int i = 1; i <= n; i++) {
                dp[i] = Math.max(dp[i], dp[i - 1]); // 计算最大字段和
            }

            for (int i = n; i >= 1; i--) {
                udp[i] = Math.max(a[i], udp[i + 1] + a[i]); // 计算最大后缀和
            }
            for (int i = n; i >= 1; i--) {
                udp[i] = Math.max(udp[i + 1], udp[i]); // 计算最大字段和
            }

            long res = -2000000000;
            for (int i = 1; i + k + 1 <= n; i++) {
                res = Math.max(res, dp[i] + udp[i + k + 1]);
            }
            System.out.println(res);
        }
        scanner.close();
    }
}
```