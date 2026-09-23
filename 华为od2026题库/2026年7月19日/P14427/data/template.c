#include "foo.c"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LEN 200000

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;

    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 去掉字符串两端的引号
    char* record = line;
    if (len >= 2 && line[0] == '"' && line[len - 1] == '"') {
        record = line + 1;
        line[len - 1] = '\0';
    }

    int returnSize;
    char** res = findRepeatedServiceTypes(record, &returnSize);

    // 按 [r,g,m] 格式输出
    printf("[");
    for (int i = 0; i < returnSize; i++) {
        if (i > 0) printf(",");
        printf("%s", res[i]);
    }
    printf("]\n");

    for (int i = 0; i < returnSize; i++) free(res[i]);
    free(res);
    return 0;
}
