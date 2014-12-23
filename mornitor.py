# encoding: utf-8

import alert
import db_connection
import datetime


def regis_alert_via_mail(item, email, subject, message):
    regis_alert._noticeEMail(email, subject, message)
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
if items:
    print "#" * 79
    for item in items:
        subject_code, email = item['subject_code'], item['email']
        wanted_sec = item.get('sec', '*')

        print "%s %s %s %s" % (datetime.datetime.utcnow(), subject_code,
                               email, wanted_sec),
        regis_alert = alert.PsuRegisAlert()
        if subject_code in queried:
            regis_dict = queried[subject_code]
            if regis_dict.get('any_room', False):
                if have_wanted_sec(wanted_sec, regis_dict['list_rooms']):
                    print " done",
                    regis_alert_via_mail(item, email, regis_dict['subject'],
                                         regis_dict['message'])
            print ""
        else:
            if regis_alert.alert(subject_code):
                subject = \
                    "[psuAlert] แจ้งเตือนลงวิชา %s" % regis_alert.subject_id
                message = regis_alert.message
                queried[subject_code] = {'any_room': True,
                                         'subject': subject,
                                         'list_rooms': regis_alert.list_rooms,
                                         'message': message}

                if have_wanted_sec(wanted_sec, regis_alert.list_rooms):
                    print " done",
                    regis_alert_via_mail(item, email, subject, message)
            else:
                queried[subject_code] = {'any_room': False}
            print ""
    print "#" * 79
