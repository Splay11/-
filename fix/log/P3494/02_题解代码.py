## 核心结论与思路

### 1) 什么时候能实现**任意排列**？

若能把任意一对**相邻**位置（共享边）完成交换，我们就能用相邻交换生成任意排列，从而把所有元素整体按降序放入矩阵（行优先）即为最优。

对一对相邻格子 $(x_1,y_1)$、$(x_2,y_2)$，若存在某个“缓冲格” $t$，使得 $t$ 与两者都**不相邻**，则用三步实现相邻交换：

$(x_1\!\leftrightarrow\! t),\ $
$(x_2\!\leftrightarrow\! t),\ $
$(x_1\!\leftrightarrow\! t)$

每一步均是允许的非相邻交换，合成效果等价于交换相邻二格。

什么时候对任意相邻对都能找到这样的 $t$？除以下**小棋盘**外都可以：

* $2\times 2$

因此，**只要棋盘不是上述四类**，就能达到任意排列 ⇒ 直接把所有数降序填回即可得到答案。
（例如 $2\times 3$、$3\times 3$……都可以。）

### 2) 小棋盘分类讨论

* **$2\times 2$**：只允许两条对角线交换：(1,1)↔(2,2) 或 (1,2)↔(2,1)。
  四种状态（不动 / 交换主对角 / 交换副对角 / 两条都换）里取字典序最大者。

### 3) 算法步骤

1. 读入 $n,m$ 与矩阵。
2. 若属于“可任意排列”的情况：把所有元素取出排序（降序），按行优先填回。
3. 否则按上节的小棋盘规则枚举有限方案，比较字典序取最大。
4. 输出矩阵。


### 4) 复杂度

* 大棋盘：排序 $O(N\log N)$，其中 $N=nm$（$nm\le 2.5\times10^5$），可行。
* 小棋盘：常数次比较与输出，$O(1)$。



## 代码

### Python

```python
import sys

def flat(mat):
    return [x for row in mat for x in row]

def lex_greater(a, b):
    # 比较一维序列字典序：a 是否更大
    for x, y in zip(a, b):
        if x != y:
            return x > y
    return False  # 完全相等则不更大

def solve():
    data = sys.stdin.read().strip().split()
    n, m = map(int, data[:2])
    arr = list(map(int, data[2:2+n*m]))
    A = [arr[i*m:(i+1)*m] for i in range(n)]

    def print_mat(M):
        out = []
        for r in M:
            out.append(" ".join(map(str, r)))
        sys.stdout.write("\n".join(out))

    # 判定是否为“任意排列”情形
    any_perm = True
    if (n == 2 and m == 2):
        any_perm = False

    if any_perm:
        b = sorted(arr, reverse=True)
        B = [b[i*m:(i+1)*m] for i in range(n)]
        print_mat(B)
        return

    # 小棋盘分类
    if n == 2 and m == 2:
        # 枚举四种
        a = [row[:] for row in A]
        cand = [flat(a)]
        b = [row[:] for row in A]
        b[0][0], b[1][1] = b[1][1], b[0][0]
        cand.append(flat(b))
        c = [row[:] for row in A]
        c[0][1], c[1][0] = c[1][0], c[0][1]
        cand.append(flat(c))
        d = [row[:] for row in b]  # 在 b 的基础上再交换副对角
        d[0][1], d[1][0] = d[1][0], d[0][1]
        cand.append(flat(d))
        best = cand[0]
        for s in cand[1:]:
            if lex_greater(s, best):
                best = s
        for i in range(n):
            print(" ".join(map(str, best[i*m:(i+1)*m])))
        return

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static boolean lexGreater(long[] a, long[] b) {
        for (int i = 0; i < a.length; i++) {
            if (a[i] != b[i]) return a[i] > b[i];
        }
        return false;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;
        st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        long[] arr = new long[n*m];
        int idx = 0;
        for (int i = 0; i < n; i++) {
            st = new StringTokenizer(br.readLine());
            for (int j = 0; j < m; j++) {
                arr[idx++] = Long.parseLong(st.nextToken());
            }
        }

        boolean anyPerm = true;
        if (n == 2 && m == 2)
            anyPerm = false;

        StringBuilder sb = new StringBuilder();
        if (anyPerm) {
            // 直接整体降序
            Long[] box = new Long[arr.length];
            for (int i = 0; i < arr.length; i++) box[i] = arr[i];
            Arrays.sort(box, Collections.reverseOrder());
            int p = 0;
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    if (j > 0) sb.append(' ');
                    sb.append(box[p++]);
                }
                if (i + 1 < n) sb.append('\n');
            }
            System.out.print(sb.toString());
            return;
        }

        // 2x2：枚举四种
        long[] a = arr.clone();                 // 原
        long[] b = arr.clone();                 // 交换主对角
        { int p00=0, p11=3; long t=b[p00]; b[p00]=b[p11]; b[p11]=t; }
        long[] c = arr.clone();                 // 交换副对角
        { int p01=1, p10=2; long t=c[p01]; c[p01]=c[p10]; c[p10]=t; }
        long[] d = b.clone();                   // 都交换
        { int p01=1, p10=2; long t=d[p01]; d[p01]=d[p10]; d[p10]=t; }

        long[][] all = new long[][]{a,b,c,d};
        long[] best = a;
        for (int i = 1; i < all.length; i++) if (lexGreater(all[i], best)) best = all[i];

        int p = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (j > 0) sb.append(' ');
                sb.append(best[p++]);
            }
            if (i + 1 < n) sb.append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
// C++17
#include <bits/stdc++.h>
using namespace std;

static bool lexGreater(const vector<long long>& a, const vector<long long>& b){
    for(size_t i=0;i<a.size();++i){
        if(a[i]!=b[i]) return a[i]>b[i];
    }
    return false;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n,m; 
    if(!(cin>>n>>m)) return 0;
    vector<long long> a(n*m);
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++){
            cin>>a[i*m+j];
        }
    }

    bool anyPerm = true;
    if(n==2 && m==2)
        anyPerm = false;

    if(anyPerm){
        // 直接整体降序
        vector<long long> b=a;
        sort(b.begin(), b.end(), greater<long long>());
        for(int i=0, p=0;i<n;i++){
            for(int j=0;j<m;j++,p++){
                if(j) cout<<' ';
                cout<<b[p];
            }
            if(i+1<n) cout<<"\n";
        }
        return 0;
    }

    // 2x2：枚举四种状态
    vector<long long> A=a;
    vector<long long> B=a; swap(B[0],B[3]); // 主对角
    vector<long long> C=a; swap(C[1],C[2]); // 副对角
    vector<long long> D=B; swap(D[1],D[2]); // 都交换
    vector<vector<long long>> cand={A,B,C,D};
    vector<long long> best=A;
    for(int i=1;i<4;i++) if(lexGreater(cand[i],best)) best=cand[i];

    for(int i=0,p=0;i<n;i++){
        for(int j=0;j<m;j++,p++){
            if(j) cout<<' ';
            cout<<best[p];
        }
        if(i+1<n) cout<<"\n";
    }
    return 0;
}
```