from flask import Flask, jsonify, request, session, redirect
from flask import send_from_directory, render_template
from flask_restful import reqparse, abort, Api, Resource
from conf import db_connect
from models import *
import sys
import datetime
import re
import os
import json
import time
from sqlalchemy.sql.expression import func, select


class DB:

    def GetListCount(self, type):
        try:
            article_model = ArticleModel()
            if type == "0":
                return article_model.query.count()
            else:
                return article_model.query.filter_by(type=type).count()
        except Exception as e:
            print(e)
            return {"status": "GetListCount error"}

    def GetList(self, type, page, limit):
        try:
            article_model = ArticleModel()
            if type == "0":
                article_info = article_model.query.limit(limit).offset(
                    (int(page)-1)*limit).all()
            else:
                article_info = article_model.query.filter_by(
                    type=type).limit(limit).offset((int(page)-1)*limit).all()
            if article_info:
                article_objs = []
                for info in article_info:
                    article_obj = {}
                    article_obj['idarticle'] = info.idarticle
                    article_obj['title'] = info.title
                    article_obj['description'] = info.description
                    article_obj['author'] = info.author
                    article_obj['src'] = info.src
                    article_obj['date'] = str(info.date)
                    article_obj['read_number'] = info.read_number
                    article_obj['type'] = info.type
                    article_obj['thumbnail'] = info.thumbnail
                    article_objs.append(article_obj)
                return article_objs
            else:
                return [{"status": "GetList null"}]
        except Exception as e:
            db.session.rollback()
            print(e)
            return [{"status": "GetList error"}]

    def SaveArticle(self, title, description, author, src, type, thumbnail):
        try:
            new_article = ArticleModel(
                title=title,
                description=description,
                author=author,
                src=src,
                date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                read_number=0,
                type=type,
                thumbnail=thumbnail)
            db.session.add(new_article)
            db.session.commit()
            article_model = ArticleModel()
            article_info = article_model.query.filter_by(src=src).first()
            article_info.status = "SaveArticle success"
            return article_info
        except Exception as e:
            db.session.rollback()
            print(e)
            return [{"status": "SaveArticle error"}]

    def UpdateReadNumber(self, idarticle):
        try:
            article_model = ArticleModel()
            article = article_model.query.filter_by(idarticle=idarticle).first()
            if(article == None):
                print("UpdateReadNumber error: nofind article!")
                return [{"status": False, "errorMsg": "UpdateReadNumber error: nofind article!"}]
            article.read_number = article.read_number + 1
            read_number = article.read_number
            db.session.add(article)
            db.session.commit()
            article_info = {}
            article_info.read_number = read_number
            article_info.status = True
            return article_info
        except Exception as e:
            db.session.rollback()
            print("UpdateReadNumber error: " + str(e))
            return [{"status": False, "errorMsg": "UpdateReadNumber error: " + str(e)}]
