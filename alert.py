#!/usr/bin/env python
# encoding: utf-8

import send_mail
import query


class PsuRegisAlert():
    URL = "https://sis-hatyai6.psu.ac.th/WebRegist2005/" \
          "SubjectInfo.aspx?subject=%s"

    def __init__(self):
        self.regis_query = query.PsuRegisQuery()

    def _noticeEMail(self, toaddr, subject, message):
        send_mail.SendMail.send(toaddr, subject, message)

    def _display_result(self, subject_id, subject_name, results):
        return (subject_id + "\n" + subject_name + "\n"
                + "sec " + "\nsec ".join(results))

    def alert(self, subject_code, sec_list=None):
        url = self.URL % subject_code

        result, sec_rooms = self.regis_query.query(url)
        subject_id, subject_name, has_room = result

        if has_room:
            if sec_list:
                has_wanted_room = any([sec_rooms[i] for i in sec_list])
            else:
                has_wanted_room = True

        if has_wanted_room:
            self.subject_id = subject_id
            self.message = self._display_result(*result)
            return True
        else:
            self.subject_id = ""
            self.message = "No room"
            return False

if __name__ == '__main__':
    email = None
    subject_code = 2557200048520119
    alert = PsuRegisAlert()
    # alert.alert(subject_code, "01,03,02")
    alert.alert(subject_code)
    print alert.message
