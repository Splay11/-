#include <stdlib.h>

static int cmp(const void* a, const void* b) {
    int x = *(int*)a, y = *(int*)b;
    if (x < y) return -1;
    if (x > y) return 1;
    return 0;
}

int countProfilePairs(int* profiles, int profilesSize, int diff) {
    int* arr = (int*)malloc(profilesSize * sizeof(int));
    for (int i = 0; i < profilesSize; i++) arr[i] = profiles[i];
    qsort(arr, profilesSize, sizeof(int), cmp);

    // diff == 0：统计出现至少2次的值
    if (diff == 0) {
        int ans = 0;
        for (int i = 0; i < profilesSize; i++) {
            int cnt = 1;
            while (i + 1 < profilesSize && arr[i] == arr[i + 1]) { cnt++; i++; }
            if (cnt >= 2) ans++;
        }
        free(arr);
        return ans;
    }

    // diff > 0：对每个唯一值二分查找 v+diff
    int ans = 0;
    for (int i = 0; i < profilesSize; i++) {
        if (i > 0 && arr[i] == arr[i - 1]) continue; // 跳过重复值
        long long target = (long long)arr[i] + diff;
        // 防溢出：只查找在 int 范围内的 target
        if (target > 2147483647LL || target < -2147483648LL) continue;
        int t = (int)target;
        int lo = 0, hi = profilesSize - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] == t) { ans++; break; }
            if (arr[mid] < t) lo = mid + 1;
            else hi = mid - 1;
        }
    }

    free(arr);
    return ans;
}
