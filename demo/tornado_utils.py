
import sys, os

import tornado
import tornado.httpserver

from tornado.options import define, options
from demo.utils import randchars

def parse_config_options(args=None):
  args = args or sys.argv[:]

  define('debug', default=False,
    help='enable autoreload for tornado web apps', type=bool)

  define('port', default=8888, help='tornado listen port', type=int)

  define('cookie_secret', default=randchars(32), help='cookie hash secret')

  define('mongodb', default='localhost:27017', help='mongodb host:port')

  define('smtp', default='localhost:25', help='smtp server')

  if len(args) >= 2 and os.path.exists(args[1]):
    tornado.options.parse_config_file(args[1])
    del args[1]

  # parse the remaining command line arguments
  # should override config file settings

  tornado.options.parse_command_line(args)

def start(application_klass, args=None):
  """ Typical start script for Tornado web applications """
  parse_config_options(args)

  server = tornado.httpserver.HTTPServer(application_klass())
  server.listen(options.port)

  tornado.ioloop.IOLoop.instance().start()

class route(object):
  """
decorates RequestHandlers and builds up a list of routables handlers

Tech Notes (or "What the *@# is really happening here?")
--------------------------------------------------------

Everytime @route('...') is called, we instantiate a new route object which
saves off the passed in URI. Then, since it's a decorator, the function is
passed to the route.__call__ method as an argument. We save a reference to
that handler with our uri in our class level routes list then return that
class to be instantiated as normal.

Later, we can call the classmethod route.get_routes to return that list of
tuples which can be handed directly to the tornado.web.Application
instantiation.

Example
-------

@route('/some/path')
class SomeRequestHandler(RequestHandler):
pass

my_routes = route.get_routes()
"""
  _routes = []

  def __init__(self, uri):
    self._uri = uri

  def __call__(self, _handler):
    """gets called when we class decorate"""
    self._routes.append((self._uri, _handler))
    return _handler

  @classmethod
  def get_routes(self):
    return self._routes

