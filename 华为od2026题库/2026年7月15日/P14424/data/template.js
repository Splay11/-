// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析输入：N,[已交卷学号列表]
    const comma = line.indexOf(',');
    const n = parseInt(line.substring(0, comma).trim());
    const submitted = JSON.parse(line.substring(comma + 1).trim());  // 形如 [1,5,3,...]

    // 调用用户代码
    const ans = findMissingStudents(n, submitted);

    // 按题面格式输出：[a,b,c]（无空格）
    console.log('[' + ans.join(',') + ']');
});
