from django.urls import path, include
from rest_framework.routers import DefaultRouter
from outpatient.views import RegistrationViewSet, DepartmentViewSet, DoctorManageViewSet
from outpatient.myLogin import MyLogin

# registration_list = RegistrationViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# registration_detail = RegistrationViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

router = DefaultRouter()
# router.register(r'registration', RegistrationViewSet)
# router.register(r'department', DepartmentViewSet)
# router.register(r'doctormanage', DoctorManageViewSet)

# app_name = 'outpatient'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyLogin.as_view(), name='my_login'),
]