import alert
import db_connection


db = db_connection.DBConnection()

for item in db.query_all():
    subject_code = item['subject_code']
    email = item['email']
    regis_alert = alert.PsuRegisAlert()
    if regis_alert.alert(subject_code):
        regis_alert._noticeEMail(email, regis_alert.message)
        db.remove(item)
