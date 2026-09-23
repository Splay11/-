#include <iostream>
#include <vector>
using namespace std;

int findRoot(vector<int>& parent, vector<long long>& delta, int x) {
    // 找到根，并把途中点的差额改成相对根：delta[x] = 付款[x] - 付款[根]
    if (parent[x] != x) {
        int root = findRoot(parent, delta, parent[x]);
        delta[x] += delta[parent[x]];
        parent[x] = root;
        return root;
    }
    return x;
}

void process(int n, int k, const vector<int>& floorOf,
             const vector<int>& qa, const vector<int>& qb, const vector<long long>& qx,
             int& invalid, int& circles) {
    vector<int> parent(n + 1);
    // delta[x]：x 比当前父亲多付的钱；路径压缩后变成比根多付的钱
    vector<long long> delta(n + 1, 0);
    vector<int> sz(n + 1, 1);
    for (int i = 1; i <= n; i++) {
        parent[i] = i;
    }
    invalid = 0;
    int q = (int)qa.size();
    for (int i = 0; i < q; i++) {
        int a = qa[i];
        int b = qb[i];
        long long x = qx[i];
        // 自己跟自己比，差额只能是 0
        if (a == b) {
            if (x != 0) {
                invalid++;
            }
            continue;
        }
        int ra = findRoot(parent, delta, a);
        int rb = findRoot(parent, delta, b);
        if (ra == rb) {
            // 两人已在同一圈：推出的差额必须正好是 x
            if (delta[a] - delta[b] != x) {
                invalid++;
            }
            continue;
        }
        // 不同圈：楼层不同或合并后人数超 K，本条作废
        if (floorOf[a] != floorOf[b] || sz[ra] + sz[rb] > k) {
            invalid++;
            continue;
        }
        // 记下 pay[a] - pay[b] = x，小圈挂到大圈下面
        if (sz[ra] < sz[rb]) {
            parent[ra] = rb;
            delta[ra] = x - delta[a] + delta[b];
            sz[rb] += sz[ra];
        } else {
            parent[rb] = ra;
            delta[rb] = delta[a] - delta[b] - x;
            sz[ra] += sz[rb];
        }
    }
    circles = 0;
    for (int i = 1; i <= n; i++) {
        if (parent[i] == i) {
            circles++;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 第一行 n、发言数 q、人数上限 K
    int n, q, k;
    cin >> n >> q >> k;
    vector<int> floorOf(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> floorOf[i];
    }
    vector<int> qa(q), qb(q);
    vector<long long> qx(q);
    for (int i = 0; i < q; i++) {
        cin >> qa[i] >> qb[i] >> qx[i];
    }
    int invalid = 0;
    int circles = 0;
    process(n, k, floorOf, qa, qb, qx, invalid, circles);
    cout << invalid << "\n" << circles << "\n";
    return 0;
}
