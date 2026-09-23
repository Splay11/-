var countProfilePairs = function(profiles, diff) {
    // diff == 0：统计出现至少2次的档位
    if (diff === 0) {
        var freq = {};
        for (var i = 0; i < profiles.length; i++) {
            var v = profiles[i];
            freq[v] = (freq[v] || 0) + 1;
        }
        var ans = 0;
        for (var k in freq) {
            if (freq[k] >= 2) ans++;
        }
        return ans;
    }

    // diff > 0：对每个唯一档位检查 v+diff 是否存在
    var seen = new Set(profiles);
    var ans = 0;
    seen.forEach(function(v) {
        if (seen.has(v + diff)) ans++;
    });
    return ans;
};
