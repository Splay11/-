#include "foo.cc"
#include <iostream>
#include <string>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    // 解析三个逗号分隔的值：capacity,efficiency,scene
    int comma1 = line.find(',');
    double capacity = stod(line.substr(0, comma1));

    string rest1 = line.substr(comma1 + 1);
    int comma2 = rest1.find(',');
    double efficiency = stod(rest1.substr(0, comma2));

    int scene = stoi(rest1.substr(comma2 + 1));

    Solution solution;
    cout << solution.calculateRange(capacity, efficiency, scene) << endl;
    return 0;
}
