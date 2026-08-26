## 思路

1.观察到**每个数最多修改一次**，那么显然最优的修改方案一定是前$i$小都乘以2，前$k-i$大都除以2。

2.那么排序,枚举$i$然后模拟这个过程，去求最大值最小值，复杂度达到$O(n^2)$ 。但好在我们只关心极差，即最大值和最小值，所以不需要去模拟操作每一个数。而是考虑一次操作后结果会分成三段,分别去求这三段的最值就好了。如下图所示,我们只需要从这六个红圈中取极值即可。

![image](/file/2/nA0jqrSvnxgXpdUB82hUM.png) 

## 代码

### c++

~~~c++
#include <bits/stdc++.h>
using namespace std;

int in() {
	int x;
	cin >> x;
	return x;
}
int main()
{
	int n = in(), k = in();
    int a[n];
    for (int i = 0; i < n; i++) {
        a[i] = in();
    }
    sort(a, a+n);			//排序
    int ans = (int)1e9;
    for (int i = 0; i <= k; i++) {		//枚举修改前i小
        //三者不一定都存在，所以最小值初始化为一个较大的值，最大值初始化为一个小的值，再用三者更新
        int mi = (int)1e9, mx = 0;		
        if(i > 0) {		// 第一段的端点
            mi = min(mi, a[0]*2);
            mx = max(mx, a[i-1]*2);
        }
        if(k-i > 0) {	// 第三段的端点
            mi = min(mi, a[n-(k-i)]/2);
            mx = max(mx, a[n-1]/2);
        }
        if(n != k) {	// 第二段的端点
            mi = min(mi, a[i]);
            mx = max(mx, a[n-(k-i)-1]);
        }
        ans = min(ans, mx - mi);		//更新极差最小值
    }
    cout << ans << endl;
}
~~~

### java

~~~java
import java.util.*;
class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt(), k = in.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = in.nextInt();
        }
        Arrays.sort(a);			//排序
        int ans = (int)1e9;
        for (int i = 0; i <= k; i++) {		
            int mi = (int)1e9, mx = 0;		
            if(i > 0) {		
                mi = Math.min(mi, a[0]*2);
                mx = Math.max(mx, a[i-1]*2);
            }
            if(k-i > 0) {	
                mi = Math.min(mi, a[n-(k-i)]/2);
                mx = Math.max(mx, a[n-1]/2);
            }
            if(n != k) {	
                mi = Math.min(mi, a[i]);
                mx = Math.max(mx, a[n-(k-i)-1]);
            }
            ans = Math.min(ans, mx - mi);		
        }
        System.out.println(ans);
    }
}
~~~