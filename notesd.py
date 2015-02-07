"""
TODOs

* [x] Add -p (port)
* [x] CLI UX, URl ve ^C'yi print etsin
* [x] Add -d (index dir)
* Add -s (suffixes .md, .txt etc.)
* Jinja2 support
* [x] Class based: Notesd(handlers, config)
* Class based: index func -> IndexHandler class
* Consider adding a "serve" option: Generate static HTML
"""

import html
import os
import re

from wsgiref.simple_server import make_server

import markdown

layout_template = """\
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Notes</title>
</head>
<body>
  <h3><a href="/">Notes</a></h3>
  <hr>
  {content}
</body>
</html>
"""


def render(content):
    if isinstance(content, list):
        content = ''.join(content)
    return [layout_template.format(content=content).encode()]


def index(environ, start_response):
    config = environ.get('myapp.config')
    directory = os.path.abspath(config['directory'])
    response = ['<ul>']
    pages = ['<li><a href="/document/{doc}">{doc}</a></li>'.format(doc=doc)
             for doc in os.listdir(directory) if doc.endswith(('.md', '.txt'))]
    response.extend(pages)
    response.append('</ul>')
    start_response("200 OK", [('Content-Type', 'text/html; charset=utf-8')])
    return render(response)


def document(environ, start_response):
    args = environ.get('myapp.url_args')
    config = environ.get('myapp.config')
    directory = os.path.abspath(config['directory'])
    if args:
        path = os.path.join(directory, html.escape(args[0]))
        if os.path.exists(path):
            with open(path, encoding='utf-8') as fobj:
                content = markdown.markdown(fobj.read())
        else:
            return not_found(environ, start_response)
    else:
        return not_found(environ, start_response)
    start_response("200 OK", [('Content-Type', 'text/html; charset=utf-8')])
    return render(content)


def not_found(environ, start_response):
    start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
    return render('Not Found')


class Notesd:

    def __init__(self, handlers, config):
        self.handlers = handlers
        self.config = config

    def __call__(self, environ, start_response):
        environ['myapp.config'] = self.config
        path = environ.get('PATH_INFO', '').lstrip('/')
        for regex, callback in self.handlers:
            match = re.search(regex, path)
            if match is not None:
                environ['myapp.url_args'] = match.groups()
                return callback(environ, start_response)
        return not_found(environ, start_response)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='port', type=int, default=8586)
    parser.add_argument('-d', dest='directory', type=str, default='.')
    options = parser.parse_args()

    handlers = [
        (r'^$', index),
        (r'document/(.+)$', document)
    ]
    application = Notesd(handlers=handlers, config=dict(directory=options.directory))
    httpd = make_server('', options.port, application)

    print('Serving on port http://localhost:{}...'.format(options.port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down...')
        httpd.shutdown()
