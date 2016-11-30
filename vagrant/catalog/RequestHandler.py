import cgi
import jinja2
import os
from BaseHTTPServer import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../templates')
    JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)

    form = """
    <form action='/hello' method='post' enctype='multipart/form-data'>
      <h2>Enter your custom message:</h2>
      <input type='text' name='message'>
      <input type='submit' value='Submit'>
    </form>
    """

    def render(self, template_name, **kwargs):
        template = self.JINJA_ENV.get_template(template_name)
        self.wfile.write(template.render(kwargs))

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
                """
                output += self.form
                output += """
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
                """
                output += self.form
                output += """
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
            output += self.form
            output += """
            </body>
            </html>
            """
            self.wfile.write(output)
        except:
            print "Something went wrong!"
