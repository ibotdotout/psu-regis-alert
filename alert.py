#!/usr/bin/env python
# encoding: utf-8

import send_mail
import query


class PsuRegisAlert():
    URL = "https://sis-hatyai6.psu.ac.th/WebRegist2005/" \
          "SubjectInfo.aspx?subject=%s"

    def __init__(self):
        self.regis_query = query.PsuRegisQuery()

    def _noticeEMail(self, toaddr, message):
        send_mail.SendMail.send(toaddr, message)

    def _display_result(self, subject_id, subject_name, results):
            return subject_id + "\n" + subject_name + "\n" + '\n'.join(results)

    def alert(self, subject_code):
        url = self.URL % subject_code

        result = self.regis_query.query(url)
        subject_id, subject_name, room = result
        if room:
            self.message = self._display_result(*result)
            return True
        else:
            self.message = "No room"
            return False

if __name__ == '__main__':
    email = None
    subject_code = 2557100048520119
    alert = PsuRegisAlert()
    alert.alert(subject_code, email)
    print alert.message
