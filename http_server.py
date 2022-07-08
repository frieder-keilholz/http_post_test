# Python 3 HTTP Server
# mirrors POST requests
# GET responses contain content of latest corresponding POST

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    ressource_buffer = {}

    def do_GET(self):
        if self.path in self.ressource_buffer:
            self.send_response(200)
            self.send_header("Content-Type", self.ressource_buffer[self.path]["Content-Type"])
            self.end_headers()
            self.wfile.write(self.ressource_buffer[self.path]["Body"])
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        self.send_response(200)
        print("  Path: {}".format(self.path))
        content_type = self.headers.get('Content-type')
        print("  Content-Type: {}".format(content_type))
        self.send_header('Content-type', content_type)
        #self.send_header('Content-Length', self.headers.get('Content-Length'))
        self.end_headers()
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print("  Content-Length: {}".format(content_len))
        print("  Body: {}".format(post_body))
        self.wfile.write(post_body)
        self.ressource_buffer[self.path] = {"Content-Type": content_type, "Body": post_body}

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")