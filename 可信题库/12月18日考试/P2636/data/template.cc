#include "foo.cc"
#include <iostream>
using namespace std;
int main() {
    Solution s;
    string str;
    getline(cin, str);

    // 解析输入数据，去掉空格和多余的符号
    //str = str.substr(1, str.length() - 2); // 去掉开头的 '[' 和结尾的 ']'
    
    vector<InvokeInfo> invokes;
    stringstream ss(str);
    string temp;
    
    while (getline(ss, temp, ']')) {
        if (temp.empty()) continue;
        // 去掉每个元素的 '['
        size_t pos1 = temp.find('[');
        if (pos1 != string::npos) {
            temp = temp.substr(pos1 + 1);
            stringstream pairStream(temp);
            int time, interfaceId;
            char comma;
            pairStream >> time >> comma >> interfaceId;  // 按照 time, interfaceId 读取数据
            invokes.push_back(InvokeInfo(interfaceId, time));
        }
    }


    int timeSegment, minLimits;
    cin >> timeSegment >> minLimits;
   auto c=s.getInterfaces(invokes, timeSegment, minLimits);
   cout<<'[';
    for(int i=0;i<c.size();i++){
        if(i!=0)cout<<", ";
        cout<<c[i];
    }
   cout<<']';
    return 0;
}