#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 10000
#define MAX_TOKENS 200

int* intersectionWaitingTime(int R, int G, char* directions, int directionsSize,
                             int* arrivalTimes, int arrivalTimesSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 解析 R
    char* c1 = strchr(line, ',');
    int R = atoi(line);

    // 解析 G
    char* rest1 = c1 + 1;
    char* c2 = strchr(rest1, ',');
    *c2 = '\0';
    int G = atoi(rest1);

    // 剩余部分: [E,S,W,N],[0,1,3,6]
    char* rest2 = c2 + 1;
    char* split = strstr(rest2, "],[");
    char* dirsStr = rest2 + 1;  // 跳过 '['
    *(split + 1) = '\0';        // 截断 dirsStr
    char* timesStr = split + 3;  // 跳过 '],['
    // 去掉 timesStr 末尾的 ']'
    int timesLen = strlen(timesStr);
    if (timesLen > 0 && timesStr[timesLen - 1] == ']')
        timesStr[timesLen - 1] = '\0';

    // 解析方向字符数组
    char directions[MAX_TOKENS];
    int directionsSize = 0;
    char* tok = strtok(dirsStr, ",");
    while (tok) {
        while (*tok == ' ') tok++;
        directions[directionsSize++] = tok[0];
        tok = strtok(NULL, ",");
    }

    // 解析到达时间数组
    int arrivalTimes[MAX_TOKENS];
    int arrivalTimesSize = 0;
    tok = strtok(timesStr, ",");
    while (tok) {
        arrivalTimes[arrivalTimesSize++] = atoi(tok);
        tok = strtok(NULL, ",");
    }

    int returnSize;
    int* result = intersectionWaitingTime(R, G, directions, directionsSize,
                                          arrivalTimes, arrivalTimesSize, &returnSize);
    printf("[%d,%d]\n", result[0], result[1]);

    free(result);
    return 0;
}

#include "user.c"
