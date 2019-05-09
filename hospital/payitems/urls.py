from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payitems import views

# 创建一个路由器并注册视图集
payitem_router = DefaultRouter()
payitem_router.register('pay-items', views.PayItemsView)
payitem_router.register('registration', views.RegistrationView)
payitem_router.register('registeritems', views.RegisterItemsView)
# payitem_router.register('users', views.UserViewSet)

# app_name = 'payitems'

urlpatterns = [
    path('', include(payitem_router.urls)),
    path('pay_items_count/',views.pay_items_count),
    path('user-au/', views.UserAuthenticate.as_view()),
]
