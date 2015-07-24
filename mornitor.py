# encoding: utf-8

import alert
import db_connection
import datetime
from line_client import Line


def regis_notice(item, email, line_id, subject, message):
    if email:
        mail_notic(item, email, subject, message)
    if line_id:
        line_notice(item, line_id, subject + '\n' + message)


def mail_notic(item, email, subject, message):
    regis_alert.send_notice_mail(email, subject, message)
    db.remove(item)


def line_notice(item, line_id, message):
    line.send(line_id, message)
    db.remove(item)


def have_wanted_sec(wanted_sec, list_rooms):
    if wanted_sec == '*':
        return True
    else:
        wanted_list = wanted_sec.split(',')
        return any([i in list_rooms for i in wanted_list])


db = db_connection.DbConnection()
items = db.query_queue_all()
queried = {}
line = Line()
if items:
    print "#" * 79
    for item in items:
        subject_code = item['subject_code']
        line_id = item.get('line_id', '')
        email = item.get('email', '')
        wanted_sec = item.get('sec', '*')

        print "%s %s %s %s %s" % (datetime.datetime.utcnow(), subject_code,
                                  wanted_sec, email, line_id),

        regis_alert = alert.PsuRegisAlert()
        if subject_code in queried:
            regis_dict = queried[subject_code]
            if regis_dict.get('any_room', False):
                if have_wanted_sec(wanted_sec, regis_dict['list_rooms']):
                    print " done",
                    regis_notice(item, email, line_id,
                                 regis_dict['subject'], regis_dict['message'])
            print ""
        else:
            if regis_alert.alert(subject_code):
                subject = \
                    "[psuAlert] แจ้งเตือนลงวิชา %s" % regis_alert.subject_id
                message = regis_alert.message
                queried[subject_code] = {
                    'any_room': True,
                    'subject': subject,
                    'list_rooms': regis_alert.list_rooms,
                    'message': message}

                if have_wanted_sec(wanted_sec, regis_alert.list_rooms):
                    print " done",
                    regis_notice(item, email, line_id, subject, message)
            else:
                queried[subject_code] = {'any_room': False}
            print ""
    print "#" * 79
