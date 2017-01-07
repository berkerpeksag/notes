"""
TODOs

* [x] Add -p (port)
* [x] CLI UX, URl ve ^C'yi print etsin
* [x] Add -d (index dir)
* Add -s (suffixes .md, .txt etc.)
* Jinja2 support
* [x] Class based: Notesd(handlers, config)
* [x] Class based: index func -> IndexHandler class
* Consider adding a "serve" option: Generate static HTML
* Consider encapsulating environ in a request object and
  replacing the start_response call and the return iterator
  with a response objects.
* Recursive directories
* Add a factory for another WSGI servers
* [x] Use ExceptionMiddleware inside of Notesd
"""

import html
import http.client
import os
import re
import sys
import traceback

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


class Status:

    def __init__(self, status, message=None, content_type='text/plain'):
        self.status = '{:d} {}'.format(status, http.client.responses[status])
        self.message = message or http.client.responses[status]
        self.content_type = content_type

    def __call__(self, environ, start_response):
        start_response(self.status, [('Content-Type', self.content_type)])
        return [self.message.encode()]

NotFound = Status(404, 'Not Found', 'text/html')


class BaseHandler:

    app_label = 'myapp'

    def get_config(self, environ):
        return environ.get('{}.config'.format(self.app_label))

    def render(self, content):
        if isinstance(content, list):
            content = ''.join(content)
        return [layout_template.format(content=content).encode()]


class IndexHandler(BaseHandler):

    def __call__(self, environ, start_response):
        config = self.get_config(environ)
        directory = os.path.abspath(config['directory'])
        pages = ['<li><a href="/document/{doc}">{doc}</a></li>'.format(doc=doc)
                 for doc in os.listdir(directory) if doc.endswith(('.md', '.txt'))]
        start_response("200 OK", [('Content-Type', 'text/html; charset=utf-8')])
        return self.render('<ul>{}</ul>'.format(''.join(pages)))


class DocumentHandler(BaseHandler):

    def get_urls(self, environ):
        return environ.get('{}.url_args'.format(self.app_label))

    def __call__(self, environ, start_response):
        config = self.get_config(environ)
        urls = self.get_urls(environ)
        directory = os.path.abspath(config['directory'])
        if not urls:
            return NotFound(environ, start_response)
        path = os.path.join(directory, html.escape(urls[0]))
        if not os.path.exists(path):
            return NotFound(environ, start_response)
        with open(path, encoding='utf-8') as fobj:
            content = markdown.markdown(fobj.read())
        start_response("200 OK", [('Content-Type', 'text/html; charset=utf-8')])
        return self.render(content)


class Router:

    def __init__(self, handlers, config):
        self.handlers = handlers
        self.config = config

    def __call__(self, environ, start_response):
        environ['myapp.config'] = self.config
        path = environ.get('PATH_INFO', '').lstrip('/')
        for regex, callback in self.handlers:
            # TODO: pass a config object to these handlers
            match = re.search(regex, path)
            if match is not None:
                environ['myapp.url_args'] = match.groups()
                return callback()(environ, start_response)
        return NotFound(environ, start_response)


class ExceptionMiddleware:
    # Adapted from http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        appiter = None
        try:
            appiter = self.app(environ, start_response)
            yield from appiter
        except:
            start_response('500 INTERNAL SERVER ERROR',
                           [('Content-Type', 'text/plain')],
                           sys.exc_info())
            yield traceback.format_exc().encode()
        if hasattr(appiter, 'close'):
            appiter.close()


class Notesd:

    def __init__(self, handlers, config):
        self.handlers = handlers
        self.config = config
        self.app = Router(self.handlers, self.config)

    def __call__(self, environ, start_response):
        yield from ExceptionMiddleware(self.app)(environ, start_response)


if __name__ == '__main__':
    import argparse
    import wsgiref.simple_server

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='port', type=int, default=8586)
    parser.add_argument('-d', dest='directory', type=str, default='.')
    options = parser.parse_args()

    config = dict(directory=options.directory)
    handlers = [
        (r'^$', IndexHandler),
        (r'document/(.+)$', DocumentHandler),
    ]
    application = Notesd(handlers, config)
    httpd = wsgiref.simple_server.make_server('', options.port, application)

    print('Serving on port http://localhost:{}...'.format(options.port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down...')
        httpd.shutdown()
