from .views import *
from django.urls import path

urlpatterns = [
    path('',home,name="home"),
    path('login',login,name="login"),
    path('login',login,name="signup"),
]