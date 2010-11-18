
from pprint import pprint

from demo.test.smtp import SMTPTestInstance

class SMTPTestMixin(object):

  def setUpSMTP(self):
    self.smtp = SMTPTestInstance()
    self.smtp.start()
    return self.smtp.hostport

  def tearDownSMTP(self):
    self.smtp.stop()

  def dumplog(self, out = None):
    if self.smtp.messages:
      pprint(self.smtp.messages, out)
