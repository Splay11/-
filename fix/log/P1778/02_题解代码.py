# 思路
Dijkstra算法的变种
- dist[i][0] 表示从 1 到 i ，到达 i 的时候，使用第一种交通工具的最小花费
- dist[i][1] 表示从 1 到 i ，到达 i 的时候，使用第二种交通工具的最小花费
最终答案就是 min(dist[n][0], dist[n][1])

主要考察对于 Dijkstra 算法是否熟悉，注意这里使用的是小根堆

时间复杂度：$O(m\log n)$

# 代码
### python
```python
import heapq

INF = int(1e18)

class Edge:
    def __init__(self, u, w, t):
        self.u = u
        self.w = w
        self.t = t

class Node:
    def __init__(self, d, u, t):
        self.d = d
        self.u = u
        self.t = t
    
    def __lt__(self, other):
        return self.d < other.d

def dijkstra(s, ed):
    dist = [[INF] * 2 for _ in range(N)]
    dist[s][0] = dist[s][1] = 0
    heap = []
    heapq.heappush(heap, Node(0, 1, 0))
    heapq.heappush(heap, Node(0, 1, 1))
    while heap:
        top = heapq.heappop(heap)
        u, t = top.u, top.t
        if st[u][t]:
            continue
        st[u][t] = True
        for e in g[u]:
            next_u, next_t = e.u, e.t
            trans = 0
            if next_t != t:
                trans = a[u - 1]
            if dist[next_u][next_t] > dist[u][t] + trans + e.w:
                dist[next_u][next_t] = dist[u][t] + trans + e.w
                heapq.heappush(heap, Node(dist[next_u][next_t], next_u, next_t))
    return min(dist[ed][0], dist[ed][1])

N = 100010
g = [[] for _ in range(N)]
st = [[False] * 2 for _ in range(N)]
n, m = map(int, input().split())
a = list(map(int, input().split()))
for _ in range(m):
    u, v, w, t = map(int, input().split())
    t -= 1
    g[u].append(Edge(v, w, t))
    g[v].append(Edge(u, w, t))

print(dijkstra(1, n))

```
### java
```java
import java.util.*;

class Edge {
    int u, w, t;

    Edge(int u, int w, int t) {
        this.u = u;
        this.w = w;
        this.t = t;
    }
}

class Node implements Comparable<Node> {
    long d;
    int u, t;

    Node(long d, int u, int t) {
        this.d = d;
        this.u = u;
        this.t = t;
    }

    @Override
    public int compareTo(Node other) {
        return Long.compare(this.d, other.d);
    }
}

public class Main {
    static final long INF = (long) 1e18;
    static int N;
    static List<Edge>[] g;
    static boolean[][] st;
    static long[][] dist;
    static int[] a;

    static long dijkstra(int s, int ed) {
        for (int i = 0; i < N; i++) {
            dist[i][0] = INF;
            dist[i][1] = INF;
        }
        dist[s][0] = dist[s][1] = 0;

        PriorityQueue<Node> heap = new PriorityQueue<>();
        heap.offer(new Node(0, s, 0));
        heap.offer(new Node(0, s, 1));

        while (!heap.isEmpty()) {
            Node top = heap.poll();
            int u = top.u, t = top.t;
            if (st[u][t]) continue;
            st[u][t] = true;

            for (Edge e : g[u]) {
                int next_u = e.u, next_t = e.t;
                long trans = 0;
                if (next_t != t) {
                    trans = a[u - 1];
                }
                if (dist[next_u][next_t] > dist[u][t] + trans + e.w) {
                    dist[next_u][next_t] = dist[u][t] + trans + e.w;
                    heap.offer(new Node(dist[next_u][next_t], next_u, next_t));
                }
            }
        }
        return Math.min(dist[ed][0], dist[ed][1]);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int m = scanner.nextInt();
        N = n + 1;

        a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }

        g = new ArrayList[N];
        for (int i = 0; i < N; i++) {
            g[i] = new ArrayList<>();
        }

        for (int i = 0; i < m; i++) {
            int u = scanner.nextInt();
            int v = scanner.nextInt();
            int w = scanner.nextInt();
            int t = scanner.nextInt() - 1;
            g[u].add(new Edge(v, w, t));
            g[v].add(new Edge(u, w, t));
        }

        st = new boolean[N][2];
        dist = new long[N][2];

        System.out.println(dijkstra(1, n));
        scanner.close();
    }
}
```
### C++
```C++
#include<bits/stdc++.h>
using namespace std;
typedef long long LL;
const LL INF = 1e18;
const int N = 1e5 + 10;

int n, m, a[N];
LL dis[N][2];
bool vis[N][2];
struct node{
	int to, t, w; 
	/*
	to表示边的终点
	t表示线路类别：0：该线路为飞机线路 1：该线路为火车线路
	w表示行驶该路线所需的时间 
	*/ 
};
vector<node> edge[N];

struct Vnode{
	int startNode;
	int t;
	LL w;
	/*
	to表示边的起点
	t表示线路类别：0：该线路为飞机线路 1：该线路为火车线路
	w表示行驶该路线所需的时间 
	*/ 
}now;

bool cmp(Vnode A, Vnode B){
	if(A.w != B.w) return A.w > B.w;
	return A.startNode > B.startNode;
} 
//  decltype为c++11中的关键字，decltype(&cmp)获取了比较函数cmp的类型
priority_queue<Vnode, vector<Vnode>, decltype(&cmp)> pq(cmp); // 小顶堆 

void dijstra(){
	for(int i = 1; i <= n; i++) dis[i][0] = dis[i][1] = INF;
	dis[1][1]= dis[1][0] = 0;
	pq.push({1,0,0}); // 从1号城市的飞机站出发， 
	pq.push({1,1,0}); // 从1号城市的火车站出发， 
	while(!pq.empty()){
		now = pq.top();pq.pop();
		int u = now.startNode;
		int ut = now.t;
		if(!vis[u][ut]){
			vis[u][ut] = 1;
			int sz = int(edge[u].size());
			for(int j = 0; j < sz; j++){
				int v = edge[u][j].to;
				int w = edge[u][j].w;
				int vt = edge[u][j].t;
				if(!vis[v][vt]){
					/*
					1)如果到达当前的站的类别与出发站的类别相同，则不需要转换交通工具所需的时间
					2)如果到达当前的站的类别与出发站的类别不相同，则需要转换交通工具所需的时间
					*/ 
					if(vt == ut) dis[v][vt] = min(dis[v][vt], dis[u][vt] + w);
					else dis[v][vt] = min(dis[v][vt], dis[u][ut]+a[u]+w);
					pq.push({v,vt, dis[v][vt]});
				}
			}
		}
		
	}
}
int main(){
	
	scanf("%d%d", &n, &m);
	for(int i = 1; i <= n; i++) scanf("%d", &a[i]);
	for(int i = 1, u, v, w, t; i <= m; i++){
		scanf("%d%d%d%d", &u, &v, &w, &t);
		t--;
		edge[u].push_back({v, t, w});
		edge[v].push_back({u, t, w});
	}
	dijstra();
	printf("%lld\n", min(dis[n][0], dis[n][1]));
	return 0;
}
```