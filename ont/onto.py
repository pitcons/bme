
from owlready import (
    get_ontology,
    Ontology, Thing,
    Property, FunctionalProperty, AnnotationProperty,
)
from config import config


onto = get_ontology(config.bme3_onto)


class Article(Thing):
    ontology = onto


class title(FunctionalProperty):
    ontology = onto
    domain = [Article]
    range = [str]


class Tome(Thing):
    ontology = onto


class source(AnnotationProperty):
    ontology = onto

class first_sentence(AnnotationProperty):
    ontology = onto

class raw(AnnotationProperty):
    ontology = onto
