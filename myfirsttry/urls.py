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
    path('edit_title/<int:id>',edit_title,name="edit_title"),
    path('edit_tc/<int:id>/<int:tid>',edit_TC,name="edit_tc"),
    path('filter_tc/<int:id>',filter_TC,name="filter_tc"),
    path('del_card/<int:id>',del_card,name="del_card"),
    path('del_scope/<int:id>',del_scope,name="del_scope"),
    path('release_scope/<int:id>',release_scope,name="release_scope"),
    path('scope_add/<int:id>',scope_add,name="scope_add"),
    path('view_tcs/<int:id>',view_TCs,name="view_tcs"),
    path('del_tcs/<int:id>',del_TCs,name="del_tcs"),
    path('add_tc/<int:id>',add_TC,name="add_tc"),
    path('add_details/<int:id>',add_details,name="add_details"),
    path('show_chart/<int:id>',show_chart_Tc,name="show_chart"),
    path('show_chart_Tc_scope/<int:id>',show_chart_Tc_scope,name="show_chart_Tc_scope"),
    path('verify',verify,name="verify"),
    path('logout',logout,name="logout"),
]