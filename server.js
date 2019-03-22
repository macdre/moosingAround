// server.js
var express = require('express');
var http = require('http');
var proxy = require('http-proxy-middleware');

var fs = require('fs');
var serveStatic = require('serve-static');
var port = 5000;

app = express();
app.use(serveStatic(__dirname + "/dist"));

var options = {
    key: fs.readFileSync('./src/py/myserver.key'),
    cert: fs.readFileSync('./src/py/myserver.crt')
};
http.createServer(app).listen(port);

console.log('server started '+ port);

// Config
const { routes } = require('./proxyconfig.json');

const pApp = express();

for (route of routes) {
    pApp.use(route.route,
        proxy({
            target: route.address,
            pathRewrite: (path, req) => {
                return path.split('/').slice(2).join('/'); // Could use replace, but take care of the leading '/'
            }
        })
    );
}

port = process.env.PORT || 8000;

pApp.listen(port, () => {
    console.log('Proxy listening on port 80');
});


