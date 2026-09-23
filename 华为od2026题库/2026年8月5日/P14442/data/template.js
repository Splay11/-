const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析输入：JSON 整数数组 [a1,a2,...]
    const nums = JSON.parse(line);

    // 调用用户代码
    console.log(longestNonConsecutiveSubstring(nums));
});
