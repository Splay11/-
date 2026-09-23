#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000
#define MAX_SIZE 100

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    int N = 0, T = 0;
    int accuracy[MAX_SIZE], latency[MAX_SIZE];
    int accSize = 0, latSize = 0;
    const char* p = line;

    // 解析 N 和 T
    sscanf(p, "%d,%d,", &N, &T);
    // 移动指针跳过 N,T,
    while (*p && *p != '{') p++;
    if (*p != '{') return 0;

    // 解析 accuracy 数组
    p++;
    while (*p && *p != '}') {
        if (*p >= '0' && *p <= '9') {
            int val = atoi(p);
            accuracy[accSize++] = val;
            while (*p >= '0' && *p <= '9') p++;
        } else p++;
    }
    while (*p && *p != '{') p++;
    if (*p != '{') return 0;

    // 解析 latency 数组
    p++;
    while (*p && *p != '}') {
        if (*p >= '0' && *p <= '9') {
            int val = atoi(p);
            latency[latSize++] = val;
            while (*p >= '0' && *p <= '9') p++;
        } else p++;
    }

    // 传入模型数量 accSize，使 C 语言函数能确定数组长度
    int result = maxTotalAccuracy(N, T, accuracy, accSize, latency);
    printf("%d\n", result);
    return 0;
}
