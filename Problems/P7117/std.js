const fs = require("fs");

const INF = 1000000000;

// 把非 0 格子当成城市，用状压 DP 求从中心出发并返回的最短回路
function minSteps(grid) {
    const n = grid.length;
    const m = grid[0].length;
    const sr = Math.floor(n / 2);
    const sc = Math.floor(m / 2);
    // 点 0 固定为中心，其余点为中心以外的非 0 格子
    const pts = [[sr, sc]];
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < m; j++) {
            if (grid[i][j] !== 0 && (i !== sr || j !== sc)) {
                pts.push([i, j]);
            }
        }
    }
    const k = pts.length;
    if (k === 1) {
        return 0;
    }
    const dist = Array.from({ length: k }, () => Array(k).fill(0));
    for (let a = 0; a < k; a++) {
        for (let b = 0; b < k; b++) {
            dist[a][b] = Math.abs(pts[a][0] - pts[b][0]) + Math.abs(pts[a][1] - pts[b][1]);
        }
    }
    const full = 1 << k;
    // dp[mask][i]：已访问集合为 mask、当前停在 i 的最少步数
    const dp = Array.from({ length: full }, () => Array(k).fill(INF));
    dp[1][0] = 0;
    for (let mask = 0; mask < full; mask++) {
        for (let i = 0; i < k; i++) {
            if (((mask >> i) & 1) === 0 || dp[mask][i] >= INF) {
                continue;
            }
            for (let j = 0; j < k; j++) {
                if ((mask >> j) & 1) {
                    continue;
                }
                const nxt = mask | (1 << j);
                const cand = dp[mask][i] + dist[i][j];
                if (cand < dp[nxt][j]) {
                    dp[nxt][j] = cand;
                }
            }
        }
    }
    const end = full - 1;
    let ans = INF;
    // 访问完全部点后，还要走回中心
    for (let i = 0; i < k; i++) {
        const cand = dp[end][i] + dist[i][0];
        if (cand < ans) {
            ans = cand;
        }
    }
    return ans;
}

function main() {
    const tokens = fs.readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
    let p = 0;
    const n = tokens[p++];
    const m = tokens[p++];
    const grid = [];
    for (let i = 0; i < n; i++) {
        const row = [];
        for (let j = 0; j < m; j++) {
            row.push(tokens[p++]);
        }
        grid.push(row);
    }
    console.log(String(minSteps(grid)));
}

main();
