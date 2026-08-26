## 思路

思维题。

由于 a 数组是一个 1-n 的排列，因此对于每个 i，必然有这样的线路：
i -> a[i] -> a[a[i]] -> ... -> i

所以必然是一个圈，只需要统计每个圈的大小为 $x$ ，所有圈的平方 $x^2$ 和即为答案。 

时间复杂度：$O(n)$

### 证明：
如果说存在一个线路 i -> a[i] -> a[a[i]] -> ... -> j，满足 j != i 。

首先 j 必然不会在之前出现过，否则就与 a 数组是一个 1-n 的排列这部分冲突了。

如果 j != i，那么 a[j] 要么等于 i ，要么不等于 i （一句废话）

也就是说无论如何 j 可以继续走到 a[j] ，直到走到一个 a 的值为 i 为止。

所以必然是存在一个线路从 i -> a[i] -> a[a[i]] -> ... -> i

## 代码
### Python
```python
n = int(input())
a = list(map(int, input().split()))

for i in range(n):
    a[i] -= 1

vis = [0] * n
ans = 0
for i in range(n):
    if vis[i]:
        continue
    vis[i] = 1
    c = 1
    j = a[i]
    while j != i:
        vis[j] = 1
        j = a[j]
        c += 1
    ans += c * c

print(ans)
```

### java
```java
import java.util.*;
class Main{
    public static void main(String[] args){
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        int[] nums = new int[n+1];
        for(int i=0;i<n;i++) nums[i+1] = in.nextInt();
        boolean[] visited = new boolean[n+1];
        long ans=0;
        for(int i=1;i<n+1;i++){
            long size = 0;
            int j = nums[i];
            while(!visited[j]){
                visited[j]=true;
                size++;
                j = nums[j];
            }
            ans += size*size;
        }
        System.out.println(ans);
    }
}
```
### C++
```C++
#include <bits/stdc++.h>

using namespace std;
typedef long long ll;
const int maxn = 1e5 +10;

int dp[maxn];
int nx[maxn];
int vis[maxn];
int sz[maxn];
int num;
void dfs(int now)
{
	if(vis[now]) return ;
	vis[now] = 1;
	num++;
	dfs(nx[now]);
}
int main()
{
	int n;
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		int a;
		scanf("%d",&a);
		nx[i] = a;
		dp[a]++;
		sz[i] = 1;
	}
	queue<int>v;
	for(int i=1;i<=n;i++)
	{
		if(dp[i]==0)
		{
			v.push(i);
		}
	}
	long long ans = n;
	while(!v.empty())
	{
		int now = v.front();
		v.pop();
		ans += sz[now];
		vis[now] = 1;
		int nex = nx[now];
		sz[nex] += sz[now];
		dp[nex]--;
		if(dp[nex]==0)
			v.push(nex);
	}
	for(int i=1;i<=n;i++)
	{
		if(!vis[i])
		{
			num = 0;
			dfs(i);
			ans += 1ll*num*(num-1);
		}
	}
	cout<<ans<<endl;
	return 0;
}
```