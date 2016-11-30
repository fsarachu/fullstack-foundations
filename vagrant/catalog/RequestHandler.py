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

    def redirect(self, url):
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

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
            if self.path.endswith("/restaurants/new"):
                self.send_response(201)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-Type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    field_content = fields.get('name')

                    new_restaurant = Restaurant(name=field_content[0])
                    session.add(new_restaurant)
                    session.commit()

                    self.redirect('/restaurants')
                else:
                    self.render('new_restaurant.html', msg='Something went wrong! Try again.')


        except:
            print "Something went wrong!"
