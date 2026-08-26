## 题目思路

由题可知，每一种零件都必须选择一个，考虑深搜（dfs）枚举。

具体dfs实现：对于一种零件，循环遍历所有型号，如果说当前所剩下的钱足够买此型号，则递归对下一种零件；否则查看当前零件的下一个型号是否够钱买。如此递归，直到所有零件都被访问后记录最大性能；

注：在dfs之前，需要把ans初始化为-1，这样做的好处就是如果说没办法递归完所有的零件，则说明无法组装，即ans值不会变

## 代码

### C++

```c++
#include <algorithm>
#include <iostream>
using namespace std;
const int N = 50;
using ll = long long;
ll a[N][N], v[N][N], num[N], ans;
void dfs(int n, ll cost, ll vsum) {
    if (n == 0) { // 递归结束条件：遍历完了所有零件
        ans = max(ans, vsum); // 记录答案
        return;
    }
    for (int i = 1; i <= num[n]; ++i) {
        if (cost >= a[n][i]) { // 如果当前剩下的钱足够购买此型号
            dfs(n - 1, cost - a[n][i], vsum + v[n][i]); // 则递归下一个零件
        }
    }
}

int main() {
    int n, x;
    cin >> n >> x;
    for (int i = 1; i <= n; ++i) {
        int m;
        cin >> m;
        num[i] = m;  // 记录当前零件的个数
        for (int j = 1; j <= m; ++j) { // 记录价格
            cin >> a[i][j];
        }
        for (int j = 1; j <= m; ++j) { // 记录性能
            cin >> v[i][j];
        }
    }
    ans = -1; // 初始化为-1，若dfs不到完所有零件，则ans值不变
    dfs(n, x, 0); // 倒过来递归零件，方便处理
    cout << ans << endl;
    return 0;
}
```