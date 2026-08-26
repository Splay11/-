## 思路:贪心

容易发现，从二进制的视角来看，只要每一个$bit$都变成一样即可。所以可以分别独立的考虑每一位的最小代价。那么对于每一个$bit$ , 我们要么将所有的$0$ 都变成 $1$ , 要么将所有的$1$ 都变成 $0$. 所以最小代价就是$0,1$ 中出现次数少的那个。



举个例子:

4

1 2 3 4

那么最小代价就是5，如下图所示

![image](/file/2/so2xJSE7-jLcTzYO-KTLZ.png) 

## 代码

C++代码

```c++
#include<bits/stdc++.h>
using namespace std;
const int maxn =1e5 + 5;
#define ll long long 
// cnt[i][0] 代表这n个整数中，第i位分别出现了多少次0 
// cnt[i][1] 代表这n个整数中，第i位分别出现了多少次1 
ll cnt[40][2];
int main (){
    int n;
    cin >> n;
    for (int i = 1 ; i <= n; i++){
		ll x;
		cin >> x;
        // 统计x
		for (int j = 0 ; j < 34 ; j++){
			int v = (x >> j) & 1;
			cnt[j][v]++;
		}
    }
    // 按二进制的每一位计算贡献
    int ans = 0;
    for (int i = 0 ; i < 34 ; i++){
        // 看最小出现次数。
    	ans += min(cnt[i][0] , cnt[i][1]);
    }
    cout << ans << endl;
    return 0;
}
```