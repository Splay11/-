// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 返回从 start 处的 '[' 匹配的 ']' 的下标
    function matchBracket(s, start) {
        let depth = 0;
        for (let i = start; i < s.length; i++) {
            if (s[i] === '[') depth++;
            else if (s[i] === ']') {
                depth--;
                if (depth === 0) return i;
            }
        }
        return -1;
    }

    // warehouses：第一个 [...] 数组
    const p1 = line.indexOf('[');
    const e1 = matchBracket(line, p1);
    const warehouses = JSON.parse(line.substring(p1, e1 + 1));

    // queries：第二个 [[...]] 数组
    const p2 = line.indexOf('[', e1 + 1);
    const e2 = matchBracket(line, p2);
    const queries = JSON.parse(line.substring(p2, e2 + 1));

    // 末尾整数 numOfWarehouse
    const numOfWarehouse = parseInt(line.substring(e2 + 1).trim());

    const res = getWarehouseReport(warehouses, queries, numOfWarehouse);

    // 紧凑输出 [[..],[..]]
    const out = '[' + res.map(row => '[' + row.join(',') + ']').join(',') + ']';
    console.log(out);
});
