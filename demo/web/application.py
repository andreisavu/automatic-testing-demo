
import os
import tornado.web

from tornado.options import options
from demo.tornado_utils import route

import controllers

class Application(tornado.web.Application):
  def __init__(self):
    settings = dict(
      template_path = os.path.join(os.path.dirname(__file__), 'templates'),
      static_path = os.path.join(os.path.dirname(__file__), '../../static'),
      cookie_secret = options.cookie_secret,
      login_url = '/login',
      debug = options.debug
    )
    tornado.web.Application.__init__(self, route.get_routes(), **settings)

