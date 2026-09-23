#include <stdlib.h>

static int cmp_desc(const void* pa, const void* pb) {
    int a = *(const int*)pa, b = *(const int*)pb;
    if (a < b) return 1;
    if (a > b) return -1;
    return 0;
}

int minAuditDays(int* loads, int loadsSize) {
    /* 空数组 */
    if (loadsSize <= 0) return 0;
    /* 复制一份以便排序，不改动原数组语义 */
    int* a = (int*)malloc(loadsSize * sizeof(int));
    long long total = 0;
    for (int i = 0; i < loadsSize; i++) {
        a[i] = loads[i];
        total += loads[i];
    }
    /* 降序：优先抽大负载 */
    qsort(a, loadsSize, sizeof(int), cmp_desc);
    long long s = 0;
    int ans = loadsSize;
    for (int i = 0; i < loadsSize; i++) {
        s += a[i];
        if (s * 2 > total) {
            ans = i + 1;
            break;
        }
    }
    free(a);
    return ans;
}
