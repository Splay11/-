#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

static vector<string> splitInput(const string& text) {
    vector<string> parts;
    string current;
    bool inQuote = false;
    bool escape = false;

    for (char ch : text) {
        if (escape) {
            current.push_back(ch);
            escape = false;
            continue;
        }
        if (ch == '\\') {
            current.push_back(ch);
            escape = true;
            continue;
        }
        if (ch == '"') {
            current.push_back(ch);
            inQuote = !inQuote;
            continue;
        }
        if (ch == ',' && !inQuote) {
            parts.push_back(current);
            current.clear();
        } else {
            current.push_back(ch);
        }
    }
    parts.push_back(current);
    return parts;
}

static string trimToken(const string& s) {
    int left = 0;
    int right = (int)s.size() - 1;
    while (left <= right && isspace((unsigned char)s[left])) {
        left++;
    }
    while (right >= left && isspace((unsigned char)s[right])) {
        right--;
    }
    if (left > right) {
        return "";
    }
    return s.substr(left, right - left + 1);
}

static string parseStringToken(string token) {
    token = trimToken(token);
    if ((int)token.size() >= 2 && token.front() == '"' && token.back() == '"') {
        return token.substr(1, token.size() - 2);
    }
    return token;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string text;
    string line;
    while (getline(cin, line)) {
        text += line;
        text += '\n';
    }

    vector<string> parts = splitInput(text);
    string preorderStr;
    string inorderStr;
    char beDeletedNode;

    if (parts.size() != 3) {
        preorderStr = "";
        inorderStr = "";
        beDeletedNode = '\0';
    } else {
        preorderStr = parseStringToken(parts[0]);
        inorderStr = parseStringToken(parts[1]);
        string deletedToken = parseStringToken(parts[2]);
        beDeletedNode = deletedToken.size() == 1 ? deletedToken[0] : '\0';
    }

    string ans = Solution().buildAfterDelete(preorderStr, inorderStr, beDeletedNode);
    cout << "\"" << ans << "\"" << '\n';
    return 0;
}
