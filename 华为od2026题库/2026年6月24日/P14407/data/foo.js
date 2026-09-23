var queryNetEnergy = function(commands) {
    // 解析最后一条查询命令
    var query = commands[commands.length - 1];
    var qparts = query.split(',');
    // qparts[0] = "QueryNetEnergy", qparts[1] = version/A, qparts[2]=qs, qparts[3]=qe
    var useAll = qparts[1] === 'A';
    var qs = parseInt(qparts[2], 10);
    var qe = parseInt(qparts[3], 10);
    var maxVersion = useAll ? 1000000000 : parseInt(qparts[1], 10);

    // 按时间段交集比例计算加权贡献
    function weighted(amount, start, end, qs, qe) {
        if (start > qe || end < qs) return 0.0;
        var duration = end - start;
        if (duration === 0) {
            if (qs <= start && start <= qe) return amount;
            return 0.0;
        }
        var os = Math.max(start, qs);
        var oe = Math.min(end, qe);
        if (os > oe) return 0.0;
        var overlap = oe - os;
        return amount * overlap / duration;
    }

    // 四舍五入并夹到 int32 范围
    function roundToI32(x) {
        var val = x >= 0 ? Math.floor(x + 0.5) : Math.ceil(x - 0.5);
        if (val > 2147483647) return 2147483647;
        if (val < -2147483648) return -2147483648;
        return val;
    }

    var total = 0.0;
    var version = 0;
    for (var i = 0; i < commands.length - 1; i++) {
        version++;
        if (version > maxVersion) break;

        var parts = commands[i].split(',');
        if (parts[0] === 'AddProductionRecord') {
            // AddProductionRecord,type,amount,start,end
            var amount = parseInt(parts[2], 10);
            var start = parseInt(parts[3], 10);
            var end   = parseInt(parts[4], 10);
            total += weighted(amount, start, end, qs, qe);
        } else if (parts[0] === 'AddConsumptionRecord') {
            // AddConsumptionRecord,amount,start,end
            var amount = parseInt(parts[1], 10);
            var start = parseInt(parts[2], 10);
            var end   = parseInt(parts[3], 10);
            total -= weighted(amount, start, end, qs, qe);
        }
    }

    return roundToI32(total);
};
