#!/usr/bin/env python
# -*- coding:utf-8 -*-
# item_name:hospital
# author:16677
# datetime:2019/4/30 15:21
# software: PyCharm
from rest_framework import serializers
from database.models import Admission, Registration, DoctorManage, Department, RegisterItems


# 为住院主页建立序列化模型
class HomePageSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='registration.id')
    name = serializers.ReadOnlyField(source='registration.name')
    phone = serializers.ReadOnlyField(source='registration.phone')
    doctor = serializers.ReadOnlyField(source='registration.doctor.username')
    department = serializers.ReadOnlyField(source='registration.department.department_name')
    status = serializers.CharField(source='registration.get_status_display')

    class Meta:
        model = Admission
        fields = ('bed_id', 'pay_deposit', 'hospital_stays', 'id', 'name', 'phone', 'doctor', 'department', 'status',)


# 为挂号表建立序列化器
class RegistrationSerializers(serializers.ModelSerializer):
    # admission_url = serializers.HyperlinkedIdentityField(view_name='admission_detail', format='json')
    doctor = serializers.ReadOnlyField(source='doctor.username')
    department = serializers.ReadOnlyField(source='department.department_name')

    class Meta:
        model = Registration
        fields = (
            'name', 'phone', 'doctor', 'department', 'status', 'id_number', 'social_num', 'is_paying', 'sex', 'age',
            'is_first', 'remark',)


# 为住院表建立序列化模型
class AdmissionSerializers(serializers.ModelSerializer):
    # 设置超链接字段
    # registration_url = serializers.HyperlinkedRelatedField(view_name='registration_detail',many=True,read_only=True)
    # registration_serializers = RegistrationSerializers(many=True)

    class Meta:
        model = Admission
        fields = ('id', 'nurse', 'bed_id', 'pay_deposit', 'hospital_stays', 'state_illness', 'balance', 'registration',
                  )


# 押金序列化器
class CashPledgeSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='registration.id')
    name = serializers.ReadOnlyField(source='registration.name')
    id_number = serializers.ReadOnlyField(source='registration.id_number')

    class Meta:
        model = Admission
        fields = ('id', 'name', 'id_number', 'balance', 'pay_deposit')


# 结算序列化器
class AccountHomePageSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='registration.id')
    name = serializers.ReadOnlyField(source='registration.name')
    status = serializers.ChoiceField(choices='registration.status_choice', source='registration.status')

    class Meta:
        model = Admission
        fields = ('id', 'name', 'pay_deposit', 'balance', 'status')


# 结算详细信息
class RegisterItemsSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='registration.id')
    name = serializers.ReadOnlyField(source='registration.name')
    item_name = serializers.ReadOnlyField(source='pay_items.item_name')
    charge_amount = serializers.ReadOnlyField(source='pay_items.charge_amount')

    # registration = serializers.ReadOnlyField(source='registration.name')
    # pay_items = serializers.ReadOnlyField(source='payItems.item_name')
    # item_time = serializers.ReadOnlyField(source='registeritems.item_time')

    class Meta:
        model = RegisterItems
        fields = ('id', 'name', 'item_time', 'item_name', 'charge_amount')


class ExportSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='registration.id')
    # name = serializers.ReadOnlyField(source='registration.name')
    # phone = serializers.ReadOnlyField(source='registration.phone')
    # doctor = serializers.ReadOnlyField(source='registration.doctor.username')
    # department = serializers.ReadOnlyField(source='registration.department.department_name')
    # status = serializers.CharField(source='registration.get_status_display')
    # social_num = serializers.ReadOnlyField(source='registration.social_num')
    # is_paying = serializers.ReadOnlyField(source='registration.is_paying')
    registration = RegistrationSerializers(read_only=True)

    class Meta:
        model = Admission
        fields = ('id', 'nurse', 'bed_id', 'pay_deposit', 'hospital_stays', 'state_illness', 'registration')
