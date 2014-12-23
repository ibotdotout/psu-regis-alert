import unittest
import mock
import send_mail


class SendMailTest(unittest.TestCase):
    def test_mock_send_mail(self):
        send_to = "test@hellotest.com"
        subject = "Hello world"
        message = "Are you human ?"

        with mock.patch('ConfigParser.ConfigParser.get') as mock_config:
            with mock.patch('smtplib.SMTP') as mock_smtp:
                    mock_config.side_effect = ["username", "password", "host"]
                    mock_sendmail = mock_smtp.return_value.sendmail

                    send_mail.SendMail.send(send_to, subject, message)

                    mock_smtp.assert_called_once_with("host")
                    mock_sendmail.assert_called_once()

                    args, kwargs = mock_sendmail.call_args
                    fromaddr, toaddr, msg = args
                    self.assertEqual("username", fromaddr)
                    self.assertEqual(send_to, toaddr)
                    self.assertRegexpMatches(msg, subject)
                    self.assertRegexpMatches(msg, message)
