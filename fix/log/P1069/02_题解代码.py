## 思路

动态规划，三维dp，$dp[i][j][0]$ 代表在考虑前 $i$ 个商品的基础上，总共花费了 $j$ 元时能得到的最大的喜爱度，$dp[i][j][1]$ 代表相同条件的基础上第 $i$ 个商品用原价购买时的最大喜爱度。

$dp[i][j][0] = max(dp[i-1][j-a[i]][0] + b[i],  dp[i-1][j-a[i]][1] + b[i])$

$dp[i][j][1] = max(dp[i][j][0], dp[i-1][j-a[i]/2][0] + b[i], dp[i-1][j][1])$

在dp更新过程中得到最大值即可

#### tips

python选手在比赛的时候需要选pypy3编译器,用它不会超时，而使用python3会超时！

## 代码

### c++

~~~c++
#include <bits/stdc++.h>
using namespace std;
const int N = 1005;
long long a[N], b[N];
long long dp[N][N][2];
int in() {
	int x;
	cin >> x;
	return x;
}
int main() {
    int n = in(), x = in();
    for (int i = 1; i <= n; i++) {
        a[i] = in();
    }
    for (int i = 1; i <= n; i++) {
        b[i] = in();
    }
    long long ans = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = x; j >= a[i]; j--) {
            if (dp[i - 1][j - a[i]][0] != 0)
                dp[i][j][0] = max(dp[i][j][0], dp[i - 1][j - a[i]][0] + b[i]);
            if (dp[i - 1][j - a[i]][1] != 0)
                dp[i][j][0] = max(dp[i][j][0], dp[i - 1][j - a[i]][1] + b[i]);
            ans = max(ans, dp[i][j][0]);
        }
        for (int j = x; j >= a[i] / 2; j--) {
            if (dp[i - 1][j - a[i] / 2][0] != 0)
                dp[i][j][1] = max(dp[i][j][1], dp[i - 1][j - a[i] / 2][0] + b[i]);
            ans = max(ans, dp[i][j][1]);
        }
        for (int j = 0; j <= x; j++) {
            dp[i][j][1] = max(dp[i][j][1], dp[i - 1][j][0]);
            dp[i][j][1] = max(dp[i][j][1], dp[i - 1][j][1]);
        }
        if (a[i] <= x) {
            dp[i][a[i]][0] = max(dp[i][a[i]][0], b[i]);
            ans = max(ans, dp[i][a[i]][0]);
        }
    }
    cout << ans << endl;
}
~~~



### python

~~~python
if __name__ == '__main__':
	n, x = map(int, input().split())
	a = [0] + list(map(int, input().split()))
	b = [0] + list(map(int, input().split()))
	dp = [ [ [0,0] for i in range(x+1)] for i in range(n+1)]
	ans = 0
	for i in range(1, n+1) :
		if a[i] <= x:	
			dp[i][a[i]][0] = b[i]
			ans = max(ans, b[i])
		for j in range(a[i] ,x+1):
			for k in range(0, 2):
				t = dp[i-1][j - a[i]][k]
				if t == 0:
					continue
				dp[i][j][0] = max(dp[i][j][0], t + b[i])
				ans = max(ans, dp[i][j][0])
		for j in range(a[i] //2 ,x+1):
			t = dp[i-1][j - a[i] // 2][0]
			if t == 0:
				continue
			dp[i][j][1] = max(dp[i][j][1], t + b[i])
			ans = max(ans, dp[i][j][1])
		for j in range(x+1):
			dp[i][j][1] = max(dp[i][j][1], dp[i-1][j][1], dp[i-1][j][0])
	print(ans)
~~~

### java

~~~java
import java.util.*;
class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt(), x = in.nextInt();
        int[] a = new int[n+1], b = new int[n+1];
        for (int i = 1 ; i <= n ; i ++) {
            a[i] = in.nextInt();
        }
        for (int i = 1 ; i <= n ; i ++) {
            b[i] = in.nextInt();
        }
        long[][][] dp = new long[n+1][x+1][2];
        long ans = 0;
        for(int i = 1 ; i <= n ; i ++) {
            for(int j = x ; j >= a[i] ; j --) {
                if(dp[i-1][j-a[i]][0] != 0)
                    dp[i][j][0] = Math.max(dp[i][j][0], dp[i-1][j-a[i]][0] + b[i]);
                if(dp[i-1][j-a[i]][1] != 0)
                    dp[i][j][0] = Math.max(dp[i][j][0], dp[i-1][j-a[i]][1] + b[i]);
                ans = Math.max(ans, dp[i][j][0]);
            }
            for(int j = x ; j >= a[i]/2 ; j --) {
                if(dp[i-1][j-a[i]/2][0] != 0)
                    dp[i][j][1] = Math.max(dp[i][j][1], dp[i-1][j-a[i]/2][0] + b[i]);
                ans = Math.max(ans, dp[i][j][1]);
            }
            for(int j = 0 ; j <= x ; j ++) {
            	dp[i][j][1] = Math.max(dp[i][j][1], dp[i-1][j][0]);
            	dp[i][j][1] = Math.max(dp[i][j][1], dp[i-1][j][1]);
            }
            if(a[i] <= x) {
                dp[i][a[i]][0] = Math.max(dp[i][a[i]][0], b[i]);
                ans = Math.max(ans, dp[i][a[i]][0]);
            }
        }
        System.out.println(ans);
    }
}
~~~