var selectMaxWeightPolicies = function(n, k, weights, conflicts) {
    if (k < 0 || k > n) return [];

    // 构建冲突位掩码
    var conflictMask = new Array(n).fill(0);
    for (var i = 0; i < conflicts.length; i++) {
        var a = conflicts[i][0] - 1;
        var b = conflicts[i][1] - 1;
        conflictMask[a] |= 1 << b;
        conflictMask[b] |= 1 << a;
    }

    // popcount
    function popcount(x) {
        x = x - ((x >> 1) & 0x55555555);
        x = (x & 0x33333333) + ((x >> 2) & 0x33333333);
        x = (x + (x >> 4)) & 0x0F0F0F0F;
        x = x + (x >> 8);
        x = x + (x >> 16);
        return x & 0x3F;
    }

    // 判断独立集
    function isIndependent(mask) {
        var m = mask;
        while (m !== 0) {
            var lsb = m & -m;
            var i = 0;
            // 计算 lsb 的位位置
            while (((lsb >> i) & 1) === 0) i++;
            if ((conflictMask[i] & mask) !== 0) return false;
            m ^= lsb;
        }
        return true;
    }

    var best = null;
    var result = [];
    var totalMasks = 1 << n;

    for (var mask = 0; mask < totalMasks; mask++) {
        if (popcount(mask) !== k) continue;
        if (!isIndependent(mask)) continue;

        var total = 0;
        var combo = [];
        for (var i = 0; i < n; i++) {
            if (mask & (1 << i)) {
                total += weights[i];
                combo.push(i + 1);
            }
        }

        if (best === null || total > best) {
            best = total;
            result = [combo];
        } else if (total === best) {
            result.push(combo);
        }
    }

    if (best === null) return [];
    return result;
};
