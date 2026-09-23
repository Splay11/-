// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 整行即 JSON 字符串数组
    const dates = JSON.parse(line);

    // 调用用户代码
    const ans = normalizeDates(dates);

    // 按题面格式输出：["a","b",...]（无空格）
    console.log('[' + ans.map(s => '"' + s + '"').join(',') + ']');
});
