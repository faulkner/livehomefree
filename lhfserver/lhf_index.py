# Copyright 2011 Aditya Ojha

import os
import datetime
import logging

from google.appengine.ext import db
from google.appengine.api import users

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError



class MonitorDB(db.Model):
  """Monitor DB class."""
  phone = db.StringProperty(required=True)
  primary_phone = db.StringProperty(required=True)
  primary_email = db.StringProperty(required=True)
  #timestamp = db.DateProperty()

#   name = db.StringProperty(required=True)
#   role = db.StringProperty(required=True, choices=set(["executive", "manager", "producer"]))
#   hire_date = 
#   new_hire_training_completed = db.BooleanProperty()
#   account = db.UserProperty()
# training_registration_list = [users.User("Alfred.Smith@example.com"),
#                               users.User("jharrison@example.com"),
#                               users.User("budnelson@example.com")]

from notify import Notify
from configobj import ConfigObj

class MonitorRecord(object):
  """Monitor DB Record."""
  def __init__(self, phone, email):
    self.dst_phone_num = phone
    self.dst_email_addr = email

  def update(self, phone, email):
    self.dst_phone_num = phone
    self.dst_email_addr = email


# class MonitorDB(object):
#   """Monitor DB."""
#   def __init__(self, phone, mr):
#     self.mdb_dict = {phone: mr}


def CreateTestDataset():
  """Create test data set."""
  #mr = MonitorRecord('408-431-2586', 'livehomefreesw@gmail.com')
  mdb = MonitorDB(phone="408-431-2586",
                  primary_phone="408-431-2586",
                  primary_email="livehomefreesw@gmail.com")
  #e.hire_date = datetime.datetime.now().date()
  mdb.put()

  return MonitorDB('408-431-2586', mr)


class MainPage(webapp.RequestHandler):

  def get(self):
    """Handler for HTTP GET.""" 
    try:
      template_values = { 'title': "LiveHomeFree", }
      #path = os.path.join(os.path.dirname(__file__), 'index.html')
      #path = os.path.join(os.path.dirname(__file__), 'live-home-free-alert-configuration.htm')
      path = os.path.join(os.path.dirname(__file__), 'templates/configure.html')
      self.response.out.write(template.render(path, template_values))
    except DeadlineExceededError:
      self.response.clear()
      self.response.set_status(500)
      self.response.out.write('Oops! Something bad happened while serving your GET request')

  def _AlertDestination(self, phone, mr):
    """Send alert notification to the registered destination."""
    self.response.out.write('Send alert to dst email: %s\n' % mr.primary_email)
    s = 'Live Home Free<livehomefreesw@gmail.com>'
    sub = 'URGENT!! Alert from %s' % phone
    body = 'Please contact %s ASAP!' % phone
    logging.debug('sender: %s\nto: %s\nsub: %s\nbody: %s' % (s, mr.primary_email, sub, body))

    # TODO: less-ugly config management
#     config = ConfigObj('config.ini')
#     os.environ["TWILIO_ACCOUNT_SID"] = config['twillio_account']
#     os.environ["TWILIO_AUTH_TOKEN"] = config['twillio_token']

#     n = Notify(config)
#     n.sms(phone, 'Please contact %s ASAP!' % phone)

    self.response.out.write('Send alert to dst email: %s\n' % mr.primary_email)
    # TODO: enable for demo
#     mail.send_mail(sender=s,
#                    to=mr.primary_email,
#                    subject=sub,
#                    body=body)

  def _HandleAlert(self):
    """Handle alert message from monitor."""
    #self.response.set_status(100)
    phone = self.request.get('phone')
    print 'phone %s' % phone
    if phone:
      self.response.out.write('Recd cmd ALERT from phone num: %s\n' % phone)
      #mr = mdb.mdb_dict.get(phone)
      #self.response.out.write('keys %s\n' % mdb.mdb_dict.keys())
      mrecs = db.GqlQuery("SELECT * FROM MonitorDB WHERE phone = :1",
                          phone)
#       if len(mr) > 1:
#         self.response.out.write('More than 1 monitor config for phone num: %s\n' % phone)
#         return

      for mr in mrecs:
        print 'alert for %s' % phone
        self._AlertDestination(phone, mr)
        return

      self.response.out.write('Bad POST from phone num: %s\n' % phone)
    else:
      self.response.out.write('Bad phone number %s in POST\n' % phone)

  def _HandleConfigure(self):
    """Handle configuration update from website/app."""
    phone = self.request.get('phone') + self.request.get('phone-1') + self.request.get('phone-2')
    p_phone = self.request.get('primary_phone') + self.request.get('primary_phone-1') + self.request.get('primary_phone-2')
    p_email = self.request.get('primary_email')
    if phone:
      self.response.out.write('Recd monitor config for phone num: %s\n' % phone)
      #mr = mdb.mdb_dict.get(phone)
      mrecs = db.GqlQuery("SELECT * FROM MonitorDB WHERE phone = :1",
                       phone)
#       if len(mr) > 1:
#         self.response.out.write('More than 1 monitor config for phone num: %s\n' % phone)
#         return
      for mr in mrecs:
        # exists, update
        self.response.out.write('Update record for phone num: %s\n' % phone)
        #mr.update(p_phone, p_email)
        mr.primary_phone = p_phone
        mr.primary_email = p_email
        db.put(mr)
        return
      
      # new entry, create and add it to db
      self.response.out.write('Create record for phone num: %s\n' % phone)
        #mr = MonitorRecord(p_phone, p_email)
        #mdb.mdb_dict[phone] = mr
      mr = MonitorDB(phone=phone,
                     primary_phone=p_phone,
                     primary_email=p_email)
      mr.put()
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
        return

      # alert sent from monitor end-point
      if cmd == 'alert':
        self._HandleAlert()
        return
    except DeadlineExceededError:
      self.response.clear()
      self.response.set_status(500)
      self.response.out.write('Oops! Something bad happened while serving your POST request')


# WSGI application
application = webapp.WSGIApplication([('/', MainPage)], debug=True)
# Monitor Database
#mdb = CreateTestDataset()

def main():
  """Main method."""
  run_wsgi_app(application)

if __name__ == '__main__':
    main()
