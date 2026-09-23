#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LEN 200000

// 复制子串（调用方负责 free）
static char* my_strndup(const char* s, int len) {
    char* r = (char*)malloc(len + 1);
    strncpy(r, s, len);
    r[len] = '\0';
    return r;
}

// 提取字符串中的所有整数（支持负数），返回动态数组
static int* extractInts(const char* s, int* outCount) {
    int cap = 64, cnt = 0;
    int* res = (int*)malloc(cap * sizeof(int));
    int i = 0;
    while (s[i]) {
        if (isdigit((unsigned char)s[i]) || s[i] == '-') {
            int j = i;
            if (s[i] == '-') j++;
            while (s[j] >= '0' && s[j] <= '9') j++;
            if (cnt >= cap) { cap *= 2; res = (int*)realloc(res, cap * sizeof(int)); }
            res[cnt++] = atoi(s + i);
            i = j;
        } else {
            i++;
        }
    }
    *outCount = cnt;
    return res;
}

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 找最外层逗号，切分为 4 段
    int commas[3];
    int ccount = 0;
    int depth = 0;
    for (int i = 0; i < len && ccount < 3; i++) {
        if (line[i] == '[') depth++;
        else if (line[i] == ']') depth--;
        else if (line[i] == ',' && depth == 0) commas[ccount++] = i;
    }

    char* sN = my_strndup(line, commas[0]);
    char* sEdges = my_strndup(line + commas[0] + 1, commas[1] - commas[0] - 1);
    char* sStartA = my_strndup(line + commas[1] + 1, commas[2] - commas[1] - 1);
    char* sPatrol = my_strndup(line + commas[2] + 1, len - commas[2] - 1);

    int n = atoi(sN);

    int eCnt;
    int* eInts = extractInts(sEdges, &eCnt);
    int edgesSize = eCnt / 2;
    int** edges = (int**)malloc(edgesSize * sizeof(int*));
    int* edgesColSize = (int*)malloc(edgesSize * sizeof(int));
    for (int i = 0; i < edgesSize; i++) {
        edges[i] = (int*)malloc(2 * sizeof(int));
        edges[i][0] = eInts[2 * i];
        edges[i][1] = eInts[2 * i + 1];
        edgesColSize[i] = 2;
    }

    int startA = atoi(sStartA);

    int pCnt;
    int* patrolPath = extractInts(sPatrol, &pCnt);

    int ans = minMeetRounds(n, edges, edgesSize, edgesColSize, startA, patrolPath, pCnt);
    printf("%d\n", ans);

    free(sN); free(sEdges); free(sStartA); free(sPatrol);
    free(eInts);
    for (int i = 0; i < edgesSize; i++) free(edges[i]);
    free(edges); free(edgesColSize);
    free(patrolPath);
    return 0;
}
