# encoding: utf-8

import alert
import db_connection
import datetime


db = db_connection.DbConnection()
items = db.query_queue_all()
queried = {}
if items:
    print "#" * 79
    for item in items:
        subject_code, email = item['subject_code'], item['email']
        print "%s %s %s" % (datetime.datetime.utcnow(), subject_code,
                            email),
        regis_alert = alert.PsuRegisAlert()
        if subject_code in queried:
            regis_dict = queried[subject_code]
            if regis_dict.get('has_room', False):
                print " done"
                regis_alert._noticeEMail(email, regis_dict['subject'],
                                         regis_dict['message'])
                db.remove(item)
            else:
                print ""
        else:
            if regis_alert.alert(subject_code):
                print " done"
                subject = \
                    "[psuAlert] แจ้งเตือนลงวิชา %s" % regis_alert.subject_id
                regis_alert._noticeEMail(email, subject, regis_alert.message)
                db.remove(item)
                queried[subject_code] = {'has_room': True, 'subject': subject,
                                         'message': regis_alert.message}
            else:
                queried[subject_code] = {'has_room': False}
                print ""
    print "#" * 79
