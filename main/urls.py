# main/urls_shin.py (반드시 확인하세요)

from django.urls import path
from . import views

urlpatterns = [
    path('setting/', views.Settingv.as_view(), name='user_setting'), 
    path('notify/', views.Notifyv.as_view(), name='user_notify'),
    
    path('map/', views.MapPageView.as_view(), name='map'),
    path('route/', views.RouteSearchView.as_view(), name='route_search'),
 ]

