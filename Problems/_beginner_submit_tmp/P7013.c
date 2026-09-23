#include <stdlib.h>

static int cmp_asc(const void* pa, const void* pb) {
    int a = *(const int*)pa, b = *(const int*)pb;
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

int countNeedUpgrade(int* versions, int versionsSize, int baseline) {
    /* 空数组 */
    if (versionsSize <= 0) return 0;
    int* a = (int*)malloc(versionsSize * sizeof(int));
    for (int i = 0; i < versionsSize; i++) a[i] = versions[i];
    /* 升序排序 */
    qsort(a, versionsSize, sizeof(int), cmp_asc);
    /* 手写二分 lower_bound */
    int lo = 0, hi = versionsSize;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < baseline) lo = mid + 1;
        else hi = mid;
    }
    int ans = versionsSize - lo;
    free(a);
    return ans;
}
