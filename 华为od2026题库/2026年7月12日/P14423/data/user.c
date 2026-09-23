#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/**
 * @param directDeps 项目直属依赖数组，每条 "name:version:exclusions"
 * @param directDepsSize 直属依赖数量
 * @param depRules 全局依赖规则数组，每条 "name:depname:depversion:exclusions"
 * @param depRulesSize 规则数量
 * @param returnSize 返回数组长度指针
 * @return 按依赖顺序的 "name:version" 字符串数组（调用方负责释放）
 */
char** getDependencyOrder(char** directDeps, int directDepsSize,
                          char** depRules, int depRulesSize, int* returnSize) {
    *returnSize = 0;
    return NULL;
}
