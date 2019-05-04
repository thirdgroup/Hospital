from uuid import uuid4
from jwt import InvalidSignatureError
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache


class ValidTokenMiddleware(MiddlewareMixin):
    """
    登录验证登录中间件
    """

    def process_request(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION', None)  # 获取每个请求的token
        if jwt_token is not None and jwt_token != '':  # 如果请求携带tokne
            data = {
                'token': request.META['HTTP_AUTHORIZATION'].split(' ')[1],
            }
            try:
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']  # 找到该tokne对应的用户对象
            except (InvalidSignatureError, ValidationError):  # 如果token错误找不到用户
                return JsonResponse({"signin": ["请重新登录"]}, status=status.HTTP_400_BAD_REQUEST)
            if cache.get(user.username) is not None and cache.get(user.username) != data[
                'token']:  # 如果这个用户已经登录但是缓存中的token和实际请求携带的token不是同一个，代表多个客户端在同时登录一个用户
                user.user_secret = uuid4()  # 改变该用户的uuid使该用户强制下线
                user.save()
                return JsonResponse({"signint": ["账号在多端登录，账号存在风险，请及时修改密码"]}, status=status.HTTP_400_BAD_REQUEST)
        if request.META['PATH_INFO'] not in ['/pswdmanage/sign-in/',
                                             '/pswdmanage/captcha/']:  # 如果用户没有携带token而且请求路径不是登录和获取验证码，提示其登录后操作
            return JsonResponse({"signin": ["用户未登录"]}, status=status.HTTP_400_BAD_REQUEST)

    def process_response(self, request, response):
        if request.META['PATH_INFO'] == '/pswdmanage/sign-in/' or request.META[
            'PATH_INFO'] == '/sign-refresh/':  # 如果请求路径是登录或者刷新token
            response_data = response.data  # 将返回数据赋值
            valid_data = VerifyJSONWebTokenSerializer().validate(response_data)
            user = valid_data['user']  # 获取返回token代表的用户对象
            cache.set(user.username, response_data['token'],
                      timeout=60 * 60 * 24)  # 将这个用户对象的用户名和返回token放入在缓存中，设置时长一天，与token失效时长一致
            return response
        return response
