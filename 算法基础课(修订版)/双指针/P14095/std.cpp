#include <bits/stdc++.h>
using namespace std;

int shortestAllLettersSubstring(const string& s) {
    // 记录每个字母出现的次数
    int count[26] = {0};
    int unique = 0; // 当前窗口中不同字母的数量
    int n = s.length();
    int min_len = n + 1;
    int left = 0;

    for(int right = 0; right < n; ++right){
        char c = s[right];
        if(c >= 'a' && c <= 'z'){
            if(count[c - 'a'] == 0){
                unique++;
            }
            count[c - 'a']++;
        }

        // 当窗口包含所有26个字母时，尝试收缩左边界
        while(unique == 26){
            // 更新最小长度
            min_len = min(min_len, right - left + 1);
            char cl = s[left];
            if(cl >= 'a' && cl <= 'z'){
                count[cl - 'a']--;
                if(count[cl - 'a'] == 0){
                    unique--;
                }
            }
            left++;
        }
    }

    return (min_len <= n) ? min_len : -1;
}

int main(){
    string s;
    // 读取输入字符串
    while(getline(cin, s)){
        if(s.empty()) continue;
        cout << shortestAllLettersSubstring(s) << endl;
    }
    return 0;
}
