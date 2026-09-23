// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: ["Zhangsan", "Lisi", "Wangwu"],["Zhangsan", "Lisi", "Zhangsan"]

    const commaIndex = input.indexOf('],[');
    const namesStr = input.substring(0, commaIndex + 1);
    const ballotsStr = input.substring(commaIndex + 2);

    const names = JSON.parse(namesStr);
    const ballotTickets = JSON.parse(ballotsStr);

    console.log(JSON.stringify(getClassMonitor(names, ballotTickets)));
});
