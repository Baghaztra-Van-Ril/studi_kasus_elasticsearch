from . import es

def index_glossary(id, term, definition):
    doc = {
        "term": term,
        "definition": definition
    }
    es.index(index="glossary_index", id=id, document=doc)
