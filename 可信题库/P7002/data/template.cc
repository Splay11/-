#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    JobQueueSys* obj = nullptr;
    regex init_re(R"(JobQueueSys\(\))");
    regex submit_re(R"(submit\((-?\d+),\s*(-?\d+)\))");
    regex cancel_re(R"(cancel\((-?\d+)\))");
    regex pop_re(R"(popJob\(\))");
    regex peek_re(R"(peekJob\(\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new JobQueueSys();
            cout << "null\n";
        } else if (regex_match(line, m, submit_re)) {
            cout << (obj->submit(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, cancel_re)) {
            cout << (obj->cancel(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, pop_re)) {
            cout << obj->popJob() << "\n";
        } else if (regex_match(line, m, peek_re)) {
            cout << obj->peekJob() << "\n";
        } else {
            return 1;
        }
    }
    return 0;
}
