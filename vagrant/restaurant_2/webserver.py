from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"

                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
        except IOError:
            self.send_error(404, f"File not found {self.path}")

        
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = pdict['boundary'].encode('utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2>Okay, how about this: </h2>"
            output += "<h1> {} </h1>".format(messagecontent[0].decode('utf-8'))
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2>"
            output += "<input name='message' type='text'><input type='submit' value='Submit'></form>"

            output += "</body></html>"
            self.wfile.write(output.encode())
            print(output)
            return
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print(f"Web server is running on port {port}.")
        server.serve_forever()

    except KeyboardInterrupt:
        print(f"Keyboard interrupt, stopping web server...")
        server.socket.close()




if __name__=='__main__':
    main()
