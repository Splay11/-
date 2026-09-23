// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    // 读取整行输入
    const s = fs.readFileSync(0, 'utf8').split('\n')[0];

    // 调用用户代码
    console.log(compress(s));
});
