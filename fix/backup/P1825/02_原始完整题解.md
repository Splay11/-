## 题解

这题是一道分类讨论的题。

可以注意到最终的答案要么是 $x$ ，要么是 $0$ ，要么是 $x \% n$。

对这几种情况分类讨论即可，具体看代码。

## AC代码
### python
```python
T = int(input())
for _ in range(T):
    n, x, k = map(int, input().split())
    if x <= n:
        # k ~ n x
        if k <= x: # 最后会变成 0
            print(0)
        else:
            print(x) # 最后是 x
    else:
        if k == n + 1: # 如果是最后一项
            print(x)
        else:
            x %= n # 先 mod n
            if k < x: 
                print(0)
            else:
                print(x)
```

### c++
``` c++
#include<bits/stdc++.h>
using namespace std;

int t, n, x, k, ans;

int main(){
	scanf("%d", &t);
	while(t--){
		scanf("%d%d%d", &n, &x, &k);
		ans = x; // 表示第n+1项的值为x 
		while(n >= k){
			ans = ans % n;
			n--;
		}
		printf("%d\n", ans);
	}
	return 0;
}
```

### java
``` java
import java.util.*;
// 注意类名必须为Main
class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int T = in.nextInt();
        while (T-- > 0){
            int n = in.nextInt();
            int x = in.nextInt();
            int k = in.nextInt();
            if(k == n+1){
                System.out.println(x);
                continue;
            }
            int count = n-k+1;
            while (count-- > 0){
                x = x % (n--);
            }
            System.out.println(x);
        }
    }

}
```