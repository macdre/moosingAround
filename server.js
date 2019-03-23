// server.js
var express = require('express');
var http = require('http');
var proxy = require('http-proxy-middleware');
var fs = require('fs');
var serveStatic = require('serve-static');
var port = process.env.PORT || 5000;

app = express();
app.use(serveStatic(__dirname + "/dist"));

// Config
const { routes } = require('./proxyconfig.json');
for (route of routes) {
    app.use(route.route,
        proxy({
            target: route.address,
            pathRewrite: (path, req) => {
                return path.split('/').slice(2).join('/'); // Could use replace, but take care of the leading '/'
            }
        })
    );
}

http.createServer(app).listen(port);
console.log('server started '+ port);