# Copyright 2011 Aditya Ojha

import os

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError
#from django.http import HttpResponse


class MonitorRecord(object):
  """Monitor DB Record."""
  def __init__(self, phone, email):
    self.dst_phone_num = phone
    self.dst_email_addr = email

  def update(self, phone, email):
    self.dst_phone_num = phone
    self.dst_email_addr = email


class MonitorDB(object):
  """Monitor DB."""
  def __init__(self, phone, mr):
    self.mdb_dict = {phone: mr}


def CreateTestDataset():
  """Create test data set."""
  mr = MonitorRecord('408-431-2586', 'livehomefreesw@gmail.com')
  return MonitorDB('408-431-2586', mr)


class MainPage(webapp.RequestHandler):

  def get(self):
    """Handler for HTTP GET.""" 
    try:
      template_values = { 'title': "LiveHomeFree", }
      #path = os.path.join(os.path.dirname(__file__), 'index.html')
      path = os.path.join(os.path.dirname(__file__), 'live-home-free-alert-configuration.htm')
      self.response.out.write(template.render(path, template_values))
    except DeadlineExceededError:
      self.response.clear()
      self.response.set_status(500)
      self.response.out.write('Oops! Something bad happened while serving your GET request')

  def _AlertDestination(self, phone, mr):
    """Send alert notification to the registered destination."""
    self.response.out.write('Send alert to dst email: %s\n' % mr.dst_email_addr)
    mail.send_mail(sender='Live Home Free<livehomefreesw@gmail.com>',
                   to=mr.dst_email_addr,
                   subject='URGENT!! Alert from %s' % phone,
                   body='Please contact %s ASAP!' % phone)

  def _HandleAlert(self):
    """Handle alert message from monitor."""
    #self.response.set_status(100)
    phone = self.request.get('phone')
    print 'phone %s' % phone
    if phone:
      self.response.out.write('Recd cmd ALERT from phone num: %s\n' % phone)
      mr = mdb.mdb_dict.get(phone)
      self.response.out.write('keys %s\n' % mdb.mdb_dict.keys())
      if mr:
        print 'alert for %s' % phone
        self._AlertDestination(phone, mr)
      else:
        self.response.out.write('Bad POST from phone num: %s\n' % phone)
    else:
      self.response.out.write('Bad phone number %s in POST\n' % phone)

  def _HandleConfigure(self):
    """Handle configuration update from website/app."""
    phone = self.request.get('phone')
    p_phone = self.request.get('primary_phone')
    p_email = self.request.get('primary_email')
    if phone:
      self.response.out.write('Recd monitor config for phone num: %s\n' % phone)
      mr = mdb.mdb_dict.get(phone)
      if mr:
        # exists, update
        self.response.out.write('Update record for phone num: %s\n' % phone)
        mr.update(p_phone, p_email)
      else:
        # new, create
        self.response.out.write('Create record for phone num: %s\n' % phone)
        mr = MonitorRecord(p_phone, p_email)
        mdb.mdb_dict[phone] = mr
    else:
      self.response.out.write('Bad phone number %s in POST\n' % phone)    

  def post(self):
    """Handler for HTTP POST."""
    try:
      cmd = self.request.get('cmd')
      self.response.out.write('Recd cmd %s\n'% cmd)

      # Configuration create/update from config UI on web-server/app
      if cmd == 'configure':
        self._HandleConfigure()

      # alert sent from monitor end-point
      if cmd == 'alert':
        self._HandleAlert()

    except DeadlineExceededError:
      self.response.clear()
      self.response.set_status(500)
      self.response.out.write('Oops! Something bad happened while serving your POST request')


# WSGI application
application = webapp.WSGIApplication([('/', MainPage)], debug=True)
# Monitor Database
mdb = CreateTestDataset()

def main():
  """Main method."""
  run_wsgi_app(application)

if __name__ == '__main__':
    main()
