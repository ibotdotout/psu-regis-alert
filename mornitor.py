# encoding: utf-8

import alert
import db_connection
import datetime
from line_client import Line
import logging


def regis_notice(item, email, line_id, subject, message):
    if email:
        mail_notic(item, email, subject, message)
    if line_id:
        line_notice(item, line_id, subject + '\n' + message)
    db.remove(item)


def mail_notic(item, email, subject, message):
    regis_alert.send_notice_mail(email, subject, message)


def line_notice(item, line_id, message):
    line.send(line_id, message)


def have_wanted_sec(wanted_sec, list_rooms):
    have = True
    if wanted_sec != '*':
        wanted_list = wanted_sec.split(',')
        have = any([i in list_rooms for i in wanted_list])
    return have


def get_values(item):
    subject_code = item.get('subject_code', '')
    url = item.get('url', '')
    line_id = item.get('line_id', '')
    line_id = item.get('line_id', '')
    email = item.get('email', '')
    wanted_sec = item.get('sec', '*')
    return (url, subject_code, line_id, email, wanted_sec)


def update_quried(queried, url, subject_code, regis_alert):
    if subject_code not in queried:
        if regis_alert.alert(url):
            queried = new_quried(queried, subject_code, regis_alert)
        else:
            queried[subject_code] = {'any_room': False}
    return queried


def new_quried(queried, subject_code, reigs_alert):

    def _new_quried(subject, list_rooms, message):
        return {'any_room': True, 'subject': subject,
                'list_rooms': list_rooms, 'message': message}

    subject = "[psuAlert] แจ้งเตือนลงวิชา %s" % regis_alert.subject_id
    message = regis_alert.message

    queried[subject_code] = \
        _new_quried(subject, regis_alert.list_rooms, message)
    return queried


def have_room_that_wanted(regis_dict, wanted_sec):
    return regis_dict.get('any_room', False) and \
        have_wanted_sec(wanted_sec, regis_dict['list_rooms'])


def print_item(subject_code, wanted_sec, email, line_id, result):
    values = (datetime.datetime.utcnow(), subject_code,
              wanted_sec, email, line_id)
    line = " ".join([str(i) for i in values])
    if result:
        line += 'done'
    print(line)


def print_separate_line():
    print('#' * 79)


logging.basicConfig(format='%(asctime)s %(message)s')
db = db_connection.DbConnection()
items = db.query_queue_all()
cached_queried = {}
line = Line()

if items:
    print_separate_line()
    for item in items:
        url, subject_code, line_id, email, wanted_sec = get_values(item)

        regis_alert = alert.PsuRegisAlert()

        have_room = None
        try:
            cached_queried = \
                update_quried(cached_queried, url, subject_code, regis_alert)

            regis_dict = cached_queried[subject_code]

            have_room = have_room_that_wanted(regis_dict, wanted_sec)
            if have_room:
                regis_notice(item, email, line_id,
                             regis_dict['subject'], regis_dict['message'])
        except AttributeError as e:
            logging.error("%s", e)

        print_item(subject_code, wanted_sec, email, line_id, have_room)
    print_separate_line()
