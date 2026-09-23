#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

static void printFiles(const vector<vector<int>>& a) {
    cout << '[';
    for (size_t i = 0; i < a.size(); i++) {
        if (i) cout << ", ";
        cout << '[' << a[i][0] << ", " << a[i][1] << ", " << a[i][2] << ']';
    }
    cout << "]\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    FileLogger* obj = nullptr;
    regex ctor_re(R"(FileLogger\((-?\d+),\s*(-?\d+)\))");
    regex app_re(R"(putLog\((-?\d+),\s*(-?\d+)\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (line.rfind("FileLogger(", 0) == 0) {
            if (!regex_match(line, m, ctor_re)) return 1;
            delete obj;
            obj = new FileLogger(stoi(m[1]), stoi(m[2]));
            cout << "null\n";
        } else if (line.rfind("putLog(", 0) == 0) {
            if (!regex_match(line, m, app_re)) return 1;
            cout << obj->putLog(stoi(m[1]), stoi(m[2])) << "\n";
        } else if (line == "listFiles()") {
            printFiles(obj->listFiles());
        } else if (line == "totalSize()") {
            cout << obj->totalSize() << "\n";
        } else {
            return 1;
        }
    }
    delete obj;
    return 0;
}
