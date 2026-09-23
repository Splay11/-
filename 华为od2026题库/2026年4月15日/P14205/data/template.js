// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    let input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: "t"
    const s = JSON.parse(input);
    console.log(JSON.stringify(countKeys(s)));
});
