
import os
import subprocess

from utils import get_unused_port, wait_for_port
from tempfile import mkstemp

class ScriptTestInstance(object):
  def __init__(self, app_path, cfg):
    self.app_path = app_path
    self.cfg = cfg
    self.cfg['logging'] = 'debug'

    (handle, self.logfile) = mkstemp()
    self.cfg['log_file_prefix'] = self.logfile
    os.close(handle)

  def start(self):
    self.process = subprocess.Popen(\
      ['python', self.app_path] + \
      ['--%s=%s' % (key, value) for key, value in self.cfg.items()])

  def output(self):
    return open(self.logfile).read()

  def stop(self):
    self.process.terminate()
    self.process.wait()
    os.unlink(self.logfile)
