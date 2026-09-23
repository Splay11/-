// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // === 解析输入：priceRecords, hours, priceArray ===
    const firstComma = line.indexOf(',');
    const priceRecords = parseInt(line.substring(0, firstComma));

    const rest = line.substring(firstComma + 1);
    const secondComma = rest.indexOf(',');
    const hours = parseInt(rest.substring(0, secondComma));

    // 解析数组 [a,b,c,...]
    const arrStr = rest.substring(secondComma + 1);
    const inner = arrStr.substring(1, arrStr.length - 1);
    const priceArray = inner.split(',').map(Number);

    // 调用用户代码
    console.log(findBestChargingTime(priceRecords, hours, priceArray));
});
