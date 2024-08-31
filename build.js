const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'index.html');
const now = new Date();

const pad = (number) => number.toString().padStart(2, '0');

const version = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${pad(now.getHours() - 4)}${pad(now.getMinutes())}${pad(now.getSeconds())}`;

fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
        return console.log(err);
    }
    const result = data.replace('{{VERSION}}', version);

    fs.writeFile(filePath, result, 'utf8', (err) => {
        if (err) return console.log(err);
    });
});
