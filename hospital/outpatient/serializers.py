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


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    """
    部门（科室）信息 序列化
    """
    doctormanage = serializers.HyperlinkedRelatedField(many=True, view_name='doctormanage-detail', read_only=True)
    registration = serializers.HyperlinkedRelatedField(many=True, view_name='registration-detail', read_only=True)

    class Meta:
        model = Department
        fields = ('url', 'id', 'department_name', 'doctormanage', 'registration')


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    """
    挂号信息序列化
    """
    # department = serializers.ReadOnlyField(source='department.department_name')
    # doctor = serializers.ReadOnlyField(source='doctor.real_name')

    class Meta:
        model = Registration
        fields = ('url', 'id', 'name', 'id_number', 'cost', 'social_num',
                  'phone', 'is_paying', 'sex', 'age', 'occupation', 'is_first',
                  'regist_date', 'status', 'remark',
                  'department', 'doctor'
                  )


class RegistSerializer(serializers.ModelSerializer):
    """
    挂号信息 选择部分字段 序列化
    """
    doctor = serializers.CharField(source='doctor.real_name')
    department = serializers.CharField(source='department.department_name')
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Registration
        fields = ('url', 'id', 'doctor', 'regist_date', 'department', 'status')


class DoctorManageSerializer(serializers.HyperlinkedModelSerializer):
    """
    门诊医生管理 序列化
    """
    # department = serializers.ReadOnlyField(source='department.department_name')

    class Meta:
        model = DoctorManage
        fields = ('url', 'id', 'id_number', 'phone', 'sex', 'birthday', 'age',
                  'department', 'education', 'remark')
