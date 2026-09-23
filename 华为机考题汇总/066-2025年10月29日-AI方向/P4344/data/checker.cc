#include "testlib.h"
#include <bits/stdc++.h>
using namespace std;

int main(int argc, char *argv[]) {
    registerTestlibCmd(argc, argv);

    const double EPS = 0.005;

    int n = inf.readInt();
    int max_iter = inf.readInt();
    double alpha = inf.readDouble();
    double lambda = inf.readDouble();
    double tol = inf.readDouble();

    for (int i = 0; i < n; i++) {
        inf.readDouble(); // age
        inf.readDouble(); // income
        inf.readDouble(); // browse time
        inf.readInt();    // label
    }

    int m = inf.readInt();

    for (int i = 0; i < m; i++) {
        inf.readDouble();
        inf.readDouble();
        inf.readDouble();

        int juryLabel = ans.readInt();
        double juryProb = ans.readDouble();

        int userLabel = ouf.readInt();
        double userProb = ouf.readDouble();

        if (userLabel != 0 && userLabel != 1) {
            quitf(_wa, "Line %d: label must be 0 or 1, found %d", i + 1, userLabel);
        }

        if (userLabel != juryLabel) {
            quitf(_wa,
                  "Line %d: wrong label, expected %d, found %d",
                  i + 1, juryLabel, userLabel);
        }

        if (!isfinite(userProb)) {
            quitf(_wa, "Line %d: probability is not finite", i + 1);
        }

        if (fabs(userProb - juryProb) > EPS + 1e-12) {
            quitf(_wa,
                  "Line %d: wrong probability, expected %.10f, found %.10f, diff %.10f",
                  i + 1, juryProb, userProb, fabs(userProb - juryProb));
        }
    }
    quitf(_ok, "Accepted");
}
