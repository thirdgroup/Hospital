# -*- coding: utf-8 -*-
"""
   Product:      PyCharm
   Project:      hospital
   File:         myLogin
   Author :      ZXR 
   date：        2019/5/4
   time:         19:58 
"""
from database.models import User
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class MyLogin(View):
    def post(self, request, *args, **kwargs):
        req_info = request.POST
        username = req_info.get('username', None)
        password = req_info.get('password', None)
        try:
            user_obj = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            result = {
                'error': '用户不存在！'
            }
            return JsonResponse(result, status=404)

        if user_obj.password == password or check_password(password, user_obj.password):
            login(request, user_obj)
            result = {
                'success': '登录成功！'
            }
            return JsonResponse(result, status=200)
        result = {
            'error': '账号或密码错误！'
        }
        return JsonResponse(result, status=204)

    def get(self, request, *args, **kwargs):
        result = {
            'error': '请使用POST方式请求！'
        }
        return JsonResponse(result, status=200)
