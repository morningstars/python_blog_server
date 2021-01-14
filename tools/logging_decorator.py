# *methods - 可接受任意参数
# 包装3层 为了给装饰器传参
import jwt
from django.http import JsonResponse

from user.models import UserProfile

KEY = 'abcdef1234'


def logging_check(*methods):
    def _logging_check(func):
        def wrapper(request, *args, **kwargs):
            # token 放在request.header -> authorization
            print(request.META)
            token = request.META.get('HTTP_AUTHORIZATION')

            if not methods:
                # 如果没传methods参数，则直接返回视图
                return func(request, *args, **kwargs)

            if request.method not in methods:
                # 如果当前请求的方法不在methods内 则直接返回视图
                return func(request, *args, **kwargs)

            # 严格判断参数大小写 统一大写
            # 严格校验methods里的参数是POST,GET,PUT,DELETE

            # 校验token
            if not token or token == 'null':
                result = {'code': 107, 'error': 'Please give token'}
                return JsonResponse(result)

            # 校验token pyjwt注意异常检测
            try:
                res = jwt.decode(token, KEY, algorithms='HS256')
            except Exception as e:
                print('----token error is %s' % e)
                result = {'code': 108, 'error': 'Please login'}
                return JsonResponse(result)

            # token校验成功 根据用户名取出用户
            username = res['username']
            user = UserProfile.objects.get(username=username)
            request.user = user
            return func(request, *args, **kwargs)

        return wrapper

    return _logging_check


def get_user_by_request(request):
    '''
    通过request获取用户
    :param request:
    :return: user对象 or None
    '''
    token = request.META.get('HTTP_AUTHORIZATION')

    if not token or token == 'null':
        return None

    try:
        res = jwt.decode(token, KEY, algorithms='HS256')
    except Exception as e:
        print('token error is %s' % e)
        return None

    # 获取token中的用户名
    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user

