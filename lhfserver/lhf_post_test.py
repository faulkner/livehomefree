#!/usr/bin/python
# Copyright 2011 Aditya Ojha

import getopt
import httplib, urllib
import sys

#LHF_SERVER_ADDR = 'swlivehomefree2.appspot.com:80'
#LHF_SERVER_ADDR = 'localhost:8083'
LHF_SERVER_ADDR = 'livehomefreeprod.appspot.com:80'


def testAlert():
  params = urllib.urlencode({'cmd': 'alert', 'phone': '2222222222'})
  headers = {"Content-type": "application/x-www-form-urlencoded",
             "Accept": "text/plain"}
  conn = httplib.HTTPConnection(LHF_SERVER_ADDR)
  conn.request("POST", "/", params, headers)
  response = conn.getresponse()
  print response.status, response.reason
  data = response.read()
  print data
  conn.close()


def testConfigure():
  params = urllib.urlencode({'cmd': 'configure', 'phone': '7637426596',
                             'primary_phone': '4084312586',
                             'primary_email': 'adityao@gmail.com'})
  headers = {"Content-type": "application/x-www-form-urlencoded",
             "Accept": "text/plain"}
  conn = httplib.HTTPConnection(LHF_SERVER_ADDR)
  conn.request("POST", "/", params, headers)
  response = conn.getresponse()
  print response.status, response.reason
  data = response.read()
  print data
  conn.close()

class Usage(Exception):
  def __init__(self, msg):
      self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["alert", "configure"])
        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    print opts
    print args

    for arg, val in opts:
        print arg, val
        if arg == '--alert':
            testAlert()
        elif arg == '--configure':
            testConfigure()
        else:
            raise Usage('Bad option %s' % arg)
    

if __name__ == '__main__':
    sys.exit(main(argv=sys.argv))
