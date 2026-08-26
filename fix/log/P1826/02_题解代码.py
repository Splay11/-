用并查集维护，并记录之前是否形成过基环树。

对于每次建立连接的操作，判断节点 $u$ 和节点 $v$ 是否已经连通：

- 如果已经连通，并且连通块之前没有形成过基环树，则该连通块中添加这条边满足条件输出 `Yes`。
- 如果不连通，则将 $u$ 和 $v$ 所在的连通块合并。

## AC代码

```cpp
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    std::vector<int> p, siz;
    DSU(int n) : p(n+1), siz(n+1, 1) { std::iota(p.begin(), p.end(), 0); }
    int find(int x) {
        return p[x] == x ? x : p[x] = find(p[x]);
    }
    bool same(int x, int y) { return find(x) == find(y); }
    bool merge(int x, int y) {
        x = find(x);
        y = find(y);
        if (x == y) return false;
        siz[x] += siz[y];
        p[y] = x;
        return true;
    }
    int size(int x) { return siz[find(x)]; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n, m;
    cin >> n >> m;
    set<int> st;
    set<pair<int, int>> g;
    DSU d(n);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        if(u == v) continue;
        if (g.count({u, v}) || g.count({v, u})) {
            cout << "No\n";
            continue;
        }
        if (d.find(u) != d.find(v)) {
            d.merge(u, v);
            cout << "No\n";
        } else {
            int fa = d.find(u);
            if (st.count(fa))
                cout << "No\n";
            else {
                cout << "Yes\n";
                d.merge(u, v);
                st.insert(fa);
            }
        }
        g.insert({u, v});
        g.insert({v, u});
    }
    return 0;
}


```
### java
```java
import java.util.*;

class DSU {
    private int[] p, siz;

    // 构造函数
    public DSU(int n) {
        p = new int[n + 1];
        siz = new int[n + 1];
        Arrays.fill(siz, 1);
        for (int i = 0; i <= n; i++) {
            p[i] = i;
        }
    }

    // 查找函数（带路径压缩）
    public int find(int x) {
        if (p[x] == x) {
            return x;
        } else {
            p[x] = find(p[x]);
            return p[x];
        }
    }

    // 判断两个节点是否在同一个集合
    public boolean same(int x, int y) {
        return find(x) == find(y);
    }

    // 合并两个集合
    public boolean merge(int x, int y) {
        x = find(x);
        y = find(y);
        if (x == y) return false;
        siz[x] += siz[y];
        p[y] = x;
        return true;
    }

    // 获取集合的大小
    public int size(int x) {
        return siz[find(x)];
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int m = scanner.nextInt();

        Set<Integer> st = new HashSet<>();
        Set<String> g = new HashSet<>();
        DSU dsu = new DSU(n);

        for (int i = 0; i < m; i++) {
            int u = scanner.nextInt();
            int v = scanner.nextInt();

            if (u == v) continue; // 忽略自环边

            String edge = u < v ? u + "," + v : v + "," + u;
            if (g.contains(edge)) {
                System.out.println("No");
                continue;
            }

            if (!dsu.same(u, v)) {
                dsu.merge(u, v);
                System.out.println("No");
            } else {
                int fa = dsu.find(u);
                if (st.contains(fa)) {
                    System.out.println("No");
                } else {
                    System.out.println("Yes");
                    dsu.merge(u, v);
                    st.add(fa);
                }
            }
            g.add(edge);
        }
        scanner.close();
    }
}
```