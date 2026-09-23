var countKeys = function(s) {
    // cnt[encoded] = count
    var cnt = new Array(36).fill(0);
    var n = s.length;
    var i = 0;

    // 解析按键
    while (i < n) {
        if (i + 1 < n && s[i] === 'u' && s[i + 1] === 'u') {
            // uu → j (encoded as 19)
            cnt[19]++;
            i += 2;
        } else if (i + 1 < n && s[i] === 't' && s[i + 1] === 't') {
            // tt → b (encoded as 11)
            cnt[11]++;
            i += 2;
        } else {
            // 普通按键
            var c = s[i];
            var enc;
            if (c >= '0' && c <= '9') {
                enc = c.charCodeAt(0) - 48; // '0' = 48
            } else {
                enc = c.charCodeAt(0) - 97 + 10; // 'a' = 97
            }
            cnt[enc]++;
            i++;
        }
    }

    // 收集按键，按次数降序排序
    var result = [];
    for (var k = 0; k < 36; k++) {
        if (cnt[k] > 0) {
            result.push([k, cnt[k]]);
        }
    }

    // 按次数降序，同次数按键值升序
    result.sort(function(a, b) {
        if (b[1] !== a[1]) return b[1] - a[1];
        return a[0] - b[0];
    });

    return result;
};
