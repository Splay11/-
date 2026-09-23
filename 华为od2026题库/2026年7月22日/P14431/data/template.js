const fs = require('fs');
process.nextTick(() => {
    // 题面输入为 [a,b,...] 形式，可直接用 JSON 解析
    const line = fs.readFileSync(0, 'utf8').trim();
    const nums = JSON.parse(line);
    // 调用用户代码
    console.log(longestSubarray(nums));
});
