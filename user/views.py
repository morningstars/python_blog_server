import time
from django.http import JsonResponse
import hashlib

from tools.logging_decorator import logging_check
from user.models import UserProfile
import json
import jwt


# Create your views here.
@logging_check('PUT', 'DELETE')
def users(request, username=None):
    print('method', request.method)
    print('username', username)
    if request.method == 'GET':
        #  /v1/users/zhangsan?info=1&email=1
        if username:
            # 查询具体用户数据
            try:
                user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                user = None

            if not user:
                result = {'code': 208, 'error': 'User is not exist'}
                return JsonResponse(result)

            if request.GET.keys():
                data = {}
                print(request.GET.keys())
                for k in request.GET.keys():
                    # 数据库中最好有费控默认值
                    if hasattr(user, k):
                        data[k] = getattr(user, k)

                result = {
                    'code': 200,
                    'username': username,
                    'data': data
                }
                return JsonResponse(result)
            else:
                result = {
                    'code': 200,
                    'username': username,
                    'data': {
                        'username': user.username,
                        'info': user.info,
                        'nickname': user.nickname,
                        'sign': user.sign,
                        'avatar': str(user.avatar)
                    }}
                return JsonResponse(result)
        else:
            # 查询所有用户的数据
            users = UserProfile.objects.all()
            data = []

            for user in users:
                aDict = {
                    'username': user.username,
                    'info': user.info,
                    'email': user.email,
                    'nickname': user.nickname,
                    'avatar': str(user.avatar)
                }
                data.append(aDict)

            result = {
                'code': 200,
                'username': None,
                'data': data
            }
            return JsonResponse(result)

    elif request.method == 'POST':
        # 注册用户
        # 密码需用SHA-1

        # 获取json数据
        json_str = request.body
        if not json_str:
            result = {'code': 202, 'error': 'Please POST data'}
            return JsonResponse(result)

        json_obj = json.loads(json_str)
        username = json_obj.get('username', '')
        email = json_obj.get('email', '')
        password_1 = json_obj.get('password_1', '')
        password_2 = json_obj.get('password_2', '')

        if not username:
            result = {'code': 203, 'error': 'Please give username'}
            return JsonResponse(result)

        if not email:
            result = {'code': 204, 'error': 'Please give email'}
            return JsonResponse(result)

        if not password_1 or not password_2:
            result = {'code': 205, 'error': 'Please give password'}
            return JsonResponse(result)

        if password_1 != password_2:
            result = {'code': 206, 'error': 'The password is not same'}
            return JsonResponse(result)

        # 检查用户是否存在
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 207, 'error': 'The user is existed'}
            return JsonResponse(result)

        # 密码进行hash
        h = hashlib.sha1()
        h.update(password_1.encode())

        try:
            UserProfile.objects.create(
                username=username,
                nickname=username,
                email=email,
                password=h.hexdigest()
            )
        except Exception as e:
            print('UserProfile create error is %s' % e)
            result = {'code': 207, 'error': 'The user is existed'}
            return JsonResponse(result)

        # 根据用户名 生成token
        token = make_token(username)
        result = {'code': 200,
                  'username': username,
                  'data': {
                      'token': token
                  }}
        return JsonResponse(result)

    elif request.method == 'PUT':
        # 修改用户数据
        user = request.user

        json_str = request.body
        if not json_str:
            result = {'code': 202, 'error': 'please put data'}
            return JsonResponse(result)

        json_obj = json.loads(json_str)

        nickname = json_obj.get('nickname', '')
        sign = json_obj.get('sign', '')
        info = json_obj.get('info', '')

        user.nickname = nickname
        user.sign = sign
        user.info = info
        user.save()

        result = {'code': 200, 'username': username}
        return JsonResponse(result)

    elif request.method == 'DELETE':
        pass

    return JsonResponse({
        'code': 200,
        'data': {
            'username': 'zhangsan'
        }
    })


def make_token(username, expire=24 * 3600):
    """
    根据用户名生成token
    :param username:
    :param expire:
    :return:
    """
    key = 'abcdef1235'
    now_t = time.time()
    payload = {'username': username, 'exp': int(now_t + expire)}
    return jwt.encode(payload, key, algorithm='HS256')


@logging_check('POST')
def user_avater(request, username):
    # 当前必须是post提交
    if request.method != 'POST':
        result = {'code': 210, 'error': 'Please use post'}
        return JsonResponse(result)

    users = UserProfile.objects.filter(username=username)
    if not users:
        result = {'code': 208, 'error': 'The user is not existed'}
        return JsonResponse(result)

    if request.FILES.get('avatar'):
        # 正常提交图片信息 进行存储
        users[0].avatar = request.FILES['avatar']
        users[0].save()
        result = {'code': 200, 'username': username}
        return JsonResponse(result)
    else:
        result = {'code': 211, 'error': 'Please give avatar'}
        return JsonResponse(result)
