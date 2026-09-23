// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 3,5,[[10,1,0],[10,1,0],[10,1,0],[10,1,0],[10,1,0]]
    const firstComma = input.indexOf(',');
    const secondComma = input.indexOf(',', firstComma + 1);
    const n = parseInt(input.substring(0, firstComma).trim());
    const m = parseInt(input.substring(firstComma + 1, secondComma).trim());
    const carsStr = input.substring(secondComma + 1).trim();
    const cars = JSON.parse(carsStr);

    console.log(countFailedCharging(n, cars));
});
