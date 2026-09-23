// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 找到两个顶层数组之间的逗号（括号深度为 0 且不在字符串内）
    function findTopLevelComma(s) {
        let inString = false, bracket = 0;
        for (let i = 0; i < s.length; i++) {
            const c = s[i];
            if (c === '"') inString = !inString;
            else if (!inString) {
                if (c === '[') bracket++;
                else if (c === ']') bracket--;
                else if (c === ',' && bracket === 0) return i;
            }
        }
        return -1;
    }

    const comma = findTopLevelComma(line);
    const directDeps = JSON.parse(line.substring(0, comma));
    const depRules = JSON.parse(line.substring(comma + 1));

    const result = getDependencyOrder(directDeps, depRules);

    // 按题面样例格式输出：["name:version",...]（无空格）
    console.log("[" + result.map(x => '"' + x + '"').join(",") + "]");
});
