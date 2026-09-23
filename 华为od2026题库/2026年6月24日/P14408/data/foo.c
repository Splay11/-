#include <stdlib.h>
#include <string.h>

// popcount for GCC
static int popcount(int x) {
    return __builtin_popcount(x);
}

// 判断 mask 是否为独立集
static int isIndependent(int mask, int* conflictMask) {
    int m = mask;
    while (m) {
        int lsb = m & -m;
        // 获取最低位 1 的位置（0-indexed）
        int i = __builtin_ctz(lsb);
        if (conflictMask[i] & mask) return 0;
        m ^= lsb;
    }
    return 1;
}

int** selectMaxWeightPolicies(int n, int k, int* weights,
                               int** conflicts, int conflictsSize,
                               int* returnSize) {
    if (k < 0 || k > n) {
        *returnSize = 0;
        return NULL;
    }

    // 构建冲突位掩码
    int* conflictMask = (int*)calloc(n, sizeof(int));
    for (int i = 0; i < conflictsSize; i++) {
        int a = conflicts[i][0] - 1;
        int b = conflicts[i][1] - 1;
        conflictMask[a] |= 1 << b;
        conflictMask[b] |= 1 << a;
    }

    int best = -1;
    int* comboList[2000];     // 暂存所有最优组合
    int comboCount = 0;

    int totalMasks = 1 << n;
    for (int mask = 0; mask < totalMasks; mask++) {
        if (popcount(mask) != k) continue;
        if (!isIndependent(mask, conflictMask)) continue;

        // 计算权重和
        int total = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) total += weights[i];
        }

        if (best == -1 || total > best) {
            best = total;
            // 清空之前的组合
            for (int c = 0; c < comboCount; c++) free(comboList[c]);
            comboCount = 0;
            // 记录当前组合（0-terminated）
            int* combo = (int*)malloc((k + 1) * sizeof(int));
            int pos = 0;
            for (int i = 0; i < n; i++) {
                if (mask & (1 << i)) combo[pos++] = i + 1;
            }
            combo[k] = 0; // 终止标记
            comboList[comboCount++] = combo;
        } else if (total == best) {
            int* combo = (int*)malloc((k + 1) * sizeof(int));
            int pos = 0;
            for (int i = 0; i < n; i++) {
                if (mask & (1 << i)) combo[pos++] = i + 1;
            }
            combo[k] = 0;
            comboList[comboCount++] = combo;
        }
    }

    free(conflictMask);

    if (best == -1) {
        *returnSize = 0;
        return NULL;
    }

    // 复制到返回数组
    int** result = (int**)malloc(comboCount * sizeof(int*));
    for (int c = 0; c < comboCount; c++) {
        result[c] = comboList[c];
    }
    *returnSize = comboCount;
    return result;
}
