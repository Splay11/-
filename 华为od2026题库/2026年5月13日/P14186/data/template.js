// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: 5,3,[[1,5],[2,3],[3,7],[4,6],[5,4]]
    const firstComma = input.indexOf(',');
    const secondComma = input.indexOf(',', firstComma + 1);
    const n = parseInt(input.substring(0, firstComma).trim());
    const k = parseInt(input.substring(firstComma + 1, secondComma).trim());
    const packetsStr = input.substring(secondComma + 1).trim();
    const packets = JSON.parse(packetsStr);
    console.log(JSON.stringify(processPackets(n, k, packets)));
});
