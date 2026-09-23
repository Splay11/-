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
        if (line === 'MicQueue()') {
            obj = new MicQueue();
            outs.push('null');
        } else if ((m = line.match(/^enroll\((-?\d+),\s*(-?\d+)\)$/))) {
            outs.push(obj.enroll(+m[1], +m[2]) ? 'true' : 'false');
        } else if (line === 'nextPlay()') {
            outs.push(String(obj.nextPlay()));
        } else if ((m = line.match(/^boost\((-?\d+),\s*(-?\d+)\)$/))) {
            outs.push(obj.boost(+m[1], +m[2]) ? 'true' : 'false');
        } else if ((m = line.match(/^cancel\((-?\d+)\)$/))) {
            outs.push(obj.cancel(+m[1]) ? 'true' : 'false');
        } else if (line === 'waiting()') {
            outs.push(String(obj.waiting()));
        } else {
            throw new Error('bad op: ' + line);
        }
    }
    if (outs.length) process.stdout.write(outs.join('\n') + '\n');
});
