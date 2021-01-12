import hashlib
import json
import time

import jwt
from django.shortcuts import render
from django.http import JsonResponse
from user.models import UserProfile


# Create your views here.

def btoken(request):
    if not request.method == 'POST':
        result = {'code': 101, 'error': 'Please use POST'}
        return JsonResponse(result)

    json_str = request.body
    if not json_str:
        result = {'code': 102, 'error': 'Please POST data'}
        return JsonResponse(result)

    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    password = json_obj.get('password')

    if not username:
        result = {'code': 103, 'error': 'Please give username'}
        return JsonResponse(result)

    if not password:
        result = {'code': 104, 'error': 'Please give password'}
        return JsonResponse(result)

    users = UserProfile.objects.filter(username=username)
    if not users:
        result = {'code': 105, 'error': 'The user is not existed'}
        return JsonResponse(result)

    # 密码加密做比较
    h = hashlib.sha1()
    h.update(password.encode())

    if users.first().password != h.hexdigest():
        result = {'code': 106, 'error': 'The user or password is wrong!'}
        return JsonResponse(result)

    # 创建token
    token = make_token(username)

    return JsonResponse({
        'code': 200,
        'username': username,
        'data': {
            'token': token
        }
    })


def make_token(username, expire=24 * 3600):
    key = 'abcdef1234'
    payload = {'username': username, 'exp': int(time.time() + expire)}
    return jwt.encode(payload, key, algorithm='HS256')
