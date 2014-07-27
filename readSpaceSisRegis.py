#!/usr/bin/env python
# encoding: utf-8

import re


class SendMail():
    @classmethod
    def send(cls, toaddr, message):
        """
        Provide gmail user name and password
        Credit :
            http://code.activestate.com/recipes/577371-sending-gmail-though-python-code/
            http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email/
        """
        import smtplib
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText
        import ConfigParser

        config = ConfigParser.ConfigParser()
        config.read('config.ini')

        username = config.get('DEFAULT', 'username')
        password = config.get('DEFAULT', 'password')
        smtp_host = config.get('DEFAULT', 'smtp')

        fromaddr = username

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "[psuAlert] แจ้งเตือนลงวิชา xxx-xxx"

        body = message

        msg.attach(MIMEText(body, 'plain'))

        # functions to send an email
        server = smtplib.SMTP(smtp_host)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()


class PsuRegex():
    pattern_form = "(?<={start}){re}(?={end})"
    pattern = {'subject_id': ('<td>', r'\d{3}-\d{3}'),
               'subject_name': ('><b>ชื่อภาษาอังกฤษ</b></td><td>',
                                '.*', '</td>'),
               'session': ('SECTION_NOLabel">', r'\d\d', '</span>'),
               'reserved': ('RESERVEDLabel">', '.*', '</span>'),
               'study_group': ('STUDY_GROUPLabel">', '.*', '</span>'),
               'regis': ('NO_REGISTLabel">', r'\d{1,3}', '</span>'),
               'offer': ('NO_OFFERLabel">', r'\d{1,3}', '</span>')
               }

    def helper_pattern(self, start, re, end=''):
        """ Regex Patterns """
        return self.pattern_form.format(start=start, re=re, end=end)

    def compile_regex_suject_id(self):
        subject_id_pattern = \
            self.helper_pattern(*self.pattern['subject_id'])
        return re.compile(subject_id_pattern)

    def compile_regex_subject_name(self):
        subject_name_pattern = \
            self.helper_pattern(*self.pattern['subject_name'])
        return re.compile(subject_name_pattern)

    def compile_regex_section(self):
        section_pattern = self.helper_pattern(*self.pattern['session'])
        return re.compile(section_pattern)

    def compile_regex_reserved(self):
        reserved_pattern = self.helper_pattern(*self.pattern['reserved'])
        return re.compile(reserved_pattern)

    def compile_regex_study_group(self):
        study_group_pattern = self.helper_pattern(*self.pattern['study_group'])
        return re.compile(study_group_pattern)

    def complie_regex_regis(self):
        regis_pattern = self.helper_pattern(*self.pattern['regis'])
        return re.compile(regis_pattern)

    def compile_regex_offer(self):
        offer_pattern = self.helper_pattern(*self.pattern['offer'])
        return re.compile(offer_pattern)


class PsuRegisQuery():
    def __init__(self):
        regex = PsuRegex()
        self.re_subject_id = regex.compile_regex_suject_id()
        self.re_subject_name = regex.compile_regex_subject_name()
        self.re_section = regex.compile_regex_section()
        self.re_reserved = regex.compile_regex_reserved()
        self.re_study_group = regex.compile_regex_study_group()
        self.re_regis = regex.complie_regex_regis()
        self.re_offer = regex.compile_regex_offer()

    def _load_content_page(self, url):
        """ load content page """
        import urllib2 as urllib
        import contextlib
        with contextlib.closing(urllib.urlopen(url)) as socket:
            return socket.read()

    def _helper_search(self, x, y, start=None):
        return x.search(y[start:])

    def _result_message(self, data):
        sec, reserved, study_group, regis, offer = data
        can_regis = ""
        if regis < offer:
            can_regis = "regisable" + "  " + reserved
        if len(regis) < len(offer):
            regis = "0" * (len(offer) - len(regis)) + regis
        return \
            "%s %s/%s %s %s" % (sec, regis, offer, study_group, can_regis)

    def _query_each_section(self, m, content):
        curr = m.end()
        data = [m.group()]
        re_group = [self.re_reserved, self.re_study_group,
                    self.re_regis, self.re_offer]
        for i in re_group:
            last_re = self._helper_search(i, content, curr)
            data.append(last_re.group())
        return data

    def _query_section_data(self, content, start=None):

        result_section = \
            self.re_section.finditer(content[start:])

        return [self._result_message(self._query_each_section(m, content))
                for m in result_section]

    def query(self, url):
        content = self._load_content_page(url)

        result_subject_id = self._helper_search(self.re_subject_id, content)

        result_subject_name = \
            self._helper_search(self.re_subject_name,
                                content, result_subject_id.end())

        results = self._query_section_data(content,
                                           result_subject_name.end())

        return (result_subject_id.group(),
                result_subject_name.group(), results)


class PsuRegisAlert():
    URL = "https://sis-hatyai6.psu.ac.th/WebRegist2005/" \
          "SubjectInfo.aspx?subject=%s"

    def __init__(self):
        self.regis_query = PsuRegisQuery()

    def _noticeEMail(self, toaddr, message):
        SendMail.send(toaddr, message)

    def _display_result(self, subject_id, subject_name, results):
            return subject_id + "\n" + subject_name + "\n" + '\n'.join(results)

    def alert(self, subject_code, email):
        url = self.URL % subject_code

        result = self.regis_query.query(url)

        message = self._display_result(*result)

        if email:
            self._noticeEMail(email, message)
        else:
            print message


if __name__ == '__main__':
    email = None
    subject_code = 2556100048520119
    alert = PsuRegisAlert()
    alert.alert(subject_code, email)