#include <stdlib.h>

static int can(int* tasks, int n, int m, long long mid) {
    int need = 1;
    long long cur = 0;
    for (int i = 0; i < n; i++) {
        if (cur + tasks[i] > mid) {
            need++;
            cur = tasks[i];
            if (need > m) return 0;
        } else cur += tasks[i];
    }
    return 1;
}

long long minMaxBackupLoad(int* tasks, int tasksSize, int m) {
    if (tasksSize <= 0) return 0;
    if (m <= 0) m = 1;
    long long lo = tasks[0], hi = 0;
    for (int i = 0; i < tasksSize; i++) {
        if (tasks[i] > lo) lo = tasks[i];
        hi += tasks[i];
    }
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (can(tasks, tasksSize, m, mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
