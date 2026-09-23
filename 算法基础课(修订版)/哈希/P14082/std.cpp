#include <iostream>
#include <unordered_map>
using namespace std;

int main() {

    int n, Q;
    cin >> n >> Q;
    
    unordered_map<int, int> count_map;
    int num;
    
    // 统计每个数字出现的次数
    for(int i = 0; i < n; ++i){
        cin >> num;
        count_map[num]++;
    }
    
    // 处理每个查询
    for(int i = 0; i < Q; ++i){
        cin >> num;
        if(count_map.find(num) != count_map.end()){
            cout << count_map[num] << "\n";
        }
        else{
            cout << "0\n";
        }
    }
    
    return 0;
}
