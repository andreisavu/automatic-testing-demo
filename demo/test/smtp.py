
import smtpd
import threading
import asyncore

from utils import get_unused_port, wait_for_port

class InMemorySMTP(smtpd.SMTPServer):
  def __init__(self, host='', port=1025):
    self.messages = []
    smtpd.SMTPServer.__init__(self, (host, port), None)

  def process_message(self, peer, mailfrom, rcpttos, data):
    self.messages.append({
      'from': mailfrom,
      'to': rcpttos,
      'data': data
    })

class SMTPTestInstance(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

    self.host = 'localhost'
    self.port = get_unused_port()

    self.server = InMemorySMTP(self.host, self.port)
    wait_for_port(self.host, self.port)

  @property
  def hostport(self):
    return '%s:%s' % (self.host, self.port)

  @property
  def messages(self):
    return self.server.messages[:]

  @property
  def last_message(self):
    if not len(self.server.messages):
      return None
    return self.server.messages[-1]

  def run(self):
    asyncore.loop(timeout=2)

  def stop(self):
    self.server.close()
    asyncore.close_all()
