
from utils import get_unused_port, wait_for_port
from demo.test.script import ScriptTestInstance

class TornadoTestInstance(ScriptTestInstance):
  """ Start a tornado web application for testing """
  def __init__(self, app_path, cfg):
    super(TornadoTestInstance, self).__init__(app_path, cfg)

    self.host = 'localhost'
    self.cfg['port'] = self.port = get_unused_port()

  def start(self):
    super(TornadoTestInstance, self).start()
    wait_for_port(self.host, self.port)

