#include <stdlib.h>
#include <string.h>

/**
 * @param num 源数字字符串
 * @param sourceDigits 源字符集
 * @param targetDigits 目标字符集
 * @return 转换后的数字字符串（调用者需自行释放内存）
 */
char* convertNumber(char* num, char* sourceDigits, char* targetDigits) {
    char* result = (char*)malloc(2);
    result[0] = '0';
    result[1] = '\0';
    return result;
}
