from flask import Blueprint, request, jsonify
from .models import db, Data
from .services import index_data
from . import es

main = Blueprint('main', __name__)

@main.route('/data', methods=['POST'])
def add_data():
    content = request.json.get('content')
    new_data = Data(content=content)
    db.session.add(new_data)
    db.session.commit()

    # Index ke Elasticsearch
    index_data(new_data.id, content)

    return jsonify({"message": "Data tersimpan dan terindex", "id": new_data.id})

@main.route('/search')
def search_data():
    keyword = request.args.get('q')
    result = es.search(index="data_index", body={
        "query": {
            "match": {
                "content": keyword
            }
        }
    })
    hits = [hit["_source"] for hit in result['hits']['hits']]
    return jsonify(hits)
