const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析 JSON 数组
    const nums = JSON.parse(line);

    // 调用用户代码
    const res = sortArrayByParity(nums);

    // 输出 JSON 数组
    console.log(JSON.stringify(res));
});