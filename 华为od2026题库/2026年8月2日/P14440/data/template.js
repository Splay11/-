// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析 JSON 字符串列表，如 ["a","b","c"]
    const versions = JSON.parse(line);

    // 调用用户代码
    const result = findLatestVersion(versions);
    console.log('"' + result + '"');
});
