
import os, sys
import mechanize

from demo.test.tornado import TornadoTestInstance

def abspath(*args):
  cp = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(cp, *args)

class FrontendTestMixin(object):

  def setUpFrontend(self, cfg):
    self.frontend = TornadoTestInstance(abspath('../../../web.py'), cfg)
    self.frontend.start()
    self.browser = mechanize.Browser()

  def tearDownFrontend(self):
    self.frontend.stop()

  def dumplog(self, out = None):
    print >>(out or sys.stdout), self.frontend.output()

  def do_login(self, email, password = None):
    self.browser.open(self.url('/login'))
    assert 'login' in (self.browser.title() or '').lower()

    self.browser.select_form(name="loginForm")
    self.browser['email'] = email
    self.browser['password'] = password

    return self.browser.submit()

  def url(self, path):
    return "http://%s:%s%s" % (self.frontend.host, self.frontend.port, path)

