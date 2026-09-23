#include <string.h>
#include <stdlib.h>

/**
 * @param lights 初始灯带状态字符串（不含引号）
 * @param t 秒数
 * @return t 秒后的灯带状态字符串（不含引号，需调用方 free）
 */
char* lightStripTransform(char* lights, int t) {
    char* result = (char*)malloc(17);
    strcpy(result, lights);
    return result;
}
