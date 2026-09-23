#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 声明用户函数
int minJumps(char* treeLevelOrder, char* frm, char* to);

#define MAX_LEN 2000000

// 从 s 的 pos 开始提取一个双引号包围的字符串
static void parseQuoted(const char* s, int* pos, char* out) {
    while (s[*pos] && s[*pos] != '"') (*pos)++;
    (*pos)++;  // 跳过左引号
    int oi = 0;
    while (s[*pos] && s[*pos] != '"') {
        out[oi++] = s[*pos];
        (*pos)++;
    }
    out[oi] = '\0';
    (*pos)++;  // 跳过右引号
}

int main() {
    char* line = (char*)malloc(MAX_LEN);
    if (!line || !fgets(line, MAX_LEN, stdin)) {
        if (line) free(line);
        return 0;
    }
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    int pos = 0;
    char treeLevelOrder[MAX_LEN];
    char frm[256];
    char to[256];
    parseQuoted(line, &pos, treeLevelOrder);
    parseQuoted(line, &pos, frm);
    parseQuoted(line, &pos, to);

    int result = minJumps(treeLevelOrder, frm, to);
    printf("%d\n", result);

    free(line);
    return 0;
}
