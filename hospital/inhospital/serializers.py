#!/usr/bin/env python
# -*- coding:utf-8 -*-
# item_name:hospital
# author:16677
# datetime:2019/4/30 15:21
# software: PyCharm
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param

from database.models import Admission, Registration, DoctorManage, Department, RegisterItems


# 为住院主页建立序列化模型
class HomePageSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='registration.id')
    name = serializers.ReadOnlyField(source='registration.name')
    phone = serializers.ReadOnlyField(source='registration.phone')
    doctor = serializers.ReadOnlyField(source='registration.doctor.real_name')
    department = serializers.ReadOnlyField(source='registration.doctor.department.department_name')
    status = serializers.CharField(source='registration.get_status_display')

    class Meta:
        model = Admission
        fields = ('bed_id', 'pay_deposit', 'hospital_stays', 'id', 'name', 'phone', 'doctor', 'department', 'status',)


# 为挂号表建立序列化器
class RegistrationSerializers(serializers.ModelSerializer):
    # admission_url = serializers.HyperlinkedIdentityField(view_name='admission_detail', format='json')
    doctor = serializers.ReadOnlyField(source='doctor.real_name')
    department = serializers.ReadOnlyField(source='doctor.department.department_name')

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
    status = serializers.ReadOnlyField(source='registration.get_status_display')

    class Meta:
        model = Admission
        fields = ('id', 'name', 'pay_deposit', 'balance', 'status')


# 结算详细信息
class RegisterItemsSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='registration.id')
    name = serializers.ReadOnlyField(source='registration.name')
    item_name = serializers.ReadOnlyField(source='pay_items.item_name')
    charge_amount = serializers.ReadOnlyField(source='pay_items.charge_amount')

    class Meta:
        model = RegisterItems
        fields = ('id', 'name', 'item_time', 'item_name', 'charge_amount')


class ExportSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='registration.id')
    registration = RegistrationSerializers(read_only=True)

    class Meta:
        model = Admission
        fields = ('id', 'nurse', 'bed_id', 'pay_deposit', 'hospital_stays', 'state_illness', 'registration')


# 自定义分页的第一页和第二页
class PageCustom(PageNumberPagination):
    """
    配置分页规则，自定义第一页和最后一页
    """
    page_size = 2 # 每页显示的个数
    page_query_param = 'page' # 默认
    page_size_query_param = 'page_size' # 默认
    max_page_size = 1000

    def get_start_link(self):
        """
        第一页
        :return:
        """
        if not self.page.has_previous():
            return None
        page_number = 1
        url = self.request.build_absolute_uri()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_end_link(self):
        """
            最后一页
        """
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        print(page_number)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('start', self.get_start_link()),
            ('previous', self.get_previous_link()),
            ('next', self.get_next_link()),
            ('end', self.get_end_link()),
            ('results', data)
            ]))


