// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: [3,2,1],[[0,1]]
    const commaIndex = line.indexOf('],[');
    const dataStr = line.substring(0, commaIndex + 1);
    const opsStr = line.substring(commaIndex + 2);
    const data = JSON.parse(dataStr);
    const operations = JSON.parse(opsStr);

    console.log(JSON.stringify(processDataArray(data, operations)));
});
