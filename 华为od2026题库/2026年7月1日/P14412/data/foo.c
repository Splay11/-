#include <stdlib.h>

typedef struct {
    int id;
    int cnt;
    int first;
} Item;

static int cmp(const void* a, const void* b) {
    Item* x = (Item*)a;
    Item* y = (Item*)b;
    if (x->cnt != y->cnt) return y->cnt - x->cnt; // 件数降序
    return x->first - y->first;                     // 首次出现升序
}

int* warehouseInventory(int* items, int itemsSize, int* returnSize) {
    // 最多 100 个 item，每种编号可能不同，用简单方式
    // 统计：cnt[id] 需要 hash，但 n≤100 可暴力
    int unique[100], cnt[100], firstPos[100];
    int uniCount = 0;

    for (int i = 0; i < itemsSize; i++) {
        int x = items[i];
        int found = -1;
        for (int j = 0; j < uniCount; j++) {
            if (unique[j] == x) { found = j; break; }
        }
        if (found == -1) {
            unique[uniCount] = x;
            cnt[uniCount] = 1;
            firstPos[uniCount] = i;
            uniCount++;
        } else {
            cnt[found]++;
        }
    }

    Item* arr = (Item*)malloc(uniCount * sizeof(Item));
    for (int i = 0; i < uniCount; i++) {
        arr[i].id = unique[i];
        arr[i].cnt = cnt[i];
        arr[i].first = firstPos[i];
    }

    qsort(arr, uniCount, sizeof(Item), cmp);

    int* result = (int*)malloc(uniCount * sizeof(int));
    for (int i = 0; i < uniCount; i++) result[i] = arr[i].id;
    *returnSize = uniCount;
    free(arr);
    return result;
}
