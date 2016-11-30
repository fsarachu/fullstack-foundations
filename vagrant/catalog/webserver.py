# coding=utf-8
from BaseHTTPServer import HTTPServer

from WebserverHandler import WebserverHandler


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print "Web server running on port {}".format(port)
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping server..."
        server.socket.close()


if __name__ == '__main__':
    main()
