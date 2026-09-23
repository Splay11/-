// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 5,2,3,[10,20,30,40,50]
    const parts = line.split(',');
    const n = parseInt(parts[0].trim());
    const m = parseInt(parts[1].trim());
    const k = parseInt(parts[2].trim());
    const arrStr = line.substring(line.indexOf('['));
    const demands = JSON.parse(arrStr);

    console.log(maxChargingDemand(n, m, k, demands));
});
