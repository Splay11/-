#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 定义活动的结构体
struct Activity {
    int start;
    int end;
};

// 比较函数，用于按照活动的结束时间排序
bool compare(Activity a, Activity b) {
    return a.end < b.end;
}

// 计算最多可以选择的活动数
int maxActivities(int n, vector<Activity>& activities) {
    // 1. 按照活动的结束时间排序
    sort(activities.begin(), activities.end(), compare);

    // 2. 初始化选中的活动数量和上一个活动的结束时间
    int count = 0;
    int last_end_time = -1;

    // 3. 遍历所有活动，选择不与前一个活动重叠的活动
    for (int i = 0; i < n; ++i) {
        if (activities[i].start > last_end_time) {  // 当前活动开始时间大于上一个活动结束时间
            count++;
            last_end_time = activities[i].end;  // 更新上一个活动的结束时间为当前活动的结束时间
        }
    }

    return count;
}

int main() {
    int n;
    cin >> n;  // 输入活动数量
    vector<Activity> activities(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> activities[i].start >> activities[i].end;  // 输入每个活动的开始时间和结束时间
    }
    
    // 输出最多可以选择的活动数
    cout << maxActivities(n, activities) << endl;

    return 0;
}
