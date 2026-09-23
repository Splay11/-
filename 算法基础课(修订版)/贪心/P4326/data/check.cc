#include "testlib.h"
#include <cctype>
#include <string>
#include <vector>

using namespace std;

// 转小写
string toLowerCase(const string &s) {
	string t = s;
	for (char &c : t) c = (char)tolower((unsigned char)c);
	return t;
}

// 去除行尾空白（空格/制表/回车）
string rtrim(const string &s) {
	int r = (int)s.size() - 1;
	while (r >= 0 && (s[r] == ' ' || s[r] == '\t' || s[r] == '\r')) --r;
	return s.substr(0, r + 1);
}

int main(int argc, char *argv[]) {
	registerTestlibCmd(argc, argv);

	vector<string> exp, usr;

	// 逐行读取标准答案与选手输出
	while (!ans.eof()) {
		string line = ans.readLine();
		exp.push_back(toLowerCase(rtrim(line)));
	}
	while (!ouf.eof()) {
		string line = ouf.readLine();
		usr.push_back(toLowerCase(rtrim(line)));
	}

	// 去掉末尾完全空行（可选，更宽松）
	while (!exp.empty() && exp.back().empty()) exp.pop_back();
	while (!usr.empty() && usr.back().empty()) usr.pop_back();

	if (exp.size() != usr.size()) {
		quitf(_wa, "line count mismatch: expected %d lines, found %d lines", (int)exp.size(), (int)usr.size());
	}

	for (size_t i = 0; i < exp.size(); ++i) {
		if (exp[i] != usr[i]) {
			quitf(_wa, "mismatch at line %d", (int)i + 1);
		}
	}

	quitf(_ok, "correct answer");
	return 0;
}
