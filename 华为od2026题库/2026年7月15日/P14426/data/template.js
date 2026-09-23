const fs = require('fs');
const line = fs.readFileSync(0, 'utf8').trim();

// 从字符串中提取所有整数（忽略非数字字符，如逗号、括号）
function extractInts(s) {
    const res = [];
    let cur = 0, have = false;
    for (const ch of s) {
        if (ch >= '0' && ch <= '9') {
            cur = cur * 10 + (ch.charCodeAt(0) - 48);
            have = true;
        } else if (have) {
            res.push(cur);
            cur = 0;
            have = false;
        }
    }
    if (have) res.push(cur);
    return res;
}

// 提取全部整数：前 3 个为 n, m, w，其余每 3 个为一条路线
const a = extractInts(line);
const n = a[0], m = a[1], w = a[2];
const roads = [];
for (let i = 3; i + 2 < a.length; i += 3) {
    roads.push([a[i], a[i + 1], a[i + 2]]);
}

const result = minCost(n, m, w, roads);
console.log(result);
