/**
 * Special Judge for KV Cache 稀疏化管理
 * 
 * 输出格式：
 *   - PRUNED <pos>                 (淘汰 token 时输出，无句号)
 *   - <count>                      (QUERY 时先输出缓存大小)
 *     <pos> <score>
 *     <k0> <k1> <k2> <k3>
 *     <v0> <v1> <v2> <v3>
 *     ... (重复 count 次)
 *
 * 浮点数比较：误差 < 0.1
 *
 * HydroOJ testlib 规范：
 *   inf  - 输入文件
 *   ouf  - 选手输出
 *   ans  - 标准答案
 */

#include "testlib.h"
#include <cmath>
#include <cstdlib>
#include <string>

using namespace std;

const double EPS = 0.1;

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    while (!ans.seekEof()) {
        string token = ans.readToken();

        if (token == "PRUNED") {
            // ============ PRUNED 行 ============
            long long posAns = ans.readLong();

            string contToken = ouf.readToken();
            if (contToken != "PRUNED") {
                quitf(_wa,
                      "Expected PRUNED, but found \"%s\" in contestant output",
                      contToken.c_str());
            }

            long long posOuf = ouf.readLong();
            if (posAns != posOuf) {
                quitf(_wa,
                      "PRUNED position mismatch: expected %lld, found %lld",
                      posAns, posOuf);
            }
        } else {
            // ============ QUERY 块 ============
            // 第一个 token 应该是缓存大小（整数）
            char* endptr = nullptr;
            long long cntAns = strtoll(token.c_str(), &endptr, 10);
            if (*endptr != '\0') {
                quitf(_fail,
                      "Unexpected token \"%s\" in answer file",
                      token.c_str());
            }

            long long cntOuf = ouf.readLong();
            if (cntAns != cntOuf) {
                quitf(_wa,
                      "Cache size mismatch: expected %lld, found %lld",
                      cntAns, cntOuf);
            }

            // 逐个比较缓存条目
            for (long long i = 0; i < cntAns; i++) {
                // --- 位置 ---
                long long posAns = ans.readLong();
                long long posOuf = ouf.readLong();
                if (posAns != posOuf) {
                    quitf(_wa,
                          "Position mismatch in QUERY block #%lld: "
                          "expected %lld, found %lld",
                          i, posAns, posOuf);
                }

                // --- 分数 ---
                double scoreAns = ans.readDouble();
                double scoreOuf = ouf.readDouble();
                if (fabs(scoreAns - scoreOuf) >= EPS) {
                    quitf(_wa,
                          "Score mismatch for position %lld: "
                          "expected %.10f, found %.10f",
                          posAns, scoreAns, scoreOuf);
                }

                // --- Key 向量 (4 个 double) ---
                for (int j = 0; j < 4; j++) {
                    double vAns = ans.readDouble();
                    double vOuf = ouf.readDouble();
                    if (fabs(vAns - vOuf) >= EPS) {
                        quitf(_wa,
                              "Key[%d] mismatch for position %lld: "
                              "expected %.10f, found %.10f",
                              j, posAns, vAns, vOuf);
                    }
                }

                // --- Value 向量 (4 个 double) ---
                for (int j = 0; j < 4; j++) {
                    double vAns = ans.readDouble();
                    double vOuf = ouf.readDouble();
                    if (fabs(vAns - vOuf) >= EPS) {
                        quitf(_wa,
                              "Value[%d] mismatch for position %lld: "
                              "expected %.10f, found %.10f",
                              j, posAns, vAns, vOuf);
                    }
                }
            }
        }
    }

    // 选手输出不能有额外内容
    if (!ouf.seekEof()) {
        string extra = ouf.readToken();
        quitf(_wa,
              "Extra output from contestant after expected end: \"%s\"",
              extra.c_str());
    }

    quitf(_ok, "Accepted");
    return 0;
}
