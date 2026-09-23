#include <iostream>
#include <vector>
using namespace std;

const int MAX = 1001; // 根据题目数据范围定义最大节点数
vector<int> adj[MAX];  // 定义邻接表
bool visited[MAX];     // 访问标记数组

// DFS 函数（递归实现）
void DFS(int node) {
	visited[node] = true;
	for(auto neighbor : adj[node]){
		if(!visited[neighbor]){
			DFS(neighbor);
		}
	}
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	
	int n, m;
	cin >> n >> m;
	
	// 初始化访问标记数组
	for(int i = 1; i <= n; ++i){
		visited[i] = false;
	}
	
	// 读取边并构建邻接表
	for(int i = 0; i < m; ++i){
		int u, v;
		cin >> u >> v;
		if(u != v){ // 忽略自环
			adj[u].push_back(v);
			adj[v].push_back(u);
		}
	}
	
	int count = 0;
	
	// 遍历所有节点，进行 DFS
	for(int i = 1; i <= n; ++i){
		if(!visited[i]){
			DFS(i);
			count++;
		}
	}
	
	cout << count;
	
	return 0;
}
