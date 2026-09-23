#include <deque>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<int> processPacketCommands(vector<string>& commands) {
    deque<int> buffer, send_q;       // 缓冲区与发送区
    unordered_set<int> in_buffer;    // 缓冲区中已有的编号
    vector<int> ans;

    auto flush = [&]() {
      // 发送区为空时，将缓冲区整批移入发送区
      while (!buffer.empty()) {
        int x = buffer.front();
        buffer.pop_front();
        in_buffer.erase(x);
        send_q.push_back(x);
      }
    };

    for (const string& cmd : commands) {
      size_t sp = cmd.find(' ');
      string op = (sp == string::npos) ? cmd : cmd.substr(0, sp);
      if (op == "RECEIVE") {
        int x = stoi(cmd.substr(sp + 1));
        // 仅检查缓冲区是否重复
        if (in_buffer.count(x)) {
          ans.push_back(-1);
        } else {
          buffer.push_back(x);
          in_buffer.insert(x);
          ans.push_back(x);
        }
      } else if (op == "SEND") {
        if (!send_q.empty()) {
          // 发送区非空，弹出队首并输出
          ans.push_back(send_q.front());
          send_q.pop_front();
        } else if (!buffer.empty()) {
          flush();
          ans.push_back(send_q.front());
          send_q.pop_front();
        } else {
          ans.push_back(0);  // 两区皆空
        }
      } else if (op == "QUERY") {
        if (!send_q.empty()) {
          ans.push_back(send_q.front());  // 只查队首，不弹出
        } else if (!buffer.empty()) {
          flush();
          ans.push_back(send_q.front());
        } else {
          ans.push_back(0);
        }
      }
    }
    return ans;
  }
};
