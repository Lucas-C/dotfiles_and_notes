const fs = require('fs'),
      http = require('http'),
      path = require('path'),
      qs = require('querystring'),
      url = require('url');
http.createServer((request, response) => {
    console.log(request.method, request.url)
    let uri = url.parse(request.url).pathname
    if (!uri || uri === '/') uri = '/index.html'
    if (request.method === 'POST') {
        let body = ''
        request.on('data', data => body += data)
        request.on('end', function () {
            console.log('-> body:', qs.parse(body))
            response.writeHead(302, {'Location': uri})
            response.write('302 Found\n')
            response.end()
        })
    } else {
        let filename = path.join(process.cwd(), uri)
        if (!fs.existsSync(filename)) {
            response.writeHead(404)
            response.write('404 Not Found\n')
            response.end()
            return
        }
        response.writeHead(200)
        fs.createReadStream(filename).pipe(response)
    }
}).listen(8000)
