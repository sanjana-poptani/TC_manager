from .views import *
from django.urls import path

urlpatterns = [
    path('',home,name="home"),
    path('login',login,name="login"),
    path('signup',signup,name="signup"),
    path('cards',cards,name="cards"),
    path('releases',releases,name="releases"),
    path('release_sheet',releases,name="releases"),
]