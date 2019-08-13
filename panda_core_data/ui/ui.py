import base64
import cefpython3.cefpython_py37 as cef
from jinja2 import Environment, FileSystemLoader, select_autoescape

MIME_PREPEND = "data:"
MIME_SUFFIX = ";base64,"
APP_NAME = "Raw Editor"

MIME_TYPES = {
    #images
    "png": "image/png",
    "jpg": "image/jpg",

    #stylesheets
    "css": "text/css",

    #scripts
    "js": "application/javascript",
    "coffee": "application/vnd.coffeescript"
}

def to_base64(filename):
    extension = filename.split(".")[-1]
    with open(filename, "rb") as image_file:
        base_prefix = MIME_PREPEND + MIME_TYPES[extension] + MIME_SUFFIX
        return base_prefix + base64.b64encode(image_file.read()).decode('utf8')

def main():
    jinja_loader = FileSystemLoader("templates")
    jinja_autoescape = select_autoescape(['html',])

    env = Environment(loader=jinja_loader, autoescape=jinja_autoescape)
    env.filters['to_base64'] = to_base64

    template = env.get_template('main.html')
    html = template.render()

    cef.Initialize()
    browser = cef.CreateBrowserSync(url=cef.GetDataUrl(html), window_title=APP_NAME)

    cef.MessageLoop()
    del browser
    cef.Shutdown()


if __name__ == '__main__':
    main()
