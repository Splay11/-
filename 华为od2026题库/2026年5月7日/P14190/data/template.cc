#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string input((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
    vector<int> values;
    for (int i = 0; i < (int)input.size(); ++i) {
        if (isdigit((unsigned char)input[i])) {
            int value = 0;
            while (i < (int)input.size() && isdigit((unsigned char)input[i])) {
                value = value * 10 + (input[i] - '0');
                ++i;
            }
            values.push_back(value);
        }
    }
    if (values.empty()) return 0;

    int optimize = values.back();
    values.pop_back();
    vector<int> goodProceeTime = values;

    Solution solution;
    cout << solution.minProcessTime(goodProceeTime, optimize) << endl;
    return 0;
}
