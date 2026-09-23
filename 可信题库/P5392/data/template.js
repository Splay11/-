const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8');
    const lines = raw.split(/\r?\n/);
    let obj = null;
    const outs = [];
    for (let line of lines) {
        line = line.trim();
        if (!line) continue;
        let m;
        if (line === 'FileLockBoard()') {
            obj = new FileLockBoard();
            outs.push('null');
        } else if ((m = line.match(/^lock\((-?\d+),\s*(-?\d+)\)$/))) {
            outs.push(obj.lock(+m[1], +m[2]) ? 'true' : 'false');
        } else if ((m = line.match(/^unlock\((-?\d+),\s*(-?\d+)\)$/))) {
            outs.push(obj.unlock(+m[1], +m[2]) ? 'true' : 'false');
        } else if ((m = line.match(/^holder\((-?\d+)\)$/))) {
            outs.push(String(obj.holder(+m[1])));
        } else if (line === 'lockedCount()') {
            outs.push(String(obj.lockedCount()));
        } else {
            throw new Error('bad op: ' + line);
        }
    }
    if (outs.length) process.stdout.write(outs.join('\n') + '\n');
});
