#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

// 常量定义
const int MOD = 1e9 + 7;

// 树状数组（Fenwick Tree）结构
struct BIT {
    int size;
    vector<ll> tree;

    BIT(int n) : size(n), tree(n + 1, 0) {}

    // 在索引x处增加value
    void add(int x, ll value) {
        while (x <= size) {
            tree[x] = (tree[x] + value) % MOD;
            x += x & -x;
        }
    }

    // 查询前缀和 [1, x]
    ll query(int x) const {
        ll res = 0;
        while (x > 0) {
            res = (res + tree[x]) % MOD;
            x -= x & -x;
        }
        return res;
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);

    int n;
    cin >> n;
    vector<int> a(n);
    vector<int> alls;
    alls.reserve(n);

    // 读取数组并收集所有元素用于离散化
    for(int &x : a){
        cin >> x;
        alls.push_back(x);
    }

    // 离散化：排序并去重
    sort(alls.begin(), alls.end(), greater<int>()); // 降序排序
    alls.erase(unique(alls.begin(), alls.end()), alls.end());

    // 树状数组的大小为离散化后的唯一元素个数
    int size = alls.size();
    BIT bit(size);

    ll ans = 0;

    // 遍历数组中的每个元素
    for(int i = 0; i < n; ++i){
        // 在降序排序的alls中找到a[i]的索引（1-based）
        int id = lower_bound(alls.begin(), alls.end(), a[i], greater<int>()) - alls.begin() + 1;

        // 查询比a[i]大的所有元素对应的子序列数之和
        ll sum = bit.query(id - 1); // 因为alls是降序，所以id-1之前的元素都大于a[i]

        // 当前元素自身也可以作为一个子序列
        ll res = (sum + 1) % MOD;

        // 累加到答案中
        ans = (ans + res) % MOD;

        // 更新树状数组
        bit.add(id, res);
    }

    cout << ans;
    return 0;
}
