#include <bits/stdc++.h>
using namespace std;

int main() {
	int a, b;
	cin >> a >> b;
	
	// 如果b小于1，直接输出-1
	if (b < 1) {
		cout << -1;
		return 0;
	}
	
	// 定义一个数组来记录访问状态，范围到10^6
	vector<int> visited(1000001, -1);
	queue<int> q;
	
	// 从1开始
	q.push(1);
	visited[1] = 0;
	
	while (!q.empty()) {
		int current = q.front();
		q.pop();
		
		// 如果到达目标，输出结果
		if (current == b) {
			cout << visited[current];
			return 0;
		}
		
		// 第一种魔法：乘以a
		long long next1 = (long long)current * a;
		if (next1 <= 1000000 && visited[next1] == -1) {
			visited[next1] = visited[current] + 1;
			q.push(next1);
		}
		
		// 第二种魔法：循环右移一次
		// 只有当当前数字 >=10 且最后一位不为0时才可以旋转
		if (current >= 10 && current % 10 != 0) {
			string s = to_string(current);
			// 循环右移一次
			string rotated = to_string(current);
			rotated = rotated.substr(rotated.size() - 1) + rotated.substr(0, rotated.size() - 1);
			// 转换回整数
			int next2 = stoi(rotated);
			if (next2 <= 1000000 && visited[next2] == -1) {
				visited[next2] = visited[current] + 1;
				q.push(next2);
			}
		}
	}
	
	// 如果无法到达目标，输出-1
	cout << -1;
	return 0;
}
