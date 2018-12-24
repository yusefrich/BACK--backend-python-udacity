from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output = "<html><body>Hello!</body></html>"
                self.wfile.write(output)
                print("pagina inicial")
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output = "<html><body>Hello!  <a href = '/hello'>back to hello</a></body></html>"
                self.wfile.write(output)
                print("pagina inicial")
                return

        except IOError:
            self.send_error(404, "file not found %s" % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^c used, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
