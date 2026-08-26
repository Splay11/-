## 思路

### 解法一：建图技巧+最短路

**1.如果没有传送机会**

​	那么就是一个裸的最短路。建立一张网格图，然后跑dijstra即可。

**2.有传送机会**

​	1.提升维度：$dp[i][j=0/1]$ 代表当前站在点$i$ 并且是否使用过传送机会时的 最短路。

​	2.暴力建图：任意两个相同权值的点之间建立一条**虚边**。在跑dijstra的时候注意分两类边讨论：

​		普通的边：第二维状态不变。

​		**虚边** ： 第二维状态从 $0 \rightarrow 1$ , 且当且仅当第二维 $j=0$ 时才允许经过虚边。

**3.建图优化**

​	上面那种暴力建图方式会使得$E = n^4$.无法通过本题。这里使用超级源点技巧，即：拉若干个**虚点**出来，让所有相同权值的点都连一条边到同一个虚点即可。dijstra的时候与上面同理地进行分类讨论。这种方法可以轻松拓展至**有$k(k=2,3,4)$次传送机会** 

### 解法二：巧妙思维+最短路

由于相同的点之间传送无需花费，且只允许一次，而且又是无向图。所以有一种比较巧妙的做法：正向跑一遍dijstra，反向跑一遍dijstra.

接着相同权值的点(假设权值为$x$)的最短路即为 正向到任意一个权值为$x$点的最短路的最小值 + 反向到任意一个权值为$x$点的最短路的最小值

## 代码(解法1)

### C++代码

```c++
#include <bits/stdc++.h>
using namespace std;
#define ll long long
const int maxn = 505;
const int maxv = maxn * maxn + maxn;
int a[maxn][maxn];
int n , m;
int trans (int x , int y) {
    return (x - 1) * m + y;
}
vector<pair<int,ll>> e[maxv];
int dx[4] = {-1 , 1 , 0 , 0};
int dy[4] = {0 , 0 , -1 , 1};
// dijstra
ll dp[maxv][2];
int bk[maxv][2];
struct Node {
    int id , vis;
    ll val;
    bool operator < (const  Node & a) const{
        return val > a.val;
    }
};
priority_queue<Node> q;
void dij(){
    memset(dp , -1 , sizeof dp);
    dp[1][0] = 0;
    q.push({1 , 0 , 0});
    while (q.size()){
        Node g = q.top();
        q.pop();
        int u = g.id , vis = g.vis;
        if (bk[u][vis]) continue;
        bk[u][vis] = 1;
        for (auto t : e[u]){
            int v = t.first;
            ll w = t.second;
            // 分两种边讨论第二维的状态变化
            // 到虚点的边：0 -> 1
            if (v > n * m){
                if (vis) continue;
                if (dp[v][1] == -1 || dp[v][1] > dp[u][0] + w){
                    dp[v][1] = dp[u][0] + w;
                    q.push({v , 1 , dp[v][1]});
                }
            }// 经过普通边:0->0 , 1->1
            else {
                if (dp[v][vis] == -1 || dp[v][vis] > dp[u][vis] + w){
                    dp[v][vis] = dp[u][vis] + w;
                    q.push({v , vis , dp[v][vis]});
                }
            }
        }
    }
    return ;
}
int main() {
    cin >> n >> m;
    for (int i = 1 ; i <= n ; i++){
        for (int j = 1 ; j <= m ; j++){
            cin >> a[i][j];
        }
    }
    // 建图
    // 普通边
    map<int,vector<int>> mp;
    for (int i = 1 ; i <= n ; i++){
        for (int j = 1 ; j <= m ; j++){
            for (int d = 0 ; d < 4 ; d++){
                int ni = i + dx[d];
                int nj = j + dy[d];
                if (ni < 1 || ni > n || nj < 1 || nj > m) continue;
                e[trans(i , j)].push_back({trans(ni , nj) , abs(a[i][j] - a[ni][nj])});
            }
            mp[a[i][j]].push_back(trans(i , j));
        }
    }
    // 虚点 + 虚边
    int cnt = n * m + 1;
    for (auto x : mp){
        for (auto y : x.second){
            e[y].push_back({cnt , 0});
            e[cnt].push_back({y , 0});
        }
        cnt++;
    }
    dij();
    ll ans = dp[trans(n , m)][0];
    if (dp[trans(n , m)][1] != -1) ans = min(ans , dp[trans(n , m)][1]);
    cout << ans << endl;
	return 0;
}
```