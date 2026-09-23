// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 9,2,[10,5,20,10,5,15,10,5,25]
    const firstComma = line.indexOf(',');
    const secondComma = line.indexOf(',', firstComma + 1);

    const n = parseInt(line.substring(0, firstComma).trim());
    const w = parseInt(line.substring(firstComma + 1, secondComma).trim());
    const scoresStr = line.substring(secondComma + 1).trim();
    const scores = JSON.parse(scoresStr);

    console.log(JSON.stringify(findMaintenanceWindow(n, w, scores)));
});
