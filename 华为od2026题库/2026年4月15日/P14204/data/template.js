// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: [1,2],[10,12]
    const commaIndex = line.indexOf('],[');
    const cardAStr = line.substring(0, commaIndex + 1);
    const cardBStr = line.substring(commaIndex + 2);
    const cardA = JSON.parse(cardAStr);
    const cardB = JSON.parse(cardBStr);
    console.log(catFishCardGame(cardA, cardB));
});
