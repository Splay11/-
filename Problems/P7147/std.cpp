#include <iostream>
#include <vector>
#include <cstdlib>
using namespace std;

// 用栈模拟碰撞：只有栈顶向右、当前向左才会撞
vector<int> solve(const vector<int>& asteroids) {
    vector<int> stack;
    for (int x : asteroids) {
        bool alive = true;
        // 只有「右行遇上左行」才会碰撞
        while (alive && !stack.empty() && stack.back() > 0 && x < 0) {
            int top = stack.back();
            if (abs(top) < abs(x)) {
                // 栈顶更小，炸掉栈顶，当前小行星继续往左撞
                stack.pop_back();
                continue;
            }
            if (abs(top) == abs(x)) {
                // 一样大，两颗一起炸
                stack.pop_back();
            }
            // 栈顶更大或已经同归于尽，当前这颗不再存活
            alive = false;
        }
        if (alive) {
            stack.push_back(x);
        }
    }
    return stack;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    vector<int> rest = solve(a);
    cout << (int)rest.size() << '\n';
    // 没有剩余时只输出 0，不要再打空的第二行
    if (!rest.empty()) {
        for (int i = 0; i < (int)rest.size(); i++) {
            if (i) {
                cout << ' ';
            }
            cout << rest[i];
        }
        cout << '\n';
    }
    return 0;
}
