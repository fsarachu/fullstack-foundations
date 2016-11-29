# coding=utf-8
import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = """
                    <!doctype html>
                    <html lang='en'>
                    <head>
                        <meta charset='UTF-8'>
                        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                        <meta http-equiv='X-UA-Compatible' content='ie=edge'>
                        <title>Hello!</title>
                    </head>
                    <body>
                      <h1>Hello!</h1>
                    </body>
                    </html>
                """
                self.wfile.write(output)

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = """
                    <!doctype html>
                    <html lang='en'>
                    <head>
                        <meta charset='UTF-8'>
                        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                        <meta http-equiv='X-UA-Compatible' content='ie=edge'>
                        <title>¡Hola!</title>
                    </head>
                    <body>
                      <h1>¡Hola!</h1>
                      <a href='/hello'>Go back to Hello!</a>
                    </body>
                    </html>
                """
                self.wfile.write(output)

        except IOError:
            self.send_error(404, "File not found: {}".format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('Content-Type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                message_content = fields.get('message')
            output = """
            <!doctype html>
            <html lang='en'>
            <head>
              <meta charset='UTF-8'>
              <meta name='viewport' content='width=device-width, initial-scale=1.0'>
              <meta http-equiv='X-UA-Compatible' content='ie=edge'>
              <title>Custom Message</title>
            </head>
            <body>
            """
            output += '<h1>{}</h1>'.format(message_content[0])
            output += """
            </body>
            </html>
            """
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port {}".format(port)
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping server..."
        server.socket.close()


if __name__ == '__main__':
    main()
