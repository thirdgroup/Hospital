from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import action
import numpy
import pandas as pd
from database.models import Admission, Registration, DoctorManage, RegisterItems
from rest_framework.views import APIView
from inhospital.serializers import AdmissionSerializers, RegistrationSerializers, HomePageSerializers, \
    CashPledgeSerializers, AccountHomePageSerializers, RegisterItemsSerializers, ExportSerializers
from django.http import JsonResponse, Http404
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets


# Create your views here.
class AdmissionViewSet(viewsets.ModelViewSet):

    # 主页数据接口
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print('查询完的%s' % queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HomePageSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = HomePageSerializers(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def get_queryset(self):
        """
        自定义get_queryset方法，用来条件查询queryset
        :return:
        """
        query_set = self.queryset
        record_no = self.request.query_params.get('record_no', None)

        if record_no:  # 对于病历号的模糊查询
            id_list = Registration.objects.values_list('id')
            id_list = list(id_list)
            new_list = list()
            if id_list:
                new_list = [str(i[0]) for i in id_list if record_no in str(i[0])]
            query_set = Admission.objects.filter(registration__in=new_list)
        doctor = self.request.query_params.get('doctor', None)
        if doctor:  # 对于主治医生的模糊查询
            # query_set = query_set.filter(doctor__real_name__icontains=doctor)
            query_set = query_set.filter(registration__doctor__real_name__icontains=doctor)
        department = self.request.query_params.get('department', None)
        if department:  # 对于门诊科室的模糊查询
            # query_set = query_set.filter(department__department_name__icontains=department)
            query_set = query_set.filter(registration__department__department_name__icontains=department)
        start = self.request.query_params.get('start_time', None)
        end = self.request.query_params.get('end_time', None)

        if start and end:  # 对于挂号时间的模糊查询
            query_set = query_set.filter(hospital_stays__gte=start).filter(hospital_stays__lte=end)
        return query_set

    # 添加住院
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        registration_obj = Registration.objects.get(id=request.data['registration'])
        registration_obj.status = 1
        registration_obj.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 修改住院信息
    def update(self, request, pk, *args, **kwargs):
        data_dict = request.data
        # print(data_dict)
        if not data_dict:
            try:
                admission_obj = Admission.objects.get(id=pk)
            except Admission.DoesNotExist:
                return JsonResponse({'status': 404,
                                     'PATCH': '该id不存在'})
            serializer = AdmissionSerializers(instance=admission_obj, context={'request': request})
            return Response(serializer.data)
        if 'balance' in data_dict or 'hospital_stays' in data_dict or 'registration' in data_dict or 'pay_deposit' in data_dict:  # 余额,住院时间
            return JsonResponse({'PATCH': '该字段不能被修改'})
        try:
            admission_obj = Admission.objects.get(id=pk)
        except Admission.DoesNotExist:
            return JsonResponse({'status': 404,
                                 'PATCH': '该id不存在'})
        if 'status' in data_dict:
            # obj = Registration.objects.get(id=pk)
            relevance_obj = admission_obj.registration
            if int(data_dict['status']) == 6 or int(data_dict['status']) == 2:
                if relevance_obj.status == 3:

                    relevance_obj.status = int(data_dict['status'])
                else:
                    return JsonResponse({'PATH': '您还没有结算医药费，不能出院或退院'})
            relevance_obj.status = int(data_dict['status'])
            relevance_obj.save()
        # 护理
        if 'nurse' in data_dict:
            admission_obj.nurse = data_dict['nurse']
        # 床位号
        if 'bed_id' in data_dict:
            admission_obj.bed_id = data_dict['bed_id']
        if 'state_illness' in data_dict:  # 病情
            admission_obj.state_illness = data_dict['state_illness']
        admission_obj.save()
        return JsonResponse({'status': 'ok'})

    @action(detail=False, methods=['GET', 'POST'])
    def export(self, request):
        info = request.GET
        print(info)
        id_list = eval(info.get('id', None))
        # registration_list = nurse_list = bed_id_list = pay_deposit_list = hospital_stays = state_illness = \
        # name = phone = doctor = department = status = id_number = social_num = is_paying = sex = age = is_first = \
        # remark = list()
        for i in id_list:
            adm_obj = Admission.objects.get(registration_id=i)
            serializer = ExportSerializers(instance=adm_obj)
            admission_data_dict = dict(serializer.data)
            registration_dict = dict(admission_data_dict.pop('registration'))
            admission_data_dict.update(registration_dict)
            print(admission_data_dict)
            df = pd.DataFrame(admission_data_dict, columns=admission_data_dict.keys(),
                              index=[admission_data_dict['id']])
            try:
                with open(r'../data.csv') as f:
                    df.to_csv('../data.csv', mode='a', index=False, header=False)
            except FileNotFoundError:
                df.to_csv('../data.csv', index=False)
        return HttpResponse('ok')
        # return JsonResponse({'status', '123'}, safe=False)

    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializers


class RegistrationViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, pk, *args, **kwargs):
        # pk = request.data['registration_id']
        registration_obj = Registration.objects.get(id=pk)
        serializer = RegistrationSerializers(instance=registration_obj)
        return JsonResponse(serializer.data, safe=False)

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializers


class CashPledgeViewSet(viewsets.ModelViewSet):
    def update(self, request, pk, *args, **kwargs):
        data_dict = request.data
        # if 'pay_deposit' in data_dict:
        try:
            premium_received = float(data_dict['pay_deposit'])
        except ValueError:
            return JsonResponse({'PATCH': '金钱字段必须为正数'})
        # 押金
        try:
            admission_obj = Admission.objects.get(id=pk)
        except Admission.DoesNotExist:
            return JsonResponse({'Update': '该id不存在'})
        premium_received_old = float(admission_obj.pay_deposit)
        admission_obj.pay_deposit = premium_received_old + premium_received
        # 余额
        deposit_balance = float(admission_obj.balance)
        admission_obj.balance = deposit_balance + premium_received
        admission_obj.save()
        return JsonResponse({'status': 'ok'})

    queryset = Admission.objects.all()
    serializer_class = CashPledgeSerializers


# 住院结算主页信息
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AccountHomePageSerializers


# 住院结算详细信息
class RegisterItemsViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, pk, *args, **kwargs):
        registration_obj = RegisterItems.objects.filter(registration_id=pk)
        serializers = RegisterItemsSerializers(instance=registration_obj, many=True, context={'Request': 'request'})
        return JsonResponse(serializers.data, safe=False)

    queryset = RegisterItems.objects.all()
    serializer_class = RegisterItemsSerializers


# 导出Excel
class Export(APIView):

    def get(self, request):
        info = request.GET
        print(info)
        export_list = info.get('admission_id', None)
        print(export_list)
        for i in export_list:
            obj = Admission.objects.get(registration_id=i)
            serializer = AdmissionSerializers(instance=obj, context={'request': request})
            print(serializer.data)

        return JsonResponse({'status': 'ok'})
