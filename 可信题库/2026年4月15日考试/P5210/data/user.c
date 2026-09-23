#include <stdlib.h>

/**
 * Return an array of arrays of size *returnSize.
 * The sizes of the arrays are returned as *returnColumnSizes array.
 * Note: Both returned array and *columnSizes array must be malloced, assume caller calls free().
 *
 * @param cards 卡片列表，每张为 [x, y, width, height]
 * @param cardsSize 卡片数量
 * @param cardsColSize 每张卡片的列数（均为 4）
 * @param alignment 对齐方式字符串
 * @param returnSize 返回行数
 * @param returnColumnSizes 返回每行列数
 */
int** alignCards(int** cards, int cardsSize, int* cardsColSize, char* alignment, int* returnSize,
                 int** returnColumnSizes) {
    (void)cards;
    (void)cardsSize;
    (void)cardsColSize;
    (void)alignment;
    *returnSize = 0;
    *returnColumnSizes = NULL;
    return NULL;
}
