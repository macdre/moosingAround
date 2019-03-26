// server.js
var url = require('url');
var _ = require('lodash');
var express = require('express');
var httpProxy = require('http-proxy');
var serveStatic = require('serve-static');
var port = process.env.PORT || 5000;

app = express();
app.use(serveStatic(__dirname + "/dist"));

var proxy = httpProxy.createProxyServer();
app.all('/api/*', (req, res) => {
    const __path = _.drop(req.url.split('/'), 2);
    proxy.proxyRequest(req, res, {
      target: url.resolve('http://localhost:9090', __path.join('/')),
      ignorePath: true,
      changeOrigin: true
    });
});

proxy.on('proxyRes', function (proxyRes, req, res) {
    console.log("Response received");
});
  
proxy.on('error', function (err, req, res) {
    console.log("Error received");
    console.log(err);
});


app.listen(port);
console.log('server started '+ port);
