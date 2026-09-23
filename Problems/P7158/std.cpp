#include <iostream>
#include <vector>
using namespace std;

// 从两端拿 k 张 = 中间留下连续 n-k 张；留下段越小，拿走的点数越大
int solve(const vector<int>& cards, int k) {
    int n = (int)cards.size();
    long long total = 0;
    for (int i = 0; i < n; i++) {
        total += cards[i];
    }
    int leave = n - k;
    // 必须拿完全部牌时，中间不留牌
    if (leave == 0) {
        return (int)total;
    }
    long long window = 0;
    for (int i = 0; i < leave; i++) {
        window += cards[i];
    }
    long long best = window;
    for (int i = leave; i < n; i++) {
        window += cards[i] - cards[i - leave];
        if (window < best) {
            best = window;
        }
    }
    return (int)(total - best);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> cards(n);
    for (int i = 0; i < n; i++) {
        cin >> cards[i];
    }
    cout << solve(cards, k) << '\n';
    return 0;
}
