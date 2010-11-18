
from demo.test.mongo import MongoTestInstance

from demo.db import get_connection

class MongoTestMixin(object):

  def setUpMongo(self):
    self.mongodb = MongoTestInstance()
    self.mongodb.start()

    self.mongo = get_connection(self.mongodb.host, self.mongodb.port)
    self.demo = self.mongo.demo
    
    return self.mongodb.hostport

  def tearDownMongo(self):
    self.mongo.disconnect()
    self.mongodb.stop()

  def dumplog(self, out = None): pass

  def create_user(self, email, password = None):
    u = self.demo.users.User()
    u.email = email
    u.set_password(password or email)
    u.save()
    return u
