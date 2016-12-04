import cgi
import jinja2
import re
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

    ROUTES = dict()
    ROUTES['restaurants'] = re.compile('^/restaurants$')
    ROUTES['restaurants_new'] = re.compile('^/restaurants/new$')
    ROUTES['restaurants_edit'] = re.compile('^/restaurants/(\d+)/edit$')

    def render(self, template_name, http_response=200, **kwargs):
        self.send_response(http_response)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        template = self.JINJA_ENV.get_template(template_name)
        self.wfile.write(template.render(kwargs))

    def redirect(self, url):
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

    def do_GET(self):
        try:
            if re.match(self.ROUTES['restaurants'], self.path):
                restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
                self.render('restaurants.html', restaurants=restaurants)

            if re.match(self.ROUTES['restaurants_new'], self.path):
                self.render('restaurant_new.html')

            if re.match(self.ROUTES['restaurants_edit'], self.path):
                id = re.search(self.ROUTES['restaurants_edit'], self.path).group(1)
                restaurant = session.query(Restaurant).filter_by(id=id).first()

                if not restaurant:
                    self.render('404.html', http_response=404, msg='Restaurant {} doesn\'t exists'.format(id))
                else:
                    self.render('restaurant_edit.html', restaurant=restaurant)

        except IOError:
            self.send_error(404, "File not found: {}".format(self.path))

    def do_POST(self):
        try:
            if re.match(self.ROUTES['restaurants_new'], self.path):
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-Type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    field_content = fields.get('name')

                    new_restaurant = Restaurant(name=field_content[0])
                    session.add(new_restaurant)
                    session.commit()

                    self.redirect('/restaurants')
                else:
                    self.render('restaurant_new.html', msg='Something went wrong! Try again.')

        except:
            print "Something went wrong!"
