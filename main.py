# coding=utf8
from flask import Flask, jsonify, request, session, redirect
from flask import send_from_directory, render_template, make_response
from flask_restful import reqparse, abort, Api, Resource
from flask.logging import default_handler
from conf import db_connect
from DB import DB
from models import *
import urllib
import sys
import time
import re
import os
import json
import logging
import uuid
import random
from sqlalchemy.sql.expression import func, select

defaultencoding = 'utf-8'

if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


def http_get(url):
    response = urllib.request.urlopen(url)
    return response.read()


def http_post(url, values):
    jdata = json.dumps(values)
    req = urllib.request(url, jdata)
    response = urllib.request.urlopen(req)
    return response.read()


def http_post_json(url, values):
    jdata = json.dumps(values)
    headers = {'Content-Type': 'application/json'}
    req = urllib.request(url, headers=headers, data=jdata)
    response = urllib.request.urlopen(req)
    return response.read()


def random_str(num):
    uln = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    rs = random.sample(uln, num)  # 生成一个指定位数的随机字符串
    a = uuid.uuid1()  # 根据时间戳生成uuid,保证全球唯一
    b = ''.join(rs+str(a).split("-"))
    return b


DB = DB()
parser = reqparse.RequestParser()
parser.add_argument('title', location=['json', 'args'])
parser.add_argument('description', location=['json', 'args'])
parser.add_argument('author', location=['json', 'args'])
parser.add_argument('date', location=['json', 'args'])
parser.add_argument('type', location=['json', 'args'])
parser.add_argument('thumbnail', location=['json', 'args'])
parser.add_argument('content', location=['json', 'args'])


class get_list(Resource):

    def get_page_sum(self, type):
        page_num = DB.GetListCount(str(type))
        if int(page_num) % 6 == 0:
            return int(page_num)/6
        else:
            return int(page_num)/6 + 1

    def get(self, page, type):
        list = DB.GetList(str(type), str(page), 6)
        page_sum = self.get_page_sum(str(type))
        JsonInfo = {}
        JsonInfo['article_list'] = list
        JsonInfo['page_sum'] = int(page_sum)
        JsonInfo['page_num'] = int(page)
        rst = make_response(json.dumps(JsonInfo))
        return rst


class save_article(Resource):

    def post(self):
        args = parser.parse_args()
        if args['type'] == "1":
            src = "/blog/" + random_str(6) + ".html"
        elif args['type'] == "2":
            src = "/file/" + random_str(6) + ".html"
        saved = DB.SaveArticle(
            args['title'],
            args['description'],
            args['author'],
            src,
            args['type'],
            args['thumbnail'])
        src = "../www" + src
        if saved.status == "SaveArticle success":
            if str(saved.type) == "1":
                with open(src, 'w', encoding='utf-8') as f:
                    f.write(str(render_template(
                        'blog_template.html',
                        info=saved,
                        content=str(args['content']))))
            elif str(saved.type) == "2":
                with open(src, 'w', encoding='utf-8') as f:
                    f.write(str(render_template(
                        'file_template.html',
                        info=saved,
                        content=str(args['content']))))
            JsonInfo = {}
            JsonInfo['title'] = str(saved.title)
            JsonInfo['content'] = str(args['content'])
            JsonInfo['date'] = str(saved.date)
            JsonInfo['statu'] = "SaveArticle success"
            return make_response(json.dumps(JsonInfo))
        else:
            if(os.path.exists(src)):
                os.remove(src)
            JsonInfo = {}
            JsonInfo['statu'] = "SaveArticle error"
            return make_response(json.dumps(JsonInfo))


@app.route('/share', methods=['GET', 'POST'])
def element():
    return render_template('share.html')


api = Api(app)
# apis
api.add_resource(get_list, '/page/<type>/<page>')
api.add_resource(save_article, '/save_article')
if __name__ == '__main__':
    app.debug = True
    app.config['SQLALCHEMY_BINDS'] = {'app': app_url}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - \
            %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    for logger in (
            app.logger,
            logging.getLogger('sqlalchemy'),
            logging.getLogger('other_package')):
        logger.addHandler(default_handler)
    app.logger.addHandler(handler)
    app.run(host='127.0.0.1', port=6016)
