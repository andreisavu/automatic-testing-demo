""" Test utility classes """

import os, sys, signal
import subprocess
import logging
import time
import socket

from tempfile import mkdtemp, mkstemp
from shutil import rmtree

from pymongo import Connection
from pymongo.errors import ConnectionFailure

def get_unused_port():
  """ Vulnerable to race conditions but good enough for now"""
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 0))
  addr, port = s.getsockname()
  s.close()
  return port

def wait_for_port(host, port):
  s = socket.socket()
  while True:
    try:
      s.connect((host, port))
      s.close()
      return

    except socket.error:
      time.sleep(0.1)

def wait_for_process_exit(pid):
  while True:
    try:
      os.kill(pid, 0)
    except OSError:
      return

def wait_for_pidfile(file_name):
  while True:
    try:
      pid = int(open(file_name).read())
      os.kill(pid, 0)
      return

    except (ValueError, TypeError, OSError, IOError):
      time.sleep(0.1)

def wait_for_mongodb(host, port):
  while True:
    try:
      conn = Connection(host, port, network_timeout=1)
      conn.disconnect()
      return

    except ConnectionFailure:
      time.sleep(0.1)
