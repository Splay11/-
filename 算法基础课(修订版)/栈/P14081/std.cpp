#include <bits/stdc++.h>
using namespace std;

int main(){
    // 读取输入
    vector<int> arr;
    int num;
    while(cin >> num){
        arr.push_back(num);
    }

    // 定义一个栈来存储元素
    stack<int> stk;

    for(auto &x : arr){
        stk.push(x);
        // 检查栈中是否有至少三个相同的连续元素
        if(stk.size() >= 3){
            int top1 = stk.top(); stk.pop();
            int top2 = stk.top(); stk.pop();
            int top3 = stk.top(); stk.pop();
            if(top1 == top2 && top2 == top3){
                // 三个相同，消除它们
                // 不需要将它们放回栈
            }
            else{
                // 不相同，将弹出的元素放回栈
                stk.push(top3);
                stk.push(top2);
                stk.push(top1);
            }
        }
    }

    // 构建结果数组
    vector<int> result;
    while(!stk.empty()){
        result.push_back(stk.top());
        stk.pop();
    }

    // 逆序结果以恢复原始顺序
    reverse(result.begin(), result.end());

    // 输出结果
    if(result.empty()){
        cout << "[]" << endl;
    }
    else{
        for(int i=0; i<result.size(); ++i){
            if(i > 0) cout << " ";
            cout << result[i];
        }
        cout << endl;
    }

    return 0;
}
