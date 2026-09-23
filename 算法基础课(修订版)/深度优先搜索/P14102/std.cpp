#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void dfs_permutations(vector<int>& nums, vector<int>& path, vector<bool>& visited, vector<vector<int>>& result) {
	if (path.size() == nums.size()) {
		result.push_back(path); // 将当前路径加入结果
		return;
	}
	
	for (int i = 0; i < nums.size(); i++) {
		if (!visited[i]) { // 如果当前数字未被访问
			visited[i] = true; // 标记为已访问
			path.push_back(nums[i]); // 加入路径
			dfs_permutations(nums, path, visited, result); // 递归调用
			path.pop_back(); // 回溯，移除路径中的最后一个数字
			visited[i] = false; // 恢复标记为未访问
		}
	}
}

int main() {
	int n;
	cin >> n;
	
	vector<int> nums(n);
	for (int i = 0; i < n; i++) {
		cin >> nums[i];
	}
	
	// 按字典序排序
	sort(nums.begin(), nums.end());
	
	vector<vector<int>> result; // 存储所有排列
	vector<int> path;           // 当前路径
	vector<bool> visited(n, false); // 标记每个数字是否被访问
	
	// 调用 DFS
	dfs_permutations(nums, path, visited, result);
	
	// 按字典序输出结果
	for (const auto& permutation : result) {
		for (int i = 0; i < permutation.size(); i++) {
			if (i > 0) cout << " ";
			cout << permutation[i];
		}
		cout << endl;
	}
	
	return 0;
}
