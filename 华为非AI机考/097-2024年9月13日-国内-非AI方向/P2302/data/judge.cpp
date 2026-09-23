#include "testlib.h"
#include<bits/stdc++.h>
using namespace std;
int main(int argc,char *argv[])
{
    registerTestlibCmd(argc,argv);
    int h = inf.readInt();
    int n = inf.readInt();
    int m = inf.readInt();
    string a[n][m];
    int sx , sy , ex , ey;
    for (int i = 0 ; i < n ; i++){
        for (int j = 0 ; j < m ; j++){
            a[i][j] = inf.readToken();
            if (a[i][j] == "s"){
                sx = i;
                sy = j;
            }
            if (a[i][j] == "t"){
                ex = i;
                ey = j;
            }
        }
    }
    vector<pair<int,int>> ans_path;
    int sz1 = ans.readInt();
    for (int i = 0 ; i < sz1 ; i++){
        int x = ans.readInt();
        int y = ans.readInt();
        ans_path.push_back({x,y});
    }
    vector<pair<int,int>> ouf_path;
    int sz2 = ouf.readInt();
    for (int i = 0 ; i < sz2 ; i++){
        int x = ouf.readInt();
        int y = ouf.readInt();
        ouf_path.push_back({x,y});
    }

    if (sz1 == 1){
        if (sz1 != sz2){
            quitf(_wa,"wrong answer:there is no path");
            
        }else {
            if (ans_path[0] == ouf_path[0]){
                quitf(_ok,"ok");
            }else {
                quitf(_wa,"wrong answer:start point is wrong");
            }
        }
        return 0;
    }
    int now_h = h;
    int dx[] = {0,0,1,-1};
    int dy[] = {1,-1,0,0};
    // 开始是s 
    if (a[ouf_path[0].first][ouf_path[0].second] != "s"){
        quitf(_wa,"wrong answer : first point is not s");
        return 0;
    }
    // 结束是t
    if (a[ouf_path[sz2 - 1].first][ouf_path[sz2 - 1].second] != "t"){
        quitf(_wa,"wrong answer: last point is not t");
        return 0;
    }
    // 中间都是高度 
    now_h = h;
    for (int i = 1 ; i < sz2 - 1; i++){
        now_h += 1;
        int x = ouf_path[i].first;
        int y = ouf_path[i].second;
        if (a[x][y] == "s" || a[x][y] == "t"){
            quitf(_wa,"wrong answer: mid point is s or t");
            return 0;
        }
        int h_1 = stoi(a[x][y]);
        if (now_h >= h_1){
            quitf(_wa,"wrong answer: height is wrong");
            return 0;
        }
    }
    quitf(_ok,"ok");
    
    /*
    int t = inf.readInt();
    bool ok = true;
    for (int i = 1 ; i <= t ; i++){
        int x = inf.readInt();
        long long y = ouf.readLong();
        if (y > 20000000000){
            ok = false;
            break;
        }
        long long res = y * x;
        // 将res转换为字符串
        string s = to_string(res);
        set<char> st;
        for (int j = 0 ; j < s.size() ; j++){
            st.insert(s[j]);
        }
        if (st.size() != 10){
            ok = false;
            break;
        }
    }
    if (ok){
        quitf(_ok,"ok");
    }else {
        quitf(_wa,"wrong answer");
    }
    */
    return 0;
}