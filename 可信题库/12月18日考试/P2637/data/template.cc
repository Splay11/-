#include "foo.cc"
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

static string stripQuotes(string s) {
    size_t q1 = s.find('"');
    size_t q2 = s.find('"', q1 + 1);
    if (q1 == string::npos || q2 == string::npos) return s;
    return s.substr(q1 + 1, q2 - q1 - 1);
}

int main() {
    ServiceMgrSys sys;
    string line;
    cout << "null" << endl;
    if (!getline(cin, line)) return 0; // ServiceMgrSys()
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (line.find("startService") == 0) {
            size_t start = line.find('(') + 1;
            size_t end = line.rfind(')');
            string params = line.substr(start, end - start);
            stringstream ss(params);
            string serverIdStr, serviceName;
            getline(ss, serverIdStr, ',');
            getline(ss, serviceName);
            int serverId = stoi(serverIdStr);
            serviceName = stripQuotes(serviceName);
            cout << (sys.startService(serverId, serviceName) ? "true" : "false") << endl;
        } else if (line.find("addDependency") == 0) {
            size_t start = line.find('(') + 1;
            size_t end = line.rfind(')');
            string params = line.substr(start, end - start);
            stringstream ss(params);
            string fromServiceName, toServiceName;
            getline(ss, fromServiceName, ',');
            getline(ss, toServiceName);
            fromServiceName = stripQuotes(fromServiceName);
            toServiceName = stripQuotes(toServiceName);
            cout << (sys.addDependency(fromServiceName, toServiceName) ? "true" : "false") << endl;
        } else if (line.find("isServiceAvailable") == 0) {
            size_t start = line.find('(') + 1;
            size_t end = line.rfind(')');
            string serviceName = stripQuotes(line.substr(start, end - start));
            cout << (sys.isServiceAvailable(serviceName) ? "true" : "false") << endl;
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
            cout << "null" << endl;
        }
    }
    return 0;
}
