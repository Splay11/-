#include "foo.cc"
#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    MicQueue* obj = nullptr;
    regex init_re(R"(MicQueue\(\))");
    regex enroll_re(R"(enroll\((-?\d+),\s*(-?\d+)\))");
    regex next_re(R"(nextPlay\(\))");
    regex boost_re(R"(boost\((-?\d+),\s*(-?\d+)\))");
    regex cancel_re(R"(cancel\((-?\d+)\))");
    regex wait_re(R"(waiting\(\))");
    smatch m;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (regex_match(line, m, init_re)) {
            obj = new MicQueue();
            cout << "null\n";
        } else if (regex_match(line, m, enroll_re)) {
            cout << (obj->enroll(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, next_re)) {
            cout << obj->nextPlay() << "\n";
        } else if (regex_match(line, m, boost_re)) {
            cout << (obj->boost(stoi(m[1]), stoi(m[2])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, cancel_re)) {
            cout << (obj->cancel(stoi(m[1])) ? "true" : "false") << "\n";
        } else if (regex_match(line, m, wait_re)) {
            cout << obj->waiting() << "\n";
        } else {
            return 1;
        }
    }
    delete obj;
    return 0;
}
