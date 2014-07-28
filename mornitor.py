# encoding: utf-8

import alert
import db_connection


db = db_connection.DbConnection()

for item in db.query_all():
    subject_code = item['subject_code']
    email = item['email']
    regis_alert = alert.PsuRegisAlert()
    if regis_alert.alert(subject_code):
        subject = "[psuAlert] แจ้งเตือนลงวิชา %s" % regis_alert.subject_id
        regis_alert._noticeEMail(email, subject, regis_alert.message)
        db.remove(item)
