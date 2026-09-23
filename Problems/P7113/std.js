const fs = require("fs");

// 删完数组 a[i..j] 的最小代价
function minCost(a) {
    const n = a.length;
    // dp[i][j]：把下标 i..j 这一段全部删完的最小代价
    const dp = Array.from({ length: n }, () => Array(n).fill(0));
    // 长度为 1：当前长度是 1，代价就是元素本身
    for (let i = 0; i < n; i++) {
        dp[i][i] = a[i];
    }
    // 按区间长度从小到大填表，保证转移时子区间已经算好
    for (let length = 2; length <= n; length++) {
        for (let i = 0; i + length - 1 < n; i++) {
            const j = i + length - 1;
            // 先删左端 a[i]，代价为当前长度 * a[i]，再加上删完剩余区间的最优代价
            const left = length * a[i] + dp[i + 1][j];
            // 先删右端 a[j]，同理
            const right = length * a[j] + dp[i][j - 1];
            dp[i][j] = left < right ? left : right;
        }
    }
    return dp[0][n - 1];
}

function main() {
    const tokens = fs.readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
    const n = tokens[0];
    const a = tokens.slice(1, 1 + n);
    console.log(String(minCost(a)));
}

main();
