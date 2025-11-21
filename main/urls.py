from django.urls import path
from . import views

urlpatterns = [
    # root URL ('')이 들어오면 views.py의 index 함수를 실행해라
    #path('', views.index, name='index'), 
    path('map/', views.MapPageView.as_view(), name='map'),

    # 아까 만든 길찾기 API도 여기에 있어야 합니다.
    path('route/', views.get_route, name='get_route'), 
]