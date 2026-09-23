#include <bits/stdc++.h>
using namespace std;

vector<array<int, 2>> child;

// 将一个读数插入二进制字典树
void insertNumber(int x) {
    int node = 0;

    for (int b = 30; b >= 0; b--) {
        int bit = (x >> b) & 1;

        if (child[node][bit] == -1) {
            child[node][bit] = (int)child.size();
            child.push_back({-1, -1});
        }

        node = child[node][bit];
    }
}

// 查询与 x 异或能得到的最大值
int queryMaxXor(int x) {
    int node = 0;
    int res = 0;

    for (int b = 30; b >= 0; b--) {
        int bit = (x >> b) & 1;
        int want = bit ^ 1;

        // 优先走相反位，使当前位异或结果为 1
        if (child[node][want] != -1) {
            res |= 1 << b;
            node = child[node][want];
        } else {
            node = child[node][bit];
        }
    }

    return res;
}

// 计算每个位置是否可行
string solveArray(vector<int>& v) {
    int n = (int)v.size();
    int M = *max_element(v.begin(), v.end());  // 序列最大值

    child.clear();
    child.push_back({-1, -1});

    string ans(n, '0');

    // 从右往左维护后缀字典树
    for (int i = n - 1; i >= 0; i--) {
        if (i < n - 1) {
            int best = queryMaxXor(v[i]);
            if (best >= M) {
                ans[i] = '1';
            }
        }

        // 当前读数插入，供左侧位置查询
        insertNumber(v[i]);
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i];
    }

    cout << solveArray(v) << '\n';

    return 0;
}
