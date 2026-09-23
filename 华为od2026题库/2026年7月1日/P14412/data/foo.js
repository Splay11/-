var warehouseInventory = function(items) {
    // 统计每种编号的出现次数和首次位置
    var cnt = {};
    var first = {};
    for (var i = 0; i < items.length; i++) {
        var x = items[i];
        cnt[x] = (cnt[x] || 0) + 1;
        if (!(x in first)) first[x] = i;
    }
    // 获取所有不同编号
    var ids = Object.keys(cnt).map(Number);
    // 排序：件数降序，件数相同按首次出现位置升序
    ids.sort(function(a, b) {
        if (cnt[b] !== cnt[a]) return cnt[b] - cnt[a];
        return first[a] - first[b];
    });
    return ids;
};
