// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 输入形如: ["Zhangsan", "Lisi", "Wangwu"],["Zhangsan", "Lisi", "Zhangsan"]
    const splitIdx = line.indexOf('],[');
    const studentsStr = line.substring(0, splitIdx + 1);
    const votesStr = '[' + line.substring(splitIdx + 3);
    const students = JSON.parse(studentsStr);
    const votes = JSON.parse(votesStr);

    console.log('"' + electMonitor(students, votes) + '"');
});
