#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    int comma = line.find(',');
    int n = stoi(line.substr(0, comma));

    string rest = line.substr(comma + 1);
    vector<int> energies;

    // 解析 [a1,a2,...,an]
    int i = 0;
    while (i < (int)rest.size() && rest[i] != '[') i++;
    i++; // 跳过 '['
    string num;
    while (i < (int)rest.size()) {
        if (rest[i] == ',' || rest[i] == ']') {
            if (!num.empty()) {
                energies.push_back(stoi(num));
                num.clear();
            }
            if (rest[i] == ']') break;
        } else {
            num += rest[i];
        }
        i++;
    }

    Solution sol;
    vector<int> result = sol.energyCollision(energies);

    cout << '[';
    for (int j = 0; j < (int)result.size(); j++) {
        if (j > 0) cout << ',';
        cout << result[j];
    }
    cout << ']' << endl;

    return 0;
}
