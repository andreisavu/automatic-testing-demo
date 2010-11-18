
from StringIO import StringIO

from demo.test.base import WebApplicationTestCase

class AuthTest(WebApplicationTestCase):

  def test_login(self):
    self.create_user(u'test@example.com', u'test')
    r = self.do_login('test@example.com', 'test')

    assert r.geturl() == self.url('/')

  def test_failed_login_try(self):
    r = self.do_login('123', '123')

    assert r.geturl() == self.url('/login')
    assert 'invalid credentials' in r.read().lower()

  def test_case_insensitive_email_address(self):
    self.create_user(u'Test@eXample.com', u'test')
    r = self.do_login('tEsT@example.com', 'test')

    assert r.geturl() == self.url('/')

  def test_login_and_logout(self):
    self.create_user(u'test@example.com', u'test')

    r = self.do_login('test@example.com', 'test')
    assert r.geturl() == self.url('/')

    self.browser.open(self.url('/logout'))
    assert 'login' in (self.browser.title() or '').lower()

  def test_password_reset(self):
    self.create_user(u'test@example.com')

    self.browser.open(self.url('/password/reset'))
    self.browser.select_form('resetForm')
    self.browser['email'] = 'test@example.com'
    r = self.browser.submit()

    assert 'check your inbox' in r.read().lower()
    assert self.smtp.last_message is not None

    content = self.smtp.last_message['data']
    reset_url = self._extract_link(content)
    assert reset_url

    self.browser.open(reset_url)
    self.browser.select_form(name='resetForm')

    self.browser['new'] = 'newpass'
    self.browser['repeat'] = 'newpass'
    r = self.browser.submit()
    assert r.geturl() == self.url('/login')

    r = self.do_login('test@example.com', 'newpass')
    assert r.geturl() == self.url('/')

    try:
      self.browser.open(reset_url)
      assert False

    except Exception, e:
      assert 'error 401' in str(e).lower()

  def _extract_link(self, content):
    """ Extract a line that contains a link. Naive check """
    h = StringIO(content)

    for line in h.readlines():
      if line.startswith('http'):
        return line.strip()

    return None

