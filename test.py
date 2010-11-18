#!/usr/bin/env python

import unittest
import logging

from demo.test.functional.auth import AuthTest

if __name__ == '__main__':
  logging.basicConfig(level = logging.ERROR)
  unittest.main()

