const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析 k,m,w,[...]
    const firstComma = line.indexOf(',');
    const k = parseInt(line.substring(0, firstComma).trim());

    const rest1 = line.substring(firstComma + 1);
    const secondComma = rest1.indexOf(',');
    const m = parseInt(rest1.substring(0, secondComma).trim());

    const rest2 = rest1.substring(secondComma + 1);
    const thirdComma = rest2.indexOf(',');
    const w = parseInt(rest2.substring(0, thirdComma).trim());

    const rest3 = rest2.substring(thirdComma + 1).trim();
    const a = JSON.parse(rest3);

    // 调用用户代码
    console.log(minSkillSegments(k, m, w, a));
});
