from rest_framework import serializers
from django.core.cache import cache
from django.contrib.auth import authenticate
from pswdmanage.utils.getip import GetIp


class SignInCaptchaSerializer(serializers.Serializer):
    """
    登录验证码验证
    """
    captcha = serializers.CharField(required=True, error_messages={'required': '验证码不可为空'})

    def validate_captcha(self, captcha):
        ip = GetIp().getip(self.context['request'])  # 获取请求用户的ip地址
        cache_captcha = cache.get(ip + 'captcha')  # 在缓存中获取这个ip生成的正确验证码
        try:
            if not captcha.upper() == cache_captcha:
                raise serializers.ValidationError('验证码错误')
        except AttributeError:
            raise serializers.ValidationError('验证码错误')
        return captcha


class ChangeSerializer(serializers.Serializer):
    """
    修改密码
    """
    oldpwd = serializers.CharField(required=True, error_messages={'required': '原密码不可为空'})
    newpwd = serializers.CharField(required=True, min_length=6, max_length=16, error_messages={
        'required': '新密码不可为空',
        'min_length': '密码长度不可少于6位',
        'max_length': '密码长度不可大于16位'
    })
    irmpwd = serializers.CharField(required=True, error_messages={'required': '确认密码不可为空'})

    def validate_oldpwd(self, oldpwd):
        username = self.context['request'].user.username  # 获取请求的用户对象的用户名
        if not authenticate(username=username, password=oldpwd):  # 对比请求用户和输入密码的正确性
            raise serializers.ValidationError('密码错误')
        return oldpwd

    def validate(self, attrs):
        if attrs['newpwd'] != attrs['irmpwd']:  # 对比新密码和确认密码是否一致
            raise serializers.ValidationError({'irmpwd': '两次密码不一致'})
        user = self.context['request'].user  # 获取请求用户对象
        user.set_password(attrs['irmpwd'])  # 设置新的密码
        user.save()
        return attrs
