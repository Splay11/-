#include "foo.cc"
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

static string trim(const string& s) {
    size_t a = 0;
    while (a < s.size() && isspace((unsigned char)s[a])) a++;
    size_t b = s.size();
    while (b > a && isspace((unsigned char)s[b - 1])) b--;
    return s.substr(a, b - a);
}

static string extractQuoted(const string& s, size_t lparen) {
    size_t i = lparen + 1;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '"') exit(1);
    i++;
    string msg;
    while (i < s.size() && s[i] != '"') {
        msg.push_back(s[i]);
        i++;
    }
    return msg;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    LogSystem* obj = nullptr;
    bool first = true;
    while (getline(cin, line)) {
        line = trim(line);
        if (line.empty()) continue;
        if (!first) cout << "\n";
        first = false;
        if (line == "LogSystem()") {
            delete obj;
            obj = new LogSystem();
            cout << "null";
        } else if (line.rfind("log(", 0) == 0) {
            string msg = extractQuoted(line, 3);
            cout << "\"" << obj->log(msg) << "\"";
        } else if (line.rfind("enter(", 0) == 0) {
            size_t lp = line.find('(');
            size_t comma = line.find(',', lp);
            size_t rp = line.rfind(')');
            int id = stoi(trim(line.substr(lp + 1, comma - lp - 1)));
            string b = trim(line.substr(comma + 1, rp - comma - 1));
            obj->enter(id, b == "true");
            cout << "null";
        } else if (line.rfind("leave(", 0) == 0) {
            size_t lp = line.find('(');
            size_t rp = line.rfind(')');
            int id = stoi(trim(line.substr(lp + 1, rp - lp - 1)));
            obj->leave(id);
            cout << "null";
        } else {
            return 1;
        }
    }
    cout << "\n";
    delete obj;
    return 0;
}
