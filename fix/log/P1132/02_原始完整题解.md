## 题目思路

首先将斜率为1和-1的直线分开，由于给出的两点一定在矩形内，所以该直线一定与矩形相交。首先将斜率为-1（或1）的直线先切到矩形上，那么会将矩形分成斜率为-1（或1）的直线条数加一。再将斜率为1（或-1）的直线加入进来，无论与其他直线有没有交点都会产生一个新的矩形。如果该直线与已有的-1（或1）的直线的交点在矩形外，那么将不产生新得矩形，如果交点在矩形内部那么就会产生一个新的矩形。

## 代码
C++
```c++
#include<bits/stdc++.h>

using namespace std;

const int M = 1e3 + 5;
const double eps = 1e-8;

int sgn(double x){
    if(fabs(x) < eps)return 0;
    if(x < 0)return -1;
    else return 1;
}

struct Point{
    double x, y;

    void input(){
        scanf("%lf%lf",&x,&y);
    }
    Point(){}
    Point(double _x, double _y){
        x = _x, y = _y;
    }

    double operator^ (const Point &b)const{
        return x * b.y - y * b.x;
    }

    double operator* (const Point &b)const{
        return x * b.x + y * b.y;
    }

    Point operator -(const Point &b)const{
        return Point(x-b.x,y-b.y);
    }
};

struct Line {
    Point s, e;

    void input(){
        s.input();
        e.input();
    }

    Point crosspoint(Line v){
        double a1 = (v.e - v.s)^(s - v.s);
        double a2 = (v.e - v.s)^(e - v.s);
        return Point((s.x * a2 - e.x * a1) / (a2 - a1), (s.y * a2 - e.y * a1) / (a2 - a1));
    }//求两直线交点

    bool isone() {
        return (e.y - s.y) / (e.x - s.x) > 0;
    }//判断斜率是1还是-1,1为true,-1为false
};


int h, w;

void solve() {
    cin >> h >> w;
    int m;
    cin >> m;
    vector<Line> v1, v2;//v1存斜率为1的直线，v2存斜率为-1的直线
    Line l;
    for (int i = 1; i <= m; i++) {
        l.input();
        if (l.isone()) v1.push_back(l);
        else v2.push_back(l);
    }
    int ans = v1.size() + 1;//初始化为斜率为1的直线的个数加一
    for (int i = 0; i < v2.size(); i++) {
        int cnt = 1;//必会产生新矩形
        for (int j = 0; j < v1.size(); j++) {
            Point p = v2[i].crosspoint(v1[j]);
            if (p.x < w && p.x > 0 && p.y < h && p.y > 0) {//判断交点是否在矩形内,记录这类交点个数
                cnt++;
            }
        }
        ans += cnt;
    }
    cout << ans << endl;
}

int main() {
    int t = 1;
    // cin >> t;
    while (t--) solve();
    return 0;
}
```
Python
```python
from collections import deque
h, w = [int(_)*4 for _ in input().split()]
m = int(input())
flag = [[0]*(w+5) for _ in range(h+5)]
for _ in range(m):
    x1, y1, x2, y2 = [int(_)*4 for _ in input().split()]
    k = (y2-y1)//(x2-x1)
    b = y1-k*x1
    ii = b
    jj = 0
    if b > 0:
        ii = min(b, h)
        jj = (ii-b)//k
    if b < 0:
        ii = 0
        jj = -b//k
    if k == 1:
        while 1:
            flag[ii][jj] = 1
            ii += 1
            jj += 1
            if ii < 0 or ii > h or jj < 0 or jj > w:
                break
    else:
        while 1:
            flag[ii][jj] = 1
            ii -= 1
            jj += 1
            if ii < 0 or ii > h or jj < 0 or jj > w:
                break
vis = [[0]*(w+5) for _ in range(h+5)]
res = 0
dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
for i in range(h+1):
    for j in range(w+1):
        if vis[i][j] or flag[i][j]:
            continue
        res += 1
        vis[i][j] = 1
        q = deque()
        q.append((i, j))
        while len(q):
            x, y = q.popleft()
            for k in range(4):
                dx = dir[k][0]+x
                dy = dir[k][1]+y
                if dx < 0 or dx > h or dy < 0 or dy > w:
                    continue
                if vis[dx][dy] or flag[dx][dy]:
                    continue
                vis[dx][dy] = 1
                q.append((dx, dy))
print(res)
```

Java
```java
import java.util.*;

// 注意类名必须为 Main, 不要有任何 package xxx 信息
public class Main {

    static final int num = 26;

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int h = in.nextInt(), w = in.nextInt();
        int m = in.nextInt();
        Set<Integer> positiveLine = new HashSet<>();
        Set<Integer> negativeLine = new HashSet<>();
        for (int i = 0; i < m; i++) {
            int x1 = in.nextInt(), y1 = in.nextInt(), x2 = in.nextInt(), y2 = in.nextInt();
            int y = y1 - x1 * (y2 - y1) / (x2 - x1);
            if ((y2 - y1) * (x2 - x1) > 0) {
                positiveLine.add(y);
            } else {
                negativeLine.add(y);
            }
        }
        int count = 0;
        for (int num1: positiveLine) {
            for (int num2: negativeLine) {
                double crossX = ((double) num2 - (double)num1) / 2;
                double crossY = (double) num2 - crossX;
                if (isIn(h, w, crossX, crossY)) {
                    count++;
                }
            }
        }
        System.out.println(m + 1 + count);
    }

    public static boolean isIn(int h, int w, double x, double y) {
        return x > 0.0 && x < (double) w && y > 0.0 && y < (double) h;
    }
}
```