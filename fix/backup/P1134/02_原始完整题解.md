## 思路:懒标记 + dfs

1.末尾的0



某个数$x$的末尾0的个数 等价于  $x$ 质因分解后$2,5$ 的个数中的较小值。所以我们去记录每个节点的权值中2的个数以及5的个数即可。

例如:$25000 = 2^3 * 5^5$ ,  所以它末尾有$min(3,5)=3$ 个0

$123 = 3 * 41$ , 它里面没有$2,5$  ,所以末尾没有0



2.懒标记技巧

​	每次操作，我们都暴力的dfs整个子树,这个复杂度显然是不够的。根据数据范围我们希望有一个$O(1)$的做法。不难发现我们可以先只在被操作的节点上加上2，5个数。然后所有操作做完之后，我们使用一遍dfs，自顶向下的将这些贡献往下传递累加。这样的技巧又称为懒标记技巧。



3.最后

​	题目让求的是以节点$i$为根的子树的**所有点的权值的乘积** . 所以最后还需要一遍自底向上的dfs，求一个子树和。



## 代码

python

```python
from collections import defaultdict
# 计算x中有多少个y
def get(x , y):
	cnt = 0
	while x % y == 0:
		cnt += 1
		x //= y
	return cnt
# e 是邻接矩阵
e = defaultdict(list)
# lazy 是懒标记
lazy = defaultdict(list)
# 读入
n = int(input())
a = [0] + list(map(int , input().split()))
for i in range (n - 1):
	u , v = list(map(int , input().split()))
	e[u].append(v)
	e[v].append(u)
for i in range (1 , n + 1):
	lazy[i].append(0)
	lazy[i].append(0)
q = int(input())
for i in range (q):
	t , g = list(map(int , input().split()))
	x = get(g , 2)
	y = get(g , 5)
    # 先在被操作的点上打上标记
	lazy[t][0] += x
	lazy[t][1] += y
res = []
for i in range (n + 1):
	res.append([0 , 0])
# 第一遍dfs,自顶向下的将lazy的贡献往下传递
def dfs1(u , fa):
	for v in e[u]:
		if v == fa:
			continue
		lazy[v][0] += lazy[u][0]
		lazy[v][1] += lazy[u][1]
		dfs1(v , u)
	return 
# 第二遍dfs,自底向上的求子树的lazy和
def dfs2(u , fa):
	for v in e[u]:
		if v == fa:
			continue
		dfs2(v , u)
		lazy[u][0] += lazy[v][0]
		lazy[u][1] += lazy[v][1]
	res[u] = lazy[u][:]
	return 
dfs1(1 , -1)
# 记得把本身也加上
for i in range (1 , n + 1):
	lazy[i][0] += get(a[i] , 2)
	lazy[i][1] += get(a[i] , 5)
dfs2(1 , -1)
# 输出
for i in range (1 , n + 1):
	print (min(res[i][0] , res[i][1]) , end = " ")
```
c++
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
const int N = 1e5 + 10;
int twos[N], fives[N];
vector<int> e[N];
int t, n;
int in[N], Size[N], idx;
int dt[N], df[N];

void dfs(int u, int fa) {
    in[u] = ++idx;
    Size[u] = 1;

    for (auto v : e[u]) {
        if (v == fa) continue;

        dfs(v, u);
        Size[u] += Size[v];
    }
}
void sdfs(int u, int fa) {
    for (auto v : e[u]) {
        if (v == fa) continue;
        sdfs(v, u);
        dt[in[u]] += dt[in[v]];
        df[in[u]] += df[in[v]];
    }
}
void add(int l, int r, int x, int *a) {
    a[l] += x;
    a[r + 1] -= x;
}
signed main() {
    cin >> n;
    for (int i = 1, x; i <= n; i++) {
        cin >> x;
        int two = 0, five = 0;
        while (x % 2 == 0) {
            two++;
            x /= 2;
        }
        while (x % 5 == 0) {
            x /= 5;
            five++;
        }
        twos[i] = two, fives[i] = five;
    }

    for (int i = 1; i <= n - 1; i++) {
        int a, b;
        cin >> a >> b;
        e[a].push_back(b);
        e[b].push_back(a);
    }

    dfs(1, 0);
    // cout << Size[1] << endl;

    for (int i = 1; i <= n; i++) {
        add(in[i], in[i], twos[i], dt);
        add(in[i], in[i], fives[i], df);
    }

    cin >> t;
    while (t--) {
        int u, x;
        cin >> u >> x;
        int two = 0, five = 0;
        while (x % 2 == 0) {
            two++;
            x /= 2;
        }
        while (x % 5 == 0) {
            x /= 5;
            five++;
        }
        add(in[u], in[u] + Size[u] - 1, two, dt);
        add(in[u], in[u] + Size[u] - 1, five, df);
    }

    // sdfs(1, 0);
    for (int i = 1; i <= n; i++) {
        dt[i] += dt[i - 1];
        df[i] += df[i - 1];
    }
    sdfs(1, 0);
    for (int i = 1; i <= n; i++) {
        cout << min(dt[in[i]], df[in[i]]) << " ";
    }
    cout << endl;
}
```
java
```java

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    static int[][] vals;//【0】为2的个数，【1】为5的个数
    static List<Integer>[] edges;//边表
    static int[][] lazy;//懒加载
    static boolean[] iscan;//记录节点是否访问过

    public static void main(String[] args) throws FileNotFoundException {
        Scanner sc = new Scanner(System.in);
        int N = sc.nextInt();
        vals = new int[N+1][2];
        for (int i = 1; i <= N; i++) {
            int num = sc.nextInt();
            vals[i][0] = getN(num,2);
            vals[i][1] = getN(num,5);
        }
        lazy = new int[N+1][2];
        edges = new List[N+1];
        iscan = new boolean[N+1];
        for (int i = 1; i < edges.length; i++) {
            edges[i] = new ArrayList<>();
        }
        for (int i = 0; i < N - 1; i++) {
            int from = sc.nextInt();
            int to = sc.nextInt();
            edges[from].add(to);
            edges[to].add(from);
        }
        int Q = sc.nextInt();
        for (int i = 0; i < Q; i++) {
            int node = sc.nextInt();
            int mulNum = sc.nextInt();
            lazy[node][0] += getN(mulNum,2);
            lazy[node][1] += getN(mulNum,5);
        }
        dfs1(1);
        clear(iscan);
        dfs2(1);
        for (int i = 1; i <=N ; i++) {
            System.out.print(Math.min(vals[i][0],vals[i][1])+" ");
        }
    }

    private static void dfs2(int root) {//自低向上进行求和
        List<Integer> edge = edges[root];
        iscan[root] = true;
        for (Integer integer : edge) {
            if (!iscan[integer]){
                dfs2(integer);
                vals[root][0]+=vals[integer][0];
                vals[root][1]+=vals[integer][1];
            }
        }
    }

    private static void dfs1(int root) {//自顶向下处理lazy数组
        int i2 = lazy[root][0];
        int i5 = lazy[root][1];
        vals[root][0]+=i2;
        vals[root][1]+=i5;
        iscan[root] = true;
        List<Integer> edge = edges[root];
        for (Integer integer : edge) {
            if (!iscan[integer]){
                lazy[integer][0]+=i2;
                lazy[integer][1]+=i5;
                dfs1(integer);
            }
        }
    }

    private static int getN(int a, int b ) {
        int ans = 0;
        while ((a%b) == 0){
            ans++;
            a/=b;
        }
        return ans;
    }

    private static void clear(boolean[] iscan) {//重置iscan数组
        for (int i = 0; i < iscan.length; i++) {
            iscan[i] = false;
        }
    }

}
```