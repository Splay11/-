#include <algorithm>
#include <iostream>
#include <string>
using namespace std;

const string WAN = "123456789";
const string TONG = "abcdefghi";
const string TIAO = "ABCDEFGHI";
const string ALL = "123456789abcdefghiABCDEFGHI";

int suit_of(char ch) {
    if (WAN.find(ch) != string::npos) {
        return 0;
    }
    if (TONG.find(ch) != string::npos) {
        return 1;
    }
    return 2;
}

char next_in_suit(char ch, int step) {
    // 同一门里往后数 step 张，跨出门就没有顺子
    const string* groups[3] = {&WAN, &TONG, &TIAO};
    for (int g = 0; g < 3; g++) {
        int pos = (int)groups[g]->find(ch);
        if (pos != (int)string::npos) {
            int nxt = pos + step;
            if (nxt >= 0 && nxt < 9) {
                return (*groups[g])[nxt];
            }
            return 0;
        }
    }
    return 0;
}

int suit_count(int cnt[]) {
    // 统计手里实际出现了几门花色
    int used[3] = {0, 0, 0};
    for (int i = 0; i < (int)ALL.size(); i++) {
        char ch = ALL[i];
        if (cnt[(int)ch] > 0) {
            used[suit_of(ch)] = 1;
        }
    }
    return used[0] + used[1] + used[2];
}

bool try_melds(int cnt[]) {
    // 把剩下的牌拆成若干顺子或刻子，必须拆空
    char first = 0;
    for (int i = 0; i < (int)ALL.size(); i++) {
        if (cnt[(int)ALL[i]] > 0) {
            first = ALL[i];
            break;
        }
    }
    if (first == 0) {
        return true;
    }
    int f = (int)first;
    // 先试刻子：三张相同
    if (cnt[f] >= 3) {
        cnt[f] -= 3;
        if (try_melds(cnt)) {
            cnt[f] += 3;
            return true;
        }
        cnt[f] += 3;
    }
    // 再试顺子：同一门连续三张
    char a = next_in_suit(first, 1);
    char b = next_in_suit(first, 2);
    if (a != 0 && b != 0 && cnt[(int)a] > 0 && cnt[(int)b] > 0) {
        cnt[f]--;
        cnt[(int)a]--;
        cnt[(int)b]--;
        if (try_melds(cnt)) {
            cnt[f]++;
            cnt[(int)a]++;
            cnt[(int)b]++;
            return true;
        }
        cnt[f]++;
        cnt[(int)a]++;
        cnt[(int)b]++;
    }
    return false;
}

bool can_hu(int cnt[]) {
    // 14 张、缺一门，并且能拆成 k 组面子加一对将
    int tot = 0;
    for (int i = 0; i < (int)ALL.size(); i++) {
        tot += cnt[(int)ALL[i]];
    }
    if (tot != 14) {
        return false;
    }
    int sc = suit_count(cnt);
    if (sc < 1 || sc > 2) {
        return false;
    }
    for (int i = 0; i < (int)ALL.size(); i++) {
        int t = (int)ALL[i];
        if (cnt[t] >= 2) {
            cnt[t] -= 2;
            bool ok = try_melds(cnt);
            cnt[t] += 2;
            if (ok) {
                return true;
            }
        }
    }
    return false;
}

string winning_tiles(const string& hand) {
    // 枚举所有还能再摸的牌面，收集能胡的那些
    int cnt[128] = {0};
    for (int i = 0; i < (int)hand.size(); i++) {
        cnt[(int)hand[i]]++;
    }
    string ans = "";
    for (int i = 0; i < (int)ALL.size(); i++) {
        int t = (int)ALL[i];
        if (cnt[t] >= 4) {
            continue;
        }
        cnt[t]++;
        if (can_hu(cnt)) {
            ans.push_back(ALL[i]);
        }
        cnt[t]--;
    }
    if (ans.empty()) {
        return "-1";
    }
    // 题面要求按 ASCII 从小到大输出
    sort(ans.begin(), ans.end());
    return ans;
}

int main() {
    string s;
    cin >> s;
    cout << winning_tiles(s) << endl;
    return 0;
}
