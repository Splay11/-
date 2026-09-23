const fs = require('fs');
process.nextTick(() => {
    const text = fs.readFileSync(0, 'utf8');
    const lines = text.split(/\r?\n/);
    let obj = null;
    const outs = [];
    for (let raw of lines) {
        const line = raw.trim();
        if (!line) continue;
        let m = line.match(/^ParcelSlots\((-?\d+)\)$/);
        if (m) {
            obj = new ParcelSlots(parseInt(m[1], 10));
            outs.push('null');
            continue;
        }
        m = line.match(/^put\((-?\d+),\s*(-?\d+)\)$/);
        if (m) {
            outs.push(obj.put(parseInt(m[1], 10), parseInt(m[2], 10)) ? 'true' : 'false');
            continue;
        }
        m = line.match(/^take\((-?\d+)\)$/);
        if (m) {
            outs.push(String(obj.take(parseInt(m[1], 10))));
            continue;
        }
        m = line.match(/^moveRight\((-?\d+)\)$/);
        if (m) {
            outs.push(obj.moveRight(parseInt(m[1], 10)) ? 'true' : 'false');
            continue;
        }
        if (line === 'occupied()') {
            outs.push(String(obj.occupied()));
            continue;
        }
        throw new Error('bad op: ' + line);
    }
    if (outs.length) console.log(outs.join('\n'));
});
