from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch

db = SQLAlchemy()
es = None

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    global es
    es = Elasticsearch(
    [app.config['ELASTICSEARCH_URL']],
    basic_auth=(
        app.config['ELASTICSEARCH_USERNAME'], 
        app.config['ELASTICSEARCH_PASSWORD'],
    )
)

    from .routes import main
    app.register_blueprint(main)

    return app
