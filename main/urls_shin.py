# main/urls_shin.py (반드시 확인하세요)

from django.urls import path
from . import views_shin # 👈 이 임포트만 유지

urlpatterns = [
    # views_shin 모듈을 통해 접근
    path('setting/', views_shin.Settingv.as_view(), name='user_setting'), 
    path('notify/', views_shin.Notifyv.as_view(), name='user_notify'),
    
    path('map/', views_shin.MapPageView.as_view(), name='map'),
    path('route/', views_shin.RouteSearchView.as_view(), name='route_search'),
 ]