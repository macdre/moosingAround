// server.js
var express = require('express');
var serveStatic = require('serve-static');
var port = process.env.PORT || 5000;
var cors = require('cors');

app = express();
app.use(cors());
app.use(serveStatic(__dirname + "/dist"));
app.listen(port);
console.log('server started '+ port);
