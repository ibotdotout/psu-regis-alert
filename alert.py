#!/usr/bin/env python
# encoding: utf-8

import send_mail
import query


class PsuRegisAlert(object):

    def __init__(self):
        self.regis_query = query.PsuRegisQuery()

    def send_notice_mail(self, toaddr, subject, message):
        send_mail.SendMail.send(toaddr, subject, message)

    def _display_result(self, subject_id, subject_name, results):
        return (
            subject_id +
            "\n" +
            subject_name +
            "\n" +
            "sec " +
            "\nsec ".join(results))

    def list_sec_rooms(self, sec_rooms):
        list_sec = []
        for k, v in sec_rooms.items():
            if v:
                list_sec.append(k)
        return list_sec

    def alert(self, url):
        result, sec_rooms = self.regis_query.query(url)
        subject_id, _, has_room = result

        if has_room:
            self.subject_id = subject_id
            self.message = self._display_result(*result)
            self.list_rooms = self.list_sec_rooms(sec_rooms)
            return True
        else:
            self.subject_id = ""
            self.message = "No room"
            self.list_rooms = None
            return False

if __name__ == '__main__':
    email = None
    # hatyai normal url
    url = \
        "https://sis-hatyai6.psu.ac.th/WebRegist2005/" \
        "SubjectInfo.aspx?subject=2558100048520119"
    # hatyai normal url with login require
    # that should avoid by remove /Student
    url = "https://sis-hatyai46.psu.ac.th/WebRegist2005/" \
        "Student/SubjectInfo.aspx?subject=2558100064080120"
    # phuket normal url
    # that should enable cookie before open request
    url = "https://sis-phuket4.psu.ac.th/WebRegist2005/" \
        "SubjectInfo.aspx?subject=2558100024830001"
    alert = PsuRegisAlert()
    try:
        if alert.alert(url):
            print alert.list_rooms
        print alert.message
    except AttributeError as e:
        print(e)
