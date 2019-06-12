# coding=utf-8

import logging
import sys
import decimal

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_app import app
from conf.db_connect import app_url

sys.stdout = sys.stderr
logging.basicConfig(stream=sys.stderr)

app.config['SQLALCHEMY_BINDS'] = {'app': app_url}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# NOTE: Order matters! db = SQLAlchemy(app) must precede ma = Marshmallow(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
MYSQL_ARGS = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8',
    'mysql_collate': 'utf8_unicode_ci',
}


class ArticleModel(db.Model):
    __bind_key__ = 'app'
    __tablename__ = 'article'
    __table_args__ = MYSQL_ARGS

    idarticle = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    author = db.Column(db.String(255))
    src = db.Column(db.String(255))
    date = db.Column(db.TIMESTAMP)
    read_number = db.Column(db.Integer)
    type = db.Column(db.Integer)
    thumbnail = db.Column(db.String(255))

    __mapper_args__ = {
        "order_by": date.desc()
    }


class ArticleSchema(ma.Schema):
    class Meta:
        fields = (
            'idarticle',
            'title',
            'description',
            'author',
            'src',
            'date',
            'read_number',
            'type',
            'thumbnail')


article_schema = ArticleSchema(many=True)
db.create_all()
