#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

// 全局变量存储任务冲突信息
int jobNum;
ll executionTime[30];
ll conflict[30];
ll maxCount = 0;
ll minTotalTime = LLONG_MAX;

// DFS函数
void dfs(int index, ll currentMask, ll count, ll totalTime) {
    // 更新全局最优解
    if (count > maxCount || (count == maxCount && totalTime < minTotalTime)) {
        maxCount = count;
        minTotalTime = totalTime;
    }

    // 逐个尝试添加任务
    for (int i = index; i < jobNum; ++i) {
        // 检查任务i是否与当前任务组冲突
        if (!(currentMask & (1LL << i))) {
            // 检查任务i是否与已选任务冲突
            if ((conflict[i] & currentMask) == 0) {
                // 选择任务i
                dfs(i + 1, currentMask | (1LL << i), count + 1, totalTime + executionTime[i]);
            }
        }
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    // 输入任务数量
    cin >> jobNum;
    // 输入每个任务的执行时间
    for(int i = 0; i < jobNum; ++i){
        cin >> executionTime[i];
    }
    // 初始化冲突数组
    for(int i = 0; i < jobNum; ++i){
        conflict[i] = 0;
    }
    // 输入不亲和关系的数量
    int mutexNum;
    cin >> mutexNum;
    for(int i = 0; i < mutexNum; ++i){
        int u, v;
        cin >> u >> v;
        --u; --v; // 转换为0基索引
        conflict[u] |= (1LL << v);
        conflict[v] |= (1LL << u);
    }
    
    // 开始DFS
    dfs(0, 0, 0, 0);
    
    // 输出结果
    cout << minTotalTime;
    return 0;
}
