#include <stdlib.h>
#include <string.h>

/**
 * @param s 输入字符串（仅含大小写英文字母）
 * @return 压缩后的字符串（由 malloc 分配，以 '\0' 结尾，调用方负责 free）
 */
char* compress(const char* s) {
    // 仅占位实现：返回空字符串（malloc 分配，可被安全 free）
    char* res = (char*)malloc(1);
    res[0] = '\0';
    return res;
}
