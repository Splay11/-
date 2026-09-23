var maxEnergyDivisibleByK = function(nums, n, k) {
    var queues = new Array(k);
    for (var i = 0; i < k; i++) {
        queues[i] = [];
    }

    queues[0].push([0, 0]);

    var prefix = 0;
    var ans = -Infinity;
    var found = false;

    var getMod = function(x) {
        var m = x % k;
        return m < 0 ? m + k : m;
    };

    for (var r = 1; r <= 2 * n; r++) {
        prefix += nums[(r - 1) % n];
        var mod = getMod(prefix);
        var q = queues[mod];

        while (q.length > 0 && q[0][0] < r - n) {
            q.shift();
        }

        if (q.length > 0) {
            ans = Math.max(ans, prefix - q[0][1]);
            found = true;
        }

        while (q.length > 0 && q[q.length - 1][1] >= prefix) {
            q.pop();
        }

        q.push([r, prefix]);
    }

    return found ? ans : 0;
};
