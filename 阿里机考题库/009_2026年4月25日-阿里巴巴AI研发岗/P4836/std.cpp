#include <bits/stdc++.h>
using namespace std;

string solveOne(int length, string tag) {
    // rightCnt 统计当前位右侧尚未处理的原标签字符数量
    vector<int> rightCnt(26, 0);
    for (char ch : tag) {
        rightCnt[ch - 'a']++;
    }

    // leftCnt 统计左侧已校正完成的最终字符数量
    vector<int> leftCnt(26, 0);

    string ans;

    for (char ch : tag) {
        int idx = ch - 'a';

        // 当前字符不再属于右侧，先从右侧计数中删去
        rightCnt[idx]--;

        // leftCnt：左侧最终字符中等于当前 glyph 的个数
        int leftCntVal = leftCnt[idx];

        // rightCnt：右侧原串中等于当前 glyph 的个数
        int rightCntVal = rightCnt[idx];

        int newIdx;

        // 两侧计数相等则轮询到下一个小写字母
        if (leftCntVal == rightCntVal) {
            newIdx = (idx + 1) % 26;
        } else {
            newIdx = idx;
        }

        ans.push_back(char('a' + newIdx));
        leftCnt[newIdx]++;
    }

    return ans;
}

int main() {
    int tc;
    cin >> tc;

    while (tc--) {
        int length;
        string tag;

        cin >> length;
        cin >> tag;

        cout << solveOne(length, tag) << '\n';
    }

    return 0;
}
