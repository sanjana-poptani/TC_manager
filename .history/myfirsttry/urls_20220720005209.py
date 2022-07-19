from .views import *
from django.urls import path

urlpatterns = [
    path('',home,name="home"),
    path('login',login,name="login"),
    path('signup',signup,name="signup"),
    path('cards',cards,name="cards"),
    path('card_add',card_add,name="card_add"),
    path('del_card',del_card,name="card_add"),
    path('releases',releases,name="releases"),
    path('release_sheet',release_sheet,name="release_sheet"),
    path('verify',verify,name="verify"),
    path('logout',logout,name="logout"),
]