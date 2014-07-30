# encoding: utf-8

import alert
import db_connection
import datetime


db = db_connection.DbConnection()
items = db.query_queue_all()
if items:
    for item in items:
        subject_code, email = item['subject_code'], item['email']
        print "%s %s %s" % (datetime.datetime.utcnow(), subject_code,
                            email),
        regis_alert = alert.PsuRegisAlert()
        if regis_alert.alert(subject_code):
            print " done"
            subject = "[psuAlert] แจ้งเตือนลงวิชา %s" % regis_alert.subject_id
            regis_alert._noticeEMail(email, subject, regis_alert.message)
            db.remove(item)
        else:
            print ""
