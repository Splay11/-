// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: ["Error in system", "warning: error detected", "No errors found"],["error", "warning"]
    const separatorIndex = input.indexOf('],[');
    const logsStr = input.substring(0, separatorIndex + 1);
    const keywordsStr = input.substring(separatorIndex + 2);
    const logs = JSON.parse(logsStr);
    const keywords = JSON.parse(keywordsStr);
    console.log(JSON.stringify(analyzeLogKeywords(logs, keywords)));
});
