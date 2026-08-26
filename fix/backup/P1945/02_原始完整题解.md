## 思路

简单数学，计算小时，分钟，秒钟的差之后 / 60即可得到秒钟转的圈数。

## 代码

### python
```python
# 不保证time_1 < time_2,需要考虑隔天的情况
def calc_second (time_1 , time_2):
    time_1 = time_1.split(":")
    time_2 = time_2.split(":")
    h1 , m1 , s1 = int(time_1[0]) , int(time_1[1]) , int(time_1[2])
    h2 , m2 , s2 = int(time_2[0]) , int(time_2[1]) , int(time_2[2])
    #考虑隔天的情况
    if h1 > h2 or (h1 == h2 and m1 > m2) or (h1 == h2 and m1 == m2 and s1 > s2):
        h2 += 24
    second = (h2 - h1) * 3600 + (m2 - m1) * 60 + (s2 - s1)
    return second
n = int(input())
time_arr = input().split()
res = []
for i in range(n - 1):
    tmp = calc_second(time_arr[i] , time_arr[i + 1]) / 60
    # 强制保留两位小数 , 不过的补0
    res.append(f"{tmp:.2f}")
print(" ".join(map(str , res)))
```
### C++
```C++
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>

using namespace std;

vector<string> spliString(string s,char del){
    vector<string> res;
    stringstream ss(s);
    string t;
    while(getline(ss,t,del)){
        res.push_back(t);
    }
    return res;
}

int main(){
    long long n;
    cin>>n;

    string pre;
    cin>>pre;
    char del = ':';

    n--;
    while(n--){
        vector<string> ptime = spliString(pre, del);
        int phour = stoi(ptime[0]);
        int pmin = stoi(ptime[1]);
        int pst = stoi(ptime[2]);

        string nex;
        cin>>nex;
        vector<string> ntime = spliString(nex, del);
        int nhour = stoi(ntime[0]);
        int nmin = stoi(ntime[1]);
        int nst = stoi(ntime[2]);

        if(nhour<phour){
            nhour+=24;
            if(nmin<pmin){
                nhour--;
                nmin+=60;
            }
            if(nst<pst){
                nmin--;
                nst+=60;
            }
        }

        if(nhour==phour&&nmin<pmin){
            nhour+=24;
            if(nmin<pmin){
                nhour--;
                nmin+=60;
            }
            if(nst<pst){
                nmin--;
                nst+=60;
            }
        }

        if(nhour==phour&&nmin==pmin&&nst<pst){
            nhour+=24;
            if(nmin<pmin){
                nhour--;
                nmin+=60;
            }
            if(nst<pst){
                nmin--;
                nst+=60;
            }
        }

        int sums = (nhour-phour)*3600+(nmin-pmin)*60+nst-pst;

        double cil = sums/60.00;
        cout<<fixed<<setprecision(2)<<cil<<" ";

        pre = nex;
    }
}
```
OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。