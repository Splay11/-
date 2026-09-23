#include "testlib.h"
#include <string>

int main(int argc, char* argv[]) {
    // 设置 Special Judge 的名称
    setName("checks");

    // 初始化测试库
    registerTestlibCmd(argc, argv);
    std::stringstream ssInf(inf.readLine());
    int x;

    std::vector<int> numsOuf;
    std::stringstream ssOuf(ouf.readLine());
    while (ssOuf >> x) {
        numsOuf.push_back(x);
    }

    std::vector<int> numsAns;
    std::stringstream ssAns(ans.readLine());
    while (ssAns >> x) {
        numsAns.push_back(x);
    }

    if (numsAns[0]==-1&&(numsOuf.size()==1&&numsOuf[0]==-1)) {
        quitf(_ok, "accept");
    }

    std::vector<int> numsInf;
    while (ssInf >> x) {
        numsInf.push_back(x);
    }

    int k = inf.readInt();

    int n = numsInf.size();
    if (numsAns[0]==-1&&(numsOuf.size()!=1||numsOuf[0]!=-1)) {
        quitf(_wa, "error");
    }
    if(numsAns.size()>1){
        for (int i = 0; i < n - 1; ++i) {
            if (numsAns[i] != numsOuf[i]) {
                int a = numsAns[i];
                int b = numsOuf[i];
                if (b < 0 || b >= n) {
                    quitf(_wa, "output out of bounds");
                } else if (b<i-k+1||b>i+k) {
                    quitf(_wa, "output out of bounds");
                } else if (numsInf[a] != numsInf[b]) {
                    quitf(_wa, "not min");
                }
            }
        }
    }

    quitf(_ok, "accept");

}