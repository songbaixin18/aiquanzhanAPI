# coding=utf-8

import json
# import logging
# import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from functools import partial

import requests
from flask import Flask, Response, make_response
from requests.exceptions import Timeout

# sys.stdout = sys.stderr
# logging.basicConfig(stream=sys.stderr)


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return type(obj)


json_encoder = MyJSONEncoder(indent=2, ensure_ascii=False)
compact_json_encoder = MyJSONEncoder(ensure_ascii=False, separators=(',', ':'))


def make_wrapped_response(data, status_code):
    body = json_encoder.encode({'status_code': status_code, 'data': data})
    # print '%%% RESPONSE BODY BEGIN %%%'  # debug
    # print body.encode('utf8')  # debug
    # print '%%% RESPONSE BODY END %%%'  # debug
    # print  # debug
    return make_response(body, status_code)


def ok(obj):
    return make_wrapped_response(obj, 200)


def error(err_msg, status_code, **kwargs):
    body = {'err_msg': err_msg}
    body.update(kwargs)
    return make_wrapped_response(body, status_code)


bad_request = partial(error, status_code=400)
unauthorized = partial(error, status_code=401)
forbidden = partial(error, status_code=403)
not_found = partial(error, status_code=404)
too_many_requests = partial(error, status_code=429)
internal_server_error = partial(error, status_code=500)
service_unavailable = partial(error, status_code=503)


class JSONResponse(Response):
    default_mimetype = 'application/json; charset=utf-8'


app = Flask(__name__)
# app.response_class = JSONResponse
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

app.permanent_session_lifetime = timedelta(minutes=200)


def requests_get_no_wait(url, timeout=1):  # type: (str) -> None
    """
    Send HTTP GET request and do not wait for response.
    """

    try:
        requests.get(url, timeout=timeout)
    except Timeout:
        pass


def requests_get_wait(url, pararm_dict):
    """
    请求的接口
    :param url: url
    :param pararm_dict: url中的参数
    :return: data 返回的数据
    """
    data = requests.get(url, params=pararm_dict)
    print (data.url)
    return data


