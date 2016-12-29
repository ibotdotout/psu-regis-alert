import regex as rex
import collections as coll
import urllib2
import contextlib


class PsuRegisQuery(object):

    def __init__(self):
        regex = rex.PsuRegex()
        self.re_subject_id = regex.compile_regex_subject_id()
        self.re_subject_name = regex.compile_regex_subject_name()
        self.re_section = regex.compile_regex_section()
        self.re_reserved = regex.compile_regex_reserved()
        self.re_study_group = regex.compile_regex_study_group()
        self.re_regis = regex.compile_regex_regis()
        self.re_offer = regex.compile_regex_offer()

    def _load_content_page(self, url):
        """ load content page """
        # Enable cookier to avoid self redirect
        # http://stackoverflow.com/questions/4098702/python-urllib2-urlopen-returning-302-error-even-though-page-exists
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        with contextlib.closing(opener.open(url)) as socket:
            return socket.read()

    def _helper_search(self, x, y, start=None):
        return x.search(y[start:])

    def _result_message(self, data, rooms):
        sec, reserved, study_group, regis, offer = data
        can_regis = ""
        if int(regis) < int(offer) and not reserved:
            rooms[sec] = True
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

        results = []
        rooms = coll.defaultdict(bool)
        for m in result_section:
            data = self._query_each_section(m, content)
            x = self._result_message(data, rooms)
            if x:
                results.append(x)
        return results, rooms

    def query(self, url):
        content = self._load_content_page(url)

        result_subject_id = self._helper_search(self.re_subject_id, content)

        result_subject_name = \
            self._helper_search(self.re_subject_name,
                                content, result_subject_id.end())

        results, rooms = \
            self._query_section_data(content, result_subject_name.end())

        return (result_subject_id.group(),
                result_subject_name.group(), results), rooms
