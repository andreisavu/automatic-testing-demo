import smtplib
import tornado.web

from tornado.options import options
from tornado.web import HTTPError

from email.mime.text import MIMEText

from mongokit import Connection
from pymongo.errors import DuplicateKeyError

from demo.db import get_connection
from demo.web.flash import Flash
from demo.validators import valid_email
from demo.tornado_utils import route

class BaseHandler(tornado.web.RequestHandler):
  def __init__(self, *args, **kwargs):
    tornado.web.RequestHandler.__init__(self, *args, **kwargs)
    self.flash = Flash(self)

    self.mongo = get_connection()
    self.demo = self.mongo.demo

  def get_current_user(self):
    email = self.get_secure_cookie("email")
    return self.demo.users.User.find_one({'email': email})

  def send_email(self, toaddr, fromaddr, subject, template, *args, **kwargs):
    content = self.render_string(template, *args, **kwargs)

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Reply-To'] = fromaddr

    host, port = options.smtp.split(':')
    smtp = smtplib.SMTP(host, int(port))
    smtp.sendmail(fromaddr, [toaddr], msg.as_string())
    smtp.quit()

@route('/')
class HomeHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self): pass # empty page

@route('/login')
class LoginHandler(BaseHandler):
  def get(self):
    if self.current_user:
      self.redirect('/')
    else:
      self.render('login.html')

  def post(self):
    email = self.get_argument('email', None)
    password = self.get_argument('password', None)
    try:
      self.authenticate(email, password)
      self.redirect('/')

    except ValueError, e:
      self.flash.error = str(e)
      self.render('login.html')

  def authenticate(self, email, password):
    if not email or not password:
      raise ValueError('Both fields are mandatory.')

    email = email.lower()
    record = self.demo.users.User.find_one({'email': email})

    if record and record.is_valid_password(password):
      if record.active:
        self.set_secure_cookie('email', record.email)
        return True

      else:
        raise ValueError('Deactivated Account.')

    raise ValueError('Invalid credentials.')

@route('/logout')
class LogoutHandler(BaseHandler):
  def get(self):
    self.clear_cookie('email')
    self.redirect('/login')

@route('/password/reset')
class RequestResetHandler(BaseHandler):
  def get(self):
    self.render('request_reset.html')

  def post(self):
    email = self.get_argument('email', None)
    try:
      self.prepare_reset(email)
      self.flash.message = 'The reset email was '\
        'sent. Check your inbox.'

    except ValueError, e:
      self.flash.error = str(e)

    self.render('request_reset.html', page='reset')

  def prepare_reset(self, email):
    if not email or not valid_email(email):
      raise ValueError('Invalid email address')

    email = email.lower()
    if not self.demo.users.User.find_one({'email': email}):
      raise ValueError('No account found for this email address')

    key = self.generate_reset_key(email)
    reset_url = '%s://%s/password/change/%s' % \
      (self.request.protocol, self.request.host, key)

    self.send_email(email,
      'noreply@example.com',
      'Password Reset',
      'emails/reset.txt',
      reset_url = reset_url
    )

  def generate_reset_key(self, email):
    """ Try until the generated one is unique """
    while True:
      try:
        r = self.demo.reset.ResetRequest()
        r.email = email
        r.save()
        return r.key

      except DuplicateKeyError:
        pass

@route('/password/change/(.*)')
class PasswordResetHandler(BaseHandler):
  def get(self, key):
    if not self.get_user(key):
      raise HTTPError(401)

    self.render('password_reset.html', key=key)

  def post(self, key):
    new, repeat = self.get_argument('new', None), \
      self.get_argument('repeat', None)
    try:
      self.change_password(new, repeat, key)
      self.redirect('/login')

    except ValueError, e:
      self.flash.error = str(e)

    self.render('password_reset.html', key=key)

  def change_password(self, new, repeat, key):
    user = self.get_user(key)
    if not user: raise HTTPError(401)

    if not new or not repeat:
      raise ValueError('All fields are mandatory')

    if new != repeat:
      raise ValueError('Passwords do not match')

    user.set_password(new)
    user.save()

    self.demo.reset.remove({'key': key})

  def get_user(self, key):
    r = self.demo.reset.ResetRequest.find_one({'key':key})
    if not r: return None

    return self.demo.users.User.find_one({'email': r.email})

