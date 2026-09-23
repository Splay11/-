#include <stdbool.h>

int countIsolatedIntervals(int** intervals, int intervalsSize, int* intervalsColSize) {
    int ans = 0;
    for (int i = 0; i < intervalsSize; i++) {
        int s1 = intervals[i][0], e1 = intervals[i][1];
        bool isolated = true;
        for (int j = 0; j < intervalsSize; j++) {
            if (i == j) continue;
            int s2 = intervals[j][0], e2 = intervals[j][1];
            // 标准区间相交判定
            if (s1 <= e2 && s2 <= e1) {
                isolated = false;
                break;
            }
        }
        if (isolated) ans++;
    }
    return ans;
}
