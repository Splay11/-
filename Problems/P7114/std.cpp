#include <iostream>
using namespace std;

// Bash 博弈：n 能被 k+1 整除则后手胜，否则先手胜
string who_wins(long long n, long long k) {
    // 每 k+1 颗构成一轮：先手若面对 k+1 的倍数，无论取 1~k 颗，
    // 后手都能取到刚好补成 k+1，把倍数局面丢回给先手
    if (n % (k + 1) == 0) {
        return "后手";
    }
    return "先手";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n, k;
    cin >> n >> k;
    cout << who_wins(n, k) << "\n";
    return 0;
}
