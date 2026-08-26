长度为k的区间满足"顺子"的充要条件:

1.具有k个不同的数

2.该区间的最大值减最小值为:k-1

做法：

用ST表查询区间最大值和最小值

统计区间的不同的数可以开一个桶 $num[]$ :若加入该数 $a[i]$ 前 $num[a[i]]=0$ 则数量+1。若减去该数 $a[i-k+1]$ 前 $num[a[i]]=1$ 则数量-1

每一次往右移动一个区间加入一个数并删除一个数更新 $num[]$ 
C++
```cpp
#include<bits/stdc++.h>
using ll = long long;
using namespace std;
int main() {
	ios::sync_with_stdio(0);
	cin.tie(0);
	ll n, k;
	cin >> n >> k;
	vector<ll> v(n);
	for (auto& i : v) cin >> i;
	set<ll> st;
	ll res = 0;
	ll j = 0;
	for (ll i = 0; i < n; ++i) {
		if (st.count(v[i])) {
			while (st.count(v[i])) {
				st.erase(v[j++]);
			}
		}
		st.insert(v[i]);
		while (st.size() > k) {
			st.erase(v[j++]);
		}
		if (i - j + 1 == k) {
			ll l = *st.begin(), r = *st.rbegin();
			if (r - l + 1 == k) {
				res += 1;
			}
		}
	}
	cout << res;
}
```

Java
```java
import java.util.*;

class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        int n=in.nextInt(),k=in.nextInt();
        int[] nums=new int[n];
        for(int i=0;i<n;i++)
            nums[i]=in.nextInt();
        PriorityQueue<Integer> p1=new PriorityQueue<>((a,b)->(nums[a]-nums[b]));
        PriorityQueue<Integer> p2=new PriorityQueue<>((a,b)->(nums[b]-nums[a]));
        int[] vis=new int[1000006];
        int res=0,l=0,r=-1;
        while(r<n){
            while(r-l<k-1){
                r++;
                if(r>=n){
                    break;
                }
                vis[nums[r]]++;
                p1.add(r);
                p2.add(r);
                while(vis[nums[r]]>1){
                    vis[nums[l]]--;
                    l++;
                }
            }

            if(r<n&&r-l==k-1){//System.out.println(r);
                int min=0,max=0;
                while(r-(min=p1.peek())>=k){

                    p1.poll();
                }
                while(r-(max=p2.peek())>=k){
                    p2.poll();
                }
                if(nums[max]-nums[min]==k-1)
                    res++;
                //System.out.println(l+" "+r+" "+min+" "+max);
                vis[nums[l++]]--;
            }
        }
        System.out.println(res);
    }
}
```

Python
```python
import math

n, k = map(int, input().split())
a = list(map(int, input().split()))
#----------------------------------------ST表，查询区间最大值和最小值
f = [[0] * 18 for i in range(1 + n)]
g = [[int(1e9)] * 18 for i in range(1 + n)]

for i in range(1, n + 1):
    f[i][0] = g[i][0] = a[i - 1]

for j in range(1, int(math.log2(n)) + 1):
    for i in range(1, n - 2 ** j + 2):
        f[i][j] = max(f[i][j - 1], f[i + 2 ** (j - 1)][j - 1])
        g[i][j] = min(g[i][j - 1], g[i + 2 ** (j - 1)][j - 1])
def getmin(l, r):
    l += 1; r += 1
    k = int(math.log2(r - l + 1))
    return min(g[l][k], g[r - 2 ** k + 1][k])


def getmax(l, r):
    l += 1; r += 1
    k = int(math.log2(r - l + 1))
    return max(f[l][k], f[r - 2 ** k + 1][k])
#---------------------------------------------------------
num = [0] * int(1e6 + 3)#记录每个数出现的次数
cnt = 0#区间内不同的数
for i in range(k - 1):
    if num[a[i]] == 0: cnt += 1
    num[a[i]] += 1

ans = 0
for i in range(k - 1, n):
    if num[a[i]] == 0: cnt += 1
    num[a[i]] += 1
    if cnt == k:#条件1
        mi = getmin(i - k + 1, i)
        if getmax(i - k + 1, i) == mi + k - 1:#条件2
            ans += 1
    if num[i - k + 1] == 1: cnt -= 1
    num[i - k + 1] -= 1
print(ans)
```