// server.js
var express = require('express');
var serveStatic = require('serve-static');
var port = process.env.PORT || 5000;
var cors = require('cors');

app = express();
//app.use(cors());
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "POST, GET, PUT");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});
app.use(serveStatic(__dirname + "/dist"));
app.listen(port);
console.log('server started '+ port);
