#include <iostream>
#include <string>
#include <vector>
using namespace std;

const int MAXN = 200010;

int segSum[MAXN << 2], segMn[MAXN << 2], segMx[MAXN << 2], lazyFlip[MAXN << 2];
string w;

// 用孩子重算这一段的和、最小前缀、最大前缀
void pull(int p) {
    int left = p << 1, right = left | 1;
    segSum[p] = segSum[left] + segSum[right];
    segMn[p] = min(segMn[left], segSum[left] + segMn[right]);
    segMx[p] = max(segMx[left], segSum[left] + segMx[right]);
}

// 整段开合对调：和取反，最小前缀与最大前缀互换后再变号
void apply(int p) {
    segSum[p] = -segSum[p];
    int oldMn = segMn[p];
    segMn[p] = -segMx[p];
    segMx[p] = -oldMn;
    lazyFlip[p] ^= 1;
}

void push(int p) {
    if (lazyFlip[p]) {
        apply(p << 1);
        apply((p << 1) | 1);
        lazyFlip[p] = 0;
    }
}

void build(int p, int l, int r) {
    if (l == r) {
        int val = w[l - 1] == '[' ? 1 : -1;
        segSum[p] = segMn[p] = segMx[p] = val;
        return;
    }
    int mid = (l + r) >> 1;
    build(p << 1, l, mid);
    build((p << 1) | 1, mid + 1, r);
    pull(p);
}

void flip(int p, int l, int r, int a, int b) {
    if (a <= l && r <= b) {
        apply(p);
        return;
    }
    push(p);
    int mid = (l + r) >> 1;
    if (a <= mid) {
        flip(p << 1, l, mid, a, b);
    }
    if (b > mid) {
        flip((p << 1) | 1, mid + 1, r, a, b);
    }
    pull(p);
}

// 返回这一段的区间和、最小前缀和
pair<int, int> ask(int p, int l, int r, int a, int b) {
    if (a <= l && r <= b) {
        return {segSum[p], segMn[p]};
    }
    push(p);
    int mid = (l + r) >> 1;
    if (b <= mid) {
        return ask(p << 1, l, mid, a, b);
    }
    if (a > mid) {
        return ask((p << 1) | 1, mid + 1, r, a, b);
    }
    pair<int, int> L = ask(p << 1, l, mid, a, b);
    pair<int, int> R = ask((p << 1) | 1, mid + 1, r, a, b);
    return {L.first + R.first, min(L.second, L.first + R.second)};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, t;
    cin >> m >> t >> w;
    build(1, 1, m);
    for (int i = 0; i < t; i++) {
        int op, a, b;
        cin >> op >> a >> b;
        if (op == 1) {
            flip(1, 1, m, a, b);
        } else {
            pair<int, int> res = ask(1, 1, m, a, b);
            // 和为 0 且最小前缀不小于 0，这一段才配平
            cout << (res.first == 0 && res.second >= 0 ? 1 : 0) << '\n';
        }
    }
    return 0;
}
