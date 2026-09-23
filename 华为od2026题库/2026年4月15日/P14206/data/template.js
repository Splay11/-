// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: ["a","b"],[1,2]
    const splitPos = line.indexOf('],[');
    const pathsStr = line.substring(0, splitPos + 1);
    const responseTimesStr = line.substring(splitPos + 2);
    const paths = JSON.parse(pathsStr);
    const responseTimes = JSON.parse(responseTimesStr);
    console.log(JSON.stringify(mergeLogs(paths, responseTimes)));
});
