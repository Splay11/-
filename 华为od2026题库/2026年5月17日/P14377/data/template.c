#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 100000

int countWinningHands(int* colors, int* numbers);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);

    // remove newlines
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 找到 "], " 作为两个数组的分界线
    int split = 0;
    for (int i = 0; i < len; i++) {
        if (line[i] == ']' && i + 2 < len && line[i + 1] == ',' && line[i + 2] == ' ') {
            split = i + 1;
            break;
        }
    }

    int colors[14], numbers[14];
    int cnt = 0;

    // 解析第一个数组（colors）
    for (int i = 0; i < split && cnt < 14; ) {
        while (i < split && (line[i] == '[' || line[i] == ']' || line[i] == ',' || line[i] == ' ' || line[i] == '，')) i++;
        if (i >= split) break;
        int val = 0;
        while (i < split && line[i] >= '0' && line[i] <= '9') {
            val = val * 10 + (line[i] - '0');
            i++;
        }
        colors[cnt++] = val;
    }

    // 解析第二个数组（numbers）
    cnt = 0;
    for (int i = split; i < len && cnt < 14; ) {
        while (i < len && (line[i] == '[' || line[i] == ']' || line[i] == ',' || line[i] == ' ' || line[i] == '，')) i++;
        if (i >= len) break;
        int val = 0;
        while (i < len && line[i] >= '0' && line[i] <= '9') {
            val = val * 10 + (line[i] - '0');
            i++;
        }
        numbers[cnt++] = val;
    }

    int result = countWinningHands(colors, numbers);
    printf("%d\n", result);

    return 0;
}
