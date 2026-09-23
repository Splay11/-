// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: 3,[[1,5],[2,3],[4,6]]
    const firstComma = input.indexOf(',');
    const playerCount = parseInt(input.substring(0, firstComma).trim());
    const playerTimeRangeStr = input.substring(firstComma + 1).trim();
    const playerTimeRange = JSON.parse(playerTimeRangeStr);

    console.log(MaxPlayers(playerCount, playerTimeRange));
});
