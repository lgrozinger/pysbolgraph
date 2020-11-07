import unittest
from pathlib import Path
from rdflib import Literal, URIRef


from pysbolgraph.terms import SBOL2
from pysbolgraph.SBOL2Graph import SBOL2Graph as Graph
from pysbolgraph.S2Identified import S2Identified


class TestIdentified(unittest.TestCase):

    def setUp(self):
        testfile = Path(__file__).parent.parent / "SBOLTestSuite/SBOL2/pAGM1467.xml"
        self.graph = Graph()
        self.graph.load(str(testfile))
        self.thing = S2Identified(self.graph, "http://www.async.ece.utah.edu/pAGM1467")

    def test_getproperty_succeeds(self):
        self.assertEqual(self.thing[SBOL2.displayId], Literal("pAGM1467"))

    def test_getproperty_fails_keyerror(self):
        with self.assertRaises(KeyError):
            self.thing["nonexistent"]

    def test_getproperty_fails_typerror(self):
        with self.assertRaises(TypeError):
            self.thing[12345]

    def test_setproperty_succeeds(self):
        before = self.thing[SBOL2.displayId]
        expected = Literal("adisplayid")
        self.assertNotEqual(expected, before)
        self.thing[SBOL2.displayId] = expected
        after = self.thing[SBOL2.displayId]
        self.assertEqual(expected, after)


