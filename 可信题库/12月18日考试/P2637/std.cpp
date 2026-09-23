#include <bits/stdc++.h>
using namespace std;

class ServiceMgrSys {
public:
    unordered_map<string, unordered_set<int>> running;
    unordered_map<int, unordered_set<string>> onServer;
    unordered_map<string, unordered_set<string>> deps;

    ServiceMgrSys() {}

    void rebootServers(vector<int>& serverIds) {
        for (int sid : serverIds) {
            auto it = onServer.find(sid);
            if (it == onServer.end()) continue;
            for (const string& name : it->second) {
                running[name].erase(sid);
                if (running[name].empty()) running.erase(name);
            }
            it->second.clear();
        }
    }

    bool startService(int serverId, string serviceName) {
        if (onServer[serverId].count(serviceName)) return false;
        onServer[serverId].insert(serviceName);
        running[serviceName].insert(serverId);
        return true;
    }

    bool addDependency(string fromServiceName, string toServiceName) {
        if (deps[fromServiceName].count(toServiceName)) return false;
        deps[fromServiceName].insert(toServiceName);
        return true;
    }

    bool isServiceAvailable(string serviceName) {
        unordered_map<string, bool> memo;
        function<bool(const string&)> dfs = [&](const string& name) -> bool {
            if (memo.count(name)) return memo[name];
            if (!running.count(name) || running[name].empty()) {
                return memo[name] = false;
            }
            for (const string& dep : deps[name]) {
                if (!dfs(dep)) return memo[name] = false;
            }
            return memo[name] = true;
        };
        return dfs(serviceName);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 将 stdin 原样交给与评测相同的调用逻辑：本地验题时直接复用 data/template.cc 思路
    ServiceMgrSys sys;
    string line;
    cout << "null\n";
    if (!getline(cin, line)) return 0; // 构造行
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (line.find("startService") == 0) {
            size_t start = line.find('(') + 1;
            size_t end = line.find(')');
            string params = line.substr(start, end - start);
            stringstream ss(params);
            string serverIdStr, serviceName;
            getline(ss, serverIdStr, ',');
            getline(ss, serviceName, ',');
            int serverId = stoi(serverIdStr);
            size_t q1 = serviceName.find('"');
            size_t q2 = serviceName.find('"', q1 + 1);
            serviceName = serviceName.substr(q1 + 1, q2 - q1 - 1);
            cout << (sys.startService(serverId, serviceName) ? "true" : "false") << "\n";
        } else if (line.find("addDependency") == 0) {
            size_t start = line.find('(') + 1;
            size_t end = line.find(')');
            string params = line.substr(start, end - start);
            stringstream ss(params);
            string fromServiceName, toServiceName;
            getline(ss, fromServiceName, ',');
            getline(ss, toServiceName, ',');
            auto strip = [](string s) {
                size_t q1 = s.find('"');
                size_t q2 = s.find('"', q1 + 1);
                return s.substr(q1 + 1, q2 - q1 - 1);
            };
            fromServiceName = strip(fromServiceName);
            toServiceName = strip(toServiceName);
            cout << (sys.addDependency(fromServiceName, toServiceName) ? "true" : "false") << "\n";
        } else if (line.find("isServiceAvailable") == 0) {
            size_t start = line.find('(') + 1;
            size_t end = line.find(')');
            string serviceName = line.substr(start, end - start);
            size_t q1 = serviceName.find('"');
            size_t q2 = serviceName.find('"', q1 + 1);
            serviceName = serviceName.substr(q1 + 1, q2 - q1 - 1);
            cout << (sys.isServiceAvailable(serviceName) ? "true" : "false") << "\n";
        } else if (line.find("rebootServers") == 0) {
            size_t start = line.find('[') + 1;
            size_t end = line.find(']');
            string params = line.substr(start, end - start);
            stringstream ss(params);
            vector<int> serverIds;
            string serverIdStr;
            while (getline(ss, serverIdStr, ',')) {
                if (serverIdStr.find_first_not_of(" \t") == string::npos) continue;
                serverIds.push_back(stoi(serverIdStr));
            }
            sys.rebootServers(serverIds);
            cout << "null\n";
        }
    }
    return 0;
}
