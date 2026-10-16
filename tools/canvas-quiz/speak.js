// Reads a JSON array of TeX strings on stdin, prints a JSON object {tex: plain-words reading}.
// It uses the same texToSpeech function that the web pages use (template/app.js), so the quiz and the pages say the same thing.
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '../../template/app.js'), 'utf8');
const block = src.split('/*SPEECH-START*/')[1].split('/*SPEECH-END*/')[0];
const texToSpeech = new Function(block + '; return texToSpeech;')();
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const out = {};
input.forEach((t) => { out[t] = texToSpeech(t); });
process.stdout.write(JSON.stringify(out));
