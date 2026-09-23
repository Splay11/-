var countIsolatedIntervals = function(intervals) {
    var n = intervals.length;
    var ans = 0;
    for (var i = 0; i < n; i++) {
        var s1 = intervals[i][0], e1 = intervals[i][1];
        var isolated = true;
        for (var j = 0; j < n; j++) {
            if (i === j) continue;
            var s2 = intervals[j][0], e2 = intervals[j][1];
            // 标准区间相交判定
            if (s1 <= e2 && s2 <= e1) {
                isolated = false;
                break;
            }
        }
        if (isolated) ans++;
    }
    return ans;
};
