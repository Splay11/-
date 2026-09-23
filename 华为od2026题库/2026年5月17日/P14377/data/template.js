// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2], [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 4]
    const commaIndex = input.indexOf('],');
    const colorsStr = input.substring(0, commaIndex + 1).trim();
    const numbersStr = input.substring(commaIndex + 2).trim();
    const colors = JSON.parse(colorsStr);
    const numbers = JSON.parse(numbersStr);
    console.log(countWinningHands(colors, numbers));
});
