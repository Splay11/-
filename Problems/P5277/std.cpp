#include <algorithm>
#include <iostream>
#include <map>
#include <set>
#include <vector>
using namespace std;

using ll = long long;
multiset<ll> pos;
multiset<ll> gaps;

void add_gap(ll diff) {
  ll g = diff / 2;
  if (g > 0) gaps.insert(g);
}

void remove_gap(ll diff) {
  ll g = diff / 2;
  if (g > 0) {
    auto it = gaps.find(g);
    if (it != gaps.end()) gaps.erase(it);
  }
}

void insert_pos(ll y) {
  auto it = pos.lower_bound(y);
  ll pred = -1, succ = -1;
  if (it != pos.end()) succ = *it;
  if (it != pos.begin()) pred = *prev(it);
  if (pred != -1 && succ != -1) remove_gap(succ - pred);
  if (pred != -1) add_gap(y - pred);
  if (succ != -1) add_gap(succ - y);
  pos.insert(y);
}

void remove_pos(ll v) {
  auto it = pos.find(v);
  ll pred = -1, succ = -1;
  if (it != pos.begin()) pred = *prev(it);
  auto nit = next(it);
  if (nit != pos.end()) succ = *nit;
  if (pred != -1) remove_gap(v - pred);
  if (succ != -1) remove_gap(succ - v);
  if (pred != -1 && succ != -1) add_gap(succ - pred);
  pos.erase(it);
}

ll max_g() {
  return gaps.empty() ? 0 : *gaps.rbegin();
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<ll> b(n);
  for (int i = 0; i < n; i++) {
    cin >> b[i];
    pos.insert(b[i]);
  }
  vector<ll> sorted_vals;
  for (ll v : pos) sorted_vals.push_back(v);
  for (int i = 0; i < n - 1; i++) add_gap(sorted_vals[i + 1] - sorted_vals[i]);

  for (int i = 0; i < m; i++) {
    int x;
    ll y;
    cin >> x >> y;
    --x;
    ll old = b[x];
    if (old != y) {
      remove_pos(old);
      insert_pos(y);
      b[x] = y;
    }
    cout << max_g() << '\n';
  }
  return 0;
}
