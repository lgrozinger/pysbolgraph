from rdflib import Literal, URIRef

from .terms import SBOL2, Dcterms


class S2Identified:
    def __init__(self, g, uri):
        self.g = g
        self.uri = uri

    def __getitem__(self, predicate):
        try:
            matches = self.g.objects(URIRef(self.uri), URIRef(predicate))
            return next(matches)
        except StopIteration:
            raise KeyError(f"{self.uri} has no property {predicate}")
        except TypeError:
            raise TypeError(f"Properties must be URIs, {predicate} is not")

    def __setitem__(self, predicate, value):
        value = value.uri if isinstance(value, S2Identified) else value
        self.g.remove((URIRef(self.uri), URIRef(predicate), None))
        self.g.add((URIRef(self.uri), URIRef(predicate), value))

    @property
    def name(self):
        return self[Dcterms.title]

    @name.setter
    def name(self, name):
        self[Dcterms.title] = name

    @property
    def display_id(self):
        return self[SBOL2.displayId]

    @property
    def persistent_identity(self):
        return self[SBOL2.persistentIdentity]

    @property
    def version(self):
        return self[SBOL2.version]

    @property
    def display_name(self):
        try:
            name = self.name
            return name
        except KeyError:
            return self.display_id
