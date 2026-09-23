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
        if (line === 'PickupDesk()') {
            obj = new PickupDesk();
            outs.push('null');
        } else if ((m = line.match(/^order\((-?\d+)\)$/))) {
            outs.push(obj.order(+m[1]) ? 'true' : 'false');
        } else if (line === 'serve()') {
            outs.push(String(obj.serve()));
        } else if (line === 'waiting()') {
            outs.push(String(obj.waiting()));
        } else {
            throw new Error('bad op: ' + line);
        }
    }
    if (outs.length) process.stdout.write(outs.join('\n') + '\n');
});
