# coding=utf8
from flask import Flask,jsonify, request, session, redirect, send_from_directory, render_template, make_response
from flask_restful import reqparse, abort, Api, Resource
from flask.logging import default_handler
from conf import db_connect
from DB import DB
from models import *
import urllib
import urllib2
import sys
import time
import re
import os
import json
import logging
from  sqlalchemy.sql.expression import func, select

defaultencoding = 'utf-8'

if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


def http_get(url):
    response = urllib2.urlopen(url)
    return response.read()


def http_post(url,values):
    jdata = json.dumps(values)
    req = urllib2.Request(url, jdata)
    response = urllib2.urlopen(req)
    return response.read()


def http_post_json(url,values):
    jdata = json.dumps(values)
    headers = {'Content-Type': 'application/json'}
    req = urllib2.Request(url, headers = headers, data = jdata)
    response = urllib2.urlopen(req)
    return response.read()


DB = DB()


class get_list(Resource):

    def get_page_sum(self,type):
        page_num = DB.GetListCount(str(type))
        app.logger.debug(page_num)
        if int(page_num) % 6 == 0:
            return int(page_num)/6
        else:
            return int(page_num)/6 + 1

    def get(self,page,type):
        list = DB.GetList(str(type),str(page),6)
        page_sum = self.get_page_sum(str(type))
        JsonInfo = {}
        JsonInfo['article_list'] = list
        JsonInfo['page_sum'] = page_sum
        JsonInfo['page_num'] = int(page)
        rst = make_response(json.dumps(JsonInfo))
        return rst


@app.route('/share', methods=['GET', 'POST'])
def element():
    return render_template('share.html')


api = Api(app)
# apis
api.add_resource(get_list, '/page/<type>/<page>')
if __name__ == '__main__':
    app.debug = True
    app.config['SQLALCHEMY_BINDS'] = {'app': app_url}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    for logger in (
            app.logger,
            logging.getLogger('sqlalchemy'),
            logging.getLogger('other_package'),
        ):
        logger.addHandler(default_handler)
    app.logger.addHandler(handler)
    app.run(host='127.0.0.1', port=6016)
