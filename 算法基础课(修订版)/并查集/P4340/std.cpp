#include <bits/stdc++.h>
using namespace std;

// 并查集
struct DSU {
	vector<int> p, r;
	DSU(int n = 0) { init(n); }
	void init(int n) {
		p.resize(n);
		r.assign(n, 0);
		iota(p.begin(), p.end(), 0);
	}
	int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
	bool unite(int a, int b) {
		a = find(a); b = find(b);
		if (a == b) return false;
		if (r[a] < r[b]) swap(a, b);
		p[b] = a;
		if (r[a] == r[b]) r[a]++;
		return true;
	}
};

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T; 
	if (!(cin >> T)) return 0;
	while (T--) {
		int n; long long m;
		cin >> n >> m; // m 不直接使用
		vector<int> a(n), b(n);
		for (int i = 0; i < n; ++i) cin >> a[i];
		for (int i = 0; i < n; ++i) cin >> b[i];

		// 收集出现的所有值并排序去重（坐标压缩）
		vector<int> vals; 
		vals.reserve(2 * n);
		for (int i = 0; i < n; ++i) {
			vals.push_back(a[i]);
			vals.push_back(b[i]);
		}
		sort(vals.begin(), vals.end());
		vals.erase(unique(vals.begin(), vals.end()), vals.end());
		int K = (int)vals.size();

		// 将值映射到 0..K-1
		auto getId = [&](int x) {
			int idx = int(lower_bound(vals.begin(), vals.end(), x) - vals.begin());
			return idx;
		};

		// 并查集合并每条边 (a_i, b_i)
		DSU dsu(K);
		for (int i = 0; i < n; ++i) {
			int u = getId(a[i]);
			int v = getId(b[i]);
			dsu.unite(u, v);
		}

		// 统计连通块个数 C
		int C = 0;
		for (int i = 0; i < K; ++i) if (dsu.find(i) == i) ++C;

		// 答案 = K - C
		cout << (K - C) << '\n';
	}
	return 0;
}
