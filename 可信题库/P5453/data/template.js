const fs = require('fs');
const lines = fs.readFileSync(0, 'utf8').split(/\r?\n/);
const outs = [];
let obj = null;
for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;
    let m;
    if ((m = line.match(/^ParkingLane\((-?\d+)\)$/))) {
        obj = new ParkingLane(+m[1]);
        outs.push('null');
    } else if ((m = line.match(/^arrive\((-?\d+)\)$/))) {
        outs.push(obj.arrive(+m[1]) ? 'true' : 'false');
    } else if (line === 'admit()') {
        outs.push(obj.admit() ? 'true' : 'false');
    } else if ((m = line.match(/^depart\((-?\d+)\)$/))) {
        outs.push(String(obj.depart(+m[1])));
    } else if (line === 'undo()') {
        outs.push(obj.undo() ? 'true' : 'false');
    } else if (line === 'front()') {
        outs.push(String(obj.front()));
    } else if (line === 'waiting()') {
        outs.push(String(obj.waiting()));
    } else if (line === 'size()') {
        outs.push(String(obj.size()));
    } else process.exit(1);
}
if (outs.length) console.log(outs.join('\n'));
