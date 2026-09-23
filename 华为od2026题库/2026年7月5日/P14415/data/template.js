const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    // 解析：teamNum,[[matches...]]
    const comma = line.indexOf(',');
    const teamNum = parseInt(line.substring(0, comma));
    const rest = line.substring(comma + 1);
    const matches = JSON.parse(rest);

    const result = getTopThree(teamNum, matches);
    console.log(JSON.stringify(result));
});
