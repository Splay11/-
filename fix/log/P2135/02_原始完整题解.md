# 线性筛求最小质因数+质因数分解+树形dp
对于求出某个数的质因数的个数，普通的质因数分解的时间复杂度为sqrt(N)，加上有n个数，时间很极限，那么加个线性筛预处理一下每个数的最小质数把质因数分解变成log级别的，第一遍树形dp把哪些边需要染色求出来，第二遍树形dp求出最小次数以及染色哪几个点即可详细实现可见代码。
## 代码如下
### cpp
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
const int N = 1e7 + 100;
int primes[N],minp[N],cnt;
bool st[N];
int a[100005];
int n;
vector<int>g[100005];
void get_primes(int n)
{
	for(int i = 2 ; i <= n ; i++)
	{
		if(!st[i]) minp[i] = i,primes[cnt++] = i;
		for(int j = 0 ; primes[j] * i <= n ;j++)
		{
			int t = primes[j] * i;
			st[t] = true;
			minp[t] = primes[j];
			if(i % primes[j] == 0) break;
		}
	}
}
int get(int x){
	set<int>s;
	while(x>1){
		s.insert(minp[x]);
		x/=minp[x];
	}
	int res=s.size();
	return res;
}
int dp[100005];
void dfs1(int u,int fa){
	for(int v:g[u]){
		if(v==fa) continue;
		dfs1(v,u);
		if(a[v]==a[u]){
			dp[v]=1;
		}
	}
}
vector<int>ans;
void dfs2(int u,int fa){
	int res=0;
	for(int v:g[u]){
		if(v==fa) continue;
		dfs2(v,u);
		res|=dp[v];
	}
	if(dp[u]==1){
		if(res==0)
			ans.push_back(u);
	}
	if(res==1){
		dp[u]=1;
	}
}
signed main() {
	get_primes(10000000);
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>a[i];
		a[i]=get(a[i]);
	}
	for(int i=1;i<n;i++){
		int u,v;
		cin>>u>>v;
		g[u].push_back(v);
		g[v].push_back(u);
	}
	dfs1(1,0);
	dfs2(1,0);
	cout<<ans.size()<<'\n';
	sort(ans.begin(),ans.end());
	for(int v:ans){
		cout<<v<<' ';
	}
	cout<<'\n';
	return 0;
}




```