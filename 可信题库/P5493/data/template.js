const fs = require('fs');
process.nextTick(() => {
    const text = fs.readFileSync(0, 'utf8');
    const lines = text.split(/\r?\n/);
    let obj = null;
    const outs = [];
    const fmt = (arr) => JSON.stringify(arr);
    for (let raw of lines) {
        const line = raw.trim();
        if (!line) continue;
        let m = line.match(/^FileLogger\((-?\d+),\s*(-?\d+)\)$/);
        if (m) {
            obj = new FileLogger(parseInt(m[1], 10), parseInt(m[2], 10));
            outs.push('null');
            continue;
        }
        m = line.match(/^putLog\((-?\d+),\s*(-?\d+)\)$/);
        if (m) {
            outs.push(String(obj.putLog(parseInt(m[1], 10), parseInt(m[2], 10))));
            continue;
        }
        if (line === 'listFiles()') {
            outs.push(fmt(obj.listFiles()));
            continue;
        }
        if (line === 'totalSize()') {
            outs.push(String(obj.totalSize()));
            continue;
        }
        throw new Error('bad op: ' + line);
    }
    if (outs.length) console.log(outs.join('\n'));
});
