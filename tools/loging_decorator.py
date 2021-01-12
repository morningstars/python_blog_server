
# *methods - 可接受任意参数
# 包装3层 为了给装饰器传参
def loging_check(*methods):
    def _loging_check(func):
        def wrapper(request, *args, **kwargs):
            # token 放在request.header -> authorization
            # 校验token pyjwt注意异常检测
            # token校验成功 根据用户名取出用户
            # request.user = user


            return func(request, *args, **kwargs)
        return wrapper
    return _loging_check
