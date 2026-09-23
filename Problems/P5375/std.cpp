#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;

const int MOD = 998244353;

int n;
vector<int> a, val, ln, pow3;

pair<int, int> encode(int x) {
    // 三进制去掉前导零后，先倒序再把 0 与 2 互换
    if (x == 0) {
        return make_pair(2, 1);
    }
    int v = 0;
    int len = 0;
    while (x > 0) {
        int d = x % 3;
        x /= 3;
        v = (int)((v * 3LL + (2 - d)) % MOD);
        len++;
    }
    return make_pair(v, len);
}

void pull(int p) {
    // 下标大的在高位：右儿子在前，左儿子在后
    int leftLen = ln[p * 2];
    ln[p] = leftLen + ln[p * 2 + 1];
    val[p] = (int)((val[p * 2 + 1] * 1LL * pow3[leftLen] + val[p * 2]) % MOD);
}

void build(int p, int l, int r) {
    if (l == r) {
        pair<int, int> e = encode(a[l]);
        val[p] = e.first;
        ln[p] = e.second;
        return;
    }
    int mid = (l + r) / 2;
    build(p * 2, l, mid);
    build(p * 2 + 1, mid + 1, r);
    pull(p);
}

void update(int p, int l, int r, int idx, int x) {
    if (l == r) {
        a[idx] = x;
        pair<int, int> e = encode(x);
        val[p] = e.first;
        ln[p] = e.second;
        return;
    }
    int mid = (l + r) / 2;
    if (idx <= mid) {
        update(p * 2, l, mid, idx, x);
    } else {
        update(p * 2 + 1, mid + 1, r, idx, x);
    }
    pull(p);
}

pair<int, int> query(int p, int l, int r, int ql, int qr) {
    // 返回 [ql,qr] 从右到左拼接后的 (值, 位数)
    if (ql <= l && r <= qr) {
        return make_pair(val[p], ln[p]);
    }
    int mid = (l + r) / 2;
    if (qr <= mid) {
        return query(p * 2, l, mid, ql, qr);
    }
    if (ql > mid) {
        return query(p * 2 + 1, mid + 1, r, ql, qr);
    }
    pair<int, int> L = query(p * 2, l, mid, ql, qr);
    pair<int, int> R = query(p * 2 + 1, mid + 1, r, ql, qr);
    int nv = (int)((R.first * 1LL * pow3[L.second] + L.first) % MOD);
    return make_pair(nv, L.second + R.second);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int q;
    cin >> n >> q;
    a.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    val.assign(n * 4 + 5, 0);
    ln.assign(n * 4 + 5, 0);
    int mx = 20 * n + 5;
    pow3.assign(mx, 0);
    pow3[0] = 1;
    for (int i = 1; i < mx; i++) {
        pow3[i] = (int)(pow3[i - 1] * 3LL % MOD);
    }
    build(1, 0, n - 1);
    for (int t = 0; t < q; t++) {
        int op;
        cin >> op;
        if (op == 1) {
            int l, r;
            cin >> l >> r;
            l--;
            r--;
            cout << query(1, 0, n - 1, l, r).first << "\n";
        } else {
            int idx, x;
            cin >> idx >> x;
            idx--;
            update(1, 0, n - 1, idx, x);
        }
    }
    return 0;
}
