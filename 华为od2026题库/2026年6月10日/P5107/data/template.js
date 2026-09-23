// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    const commaIdx = line.lastIndexOf(',');
    const snStr = line.substring(0, commaIdx).trim();
    const mStr = line.substring(commaIdx + 1).trim();
    const sn = JSON.parse(snStr);
    const m = parseInt(mStr, 10);
    console.log(rearrangeSN(sn, m));
});
