from .views import *
from django.urls import path

urlpatterns = [
    path('',home,name="home"),
    path('login',login,name="login"),
    path('signup',signup,name="signup"),
    path('cards',cards,name="cards"),
    path('card_add',card_add,name="card_add"),
    path('edit_card/<int:id>',edit_card,name="edit_card"),
    path('del_card/<int:id>',del_card,name="del_card"),
    path('del_card/<int:id>',del_card,name="del_card"),
    path('release_scope/<int:id>',release_scope,name="release_scope"),
    path('scope_add/<int:id>',scope_add,name="scope_add"),
    path('release_sheet',release_sheet,name="release_sheet"),
    path('verify',verify,name="verify"),
    path('logout',logout,name="logout"),
]