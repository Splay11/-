#include <bits/stdc++.h>
using namespace std;

// 计算 c 取 2 和 取 3 的组合数，c < k 时返回 0
static inline unsigned long long C2(unsigned long long c) {
	return (c >= 2) ? (c * (c - 1) / 2) : 0ULL;
}
static inline unsigned long long C3(unsigned long long c) {
	return (c >= 3) ? (c * (c - 1) * (c - 2) / 6) : 0ULL;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int n;
	if (!(cin >> n)) return 0;
	unordered_map<long long, int> freq;
	freq.reserve(n * 2);
	for (int i = 0; i < n; ++i) {
		long long x;
		cin >> x;
		++freq[x];
	}

	// 统计所有种类的频次
	vector<unsigned long long> counts;
	counts.reserve(freq.size());
	for (auto &kv : freq) counts.push_back((unsigned long long)kv.second);

	// 计算 S2, S3 及自项之和
	unsigned long long S2 = 0, S3 = 0;
	unsigned long long selfSum = 0; // sum C(ni,3) * C(ni,2)
	for (auto c : counts) {
		unsigned long long c2 = C2(c);
		unsigned long long c3 = C3(c);
		S2 += c2;
		S3 += c3;
		// 使用 128 位避免中间乘法溢出
		__int128 tmp = (__int128)c2 * (__int128)c3;
		selfSum += (unsigned long long)tmp;
	}

	// 答案 = S3 * S2 - 自项之和
	__int128 ans128 = (__int128)S3 * (__int128)S2 - (__int128)selfSum;
	unsigned long long ans = (unsigned long long)ans128;
	cout << ans << '\n';
	return 0;
}
