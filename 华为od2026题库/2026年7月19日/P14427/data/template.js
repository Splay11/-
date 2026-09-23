const fs = require('fs');
process.nextTick(() => {
    let line = fs.readFileSync(0, 'utf8').trim();

    // 去掉字符串两端的引号
    let record = line;
    if (line.length >= 2 && line[0] === '"' && line[line.length - 1] === '"') {
        record = line.slice(1, -1);
    }

    // 调用用户代码
    const res = findRepeatedServiceTypes(record);

    // 按 [r,g,m] 格式输出
    let output = '[';
    for (let i = 0; i < res.length; i++) {
        if (i > 0) output += ',';
        output += res[i];
    }
    output += ']';
    console.log(output);
});
