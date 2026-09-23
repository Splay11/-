#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    // 读取整行输入（含最大长度余量）
    char s[1005];
    if (!fgets(s, sizeof(s), stdin)) return 0;
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r'))
        s[--len] = '\0';

    // 调用用户代码（返回由 malloc 分配的字符串）
    char* ans = compress(s);
    printf("%s\n", ans);
    free(ans);
    return 0;
}
