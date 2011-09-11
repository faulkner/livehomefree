from twilio.rest import TwilioRestClient

class Notify(object):
    def __init__(self, options):
        # TODO: what's the ideal way to import this?
        self.options = options

    def email(self, to, subject, message):
        mail = mailer.Mailer(self.options)
        mail.send(to, subject, message)

    def sms(self, to, message, **kwargs):
        client = TwilioRestClient()
        message = client.sms.messages.create(
                to=to,
                from_=self.options['twillio_from_sms'],
                body=message)

    def call(self, to, message, **kwargs):
        client = TwilioRestClient()
        client.calls.create(to=to, from_=self.options['twillio_from_phone'], url=self.options['twillio_call_url'])

import mailer
