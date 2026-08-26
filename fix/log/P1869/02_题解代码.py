## 题目思路

考虑树形dp，为每一个节点作为链的最高节点来代表其对应的最长链，其在链中前后的节点都是它的子节点，维护它对应链的链长。

由于它有前后两个方向，有两种类型的递增，所以共有4个状态，假设`f[u][0], g[u][0]`是分别是子节点权值大于等于节点u的链中前面节点对应的最长链长和次长链长，`f[u][1], g[u][1]`是分别是子节点权值小于等于节点u的链中前面节点对应的子链链长和后面节点对应的子链链长。

维护链长可以通过子节点的最长链来更新父节点的最长链和次长链（对应前和后），由于前面节点和后面节点不能是同一个，所以只需要子节点的最长链做更新即可。

初始时所有节点的链长都是1，然后从根节点开始dfs，更新链长，最后取最长链即可。

## 代码

**Java**

~~~java
import java.util.*;

public class Main {
    static class Pair {
        long first, second;
        Pair(long first, long second) {
            this.first = first;
            this.second = second;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        for (int i = 1; i < n; i++) {
            int u = sc.nextInt() - 1;
            int v = sc.nextInt() - 1;
            adj.get(u).add(v);
            adj.get(v).add(u);
        }
        Pair[] f = new Pair[n];
        Pair[] g = new Pair[n];
        for (int i = 0; i < n; i++) {
            f[i] = new Pair(1, 1);
            g[i] = new Pair(1, 1);
        }
        dfs(0, -1, adj, a, f, g);
        long ans = 1;
        for (int i = 0; i < n; i++) {
            ans = Math.max(ans, Math.max(f[i].first + g[i].first - 1, f[i].second + g[i].second - 1));
        }
        System.out.println(ans);
    }

    static void dfs(int u, int p, List<List<Integer>> adj, int[] a, Pair[] f, Pair[] g) {
        for (int v : adj.get(u)) {
            if (v == p) continue;
            dfs(v, u, adj, a, f, g);
            if (a[v] >= a[u]) {
                if (f[v].first + 1 >= f[u].first) {
                    g[u].first = f[u].first;
                    f[u].first = f[v].first + 1;
                } else {
                    g[u].first = Math.max(f[v].first + 1, g[u].first);
                }
            }
            if (a[v] <= a[u]) {
                if (f[v].second + 1 >= f[u].second) {
                    g[u].second = f[u].second;
                    f[u].second = f[v].second + 1;
                } else {
                    g[u].second = Math.max(f[v].second + 1, g[u].second);
                }
            }
        }
    }
}

~~~

**C++**

~~~c++
#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

int main()
{
  int n;
	cin >> n;
	vector<int> a(n);
	for (int i = 0;i < n;++ i) cin >> a[i];
	vector<vector<int>> adj(n);
	for (int i = 1, u, v;i < n;++ i) {
		cin >> u >> v;
		-- u, -- v;
		adj[u].push_back(v);
		adj[v].push_back(u);
	}
	vector<array<LL, 2>> f(n, {1, 1}), g = f;
	function<void(int, int)> dfs = [&](int u, int p) {
		for (int v : adj[u]) {
			if (v == p) continue;
			dfs(v, u);
			if (a[v] >= a[u]) {
				if (f[v][0] + 1 >= f[u][0]) {
					g[u][0] = f[u][0];
					f[u][0] = f[v][0] + 1;
				} else {
					g[u][0] = max(f[v][0] + 1, g[u][0]);
				}
			}
			if (a[v] <= a[u]) {
				if (f[v][1] + 1 >= f[u][1]) {
					g[u][1] = f[u][1];
					f[u][1] = f[v][1] + 1;
				} else {
					g[u][1] = max(f[v][1] + 1, g[u][1]);
				}
			}
		}

	};
	dfs(0, 0);
	LL ans = 1;
	for (int i = 0;i < n;++ i) {
		ans = max({ans, f[i][0] + g[i][0] - 1, f[i][1] + g[i][1] - 1});
	}
	cout << ans << endl;
  return 0;
}
~~~

**Python**

~~~python
import sys
from collections import deque, defaultdict
sys.setrecursionlimit(200000)

def dfs(u, p, adj, a, f, g):
    for v in adj[u]:
        if v == p:
            continue
        dfs(v, u, adj, a, f, g)
        if a[v] >= a[u]:
            if f[v][0] + 1 >= f[u][0]:
                g[u][0] = f[u][0]
                f[u][0] = f[v][0] + 1
            else:
                g[u][0] = max(f[v][0] + 1, g[u][0])
        if a[v] <= a[u]:
            if f[v][1] + 1 >= f[u][1]:
                g[u][1] = f[u][1]
                f[u][1] = f[v][1] + 1
            else:
                g[u][1] = max(f[v][1] + 1, g[u][1])

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    index += 1
    
    a = [0] * n
    for i in range(n):
        a[i] = int(data[index])
        index += 1
    
    adj = defaultdict(list)
    for i in range(n - 1):
        u = int(data[index]) - 1
        v = int(data[index + 1]) - 1
        adj[u].append(v)
        adj[v].append(u)
        index += 2
    
    f = [[1, 1] for _ in range(n)]
    g = [[1, 1] for _ in range(n)]
    
    dfs(0, -1, adj, a, f, g)
    
    ans = 1
    for i in range(n):
        ans = max(ans, f[i][0] + g[i][0] - 1, f[i][1] + g[i][1] - 1)
    
    print(ans)

if __name__ == "__main__":
    main()

~~~

**会员可通过查看《已通过》的提交记录来查看其他语言哦~**