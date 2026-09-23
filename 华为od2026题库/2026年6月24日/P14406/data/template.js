// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: [1,5,3,4,2],2
    const commaIndex = input.lastIndexOf(',');
    const profilesStr = input.substring(0, commaIndex).trim();
    const diffStr = input.substring(commaIndex + 1).trim();
    const profiles = JSON.parse(profilesStr);
    const diff = parseInt(diffStr, 10);

    console.log(countProfilePairs(profiles, diff));
});
