# encoding: utf-8

import re


class PsuRegex():
    pattern_form = "(?<={start}){re}(?={end})"
    pattern = {'subject_id': ('<td>', r'\d{3}-\d{3}'),
               'subject_name': ('><b>ชื่อภาษาอังกฤษ</b></td><td>',
                                '.*', '</td>'),
               'section': ('SECTION_NOLabel">', r'\d\d', '</span>'),
               'reserved': ('RESERVEDLabel">', '.*', '</span>'),
               'study_group': ('STUDY_GROUPLabel">', '.*', '</span>'),
               'regis': ('NO_REGISTLabel">', r'\d{1,3}', '</span>'),
               'offer': ('NO_OFFERLabel">', r'\d{1,3}', '</span>')
               }

    def helper_pattern(self, start, re, end=''):
        """ Regex Patterns """
        return self.pattern_form.format(start=start, re=re, end=end)

    def compile_regex_subject_id(self):
        subject_id_pattern = \
            self.helper_pattern(*self.pattern['subject_id'])
        return re.compile(subject_id_pattern)

    def compile_regex_subject_name(self):
        subject_name_pattern = \
            self.helper_pattern(*self.pattern['subject_name'])
        return re.compile(subject_name_pattern)

    def compile_regex_section(self):
        section_pattern = self.helper_pattern(*self.pattern['section'])
        return re.compile(section_pattern)

    def compile_regex_reserved(self):
        reserved_pattern = self.helper_pattern(*self.pattern['reserved'])
        return re.compile(reserved_pattern)

    def compile_regex_study_group(self):
        study_group_pattern = self.helper_pattern(*self.pattern['study_group'])
        return re.compile(study_group_pattern)

    def compile_regex_regis(self):
        regis_pattern = self.helper_pattern(*self.pattern['regis'])
        return re.compile(regis_pattern)

    def compile_regex_offer(self):
        offer_pattern = self.helper_pattern(*self.pattern['offer'])
        return re.compile(offer_pattern)
