# 题解

## 题面描述

给定一个长度为$ n $的序列$ a $，总共进行$ m $次操作，每次操作按如下规则进行：  
- 在序列$ a $中，找到最小元素中最靠前（下标最小）的那个，其余所有数都减去$ k $。  

要求输出所有操作结束后序列$ a $中每个数的最终值。

---

## 思路

直接模拟每一次操作时间复杂度较高，考虑到$ n $和$ m $的上界均为$ 2\times10^5 $。观察操作规则不难发现，每一次操作对所有数都会扣除$ k $，而仅有一个数会“补回”这一$ k $。  
  
于是，我们可以把最终结果写成：
  
$$
a_i^{final}=a_i-m\times k+t_i\times k
$$

其中$ t_i $表示第$ i $个数在$ m $次操作中没有被扣$ k $的次数（即被“保留”的次数）。显然有  
$$
\sum_{i=1}^{n}t_i=m
$$  
  
操作规则要求：每一步选出的那个数一定是当前所有数中（扣除相同全局减去的$ k $后）最小的。  
  
设当前该数已经“保留”了$ t_i $次，则它的当前实际值为  
$$
a_i-current=a_i-(\text{操作步数}-t_i)\times k
$$  
注意到对于所有数，在某一步操作时，公共部分$ -(\text{操作步数})\times k $相同，因此只需比较  
$$
a_i+t_i\times k
$$  
即在每一步，选出使得$ a_i+t_i\times k $最小的数（若存在相等则选下标更小的），令其$ t_i $加$ 1 $。

这样最终的答案就可以表示为  
$$
a_i^{final}=a_i-(m-t_i)\times k
$$

我们可以利用优先队列来维护每个数的当前“键值”$ a_i+t_i\times k $，初始时所有$ t_i=0 $；每次从优先队列中取出最小值，对应数的$ t_i $加$ 1 $后，将其新的键值更新为$ a_i+(t_i+1)\times k $后重新放入队列。经过$ m $次操作后，每个数被“保留”了$ t_i $次，最终答案即为上式所示。

---

## 代码分析

- **数据结构：**  
  使用优先队列（小根堆），存储每个元素的结构为$ \{ \text{key}, \text{idx}, t \} $，其中$ \text{key}=a_i+t_i\times k $。  
- **比较规则：**  
  按照$ \text{key} $排序，若$ \text{key} $相同则按下标$ idx $从小到大优先。  
- **更新过程：**  
  循环$ m $次，每次取队首元素，将该位置的$ t_i $加一，并计算新的$ key=a_i+(t_i+1)\times k $后再插回队列。  
- **最后输出：**  
  遍历所有下标，最终值为  
  $$
  a_i^{final}=a_i-(m-t_i)\times k
  $$

---

## C++

```cpp
#include <iostream>
#include <queue>
#include <vector>
using namespace std;
 
// 定义节点结构体：存储当前键值、下标和保存次数
struct Node {
    long long key; // key = a[i] + t[i] * k
    int idx;      // 数组下标
    int t;        // 保留次数 t[i]
};
 
// 自定义比较函数：先比较 key，若相等则比较下标
struct cmp {
    bool operator()(const Node &a, const Node &b) const {
        if(a.key == b.key) return a.idx > b.idx;
        return a.key > b.key;
    }
};
 
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
 
    int T;
    cin >> T;
    while(T--){
        int n, m, k;
        cin >> n >> m >> k;
        vector<long long> a(n);
        for (int i = 0; i < n; i++){
            cin >> a[i];
        }
 
        // 初始时所有数 t[i] = 0, key = a[i]
        priority_queue<Node, vector<Node>, cmp> pq;
        vector<int> t(n, 0);
        for(int i = 0; i < n; i++){
            pq.push({a[i], i, 0});
        }
 
        // 进行 m 次操作，每次从 pq 取出最小 key 的元素，将其 t 值加一后更新 key 后再入队
        for(int op = 0; op < m; op++){
            Node cur = pq.top();
            pq.pop();
            cur.t++; // 该元素保留次数加一
            t[cur.idx] = cur.t;
            cur.key = a[cur.idx] + (long long)cur.t * k; // 更新 key
            pq.push(cur);
        }
 
        // 输出每个元素最后的结果： a[i] - (m - t[i]) * k
        for(int i = 0; i < n; i++){
            long long res = a[i] - (long long)(m - t[i]) * k;
            cout << res << " ";
        }
        cout << "\n";
    }
    return 0;
}
```
## Python

```python
import sys
import heapq
input = sys.stdin.readline

# 读取测试数据组数
T = int(input())
for _ in range(T):
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    # 初始化每个元素的保留次数 t[i] 为 0
    t = [0] * n
    # 构造优先队列，存放元素 (key, index, t)
    # key = a[i] + t[i] * k, 初始时 t[i] = 0, 所以 key = a[i]
    pq = [(a[i], i, 0) for i in range(n)]
    heapq.heapify(pq)
    
    # 进行 m 次操作，每次选出队列中 key 最小的元素
    for _ in range(m):
        key, idx, cnt = heapq.heappop(pq)
        cnt += 1           # 增加该位置的保留次数
        t[idx] = cnt       # 更新记录
        new_key = a[idx] + cnt * k  # 更新 key 值
        heapq.heappush(pq, (new_key, idx, cnt))
    
    # 输出最终结果，最终值为： a[i] - (m - t[i]) * k
    res = [str(a[i] - (m - t[i]) * k) for i in range(n)]
    sys.stdout.write(" ".join(res) + "\n")
```
## Java

```java
import java.io.*;
import java.util.*;
 
public class Main {
    // 节点类，存储 key, idx, t 值
    static class Node {
        long key; // key = a[i] + t[i] * k
        int idx;
        int t;
 
        public Node(long key, int idx, int t) {
            this.key = key;
            this.idx = idx;
            this.t = t;
        }
    }
 
    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 提高输入效率
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(new OutputStreamWriter(System.out));
        int T = Integer.parseInt(br.readLine());
 
        while (T-- > 0) {
            String[] params = br.readLine().split(" ");
            int n = Integer.parseInt(params[0]);
            int m = Integer.parseInt(params[1]);
            int k = Integer.parseInt(params[2]);
 
            long[] a = new long[n];
            String[] aStr = br.readLine().split(" ");
            for (int i = 0; i < n; i++) {
                a[i] = Long.parseLong(aStr[i]);
            }
 
            // 数组 t 存储每个位置的保留次数，初始为 0
            int[] tArr = new int[n];
 
            // 自定义小根堆，比较规则：先比较 key，再比较下标
            PriorityQueue<Node> pq = new PriorityQueue<>(new Comparator<Node>() {
                public int compare(Node o1, Node o2) {
                    if (o1.key == o2.key) return o1.idx - o2.idx;
                    return Long.compare(o1.key, o2.key);
                }
            });
 
            // 将所有元素插入优先队列，初始 key = a[i]
            for (int i = 0; i < n; i++) {
                pq.offer(new Node(a[i], i, 0));
            }
 
            // 进行 m 次操作，每一次弹出 key 最小的节点，更新其 t 后重新插入
            for (int op = 0; op < m; op++) {
                Node cur = pq.poll();
                cur.t++; // 增加保留次数
                tArr[cur.idx] = cur.t;
                cur.key = a[cur.idx] + (long)cur.t * k; // 更新 key
                pq.offer(cur);
            }
 
            // 根据公式输出最终结果： a[i] - (m - t[i]) * k
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) {
                long res = a[i] - (long)(m - tArr[i]) * k;
                sb.append(res).append(" ");
            }
            out.println(sb.toString().trim());
        }
        out.flush();
        out.close();
    }
}
```