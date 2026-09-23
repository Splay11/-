#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// W 恒非负，最大约 4e19，超过 64 位；用 4 个 32 位肢存储，兼容无 __int128 的编译器
struct Big {
  unsigned d[4];
  Big() { memset(d, 0, sizeof d); }
  void add(ll v) {
    if (v >= 0) {
      unsigned long long x = (unsigned long long)v, c = 0;
      for (int i = 0; i < 4; i++) {
        c += d[i];
        if (i == 0) c += (unsigned)(x & 0xffffffffu);
        else if (i == 1) c += (unsigned)(x >> 32);
        d[i] = (unsigned)(c & 0xffffffffu);
        c >>= 32;
      }
    } else {
      unsigned long long x = (unsigned long long)(-v);
      long long b = 0;
      for (int i = 0; i < 4; i++) {
        long long cur = (long long)d[i] - b;
        if (i == 0) cur -= (long long)(x & 0xffffffffu);
        else if (i == 1) cur -= (long long)(x >> 32);
        if (cur < 0) {
          cur += (1LL << 32);
          b = 1;
        } else {
          b = 0;
        }
        d[i] = (unsigned)cur;
      }
    }
  }
  string str() const {
    unsigned t[4];
    memcpy(t, d, sizeof t);
    auto is0 = [&]() { return !(t[0] | t[1] | t[2] | t[3]); };
    if (is0()) return "0";
    string s;
    while (!is0()) {
      unsigned long long rem = 0;
      for (int i = 3; i >= 0; i--) {
        unsigned long long cur = (rem << 32) | t[i];
        t[i] = (unsigned)(cur / 10);
        rem = cur % 10;
      }
      s.push_back(char('0' + (int)rem));
    }
    reverse(s.begin(), s.end());
    return s;
  }
};

// 树状数组：下标从 1 开始，维护频次或数值和
struct BIT {
  int n;
  vector<ll> c;
  BIT(int n = 0) { init(n); }
  void init(int n_) {
    n = n_;
    c.assign(n + 1, 0);
  }
  void add(int i, ll v) {
    // 第 i 档加上 v，并沿树向上更新
    while (i <= n) {
      c[i] += v;
      i += i & -i;
    }
  }
  ll sum(int i) {
    // 前 i 档的和；i=0 时自然得到 0
    ll s = 0;
    while (i > 0) {
      s += c[i];
      i -= i & -i;
    }
    return s;
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int T;
  cin >> T;
  while (T--) {
    int n, m;
    cin >> n >> m;
    vector<ll> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<array<ll, 3>> ops(m);
    vector<ll> xs = a;
    for (int i = 0; i < m; i++) {
      int ty;
      cin >> ty;
      ops[i][0] = ty;
      if (ty == 1) {
        cin >> ops[i][1] >> ops[i][2];
        xs.push_back(ops[i][2]);  // 修改值也要参与离散化
      }
    }
    sort(xs.begin(), xs.end());
    xs.erase(unique(xs.begin(), xs.end()), xs.end());
    int sz = (int)xs.size();
    BIT cnt(sz), sm(sz);
    auto idx = [&](ll x) {
      return int(lower_bound(xs.begin(), xs.end(), x) - xs.begin()) + 1;
    };
    auto ins = [&](ll x) {
      int i = idx(x);
      cnt.add(i, 1);
      sm.add(i, x);
    };
    auto ers = [&](ll x) {
      int i = idx(x);
      cnt.add(i, -1);
      sm.add(i, -x);
    };
    auto pair_with = [&](ll x) {
      // 小于 x：个数*x - 和；大于 x：和 - 个数*x；相等贡献为 0
      int i = idx(x);
      ll cnt_lt = cnt.sum(i - 1), sum_lt = sm.sum(i - 1);
      ll cnt_le = cnt.sum(i), sum_le = sm.sum(i);
      ll cnt_all = cnt.sum(sz), sum_all = sm.sum(sz);
      ll cnt_gt = cnt_all - cnt_le, sum_gt = sum_all - sum_le;
      return cnt_lt * x - sum_lt + sum_gt - cnt_gt * x;
    };

    Big s;
    for (ll x : a) {
      // 先插入再累加，不会和自己配对
      ins(x);
      s.add(pair_with(x));
    }
    for (int i = 0; i < m; i++) {
      if (ops[i][0] == 2) {
        cout << s.str() << "\n";
      } else {
        int p = (int)ops[i][1] - 1;
        ll y = ops[i][2];
        ll old = a[p];
        // 树里还留着旧值时先扣贡献，再替换
        s.add(-pair_with(old));
        ers(old);
        a[p] = y;
        ins(y);
        s.add(pair_with(y));
      }
    }
  }
  return 0;
}
