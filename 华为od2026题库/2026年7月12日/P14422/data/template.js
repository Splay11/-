// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    // 读取整行输入（单行二维数组 [[priority, weight], ...]）
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析二维整型数组
    const packets = JSON.parse(line);

    // 调用用户代码
    const ans = findPacket(packets);

    // 按题面样例格式输出：[id1,id2,...]（无空格）
    console.log('[' + ans.join(',') + ']');
});
