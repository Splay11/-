## 思路

根据满二叉树的定义：左右儿子是相同高度的满二叉树 或者 叶子节点。

状态:定义 $dp[i]$ 代表以$i$为根的子树是多少高度的满二叉树.(不是满二叉树时$dp[i] = 0$).

转移:
$$
\large dp[i] =\left\{\begin{matrix}
  1&  i 是叶子节点\\
  dp[l] + 1 & dp[l] \neq 0 \wedge dp[r] \neq 0 \wedge dp[l] =dp[r] \wedge dp[l] \neq 0\\
  0 & others
\end{matrix}\right.
$$
$top-down$地求一遍$dp$值即可。最后答案为
$$
ans = \large \sum_{i=1}^{n} [dp[i] \neq 0]
$$
注意，题目没有规定根。所以需要在读图的时候统计一下入度。接着寻找入度为0的点来当作根.

## 代码

### C++

```C++
#include <bits/stdc++.h>
using namespace std;
const int maxn = 2e5 + 5;
int e[maxn][2] , d[maxn] , dp[maxn];
void dfs (int u){
    // l , r为左右儿子节点
    int l = e[u][0];
    int r = e[u][1];
    // 转移case 1,也是边界条件
    if (l == -1 && r == -1) {
        dp[u] = 1;
        return;
    }
    if (l != -1) dfs(l);
    if (r != -1) dfs(r);
    // 转移case 2
    if (l != -1 && r != -1 && dp[l] == dp[r] && dp[l] != 0) dp[u] = dp[l] + 1;
    // 转移case 3
    else dp[u] = 0;
}
int main() {
    int n;
    cin >> n;
    // 读入图
    for (int i = 1 ; i <= n ; i++){
        cin >> e[i][0] >> e[i][1];
        // d用来记录度数
        if (e[i][0] != -1) d[e[i][0]]++;
        if (e[i][1] != -1) d[e[i][1]]++;
    }
    // 寻找根
    int rt = -1;
    for (int i = 1 ; i <= n ; i++)
        if (d[i] == 0)
            rt = i;
   	// 从根开始dfs
    dfs(rt);
    // 求答案
    int ans = 0;
    for (int i = 1 ; i <= n ; i++)
        ans += (dp[i] != 0);
    cout << ans << endl;
	return 0;
}

```

js

```js
#include<bits/stdc++.h>
using namespace std;

void dfs(vector<int>& dp, int node, vector<vector<int>>& child) {
    int left = child[node][0];
    int right = child[node][1];
    if (left == -1 && right == -1) {
        dp[node] = 1;
        return;
    } 
    if (left != -1) dfs(dp, left, child);
    if (right != -1) dfs(dp, right, child);
    if ((right != -1 && left != -1) && (dp[right] == dp[left]) && dp[right] != 0) {
        dp[node] = dp[left] + 1;
    } else {
        dp[node] = 0;
    }

}

int main() {
    int n;
    cin >> n;
    vector<int> in_du(n+1, 0);
    vector<int> dp(n+1, 0);
    vector<vector<int>> child(n+1, vector<int>(2));
    for (int i = 1; i <= n; i++) {
        int left, right;
        cin >> left >> right;
        if (left != -1)
            in_du[left]++;
        if (right != -1)
            in_du[right]++;
        child[i][0] = left;
        child[i][1] = right;
    }
    int root;
    for (int i = 1; i <= n; i++) {
        if (in_du[i] == 0) {
            root = i;
            break;
        }
    }
    dfs(dp, root, child);
    int ans =  0;
    for(int i = 1; i <= n; i++) {
        if (dp[i] != 0) ans++;
        // cout << i <<' ' << dp[i] << endl;
    }
    cout << ans;
}
```

java

```java
import java.util.Scanner;

class TreeNode{
    int val;
    TreeNode left;
    TreeNode right;
}

public class Main {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        TreeNode[] nodes = new TreeNode[n];
        for(int i=0;i<n;i++) nodes[i] = new TreeNode();
        for(int i=0;i<n;i++){
            int l = in.nextInt();
            int r = in.nextInt();
            if(l!=-1) nodes[i].left = nodes[l-1];
            if(r!=-1) nodes[i].right = nodes[r-1];
        }
        int result = 0;
        for(int i=0;i<n;i++){
            if(isFull(nodes[i])) result++;
        }
        System.out.println(result);
    }

    public static boolean isFull(TreeNode tree){
        if(tree==null) return true;
        TreeNode p = tree;
        int l =0;
        while (p!=null){
            l++;
            p = p.left;
        }
        int r = 0;
        p = tree;
        while (p!=null){
            r++;
            p = p.right;
        }
        return l==r && isFull(tree.left) && isFull(tree.right);
    }
}
```