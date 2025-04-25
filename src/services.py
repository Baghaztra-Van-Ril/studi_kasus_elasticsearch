from . import es

def index_data(id, content):
    es.index(index="data_index", id=id, body={"content": content})
