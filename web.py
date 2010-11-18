#!/usr/bin/env python

import sys

from demo.tornado_utils import start
from demo.web import Application

if __name__ == '__main__':
  sys.exit(start(Application))
