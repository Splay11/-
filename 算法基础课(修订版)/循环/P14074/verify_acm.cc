#include <iostream>
using namespace std;

class Solution {
public:
    int solve(int n) {
        int count = 0;
        for (int i = 1; i <= n; ++i) {
            int sumOfDigits = 0;
            int num = i;
            while (num > 0) {
                sumOfDigits += num % 10;
                num /= 10;
            }
            if (sumOfDigits % 10 == i % 10) {
                ++count;
            }
        }
        return count;
    }
};

int main() {
    int n;
    cin >> n;

    Solution solution;
    cout << solution.solve(n) << endl;

    return 0;
}
