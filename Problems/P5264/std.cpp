#include <cmath>
#include <iostream>
#include <vector>
using namespace std;

struct State {
    double mx, wd, sv;
};

State mergeState(const State& a, const State& b) {
    State c;
    c.mx = max(a.mx, b.mx);
    double ea = exp(a.mx - c.mx);
    double eb = exp(b.mx - c.mx);
    c.wd = a.wd * ea + b.wd * eb;
    c.sv = a.sv * ea + b.sv * eb;
    return c;
}

struct SegTree {
    int n, size;
    vector<State> tree;

    SegTree(const vector<State>& blocks) : n((int)blocks.size()) {
        size = 1;
        while (size < n) size <<= 1;
        tree.assign(2 * size, {0, 0, 0});
        for (int i = 0; i < n; i++) tree[size + i] = blocks[i];
        for (int i = size - 1; i >= 1; i--)
            tree[i] = mergeState(tree[i * 2], tree[i * 2 + 1]);
    }

    void update(int pos, const State& val) {
        int i = size + pos;
        tree[i] = val;
        for (i /= 2; i >= 1; i /= 2)
            tree[i] = mergeState(tree[i * 2], tree[i * 2 + 1]);
    }

    State query(int l, int r) {
        l += size;
        r += size;
        bool hasL = false, hasR = false;
        State left{}, right{};
        while (l <= r) {
            if (l & 1) {
                left = hasL ? mergeState(left, tree[l]) : tree[l];
                hasL = true;
                l++;
            }
            if (!(r & 1)) {
                right = hasR ? mergeState(tree[r], right) : tree[r];
                hasR = true;
                r--;
            }
            l /= 2;
            r /= 2;
        }
        if (!hasL) return right;
        if (!hasR) return left;
        return mergeState(left, right);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int B, Q;
    cin >> B >> Q;
    vector<State> blocks(B);
    for (int i = 0; i < B; i++) cin >> blocks[i].mx >> blocks[i].wd >> blocks[i].sv;
    SegTree seg(blocks);
    cout.setf(ios::fixed);
    cout.precision(6);
    for (int t = 0; t < Q; t++) {
        int op;
        cin >> op;
        if (op == 1) {
            int i;
            State st;
            cin >> i >> st.mx >> st.wd >> st.sv;
            seg.update(i - 1, st);
        } else {
            int l, r;
            cin >> l >> r;
            State res = seg.query(l - 1, r - 1);
            cout << res.sv / res.wd << '\n';
        }
    }
    return 0;
}
