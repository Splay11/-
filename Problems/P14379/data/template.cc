#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>

using namespace std;

static string parsePythonStringLiteral(const string& line) {
    size_t i = 0;
    while (i < line.size() && isspace((unsigned char)line[i])) i++;
    if (i >= line.size() || line[i] != '"') exit(1);
    i++;
    string out;
    while (i < line.size()) {
        char c = line[i];
        if (c == '"') {
            if (i + 1 < line.size() && line[i + 1] == '"') {
                out.push_back('"');
                i += 2;
                continue;
            }
            break;
        }
        if (c == '\\') {
            if (i + 1 >= line.size()) exit(1);
            char n = line[i + 1];
            if (n == 'n')
                out.push_back('\n');
            else if (n == 't')
                out.push_back('\t');
            else if (n == 'r')
                out.push_back('\r');
            else if (n == '\\')
                out.push_back('\\');
            else if (n == '"')
                out.push_back('"');
            else
                out.push_back(n);
            i += 2;
            continue;
        }
        out.push_back(c);
        i++;
    }
    return out;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    string story = parsePythonStringLiteral(line);
    Solution sol;
    cout << sol.lengthOfLongestSubstring(story) << "\n";
    return 0;
}
