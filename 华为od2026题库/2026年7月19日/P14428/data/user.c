#include <stdlib.h>

/**
 * @param warehouses        扁平化的仓库数据数组
 * @param warehousesSize    warehouses 元素个数
 * @param queries           查询数组，每行 [warehouseId, startDay, endDay]
 * @param queriesSize       查询个数
 * @param queriesColSize    每个查询的列数（均为 3）
 * @param numOfWarehouse    仓库个数
 * @param returnSize        返回行数（由函数填写）
 * @param returnColumnSizes 返回每行列数（由函数填写）
 * @return                  int** 每行 [累计净利润, 累计损耗, 风控标记]
 */
int** getWarehouseReport(int* warehouses, int warehousesSize, int** queries, int queriesSize,
                         int* queriesColSize, int numOfWarehouse, int* returnSize, int** returnColumnSizes) {
    *returnSize = 0;
    return 0;
}
