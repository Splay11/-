// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: 100,4,0,1,10
    const parts = line.split(',').map(x => parseInt(x.trim(), 10));
    const capacity = parts[0];
    const align = parts[1];
    const read_index = parts[2];
    const write_index = parts[3];
    const pkt_size = parts[4];
    console.log(calcWriteIndex(capacity, align, read_index, write_index, pkt_size));
});
