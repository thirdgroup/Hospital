from django.urls import path, include
from . import views

# from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'admission', views.AdmissionViewSet)
router.register(r'registration', views.RegistrationViewSet)
router.register(r'cash_pledge',views.CashPledgeViewSet)
router.register(r'account', views.AccountViewSet)
router.register(r'register_item', views.RegisterItemsViewSet)
# router.register(r'export',views.Export)
urlpatterns = [
    path('', include(router.urls)),
    # path('admission/', views.AdmissionList.as_view()),
    # path('admission/<int:pk>', views.AdmissionDetail.as_view(), name='admission_detail'),
    #
    # path('registration/', views.RegistrationList.as_view()),
    # path('registration/<int:pk>', views.RegistrationDetail.as_view(), name='registration_detail'),
    # path('search', views.Search.as_view()),# 住院表搜索
    #
    path('admission/export/', views.Export.as_view()),

    # path('admission/', views.AdmissionView.as_view({'get': 'list', 'post': 'create'})),
    # path('admission/<int:pk>', views.AdmissionView.as_view(
    #     {'get': 'retrieve', 'delete': 'destroy', 'put': 'perform_update', 'patch': 'partial_update'})),
    # path('registration/<int:pk>', views.RegistrationView.as_view(
    #     {'get': 'retrieve', 'delete': 'destroy', 'put': 'perform_update', 'patch': 'partial_update'}),
    #      name='registration-detail'),
]
