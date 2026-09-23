// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8').trim();
    // 输入带双引号包裹，使用 JSON.parse 解析为字符串
    const inputStr = JSON.parse(raw);
    console.log(processExpression(inputStr));
});
