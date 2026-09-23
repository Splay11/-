#include <stdlib.h>

/**
 * @param n 模块数
 * @param deps 依赖边 [a,b] 表示 a 依赖 b
 * @param depsSize 边数
 * @param depsColSize 每行列数
 * @param buildTime 各模块构建时间
 * @param buildTimeSize n
 * @param changed 变更模块列表
 * @param changedSize 变更数
 * @return 最小重建完成时间
 */
int minRebuildTime(int n, int** deps, int depsSize, int* depsColSize,
                   int* buildTime, int buildTimeSize, int* changed, int changedSize) {
    (void)n; (void)deps; (void)depsSize; (void)depsColSize;
    (void)buildTime; (void)buildTimeSize; (void)changed; (void)changedSize;
    return 0;
}
