
import os
import subprocess
import logging
import time
import signal

from pymongo import Connection
from tempfile import mkdtemp
from shutil import rmtree

from utils import get_unused_port, wait_for_mongodb, \
  wait_for_process_exit, wait_for_pidfile

class MongoTestInstance(object):
  """ Manage a mongodb instance used for testing """
  def __init__(self):
    self.mongobin = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../test_components/')
    self.mongod = os.path.join(self.mongobin, 'mongod')

    self.dbpath = mkdtemp()
    self.logpath = os.path.join(self.dbpath, 'mongo.log')
    self.pidfile = os.path.join(self.dbpath, 'mongod.lock')

    self.port = get_unused_port()
    self.host = 'localhost'

  @property
  def hostport(self):
    return '%s:%s' % (self.host, self.port)

  def start(self):
    logging.info("starting mongodb with " \
        "dbpath: %s on port: %s" % (self.dbpath, self.port))
    p = subprocess.Popen([self.mongod,
      '--fork',
      '--quiet',
      '--objcheck',
      '--nohttpinterface',
      '--noprealloc',
      '--dbpath', self.dbpath,
      '--logpath', self.logpath,
      '--port', str(self.port)],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)

    (out, err) = p.communicate()
    self._wait_for_db_start()

  def _wait_for_db_start(self):
    wait_for_pidfile(self.pidfile)
    wait_for_mongodb(self.host, self.port)

  def stop(self):
    logging.info("stopping mongodb instance")
    try:
      pid = int(open(self.pidfile).read())

      os.kill(pid, signal.SIGTERM)
      wait_for_process_exit(pid)
      rmtree(self.dbpath)

    except (ValueError, TypeError):
      logging.error('invalid pid file')

    except OSError:
      logging.error('unable to close mongod')

    except IOError:
      logging.exception('unable to find the running mongodb instance.')
