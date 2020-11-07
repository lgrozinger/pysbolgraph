import unittest
import requests
from pathlib import Path


from pysbolgraph.SBOL2Graph import SBOL2Graph as Graph


SBOL2DIR = Path(__file__).parent.parent / "SBOLTestSuite" / "SBOL2"
FILEPATHS = SBOL2DIR.glob("*.xml")
ENDPOINT = "https://validator.sbolstandard.org/validate/"


request = {
    'options': {
        'language': 'SBOL2',
        'test_equality': True,
        'check_uri_compliance': False,
        'check_completeness': False,
        'check_best_practices': False,
        'continue_after_first_error': True,
        'provide_detailed_stack_trace': False,
        'insert_type': False,
        'uri_prefix': 'http://foo/',
        'main_file_name': 'main file',
        'diff_file_name': 'comparison file',
    },
    'return_file': False,
    'main_file': None,
    'diff_file': None
}


def generate_test(path):
    def test(self):
        self.case = path.stem
        g = Graph()
        g.load(str(path))
        with open(path) as main:
            request['main_file'] = main.read()
            request['diff_file'] = g.serialize_xml().decode('utf-8')

            self.resp = requests.post(ENDPOINT, json=request).json()
            self.assertTrue(self.resp['valid'])
    return test

class MetaTestClass(type):

    @classmethod
    def __prepare__(mcls, name, bases):
        d = dict()
        for path in FILEPATHS:
            testname = f"test_{path.stem}"
            d[testname] = generate_test(path)
        return d


class TestValidation(unittest.TestCase, metaclass=MetaTestClass):

    def addSubTest(self, subtest, outcome):
        print(f"Testing {subtest.case}")
        if outcome is not None:
            print('❌ NOT valid')
            for e in self.resp['errors']:
                if "Namespace" not in e and e.strip():
                    print('⚠️  ' + e)
        else:
            print('✅ Valid')

        super().addSubTest(subtest, outcome)
