# -*- coding: utf-8 -*-
"""
   Product:      PyCharm
   Project:      hospital
   File:         serializers
   Author :      ZXR 
   date：        2019/4/30
   time:         14:24 
"""
from rest_framework import serializers
from database.models import Registration, DoctorManage, Department


class DoctorMSerializer(serializers.HyperlinkedModelSerializer):
    """
    门诊医生管理  部分字段 序列化
    用于 其他序列化 使用
    """

    department = serializers.ReadOnlyField(source='department.department_name')
    real_name = serializers.ReadOnlyField(source='real_name')

    class Meta:
        model = DoctorManage
        fields = ('url', 'real_name', 'id', 'department')


class DepartMSerializer(serializers.HyperlinkedModelSerializer):
    """
    部门（科室）信息 部分字段复杂序列化
    用户 其他序列化 使用
    """
    class Meta:
        model = Department
        fields = ('url', 'id', 'department_name')


class DepartmentGetSerializer(serializers.HyperlinkedModelSerializer):
    """
    部门（科室）信息  部分字段复杂序列化
    用于 GET 方法请求时使用
    """

    doctormanage = DoctorMSerializer(many=True)

    class Meta:
        model = Department
        fields = ('url', 'id', 'department_name', 'doctormanage')


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    """
    部门（科室）信息 序列化（全部字段）
    用于 POST、PUT、PATCH、DELETE 请求时使用
    """

    # doctormanage = serializers.HyperlinkedRelatedField(many=True, view_name='doctormanage-detail', read_only=True)

    class Meta:
        model = Department
        fields = ('url', 'id', 'department_name', 'doctormanage')


class DoctorManageListSerializer(serializers.HyperlinkedModelSerializer):
    """
    门诊医生管理
    用于 GET请求('list'方法)时使用此序列化器
    """
    real_name = serializers.CharField(source='user.real_name', max_length=20, label='真实姓名')

    class Meta:
        model = DoctorManage
        fields = ('url', 'id', 'real_name', 'admission_time', 'department')


class DoctorManageRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    """
    门诊医生管理
    用于 GET请求（'retrieve'）时使用序列化器
    """
    email = serializers.EmailField(source='user.email')
    real_name = serializers.CharField(source='user.real_name')
    mobile = serializers.CharField(source='user.mobile')
    status = serializers.CharField(source='user.status')
    education = serializers.CharField(source='get_education_display')
    department = DepartMSerializer()

    class Meta:
        model = DoctorManage
        fields = ('url', 'id', 'status', 'real_name', 'id_number', 'mobile', 'phone', 'sex', 'birthday',
                  'age', 'email', 'department', 'education', 'remark',)


class DoctorManageSerializer(serializers.HyperlinkedModelSerializer):
    """
    门诊医生管理 序列化（全部字段）
    用于 POST、PUT、PATCH、DELETE 请求时使用
    """
    email = serializers.EmailField(source='user.email', allow_null=True, max_length=30, label='邮箱')
    real_name = serializers.CharField(source='user.real_name', max_length=20, label='真实姓名')
    mobile = serializers.CharField(source='user.mobile', max_length=11, label='手机号')
    status = serializers.BooleanField(source='user.get_status_display', default=True, label='状态,默认启用')

    class Meta:
        model = DoctorManage
        fields = ('url', 'id', 'status', 'real_name', 'id_number', 'mobile', 'phone', 'sex', 'birthday',
                  'age', 'email', 'department', 'education', 'remark', 'user_name', 'password')


class RegistrationListSerializer(serializers.ModelSerializer):
    """
    挂号信息 选择部分字段 (复杂)序列化，
    用于 GET 请求('list’) 方法时使用 (因为使用了医生信息复杂序列化)
    """
    doctor = DoctorMSerializer()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Registration
        fields = ('url', 'id', 'doctor', 'regist_date', 'status')


class RegistrationRetrieveSerializer(serializers.ModelSerializer):
    """
    挂号信息 选择部分字段 (复杂)序列化
    用于 GET 请求('retrieve') 方法时使用
    """
    doctor = DoctorMSerializer()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Registration
        fields = ('url', 'id', 'name', 'id_number', 'cost', 'social_num',
                  'phone', 'is_paying', 'sex', 'age', 'occupation', 'is_first',
                  'regist_date', 'status', 'remark', 'doctor'
                  )


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    """
    挂号信息序列化 （全部字段）
    用于 POST、PUT、PATCH、DELETE 请求方法时使用
    """

    class Meta:
        model = Registration
        fields = ('url', 'id', 'name', 'id_number', 'cost', 'social_num',
                  'phone', 'is_paying', 'sex', 'age', 'occupation', 'is_first',
                  'regist_date', 'status', 'remark', 'doctor'
                  )
