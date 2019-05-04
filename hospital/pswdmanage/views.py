from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.views import obtain_jwt_token
from pswdmanage.utils.serializers import SignInCaptchaSerializer, ChangeSerializer
from django.http import HttpResponse
from django.core.cache import cache  # 缓存
from pswdmanage.utils.cptcha_image import GetCaptcha
from pswdmanage.utils.getip import GetIp


class Captcha(GenericAPIView):
    def get(self, request):
        """
        返回验证码图片，将验证码放入缓存，以备验证使用
        :param request:
        :return:
        """
        ip = GetIp().getip(request)  # 获取请求用户的ip地址
        captcha_str, captcha_image = GetCaptcha(2).get_captcha_image()  # 获取验证码和验证码图片
        cache.set(ip + 'captcha', captcha_str, timeout=60 * 5)  # 以用户ip为键将验证码放入缓存，设置时长五分钟
        return HttpResponse(captcha_image, content_type='image/png')  # 返回验证码图片

    def post(self, request):
        """
        校验输入验证码的正确性
        :param request:
        :return:
        """
        serializer = SignInCaptchaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)


class SignUp(GenericAPIView):
    def post(self, request):
        pass


class SignIn(GenericAPIView):
    def post(self, request):
        """
        验证验证码正确性，并返回登录token
        :param request:
        :return:
        """
        serializer = SignInCaptchaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            return obtain_jwt_token(request._request)


class SignOut(GenericAPIView):
    def post(self, request):
        pass


class Change(GenericAPIView):
    def post(self, request):
        """
        修改密码
        :param request:
        :return:
        """
        serializer = ChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            return Response({"change": ["ok"]})
