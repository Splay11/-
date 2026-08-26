## 题目思路

模拟即可，首先通过并查集找到所有的连通块和大小，对最大的连通块做最小生成树，将最小的生成树权值输出即可。

## 代码


**Java**

~~~java
import java.util.*;

public class Main {
    public static int N = (int) 2e6 + 10;
    public static int n, m = 0;
    public static int[] prime = new int[N];
    public static boolean[] st = new boolean[N];
    public static int[] pre, a, cnt;

    public static void getPrime() {
        for (int i = 2; i < N; i++) {
            if (!st[i]) {
                prime[m++] = i;
            }
            for (int j = 0; prime[j] <= (N - 1) / i; j++) {
                st[prime[j] * i] = true;
                if (i % prime[j] == 0) {
                    break;
                }
            }
        }
    }

    public static int find(int[] pre, int x) {
        if (pre[x] == x) {
            return x;
        }
        return pre[x] = find(pre, pre[x]);
    }

    public static int kruskal(int root) {
        List<int[]> edges = new ArrayList<>();
        List<Integer> nodes = new ArrayList<>();
        for (int i = 0; i < n; ++i)
            if (find(pre, i) == root) {
                nodes.add(i);
            }
        int tn = nodes.size();
        for (int i = 0; i < tn; ++i) {
            for (int j = i + 1; j < tn; ++j)
                if (!st[a[nodes.get(i)] + a[nodes.get(j)]]) {
                    edges.add(new int[] { a[nodes.get(i)] + a[nodes.get(j)], i, j });
                }
        }
        int[] t_pre = new int[tn];
        for (int i = 0; i < tn; ++i) {
            t_pre[i] = i;
        }
        Collections.sort(edges, (a, b) -> a[0] - b[0]);
        int ans = 0;
        for (int[] e : edges) {
            int u = find(t_pre, e[1]), v = find(t_pre, e[2]);
            if (u != v) {
                t_pre[u] = v;
                ans += e[0];
            }
        }
        return ans;
    }


    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        getPrime();
        a = new int[n];
        pre = new int[n];
        cnt = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
            pre[i] = i;
            cnt[i] = 1;
        }
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j)
                if (!st[a[i] + a[j]]) {
                    int u = find(pre, i), v = find(pre, j);
                    if (u != v) {
                        pre[u] = v;
                        cnt[v] += cnt[u];
                    }
                }
        }
        int mx_cnt = 0;
        for (int i = 0; i < n; ++i) {
            mx_cnt = Math.max(mx_cnt, cnt[i]);
        }
        int ans = Integer.MAX_VALUE;
        for (int i = 0; i < n; ++i)
            if (find(pre, i) == i && cnt[i] == mx_cnt) {
                ans = Math.min(ans, kruskal(i));
            }
        System.out.println(ans);
    }
}
~~~



### **Python**
``` Python
from collections import defaultdict

def check(N = int(3e6)):
    is_prime = [True]*(N)
    is_prime[0] = False
    is_prime[1] = False

    for i in range(N):
        if is_prime[i]:
            for j in range(i*i, N, i):
                is_prime[j] = False 

    return is_prime

class UnionFinder:
    # # 连通分量个数
    # _count: int
    # # 存储每个节点的父节点
    # parent: List[int]

    # n 为图中节点的个数
    def __init__(self, n: int):
        self._count = n
        self.parent = [i for i in range(n)]

    # 将节点 p 和节点 q 连通
    def union(self, p: int, q: int):
        rootP = self.find(p)
        rootQ = self.find(q)

        if rootP == rootQ:
            return

        self.parent[rootQ] = rootP
        # 两个连通分量合并成一个连通分量
        self._count -= 1

    # 判断节点 p 和节点 q 是否连通
    def connected(self, p: int, q: int) -> bool:
        rootP = self.find(p)
        rootQ = self.find(q)
        return rootP == rootQ

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    # 返回图中的连通分量个数
    def count(self) -> int:
        return self._count

if __name__ == "__main__":
    N = int(input())
    nums = [int(c) for c in input().strip().split()]
    
    is_prime = check()
    edges = []
    from queue import PriorityQueue
    q = PriorityQueue()
    for i in range(N):
        for j in range(i + 1, N):
            if is_prime[nums[i] + nums[j]]:
                q.put([nums[i] + nums[j], i, j])
                

    UF = UnionFinder(N)
    
    while not q.empty():
        val, u, v = q.get()
        # print(UF.parent)
        # print(val, u, v)
        if not UF.connected(u, v):
            UF.union(u, v)
            edges += [[u, v]]
            u_p = UF.find(u)
            v_p = UF.find(u)
    
    # print(edges)
    res = defaultdict(int)
    for v, u in edges:
        u_p = UF.find(u)
        res[u_p] += nums[u] + nums[v]
    # print(UF.parent)
    # print(res)
    print(min(res.values()))


# import java.util.*;

# public class Main {
#     public static int N = (int) 2e6 + 10;
#     public static int n, m = 0;
#     public static int[] prime = new int[N];
#     public static boolean[] st = new boolean[N];
#     public static int[] pre, a, cnt;

#     public static void getPrime() {
#         for (int i = 2; i < N; i++) {
#             if (!st[i]) {
#                 prime[m++] = i;
#             }
#             for (int j = 0; prime[j] <= (N - 1) / i; j++) {
#                 st[prime[j] * i] = true;
#                 if (i % prime[j] == 0) {
#                     break;
#                 }
#             }
#         }
#     }

#     public static int find(int[] pre, int x) {
#         if (pre[x] == x) {
#             return x;
#         }
#         return pre[x] = find(pre, pre[x]);
#     }

#     public static int kruskal(int root) {
#         List<int[]> edges = new ArrayList<>();
#         List<Integer> nodes = new ArrayList<>();
#         for (int i = 0; i < n; ++i)
#             if (find(pre, i) == root) {
#                 nodes.add(i);
#             }
#         int tn = nodes.size();
#         for (int i = 0; i < tn; ++i) {
#             for (int j = i + 1; j < tn; ++j)
#                 if (!st[a[nodes.get(i)] + a[nodes.get(j)]]) {
#                     edges.add(new int[] { a[nodes.get(i)] + a[nodes.get(j)], i, j });
#                 }
#         }
#         int[] t_pre = new int[tn];
#         for (int i = 0; i < tn; ++i) {
#             t_pre[i] = i;
#         }
#         Collections.sort(edges, (a, b) -> a[0] - b[0]);
#         int ans = 0;
#         for (int[] e : edges) {
#             int u = find(t_pre, e[1]), v = find(t_pre, e[2]);
#             if (u != v) {
#                 t_pre[u] = v;
#                 ans += e[0];
#             }
#         }
#         return ans;
#     }


#     public static void main(String[] args) {
#         Scanner sc = new Scanner(System.in);
#         n = sc.nextInt();
#         getPrime();
#         a = new int[n];
#         pre = new int[n];
#         cnt = new int[n];
#         for (int i = 0; i < n; i++) {
#             a[i] = sc.nextInt();
#             pre[i] = i;
#             cnt[i] = 1;
#         }
#         for (int i = 0; i < n; ++i) {
#             for (int j = i + 1; j < n; ++j)
#                 if (!st[a[i] + a[j]]) {
#                     int u = find(pre, i), v = find(pre, j);
#                     if (u != v) {
#                         pre[u] = v;
#                         cnt[v] += cnt[u];
#                     }
#                 }
#         }
#         int mx_cnt = 0;
#         for (int i = 0; i < n; ++i) {
#             mx_cnt = Math.max(mx_cnt, cnt[i]);
#         }
#         int ans = Integer.MAX_VALUE;
#         for (int i = 0; i < n; ++i)
#             if (find(pre, i) == i && cnt[i] == mx_cnt) {
#                 ans = Math.min(ans, kruskal(i));
#             }
#         System.out.println(ans);
#     }
# }
```


**会员可通过查看《已通过》的提交记录来查看其他语言哦~**