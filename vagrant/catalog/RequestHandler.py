import cgi
import jinja2
from BaseHTTPServer import BaseHTTPRequestHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class RequestHandler(BaseHTTPRequestHandler):
    TEMPLATE_DIR = 'templates'
    JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)

    def render(self, template_name, **kwargs):
        template = self.JINJA_ENV.get_template(template_name)
        self.wfile.write(template.render(kwargs))

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
                self.render('restaurants.html', restaurants=restaurants)

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                self.render('new_restaurant.html')

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
