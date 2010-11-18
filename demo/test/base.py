
from demo.test import MixinTestCase
from demo.test.mixins import MongoTestMixin, \
  SMTPTestMixin, FrontendTestMixin

class WebApplicationTestCase(MixinTestCase, MongoTestMixin, \
  SMTPTestMixin, FrontendTestMixin):

  def setUp(self):
    self.setUpFrontend({
      'mongodb': self.setUpMongo(),
      'smtp': self.setUpSMTP()
    })

  def tearDown(self):
    self.tearDownFrontend()
    self.tearDownMongo()
    self.tearDownSMTP()
