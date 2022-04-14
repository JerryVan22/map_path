from http.server import HTTPServer, SimpleHTTPRequestHandler
port=str(6999)
httpd = HTTPServer(("127.0.0.1", int(port)), SimpleHTTPRequestHandler)
print("Serving HTTP on localhost port " + port + " (http://localhost:" + port + "/) ...")
httpd.serve_forever()