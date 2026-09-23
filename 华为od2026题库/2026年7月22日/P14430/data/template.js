const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 提取所有整数（支持可选负号）
    const nums = (line.match(/-?\d+/g) || []).map(Number);
    console.log(countDistinctTags(nums));
});
