#include <iostream>
#include <unordered_map>
using namespace std;

int main() {

	int n;
	cin >> n;
	unordered_map<int, int> counts;  // 哈希表，记录每个数字的出现次数

	for (int i = 1; i <= n; ++i) {
		int num;
		cin >> num;
		counts[num]++;  // 更新数字 num 的出现次数
		// 直接输出数字 i 在前缀 [a1, a2, ..., ai] 中的出现次数，用空格分隔
		if (i > 1)
			cout << ' ';
		cout << counts[i];

	}

	return 0;
}
