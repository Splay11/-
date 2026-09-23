const fs = require("fs");

// 当前行动者从 a[i..j] 能拿到的最大得分
function firstScore(a) {
    const n = a.length;
    // pre[k] 为前 k 个数的和，用来 O(1) 求区间和
    const pre = Array(n + 1).fill(0);
    for (let i = 0; i < n; i++) {
        pre[i + 1] = pre[i] + a[i];
    }
    // dp[i][j]：轮到当前玩家时，从下标 i..j 能拿到的最大得分
    const dp = Array.from({ length: n }, () => Array(n).fill(0));
    for (let i = 0; i < n; i++) {
        dp[i][i] = a[i];
    }
    // 按区间长度从小到大填表
    for (let length = 2; length <= n; length++) {
        for (let i = 0; i + length - 1 < n; i++) {
            const j = i + length - 1;
            const tot = pre[j + 1] - pre[i];
            // 取左端则对手得 dp[i+1][j]；取右端则对手得 dp[i][j-1]
            // 当前得分 = 区间和 - 对手得分，应让对手拿到的更少
            const opp = dp[i + 1][j] < dp[i][j - 1] ? dp[i + 1][j] : dp[i][j - 1];
            dp[i][j] = tot - opp;
        }
    }
    return dp[0][n - 1];
}

function main() {
    const tokens = fs.readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
    const n = tokens[0];
    const a = tokens.slice(1, 1 + n);
    console.log(String(firstScore(a)));
}

main();
