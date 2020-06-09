import traceback
from http.server import HTTPServer, SimpleHTTPRequestHandler

class RequestHandler(SimpleHTTPRequestHandler, object):
    def print_info(self):
        self.log_message("%s %s\n%s", self.command, self.path, self.headers)

    def do_GET(self):
        self.print_info()
        super(RequestHandler, self).do_GET()

    def do_POST(self):
        self.do_GET()


if __name__ == '__main__':
    try:
        with HTTPServer(("127.0.0.2", 8080), RequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...", end="")
        httpd.shutdown()
        print("done")
        #print(traceback.format_exc())