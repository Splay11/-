### 思路：双指针

题目要我们求两个排列的本质不同的子排列(连续的)。

直接计算不好做，**正难则反**。先求所有可能。然后减去重复的就行。

长度为$x$的所有子排列个数为$x*(x+1)/2$，两个排列一共是$x*(x+1)$

接下来的问题就是如何找出两个排列中重复的排列。

假设两个数组分别为$a,b$，令$r$表示枚举到了$b$数组的第$r$位，$l$表示$a$数组中，$a_l=b_r$的位置。然后不断往后比对，并记录长度$x$，直到比对到不同时，减去相应的值($x*(x+1)/2$)即可。

#### 正确性

排列有一个非常重要的性质是：每个数只出现一次。所以每次找最大的长度，遇到不同就断开。这样一定可以。因为之前考虑过的数在之后一定不会再碰到。所以时间复杂度$O(N)$

这里塔子哥也提醒大家，不要漏掉题目中的任何一个条件。**仔细思考如何利用给的每个条件**

c++
```cpp
#include <iostream>
#include <cstdio>
using namespace std;
#define ll long long

const int maxn=2e5+10;
int n;
int a[maxn],b[maxn];
int ida[maxn],idb[maxn];

ll get(ll x){
	return x*(x+1)/2;
}

int main(){
	std::ios::sync_with_stdio(false);
	cin>>n;
	for(int i=1;i<=n;++i){
		cin>>a[i];
		ida[a[i]]=i;
	}
	for(int i=1;i<=n;++i){
		cin>>b[i];
		idb[b[i]]=i;
	}
	ll ans=(ll)n*(ll)n+n;
	for(int l,r=1,cnt;r<=n;){
		l=ida[b[r]];
		cnt=0;
		while(l<=n&&r<=n&&a[l]==b[r]){
			l++;
			r++;
			cnt++;
		}
		ans-=get(cnt);
	}
	cout<<ans;
	
	return 0;
}
```


java
```java
import java.util.Scanner;

public class Main {
    static final int maxn = (int) 2e5 + 10;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] a = new int[maxn];
        int[] b = new int[maxn];
        int[] ida = new int[maxn];
        int[] idb = new int[maxn];
        
        for (int i = 1; i <= n; ++i) {
            a[i] = scanner.nextInt();
            ida[a[i]] = i;
        }
        for (int i = 1; i <= n; ++i) {
            b[i] = scanner.nextInt();
            idb[b[i]] = i;
        }
        
        long ans = (long) n * n + n;
        int r = 1;
        
        while (r <= n) {
            int l = ida[b[r]];
            int cnt = 0;
            while (l <= n && r <= n && a[l] == b[r]) {
                l++;
                r++;
                cnt++;
            }
            ans -= get(cnt);
        }
        
        System.out.println(ans);
    }
    
    static long get(long x) {
        return x * (x + 1) / 2;
    }
}
```

python
```python
def get(x):
    return x * (x + 1) // 2

def main():
    maxn = int(2e5) + 10

    n = int(input())
    a = [0] * maxn
    b = [0] * maxn
    ida = [0] * maxn
    idb = [0] * maxn

    a_input = list(map(int, input().split()))
    b_input = list(map(int, input().split()))

    for i in range(1, n + 1):
        a[i] = a_input[i - 1]
        ida[a[i]] = i
    for i in range(1, n + 1):
        b[i] = b_input[i - 1]
        idb[b[i]] = i

    ans = n * n + n
    r = 1

    while r <= n:
        l = ida[b[r]]
        cnt = 0
        while l <= n and r <= n and a[l] == b[r]:
            l += 1
            r += 1
            cnt += 1
        ans -= get(cnt)

    print(ans)

if __name__ == "__main__":
    main()
```