from flask import Flask,jsonify, request, session, redirect, send_from_directory, render_template
from flask import request
from flask_restful import reqparse, abort, Api, Resource
from conf import db_connect
from models import *
import urllib
import urllib2
import sys
import datetime
import re
import os
import json
from  sqlalchemy.sql.expression import func, select


class DB:


    def GetListCount(self,type):
        try:
            article_model = ArticleModel()
            if type == "0":
                return article_model.query.count()
            else:
                return article_model.query.filter_by(type=type).count()
        except Exception, e:
            print (e)
            return {"status": "GetListCount error"}


    def GetList (self,type,page,limit):
        try:
            article_model = ArticleModel()
            if type == "0":
                article_info = article_model.query.limit(limit).offset((int(page)-1)*limit).all()
            else:
                article_info = article_model.query.filter_by(type=type).limit(limit).offset((int(page)-1)*limit).all()
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
        except Exception, e:
            db.session.rollback()
            print (e)
            return [{"status": "GetList error"}]