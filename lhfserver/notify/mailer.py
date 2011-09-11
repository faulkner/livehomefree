import smtplib
from email.utils import formatdate
from . import Notify

class Mailer(Notify):
    def send(self, to, subject, message):
        smtp = smtplib.SMTP('localhost')
        msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.options['from_email'],
                to.join(','),
                subject,
                formatdate(),
                message)

        smtp.sendmail(self.options['from_email'], to, msg)
        smtp.quit()

