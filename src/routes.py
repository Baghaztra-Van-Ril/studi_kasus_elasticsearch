from flask import Blueprint, request, jsonify, render_template
from faker import Faker
from .models import db, Glossary
from .services import index_glossary
from . import es

main = Blueprint('main', __name__)
fake = Faker()

@main.route('/')
def index_page():
    return render_template('index.html')

@main.route('/glossary', methods=['POST'])
def add_glossary():
    term = request.json.get('term')
    definition = request.json.get('definition')
    if not term or not definition:
        return jsonify({"error": "Term dan definition tidak boleh kosong"}), 400

    new_glossary = Glossary(term=term, definition=definition)
    db.session.add(new_glossary)
    db.session.commit()

    # Index ke Elasticsearch
    index_glossary(new_glossary.id, term, definition)

    return jsonify({"message": "Glossary tersimpan dan terindex", "id": new_glossary.id})

@main.route('/glossary', methods=['GET'])
def get_all():
    glossaries = Glossary.query.all()
    return jsonify([
        {
            "id": g.id, 
            "term": g.term, 
            "definition": g.definition
        } for g in glossaries
    ])

@main.route('/search', methods=['GET'])
def search_glossary():
    keyword = request.args.get('q')
    if not keyword:
        return jsonify({"error": "Query pencarian tidak boleh kosong"}), 400

    result = es.search(
        index="glossary_index",
        query={
            "multi_match": {
                "query": keyword,
                "fields": ["term^4", "definition"],
                # "fuzziness": "AUTO"
                "fuzziness": 2
            }
        }
    )
    hits = [hit["_source"] for hit in result['hits']['hits']]
    return jsonify({"results": hits, "total": len(hits)})

@main.route('/glossary/<int:id>', methods=['DELETE'])
def delete_glossary(id):
    glossary = Glossary.query.get(id)
    if not glossary:
        return jsonify({"error": "Data tidak ditemukan"}), 404

    # Hapus dari database
    db.session.delete(glossary)
    db.session.commit()

    # Hapus dari Elasticsearch
    try:
        es.delete(index="glossary_index", id=id)
    except Exception as e:
        print(f"Gagal hapus di Elasticsearch: {e}")

    return jsonify({"message": "Glossary berhasil dihapus", "id": id})

@main.route('/seed', methods=['POST'])
def seed_data():
    n = int(request.args.get('n', 10))

    for _ in range(n):
        term = fake.word()
        definition = fake.sentence()

        new_data = Glossary(term=term, definition=definition)
        db.session.add(new_data)
        db.session.flush()

        # Index ke Elasticsearch
        es.index(index="glossary_index", id=new_data.id, document={
            "term": term,
            "definition": definition
        })

    db.session.commit()
    return jsonify({"message": f"{n} data dummy berhasil dimasukkan."})
