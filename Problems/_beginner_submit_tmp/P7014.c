int maxOnline(int* changes, int changesSize) {
    /* 空序列峰值 0 */
    int cur = 0;
    int ans = 0;
    for (int i = 0; i < changesSize; i++) {
        /* 累加并更新峰值 */
        cur += changes[i];
        if (cur > ans) ans = cur;
    }
    return ans;
}
