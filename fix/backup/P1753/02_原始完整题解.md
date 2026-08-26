## 题解

将每个人需要领取礼物的次数预处理出来后，用次数 $cnt$ 做第一关键字，下标 $idx$ 做第二关键字从小到大排序，排序完成后所得的顺序就是离开队伍的顺序。

时间复杂度 $O(n \log n)$

## AC代码

- Cpp

```cpp
#include<bits/stdc++.h>

using namespace std;


int main (){
    ios::sync_with_stdio(false);
    std::cin.tie(0);
    int n, m; cin >> n >> m;
    vector<int> a(n);
    vector<pair<int, int>> ans;

    for(int i = 0; i < n; i ++)
    {
        cin >> a[i];
        ans.push_back({(a[i] + m - 1) / m, i + 1});
    }
    sort(ans.begin(), ans.end());
    for(auto i : ans)
        cout << i.second << " ";
    return 0;
}
```