#!/usr/bin/env python
# encoding: utf-8

import base64
import json
import hmac
import hashlib
import time
import urllib
import urllib2


def make_sorted_data_string(data):
    for k, v in data.viewitems():
        if isinstance(v, unicode):
            data[k] = v.encode('utf-8')
    sorted_data = sorted(data.viewitems(), key=lambda x: x[0])
    sorted_string = urllib.urlencode(sorted_data)
    return urllib.unquote(sorted_string)


def make_headers(data, api_id, api_key):
    sorted_data =make_sorted_data_string(data)
    token = hmac.new(api_key, sorted_data, hashlib.sha1).hexdigest()
    sign = base64.b64encode('{}:{}'.format(api_id, token))
    headers = {'AUTHORIZATION': 'Basic %s' % sign}
    return headers


def post_req(url, data, api_id, api_key):
    '''发送POST请求'''
    headers = make_headers(data, api_id, api_key)
    try:
        req = urllib2.Request(url, data=urllib.urlencode(data), headers=headers)
        resp = urllib2.urlopen(req)
        result = json.loads(resp.read())
        return result
    except Exception as e:
        print e


def get_req(url, data, api_id, api_key):
    '''发送GET请求'''
    headers = make_headers(data, api_id, api_key)
    try:
        query_str = urllib.urlencode(data)
        req = urllib2.Request(url + '?' + query_str, headers=headers)
        resp = urllib2.urlopen(req)
        result = json.loads(resp.read())
        return result
    except Exception as e:
        print e


if __name__ == "__main__":
    api_id = '582c10a9a54d75327c0dddee'
    api_key = '3077f20de0644a92b0ae024519063d2b'
    post_data = {
        'time': int(time.time()),
        'type': 'HTTP',
        'url': 'http://www.baidu.com',
        'name': 'cc',
    }
    post_url = 'http://localhost:8080/openapi/v1/task/create/'
    #  print post_req(post_url, post_data, api_id, api_key)

    tid = '29d6f2d8088442ecab589fadbf779028'
    get_url = 'http://localhost:8080/openapi/v1/task/%s/result/' % tid
    get_data = {
        'time': int(time.time()),
        'avg_resp_time': 0
    }
    print get_req(get_url, get_data, api_id, api_key)

    get_url = 'http://localhost:8080/openapi/v1/task/list/'
    get_data = {
        'time': int(time.time()),
    }
    print get_req(get_url, get_data, api_id, api_key)


