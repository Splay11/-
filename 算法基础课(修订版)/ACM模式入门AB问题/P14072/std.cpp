#include <iostream>
using namespace std;

int main() {
    long long num, sum = 0;
    while (cin >> num) {  // 只要能读取到数，就继续累加
        sum += num;
    }
    cout << sum << endl;  // 输出最终的和
    return 0;
}
