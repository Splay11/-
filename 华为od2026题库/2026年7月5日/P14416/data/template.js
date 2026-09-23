const fs = require('fs');
process.nextTick(() => {
    const line = fs.readFileSync(0, 'utf8').trim();

    const comma = line.indexOf(',');
    const splitLine = parseInt(line.substring(0, comma));
    const rest = line.substring(comma + 1);
    const sqlText = JSON.parse(rest);

    console.log(splitSQLToFiles(splitLine, sqlText));
});
