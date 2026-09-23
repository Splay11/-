#include <iostream>
using namespace std;

int countTriples(int n) {
    int ans = 0;
    // 枚举非降的 x、y，由异或还原 z
    for (int x = 1; x <= n; ++x) {
        for (int y = x; y <= n; ++y) {
            int z = x ^ y;
            if (y <= z && z <= n && x + y > z) {
                ++ans;
            }
        }
    }
    return ans;
}

int main() {
    int n;
    cin >> n;
    cout << countTriples(n) << endl;
    return 0;
}
