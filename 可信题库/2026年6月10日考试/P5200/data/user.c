#include <stdlib.h>

/**
 * Note: The returned array must be malloced, assume caller calls free().
 * @param rects 矩形列表，每项 [x1,y1,x2,y2]
 * @param rectsSize 矩形数量
 * @param rectsColSize 每行列数（均为 4）
 * @param queryRect 查询矩形 [qx1,qy1,qx2,qy2]
 * @param queryRectSize 查询矩形长度
 * @param returnSize 返回数组长度
 * @return 可见控件编号（降序）
 */
int* queryVisibleRects(int** rects, int rectsSize, int* rectsColSize, int* queryRect, int queryRectSize,
                       int* returnSize) {
    (void)rects;
    (void)rectsSize;
    (void)rectsColSize;
    (void)queryRect;
    (void)queryRectSize;
    *returnSize = 0;
    return NULL;
}
