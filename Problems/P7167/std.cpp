#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

// 回答 x 表示该颜色一共 x+1 只；同回答尽量塞进同一颜色组
int solve(const vector<int>& answers) {
    unordered_map<int, int> cnt;
    for (int i = 0; i < (int)answers.size(); i++) {
        cnt[answers[i]]++;
    }
    int ans = 0;
    for (unordered_map<int, int>::iterator it = cnt.begin(); it != cnt.end(); ++it) {
        int x = it->first;
        int c = it->second;
        int size = x + 1;
        int groups = (c + size - 1) / size;
        ans += groups * size;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> answers(n);
    for (int i = 0; i < n; i++) {
        cin >> answers[i];
    }
    cout << solve(answers) << '\n';
    return 0;
}
