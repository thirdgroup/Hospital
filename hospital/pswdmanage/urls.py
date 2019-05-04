from django.urls import path
from pswdmanage import views
from rest_framework_jwt.views import obtain_jwt_token,verify_jwt_token,refresh_jwt_token

urlpatterns = [
    path('captcha/',views.Captcha.as_view()),
    path('sign-up/', views.SignUp.as_view()),
    path('sign-in/', views.SignIn.as_view()),
    path('sign-out/',views.SignOut.as_view()),
    path('change/',views.Change.as_view()),
]
