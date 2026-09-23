// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 5,[(2,1)]
    const commaIndex = line.indexOf(',');
    const n = parseInt(line.substring(0, commaIndex).trim());
    const guardsPart = line.substring(commaIndex + 1).trim();

    // 去掉外层方括号
    const inner = guardsPart.slice(1, -1).trim();
    let guards = [];
    if (inner.length > 0) {
        guards = inner.split('),(').map(s => {
            s = s.replace('(', '').replace(')', '');
            const [x, y] = s.split(',').map(num => parseInt(num.trim()));
            return [x, y];
        });
    }

    console.log(JSON.stringify(countShortestPaths(n, guards)));
});
