## 题解

### 题面描述

给定一棵有 $n$ 个节点的树，每个节点 $i$ 具有权值 $a_i$。定义一条路径的权值为这条路径上所有节点权值的 $gcd(a_{b_1},a_{b_2},\dots,a_{b_h})$，其中路径上的节点编号为 $b_1,b_2,\dots,b_h$。当路径只有一个节点时，其路径权值即为该节点的权值。要求统计树中有多少条简单路径的权值为偶数。注意：我们认为 $u\to v$ 和 $v\to u$ 是同一条路径，且 $u\to u$ 也算一条路径。

### 思路

本题的核心在于利用最大公约数为偶数的充要条件，即路径上所有节点必须均为偶数，将原问题转化为仅考虑偶数节点构成的子图，然后在该子图中寻找各个连通块，对于每个连通块中包含的偶数节点数记为 $k$，简单路径数为 $\frac{k(k+1)}{2}$，最后将所有连通块的路径数累加得到答案。

观察 $gcd$ 的性质可知：对于任意一组正整数，只有当所有数均为偶数时，其 $gcd$ 才必然为偶数。也就是说，若路径中存在奇数，则 $gcd$ 一定为奇数。因此，本题实际上转化为统计所有**只包含偶数节点**的简单路径数。

在树中，若我们只考虑权值为偶数的节点，并且仅保留它们之间原本存在的边，那么得到的子图必然是一个森林（若干个连通块）。在一个连通块中，任意两个节点间都有唯一的一条简单路径，加上每个节点自身构成的单点路径，总的路径数为  
$$\frac{k(k+1)}{2},$$  
其中 $k$ 为该连通块的节点数。

因此，只需：
1. 遍历所有节点，筛选出权值为偶数的节点；
2. 利用 DFS（或 BFS）在原树中只遍历偶数节点，从而分离出各个连通块；
3. 对每个连通块，计算其简单路径数 $\frac{k(k+1)}{2}$，累加即得答案。

## cpp
```cpp
#include <iostream>
#include <vector>
#include <functional>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    cin >> n;
    // 存储节点权值，节点编号从 $1$ 到 $n$
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++){
        cin >> a[i];
    }
    
    // 构造邻接表表示树
    vector<vector<int>> adj(n + 1);
    for (int i = 1; i <= n - 1; i++){
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    
    // 用于标记节点是否已访问
    vector<bool> visited(n + 1, false);
    long long ans = 0;
    
    // DFS函数：遍历只包含偶数节点的连通块，并返回该连通块中节点的个数
    function<int(int)> dfs = [&](int u) -> int {
        visited[u] = true;
        int count = 1;
        // 遍历 $u$ 的所有相邻节点
        for (int v : adj[u]) {
            // 只有当节点未访问且权值为偶数时，才进行递归遍历
            if (!visited[v] && (a[v] % 2 == 0)) {
                count += dfs(v);
            }
        }
        return count;
    };
    
    // 遍历所有节点，针对每个未访问的偶数节点启动 DFS
    for (int i = 1; i <= n; i++){
        if (!visited[i] && (a[i] % 2 == 0)) {
            int comp_size = dfs(i);
            // 对于一个连通块，简单路径数为 $\frac{comp\_size \times (comp\_size+1)}{2}$
            ans += (long long) comp_size * (comp_size + 1) / 2;
        }
    }
    
    cout << ans << "\n";
    return 0;
}

```
## python
```python
import sys
sys.setrecursionlimit(300000)  # 设置递归深度上限，防止大树深度导致递归溢出

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    # 节点权值，节点编号从 $1$ 到 $n$
    a = [0] + list(map(int, input().split()))
    
    # 构造邻接表表示树
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    visited = [False] * (n + 1)
    ans = 0
    
    # DFS函数：遍历只包含偶数节点的连通块，返回该连通块中节点数
    def dfs(u):
        visited[u] = True
        count = 1
        for v in adj[u]:
            if not visited[v] and a[v] % 2 == 0:
                count += dfs(v)
        return count
    
    # 遍历所有节点，若节点未访问且权值为偶数，则启动 DFS
    for i in range(1, n + 1):
        if not visited[i] and a[i] % 2 == 0:
            comp_size = dfs(i)
            # 连通块中简单路径数为 $\frac{comp\_size \times (comp\_size+1)}{2}$
            ans += comp_size * (comp_size + 1) // 2
    print(ans)

if __name__ == '__main__':
    main()

```
## java
```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 提高输入效率
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());
        // 存储节点权值，节点编号从 $1$ 到 $n$
        int[] a = new int[n + 1];
        String[] parts = br.readLine().split(" ");
        for (int i = 1; i <= n; i++){
            a[i] = Integer.parseInt(parts[i - 1]);
        }
        
        // 构造邻接表表示树
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++){
            adj.add(new ArrayList<>());
        }
        for (int i = 1; i < n; i++){
            parts = br.readLine().split(" ");
            int u = Integer.parseInt(parts[0]);
            int v = Integer.parseInt(parts[1]);
            adj.get(u).add(v);
            adj.get(v).add(u);
        }
        
        boolean[] visited = new boolean[n + 1];
        long ans = 0;
        
        // 遍历所有节点，如果节点未访问且权值为偶数，则进行迭代 DFS
        for (int i = 1; i <= n; i++){
            if (!visited[i] && a[i] % 2 == 0) {
                int compSize = 0;
                // 使用栈实现 DFS
                Deque<Integer> stack = new ArrayDeque<>();
                stack.push(i);
                visited[i] = true;
                while (!stack.isEmpty()){
                    int u = stack.pop();
                    compSize++;
                    // 遍历节点 $u$ 的所有邻接点
                    for (int v : adj.get(u)){
                        if (!visited[v] && a[v] % 2 == 0){
                            visited[v] = true;
                            stack.push(v);
                        }
                    }
                }
                // 连通块中简单路径数为 $\frac{compSize \times (compSize+1)}{2}$
                ans += (long) compSize * (compSize + 1) / 2;
            }
        }
        
        System.out.println(ans);
    }
}

```