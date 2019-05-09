from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from database.models import PayItems, RegisterItems, Registration
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.utils.urls import remove_query_param, replace_query_param

class PayitemsSerializer(serializers.HyperlinkedModelSerializer):
    """
        项目收费序列化器
    """
    # registeritem = serializers.HyperllinkedRelatedField(many=True,
    # view_name='registeritems-detail', read_only=True)

    class Meta:
        model = PayItems
        fields = ('url', 'id', 'item_name', 'charge_amount')


class RegisterItemsSerializer(serializers.ModelSerializer):
    """
        项目收费登记序列化器1
    """
    # sick_id = serializers.ReadOnlyField(source='registration.id')       # 病历号
    # item_name = serializers.ReadOnlyField(source='pay_items.item_name')     # 项目名称
    # charge_amount = serializers.ReadOnlyField(source='pay_items.charge_amount')     # 收费金额
    # pay_time = serializers.ReadOnlyField(source='pay_items.create_time')    # 支付时间

    class Meta:
        model = RegisterItems
        fields = "__all__"


class RegisterItemSerializer(serializers.ModelSerializer):
    """
        项目收费登记序列化器2
    """
    # sick_id = serializers.ReadOnlyField(source='registration.id')       # 病历号
    item_name = serializers.ReadOnlyField(source='pay_items.item_name')     # 项目名称
    charge_amount = serializers.ReadOnlyField(source='pay_items.charge_amount')     # 收费金额
    pay_time = serializers.ReadOnlyField(source='pay_items.create_time')    # 支付时间

    class Meta:
        model = RegisterItems
        fields = ('id', 'item_name', 'charge_amount', 'pay_time')


class RegistrationSerializer(serializers.ModelSerializer):
    """
        项目收费登记的挂号信息
    """
    # status = serializers.ReadOnlyField(source='get_status_display')   # 选择器使用方法
    registeritem = RegisterItemSerializer(many=True, read_only=True)       # 收费姓名登记表
    hospital_stays = serializers.ReadOnlyField(source='admission.hospital_stays')   # 住院时间
    pay_deposit = serializers.ReadOnlyField(source='admission.pay_deposit')     # 押金
    balance = serializers.ReadOnlyField(source='admission.balance')     # 余额
    # print(pay_deposit)

    class Meta:
        model = Registration
        fields = ('url', 'id', 'name', 'hospital_stays', 'pay_deposit', 'balance', 'registeritem')


class StandartResultsSetPagination(PageNumberPagination):
    """
        配置分页规则, 自定义第一页，最后一页
    """

    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    def get_start_link(self):
        """
            第一页
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

# class PayitemsSerializer(serializers.ModelSerializer):
#     """
#         项目收费序列化器
#     """
#     registeritems = serializers.StringRelatedField(many=True)
#
#     class Meta:
#         model = PayItems
#         fields = ('id', 'item_name', 'charge_amount', 'registeritems')
#
#
# class RegisterItemsSerializer(serializers.ModelSerializer):
#     """
#         项目收费登记序列化器
#     """
#
#     class Meta:
#         model = RegisterItems
#         fields = ('id', 'item_time', 'registration', 'pay_items')





# class UserSerializer(serializers.ModelSerializer):
#     """
#         用户序列化器
#     """
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password')