
from tornado.options import options
from mongokit import Connection

from models import User, ResetRequest
from demo.utils import randchars

def register_all(conn):
  conn.register([User, ResetRequest])

def get_connection(host=None, port=None):
  """ Open a connection to the MongoDB server """
  if not host and not port:
    try:
      host, port = options.mongodb.split(':')
    except (AttributeError, ValueError):
      host, port = None, None

  if host and port:
    conn = Connection(host, int(port))
    register_all(conn)
    return conn

  else:
    raise Exception('You need to configure the host and port '\
      'of the MongoDB document server')
