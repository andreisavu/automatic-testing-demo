
import unittest
import re

from StringIO import StringIO

class MixinLogDumper(type):
  def __new__(cls, name, bases, dict):
    def is_mixin(cls):
      return re.match('^.+?Mixin$', cls.__name__) is not None

    def dump_logs(self, mro_list):
      """ dump logs for all mixin classes with a dumplog method """
      mixins = filter(is_mixin, mro_list)
      for cls in set(mixins):
        try:
          output = StringIO()
          getattr(cls, 'dumplog')(self, output)

          if output.getvalue().strip():
            print '*** %s Output' % cls.__name__
            print output.getvalue()

        except (AttributeError, TypeError):
          continue

    def allbases(bases):
      if not bases: return set()
      result = set()
      for klass in bases:
        try:
          result.add(klass)
          result.update(allbases(klass.mro()[1:]))
        except AttributeError:
          pass
      return result

    def decorate(fn):
      def wrapper(self, *args, **kwargs):
        try:
          return fn(self, *args, **kwargs)

        except Exception:
          dump_logs(self, allbases(bases))
          raise

      wrapper.__name__ = fn.__name__
      wrapper.__doc__ == fn.__doc__

      return wrapper

    for attr, value in dict.items():
      if callable(value) and attr.startswith('test_'):
        dict[attr] = decorate(value)

    return type.__new__(cls, name, bases, dict)

class MixinTestCase(unittest.TestCase):
  __metaclass__ = MixinLogDumper
