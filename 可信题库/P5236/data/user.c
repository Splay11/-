#include <stdlib.h>

typedef struct {
    int rowNum;
    int colNum;
    char* content;
} Cell;

/**
 * Note: The returned array must be malloced, assume caller calls free().
 * @param table 单元格数组
 * @param tableSize 单元格数量
 * @param returnSize 返回字符串行数
 * @return 表格文本行
 */
char** transformTable(Cell* table, int tableSize, int* returnSize) {
    (void)table;
    (void)tableSize;
    *returnSize = 0;
    return NULL;
}
