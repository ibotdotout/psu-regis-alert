# encoding: utf-8
import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import ConfigParser


class SendMail():
    @classmethod
    def send(cls, toaddr, subject, message):
        """
        Provide gmail user name and password
        Credit :
            http://code.activestate.com/recipes/577371-sending-gmail-though-python-code/
            http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email/
        """
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

        username = config.get('DEFAULT', 'username')
        password = config.get('DEFAULT', 'password')
        smtp_host = config.get('DEFAULT', 'smtp')

        fromaddr = username

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        body = message

        msg.attach(MIMEText(body, 'plain'))

        # functions to send an email
        server = smtplib.SMTP(smtp_host)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
