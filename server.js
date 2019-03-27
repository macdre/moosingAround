// server.js
var url = require('url');
var _ = require('lodash');
var express = require('express');
//var httpProxy = require('http-proxy');
var serveStatic = require('serve-static');
var port = process.env.PORT || 5000;
var proxy = require('express-http-proxy');

app = express();
app.use(serveStatic(__dirname + "/dist"));
//app.use('/compute', proxy('http://localhost:9090'));
app.use('/api', proxy('localhost:9090', {
    proxyReqPathResolver: function(req) {
      return new Promise(function (resolve, reject) {
        setTimeout(function () {   // simulate async
          var parts = req.url.split('?');
          var queryString = parts[1];
          var updatedPath = parts[0].replace(/api/, '/');
          var resolvedPathValue = updatedPath + (queryString ? '?' + queryString : '');
          resolve(resolvedPathValue);
        }, 200);
      });
    }
}));

// var proxy = httpProxy.createProxyServer();
// app.all('/api/*', (req, res) => {
//     const __path = _.drop(req.url.split('/'), 2);
//     proxy.proxyRequest(req, res, {
//       target: url.resolve('http://localhost:9090', __path.join('/')),
//       ignorePath: true,
//       changeOrigin: true
//     });
// });

// proxy.on('proxyRes', function (proxyRes, req, res) {
//     console.log("Response received");
// });
  
// proxy.on('error', function (err, req, res) {
//     console.log("Error received");
//     console.log(err);
// });


app.listen(port);
console.log('server started '+ port);
