from .views import *
from django.urls import path

urlpatterns = [
    path('',home,name="home"),
    path('login',login,name="login"),
    path('signup',signup,name="signup"),
    path('cards',cards,name="cards"),
    path('card_add',card_add,name="card_add"),
    path('edit_card/<int:id>',edit_card,name="edit_card"),
    path('edit_scope/<int:id>/<int:rid>',edit_scope,name="edit_scope"),
    path('del_card/<int:id>',del_card,name="del_card"),
    path('del_scope/<int:id>',del_scope,name="del_scope"),
    path('release_scope/<int:id>',release_scope,name="release_scope"),
    path('scope_add/<int:id>',scope_add,name="scope_add"),
    path('view_tcs/<int:id>',view_TCs,name="scope_add"),
    path('release_sheet',release_sheet,name="release_sheet"),
    path('verify',verify,name="verify"),
    path('logout',logout,name="logout"),
]