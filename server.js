// server.js
var express = require('express');
//var https = require('https');
var http = require('http');
var fs = require('fs');
var serveStatic = require('serve-static');
var port = 5000;

app = express();
app.use(serveStatic(__dirname + "/dist"));

var options = {
    key: fs.readFileSync('./src/py/myserver.key'),
    cert: fs.readFileSync('./src/py/myserver.crt')
};
//https.createServer(options, app).listen(port);
http.createServer(app).listen(port);

console.log('server started '+ port);
