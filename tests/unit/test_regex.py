import unittest
import regex


class RegexTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.re = regex.PsuRegex()

    def test_helper_pattern(self):
        pattern = self.re.helper_pattern('', '', '')
        self.assertTrue('(?<=)(?=)' in pattern)

    def test_compile_regex_subject_id(self):
        regexp = self.re.compile_regex_subject_id()
        for i in self.re.pattern['subject_id']:
            self.assertTrue(i in regexp.pattern)

    def test_compile_regex_subject_name(self):
        regexp = self.re.compile_regex_subject_name()
        for i in self.re.pattern['subject_name']:
            self.assertTrue(i in regexp.pattern)

    def test_compile_regex_section(self):
        regexp = self.re.compile_regex_section()
        for i in self.re.pattern['section']:
            self.assertTrue(i in regexp.pattern)

    def test_compile_regex_reserved(self):
        regexp = self.re.compile_regex_reserved()
        for i in self.re.pattern['reserved']:
            self.assertTrue(i in regexp.pattern)

    def test_compile_regex_study_group(self):
        regexp = self.re.compile_regex_study_group()
        for i in self.re.pattern['study_group']:
            self.assertTrue(i in regexp.pattern)

    def test_compile_regex_regis(self):
        regexp = self.re.compile_regex_regis()
        for i in self.re.pattern['regis']:
            self.assertTrue(i in regexp.pattern)

    def test_compile_regex_offer(self):
        regexp = self.re.compile_regex_offer()
        for i in self.re.pattern['offer']:
            self.assertTrue(i in regexp.pattern)
