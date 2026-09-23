const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 提取所有双引号内的字符串
    const parts = line.match(/"([^"]*)"/g).map(s => s.slice(1, -1));
    const num = parts[0];
    const sourceDigits = parts[1];
    const targetDigits = parts[2];

    console.log('"' + convertNumber(num, sourceDigits, targetDigits) + '"');
});
