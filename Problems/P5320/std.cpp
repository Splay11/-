#include <iostream>
#include <string>
#include <vector>
#include <cctype>
#include <cstdlib>
using namespace std;

string src;
int posi;

void skip() {
  while (posi < (int)src.size() && isspace((unsigned char)src[posi])) posi++;
}

void eat(char c) {
  skip();
  posi++;
}

double readNum() {
  skip();
  int j = posi;
  if (src[j] == '-') j++;
  while (j < (int)src.size()) {
    char c = src[j];
    if (isdigit((unsigned char)c) || c == '.' || c == 'e' || c == 'E' || c == '+' || c == '-') j++;
    else break;
  }
  double v = atof(src.substr(posi, j - posi).c_str());
  posi = j;
  return v;
}

vector<double> readVec() {
  eat('[');
  skip();
  vector<double> a;
  if (src[posi] == ']') {
    posi++;
    return a;
  }
  while (true) {
    a.push_back(readNum());
    skip();
    if (src[posi] == ',') {
      posi++;
      continue;
    }
    eat(']');
    break;
  }
  return a;
}

vector<int> solve(vector<vector<double> > feats, vector<double> labs, vector<vector<double> > test) {
  int n = (int)feats.size();
  int d = (int)feats[0].size() + 1;
  vector<vector<double> > X(n, vector<double>(d));
  vector<double> t(n);
  for (int i = 0; i < n; i++) {
    X[i][0] = 1.0;
    for (int j = 0; j < (int)feats[i].size(); j++) X[i][j + 1] = feats[i][j];
    t[i] = labs[i] == 0 ? -1.0 : 1.0;
  }
  vector<double> h(d, 0.0);
  for (int ep = 0; ep < 10; ep++) {
    for (int i = 0; i < n; i++) {
      double score = 0;
      for (int j = 0; j < d; j++) score += h[j] * X[i][j];
      double pred = score >= 0 ? 1.0 : -1.0;
      if (pred != t[i]) {
        for (int j = 0; j < d; j++) h[j] += t[i] * X[i][j];
      }
    }
  }
  vector<int> ans((int)test.size());
  for (int i = 0; i < (int)test.size(); i++) {
    double score = h[0];
    for (int j = 0; j < (int)test[i].size(); j++) score += h[j + 1] * test[i][j];
    ans[i] = score >= 0 ? 1 : 0;
  }
  return ans;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  string line;
  while (getline(cin, line)) src += line;
  posi = 0;
  vector<vector<double> > feats, test;
  vector<double> labs;
  eat('{');
  while (true) {
    skip();
    if (src[posi] == '}') break;
    eat('"');
    int ks = posi;
    while (src[posi] != '"') posi++;
    string key = src.substr(ks, posi - ks);
    posi++;
    eat(':');
    if (key == "train") {
      eat('[');
      skip();
      if (src[posi] != ']') {
        while (true) {
          eat('[');
          vector<double> f = readVec();
          eat(',');
          double lab = readNum();
          eat(']');
          feats.push_back(f);
          labs.push_back(lab);
          skip();
          if (src[posi] == ',') {
            posi++;
            continue;
          }
          break;
        }
      }
      eat(']');
    } else if (key == "test") {
      eat('[');
      skip();
      if (src[posi] != ']') {
        while (true) {
          test.push_back(readVec());
          skip();
          if (src[posi] == ',') {
            posi++;
            continue;
          }
          break;
        }
      }
      eat(']');
    }
    skip();
    if (src[posi] == ',') posi++;
  }
  vector<int> ans = solve(feats, labs, test);
  cout << "[";
  for (int i = 0; i < (int)ans.size(); i++) {
    if (i) cout << ", ";
    cout << ans[i];
  }
  cout << "]\n";
  return 0;
}
