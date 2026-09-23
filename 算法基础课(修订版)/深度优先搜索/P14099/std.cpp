#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

#define MAX 100005 // 假设最大节点数为10^5

vector<int> adjList[MAX]; // 邻接表
vector<int> traversalResult; // 存储先序遍历结果

// DFS的递归实现
void DFS(int node, int parent) {
	traversalResult.push_back(node); // 访问当前节点
	for(auto &child : adjList[node]) {
		if(child != parent) { // 避免回到父节点
			DFS(child, node); // 递归访问子节点
		}
	}
}

int main(){
	
	int n, type;
	cin >> n >> type; // 读取节点数和表示方式
	
	if(type == 1){
		// 方式一：通过边的形式输入
		for(int i = 0; i < n-1; i++){
			int u, v;
			cin >> u >> v;
			adjList[u].push_back(v); // 添加子节点
			adjList[v].push_back(u); // 添加父节点（无向树）
		}
	}
	else if(type == 2){
		// 方式二：通过father数组输入
		// father[1] = 0，表示根节点
		vector<int> father(n+1);
		for(int i = 1; i <= n; i++){
			cin >> father[i];
			if(father[i] != 0){
				adjList[father[i]].push_back(i); // 添加子节点
				adjList[i].push_back(father[i]); // 添加父节点
			}
		}
	}
	
	// 为了保证遍历顺序的一致性，先对每个节点的子节点进行排序
	for(int i = 1; i <= n; i++){
		sort(adjList[i].begin(), adjList[i].end());
	}
	
	// 执行DFS，根节点为1，父节点为0（无）
	DFS(1, 0);
	
	// 输出遍历结果
	for(int i = 0; i < traversalResult.size(); i++){
		if(i > 0) cout << ' ';
		cout << traversalResult[i];
	}
	
	return 0;
}
