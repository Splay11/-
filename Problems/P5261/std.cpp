#include <iostream>
#include <set>
#include <string>
#include <tuple>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int R, C;
    cin >> R >> C;
    vector<tuple<string, string, string>> plans;
    for (int i = 0; i < R; i++) {
        string rid, scene, ver;
        cin >> rid >> scene >> ver;
        plans.push_back({rid, scene, ver});
    }
    set<tuple<string, string, string>> ready;
    for (int i = 0; i < C; i++) {
        string rid, ver, plat, status;
        cin >> rid >> ver >> plat >> status;
        if (status == "READY") ready.insert({rid, ver, plat});
    }
    vector<string> missing;
    for (size_t i = 0; i < plans.size(); i++) {
        string rid = get<0>(plans[i]);
        string ver = get<2>(plans[i]);
        bool ok = ready.count({rid, ver, "android"}) &&
                  ready.count({rid, ver, "ios"}) &&
                  ready.count({rid, ver, "pc"});
        if (!ok) missing.push_back(rid);
    }
    if (missing.empty()) {
        cout << "none\n";
    } else {
        for (auto& x : missing) cout << x << '\n';
    }
    return 0;
}
