from django.urls import path, include
from . import views
from rest_framework import routers
# from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'admission', views.AdmissionViewSet)
router.register(r'registration', views.RegistrationViewSet)
router.register(r'cash_pledge',views.CashPledgeViewSet)
router.register(r'account', views.AccountViewSet)
router.register(r'register_item', views.RegisterItemsViewSet)
# router.register(r'export',views.Export)
urlpatterns = [
    path('', include(router.urls)),
    # path('admission/export/', views.Export.as_view()),

]
