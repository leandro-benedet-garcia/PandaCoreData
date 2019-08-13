# import your jinja2 modules here
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

class WebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extensions_map[".js"] = "application/ecmascript"
        self.extensions_map[".esm.js"] = "application/ecmascript"
        self.extensions_map[".css"] = "text/css"

    #pylint: disable=invalid-name
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            jinja_loader = FileSystemLoader("templates")
            jinja_autoescape = select_autoescape(['html',])

            env = Environment(loader=jinja_loader, autoescape=jinja_autoescape)

            template = env.get_template('main.html')
            html = template.render()
            self.wfile.write(html.encode("UTF-8"))
        else:
            super().do_GET()

def run(server_class, handler, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler)
    httpd.serve_forever()

if __name__ == '__main__':
    run(ThreadingHTTPServer, WebHandler, 8000)
